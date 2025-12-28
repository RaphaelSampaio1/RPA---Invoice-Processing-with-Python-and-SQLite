import pdfplumber
import re

def extract_data_from_pdf(pdf_path):
    data = {}
    with pdfplumber.open(pdf_path) as pdf:
        first_page = pdf.pages[0]
        text = first_page.extract_text()
        
        # Invoice Number
        match_invoice = re.search(r"Nº: ([\d-]+)", text)
        if match_invoice:
            data["numero_fatura"] = match_invoice.group(1)
            
        # Issue Date
        match_issue_date = re.search(r"Data emissão: ([\d-]+)", text)
        if match_issue_date:
            data["data_emissao"] = match_issue_date.group(1)

        # Expire Date
        match_expire_date = re.search(r"Vencimento: ([\d-]+)", text)
        if match_expire_date:
            data["data_vencimento"] = match_expire_date.group(1)

        # Client Name
        match_client_name = re.search(r"Cliente:\s*\n\s*([a-zA-Z0-9\s]+)", text)
        if match_client_name:
            data["nome_cliente"] = match_client_name.group(1).strip()

        # NIF
        match_nif = re.search(r"Cliente:\s*\n(.+?\nNIF:\s*([\w]+))", text)
        if match_nif:
            data["nif_emissor"] = match_nif.group(2).strip()

        # Address
        match_address = re.search(r"NIF:\s*([\w]+\s*\n(.+))", text)
        if match_address:
            data["endereco_cliente"] = match_address.group(2).strip()

        # Total Amount
        match_total_amount = re.search(r"Total:\s*([\d.]+)", text)
        if match_total_amount:
            data["valor_total"] = match_total_amount.group(1).strip()
    return data

if __name__ == "__main__":
    pdf_path = r"faturas\input\fatura_001.pdf"
    result = extract_data_from_pdf(pdf_path)
    print(result)
    