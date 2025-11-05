#  Task 1

import pandas as pd


input_file = r"C:\Users\vganta\OneDrive - Evoke Technologies Private Limited\Assignments\sample_employees.xlsx"
output_file = r"C:\Users\vganta\OneDrive - Evoke Technologies Private Limited\Assignments\sample_employees_updated.xlsx"


df = pd.read_excel(input_file)

print(" Data from Excel:")
print(df)

#updating data 
df.to_excel(output_file, index=False)

print(f"\n Data successfully copied to: {output_file}")

