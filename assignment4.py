import pandas as pd
from fpdf import FPDF


excel_file = "sample_employees.xlsx" 
sheet_name = "Sheet1"     
df = pd.read_excel(excel_file, sheet_name=sheet_name)

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=10)

pdf.cell(200, 10, txt="Excel Data Export", ln=True, align='C')


pdf.set_font("Arial", style='B', size=10)
col_width = pdf.w / (len(df.columns) + 1)
row_height = 8

for col_name in df.columns:
    pdf.cell(col_width, row_height, col_name, border=1)
pdf.ln(row_height)


pdf.set_font("Arial", size=9)
for i in range(len(df)):
    for col_name in df.columns:
        pdf.cell(col_width, row_height, str(df.iloc[i][col_name]), border=1)
    pdf.ln(row_height)


pdf.output("out4.pdf")
print(" PDF created successfully: output.pdf")
