import pdfplumber

with pdfplumber.open("dadosAcademicos.pdf") as pdf:
    page = pdf.pages[0]
    print(page.extract_text())
