import requests
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path
import os

script_path = Path(__file__).resolve()
script_dir = script_path.parent
file_name = 'wise_owl_ssis_exercises.xlsx'
file_path = os.path.join(script_dir, file_name)

def get_dataframe():
    """Function to get all the exercises details from Wise Owl SSIS exercises
    web page, insert these details into a dataframe and then return the 
    dataframe"""
    # Assign URL of web pages where exercises are details
    url = 'https://www.wiseowl.co.uk/integration-services/exercises/standard/'

    # Assign response object using the url
    response = requests.get(url)

    # Create and assign beautiful soup object from the response object
    soup = BeautifulSoup(response.text, 'html.parser')

    # Get all the tags wrapped in the panel grid item tags
    panel_tags = soup.find_all('panel-grid-item')

    # initiliase a list for holding the table date where each table is a dict
    list_of_tables = []

    # iterate through each panel tag getting the table cell (td) info from each
    # table and assigning to a dictionary where key will be the table column
    # title and the value will be the cell value for that column
    for panel in panel_tags:
        a = panel.find_all('a')
        td = panel.find_all('td')
        table_dict = {
            td[0].string: td[1].string,
            td[2].string: td[3].string,
            td[4].string: td[5].string,
            td[6].string: td[7].string,
            "Link:": f"https://www.wiseowl.co.uk/{a[0].get('href')}",
            "Completed:": ""
        }
        list_of_tables.append(table_dict)

    # Create a dataframe from the list of dictionaries created
    df = pd.DataFrame(list_of_tables)

    return df

def dataframe_to_excel(df, path):
    """Takes the data frame from the get dataframe function and writes this to
     an excel sheet in table format """
    
    # initlise context manager for Excel Writer bound to writer
    with pd.ExcelWriter(file_path, 
                        engine='xlsxwriter') as writer:
        
        #write the dataframe to an excel workbook, writer as first argument
        df.to_excel(writer, index=False, sheet_name = 'Wise Owl SSIS Exercises')

        # assign the relevant worksheet object
        worksheet = writer.sheets['Wise Owl SSIS Exercises']

        # iterate through rows in the Link column starting at row 1
        # e.g. (not the header) row and overwrite the contents of the link
        # column with values of the dataframe as a hyperlink
        for row_num, link in enumerate(df['Link:'], start = 1):
            worksheet.write_url(row_num, 4, link, string = "Link")

        # get max dimensions of the dataframe to know values for excel table
        (max_row, max_col) = df.shape

        # turn excel data into a table, the list comprehension produces a list
        # of dictionaries where the value is the colum header from the data frame
        worksheet.add_table(0, 0, max_row, max_col- 1, {
            'columns': [{'header': column} for column in df.columns],
            'name': 'Table1'
        })

        # iterate over the columns of the dataframe to get the max width of 
        # either the header cell or max width of a cell in that column and set 
        # the relevant column width in the worksheet. This is done by using the
        # index from enumerate e.g. for each column the set column method
        # uses the index to specify first column and last column to set width
        # for and since it's the same value it will just set the width for the
        # column in question
        for i, col in enumerate(df.columns):
            max_width = max(df[col].apply(lambda x : len(str(x))).max(), len(col))
            worksheet.set_column(i,i, max_width)

if __name__ == "__main__":

    df = get_dataframe()
    dataframe_to_excel(df, script_dir)

    print(f"New excel file created at {file_path}")