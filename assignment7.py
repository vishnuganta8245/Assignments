from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
from fpdf import FPDF
import os

app = FastAPI()

OUTPUT_DIR = r"out7"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/generate-pdf/")
async def generate_pdf(
    employee_id: int = Form(...),
    name: str = Form(...),
    department: str = Form(...),
    salary: float = Form(...)
):
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt="Employee Details", ln=True, align="C")
    pdf.ln(10)

   
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Employee ID: {employee_id}", ln=True)
    pdf.cell(200, 10, txt=f"Name: {name}", ln=True)
    pdf.cell(200, 10, txt=f"Department: {department}", ln=True)
    pdf.cell(200, 10, txt=f"Salary: {salary} INR", ln=True) 

    pdf_filename = f"employee_{employee_id}.pdf"
    pdf_path = os.path.join(OUTPUT_DIR, pdf_filename)
    pdf.output(pdf_path)  

    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=pdf_filename
    )

