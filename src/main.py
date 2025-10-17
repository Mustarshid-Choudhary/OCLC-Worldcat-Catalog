from bookops_worldcat import WorldcatAccessToken, MetadataSession
import xml.etree.cElementTree as ET
import openpyxl as op
from tkinter import Tk, filedialog
import os
import config as cf

def verify_token():
    """
    Create and return a token after verifying that it's valid.
    Insert the acquired API Key, secret, and scopes into config_template.py
    and import it here in place of config to access the variables.

    :return: a token
    """
    token = WorldcatAccessToken(key=cf.KEY, secret=cf.SECRET, scopes=cf.SCOPES)

    print(token) # > access_token: 'tk_Yebz4BpEp9dAsghA7KpWx6dYD1OZKWBlHjqW', expires_at: '2024-01-01 17:19:58Z'
    print("Is expired: " + str(token.is_expired())) # > False

    return token

def initialize_sheet(work_book):
    """
    Add the headings to each column in the new excel sheet.

    :param work_book: the workbook excel
    :return: a new work sheet with column headings
    """
    work_sheet = work_book.active
    work_sheet.title = "Book Records"

    work_sheet.append(["OCLC Number", "Online Versions", "Holdings", "Shared Prints", "Title", "Edition", "Publisher", "Date 1", "Date 2", "Record Source"])

    return work_sheet

def get_all_details(data, xml_str):
    """
    Find and return all of the details pertaining to the given OCLC number.

    :param data: a dictionary containing all information
    :param xml_str: a string containing the XML data
    :return: a list containing all of the details pertaining to the OCLC number in the order that they appear in the excel sheet
    """
    # Holdings extraction
    holdings = data['totalHoldingCount']
    sharedprints = data['totalSharedPrintCount']

    root = ET.fromstring(xml_str)
    ns = {'marc': 'http://www.loc.gov/MARC21/slim'}

    # OCLC number extraction
    oclc = root.find("marc:controlfield[@tag='001']", ns)

    oclc_number = oclc.text if oclc is not None else "Not found"
    oclc_number = '#' + oclc_number[3:]

    # online_versions extration
    online_versions = root.find("marc:datafield[@tag='776']", ns)

    if online_versions is not None:
        subfields = online_versions.findall("marc:subfield[@code='w']", ns)
        online_version_details = " ".join(sub.text for sub in subfields if sub.text)
    else:
        online_version_details = "Info: Not found"

    # Title extration
    title = root.find("marc:datafield[@tag='245']", ns)

    if title is not None:
        subfields = title.findall("marc:subfield",ns)
        title_details = " ".join(sub.text for sub in subfields if sub.text)
    else:
        title_details = "No title found"

    # Edition extraction
    edition = root.find("marc:datafield[@tag='250']",ns)

    if edition is not None:
        subfields = edition.findall("marc:subfield", ns)
        edition_details = " ".join(sub.text for sub in subfields if sub.text)
    else:
        edition_details = "-"

    # Publisher extraction only subfield b
    publisher_old = root.find("marc:datafield[@tag='260']", ns)
    publisher_new = root.find("marc:datafield[@tag='264']", ns)

    if publisher_old is not None and publisher_new is None:
        subfields = publisher_old.findall("marc:subfield[@code='b']", ns)
        publisher_details = " ".join(sub.text for sub in subfields if sub.text)

    elif publisher_old is None and publisher_new is not None:
        subfields = publisher_new.findall("marc:subfield[@code='b']", ns)  # FIXED: same as above
        publisher_details = " ".join(sub.text for sub in subfields if sub.text)

    else:
        publisher_details = "-"

    # Date extraction
    date_one = root.find("marc:controlfield[@tag='008']", ns)

    date_details = date_one.text if date_one is not None else "Not found"
    date_one_details = date_details[7:11]
    date_two_details = date_details[11:15]

    # Record source extraction
    record_source = root.find("marc:datafield[@tag='040']", ns)

    if record_source is not None:
        subfield = record_source.findall("marc:subfield[@code='a']",ns)
        record_source_details = " ".join(sub.text for sub in subfield if sub.text)
    else:
        record_source_details = "Not Found"
    
    return [oclc_number, online_version_details, holdings, sharedprints, title_details, edition_details, publisher_details, date_one_details, date_two_details, record_source_details]

def set_column_widths(work_sheet):
    """
    Set the width for each column in the excel spreadsheet.

    :param work_sheet: the excel spreadsheet
    """
    column_widths = {
        'A': 16, 'B': 21, 'C': 10, 'D': 10,
        'E': 115, 'F': 20, 'G': 25, 'H': 10,
        'I': 10, 'J': 15
    }

    for column, width in column_widths.items():
        work_sheet.column_dimensions[column].width = width

def select_result_location():
    """
    Return the path to the new excel file (where it should be saved).

    :return: a string containing the path to the new excel file
    """
    root = Tk()
    root.withdraw()

    save_path = filedialog.asksaveasfilename(
        defaultextension = ".xlsx",
        filetypes = [("Excel files", "*.xlsx")],
        title = "Save Excel File As..."
    )

    return save_path

def save_new_sheet(path, work_book):
    """
    Save the new excel spreadsheet to the indicated directory. If the save was canceled, return None.

    :param path: the path to the directory
    :param work_book: the workbook excel
    :return: the path to the excel spreadsheet, None if the save was canceled
    """
    if path:
        work_book.save(path)
        print(f"Excel file saved to: {path}")
        os.startfile(path)
        return path
    else:
        print("Save canceled.")
        return None

def run_program(input_file):
    """
    Run the script for every OCLC number in the input text file.

    :param input_file: a text file of OCLC numbers
    :return: a string containing the path to the new excel spreadsheet
    """
    token = verify_token()
    work_book = op.Workbook()
    work_sheet = initialize_sheet(work_book)
    infile = open(input_file, "r")

    for element in infile:
        with (MetadataSession(authorization = token) as session):
            result = session.bib_get(element)
            response = session.summary_holdings_get(element)
            data = response.json()
            xml_str = result.text
            details = get_all_details(data, xml_str)
            work_sheet.append(details)

    set_column_widths(work_sheet)

    save_path = select_result_location()
    return save_new_sheet(save_path, work_book)