import xlrd
import pandas as pd
import os

loc = r"C:\Users\brody.westberg\Downloads\OneDrive_2021-10-25\Historical Resin Transfer Sheets"
column_list = ['Transfer Date',
                'Transfer Lot',
                'Synthesis Lot',
                'Slurry Component 1',
                'Slurry Comp 1 mass',
                'Slurry Comp 1 Conc',
                'Slurry Component 2',
                'Slurry Comp 2 mass',
                'Slurry Comp 2 Conc',
                'Resin g',
                'Slurry g',
                'Additive 1',
                'Add 1 g',
                'Additive 2',
                'Add 2 g',
                'Instructions',
                'Pack soln',
                'Packer',
                'Pack temp °C',
                'Pack ramp sec',
                'Pack psi',
                'Pack time min']
pos_list = [(6,7),
            (6,2),
            (6,11),
            (3,21),
            (5,21),
            (6,21),
            (3,22),
            (5,22),
            (6,22),
            (3,29),
            (3,30),
            (5,33),
            (3,33),
            (5,34),
            (3,34),
            (3,39),
            (3,42),
            (3,51),
            (3,59),
            (3,61),
            (3,62),
            (3,64)]

df = pd.DataFrame()
for column, pos in zip(column_list, pos_list):
    temp = []
    for file in os.listdir(loc):
        wb = xlrd.open_workbook(loc + "\\" + file)
        sheet = wb.sheet_by_index(0)
        temp.append(sheet.cell_value(pos[1]-1,pos[0]-1))
    df[column] = temp

print(df)
df.to_excel(r"C:\Users\brody.westberg\Downloads\OneDrive_2021-10-25\TransferSheetData.xlsx")