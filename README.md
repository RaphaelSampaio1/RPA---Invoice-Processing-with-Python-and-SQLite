# RPA - Invoice Processing with Python and SQLite

This project is a **realistic RPA case** for Accounts Payable (Contas a Pagar).  
It simulates an automation that:

- Receives invoices (PDFs),
- Extracts structured data (invoice number, dates, client, NIF, address, total),
- Saves the data into a **SQLite database**,
- Organizes files into folders (input, processing, archive, error),
- Applies basic business rules (e.g., unique invoices).

The goal is to look and behave like an **enterprise-grade RPA solution**, not just a simple script.

---

## 🔧 Tech Stack

- **Language:** Python 3.x  
- **PDF Generation:** `reportlab`  
- **PDF Text Extraction:** `pdfplumber`  
- **Database:** SQLite (`sqlite3` built-in)  
- **OS / Filesystem:** `os`, `shutil`  

---

## 📁 Project Structure

```text
project_root/
├── data/
│   ├── input/          # Raw invoices (PDFs) to be processed
│   ├── processing/     # Invoices currently being processed
│   ├── archive/        # Successfully processed invoices
│   └── error/          # Invoices that failed processing
├── database/
│   └── faturas.db      # SQLite database file
├── logs/               # (optional) Log files (if you extend logging)
├── src/
│   ├── gerar_faturas_exemplo.py  # Script to generate sample invoices
│   ├── extractor.py              # PDF text extraction + regex parsing
│   ├── database_manager.py       # DB connection and CRUD operations
│   └── processor.py              # Orchestrator: moves files + calls extractor + DB
├── main.py              # Entry point to run the full process
├── requirements.txt
└── README.md
