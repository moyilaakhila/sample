from pprint import pprint
import os
import json
import win32com.client as win32 # pip install pywin32

"""
Step 1.1 Read the JSON file
"""
json_data = json.loads(open('data.json').read())
pprint(json_data)

"""
Step 1.2 Examing the data and flatten the records into a 2D layout
"""
rows = []

for record in json_data['feature_summary']['result']['data']:
   #id = record
   #name = record['featureName']
   #duration_features = record['features']['duration']
   #status_features = record['features']['status']
   #Concurrency_load = record['load']['Concurrency']
   #UEs_load = record['load']['UEs']
   #failed_scenario = record['scenario']['failed']
   #passed_scenario = record['scenario']['passed']
   #total_scenario = record['scenario']['total']
   #failed_steps = record['steps']['failed']
   #passed_steps = record['steps']['passed']
   #skipped_steps = record['steps']['skipped']
   #total_steps = record['steps']['total']   
  # rows.append([id, name, duration_features, status_features, Concurrency_load, UEs_load, failed_scenario, passed_scenario, total_scenario, failed_steps, passed_steps, skipped_steps, total_steps])
  # print()
   
   """
Step 2. Inserting Records to an Excel Spreadsheet
"""
ExcelApp = win32.Dispatch('Excel.Application')
ExcelApp.Visible = True

wb = ExcelApp.Workbooks.Add()
ws = wb.Worksheets(2)

header_labels = ('id', 'name', 'duration_features', 'status_features', 'Concurrency_load', 'UEs_load', 'failed_scenario', 'passed_scenario', 'total_scenario', 'failed_steps', 'passed_steps', 'skipped_steps', 'total_steps')


# insert header labels
for indx, val in enumerate(header_labels):
    ws.Cells(1, indx + 1).Value = val

# insert Records
row_tracker = 2
column_size = len(header_labels)

for row in rows:
    ws.Range(
        ws.Cells(row_tracker, 1),
        ws.Cells(row_tracker, column_size)
    ).value = row
    row_tracker += 1

wb.SaveAs(os.path.join(os.getcwd(), 'Json output.xlsx'), 51)
wb.Close()
ExcelApp.Quit()
ExcelApp = None
