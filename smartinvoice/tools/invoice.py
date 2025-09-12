import tempfile, json

import os
import sys

# Always set working dir to the project root (where server.py lives)
BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "..")

# print(BASE_DIR)
os.chdir(BASE_DIR)

sys.path.insert(0, BASE_DIR)

from jinja2 import Template
import subprocess
from pathlib import Path
# from smartinvoice.schema.tool_schema import schema_invoice_generate
PROJECT_PATH = Path("D:/Personal-project/MCP-SmartInvoice/MCP-SmartInvoice")
INVOICE_STORAGE = Path("D:/Personal-project/MCP-SmartInvoice/MCP-SmartInvoice/invoices") / "invoices"
INVOICE_STORAGE.mkdir(exist_ok=True)
VAT_PERCENTAGE = 0.2
# from templates
with open("smartinvoice/templates/latex_template.tex", "r") as latex_template_file:
    LATEX_TEMPLATE = latex_template_file.read()

# print(LATEX_TEMPLATE)
def generate_invoice(items: list):
    import uuid
    invoice_id = str(uuid.uuid4())[:8]
    # For demo: static prices
    catalog = {
        "Laptop": (1200, "USD"),
        "Mouse": (25, "USD"),
        "Keyboard": (45, "USD"),
    }
    total = 0
    processed_items = []
    for it in items:
        price, currency = catalog[it["product"]]
        subtotal = price * it["quantity"]
        total += subtotal
        print(it)
        processed_items.append({
            "product": it["product"],
            "quantity": it["quantity"],
            "price":  "{:.2f}".format(price),
            "currency": currency,
            "total": "{:.2f}".format(subtotal)
        })
    subtotal = total
    total = subtotal + (subtotal * VAT_PERCENTAGE)
    invoice = {
        "id": invoice_id,
        "items": processed_items,
        "subtotal":  "{:.2f}".format(subtotal),
        "total":  "{:.2f}".format(total),
        "vat": "{:.2f}".format(subtotal * VAT_PERCENTAGE),
        "currency": "USD"
    }
    # Save draft
    path = INVOICE_STORAGE / f"{invoice_id}.json"
    path.write_text(json.dumps(invoice, indent=2))

    pdf_path = confirm_invoice(invoice_id)["pdf_path"]
    invoice["invoice_path"] = str(INVOICE_STORAGE) + "/" + pdf_path
    return {"invoice": invoice,  "message": f"Invoice created successfully at D:/Personal-project/MCP-SmartInvoice/MCP-SmartInvoice/invoices/{pdf_path}."}

from jinja2 import Environment
def confirm_invoice(invoice_id: str):
    path = INVOICE_STORAGE / f"{invoice_id}.json"
    if not path.exists():
        return {"error": "Invoice not found"}
    invoice = json.loads(path.read_text())
    invoice["status"] = "confirmed"
    # Render LaTeX
    env = Environment(
        block_start_string = '\BLOCK{',
        block_end_string = '}',
        variable_start_string = '\VAR{',
        variable_end_string = '}',
        comment_start_string = '\#{',
        comment_end_string = '}',
        autoescape=False
    )

    template = env.from_string(LATEX_TEMPLATE)
    tex = template.render(invoice=invoice)
    tex_path = INVOICE_STORAGE / f"{invoice_id}.tex"
    pdf_path = INVOICE_STORAGE / f"{invoice_id}.pdf"
    tex_path.write_text(tex, encoding="utf-8")
    # subprocess.run(["pdflatex", "-interaction=nonstopmode", str(tex_path)], cwd=INVOICE_STORAGE, check=False)
    subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", str(tex_path)],
        cwd=INVOICE_STORAGE,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    path.write_text(json.dumps(invoice, indent=2))
    return {"pdf_path": str(pdf_path)}

def download_invoice(invoice_id: str):
    pdf_path = INVOICE_STORAGE / f"{invoice_id}.pdf"
    if not pdf_path.exists():
        return {"error": "No confirmed invoice found"}
    return {"pdf_path": str(pdf_path)}


# items = ["laptop", "mouse"]
# items = [{"product": "Laptop", "quantity": 1}, {"product": "Mouse", "quantity": 2}]
# invoice_info = generate_invoice(items)
# print(invoice_info["invoice"]["id"])
# confirm_invoice(invoice_info["invoice"]["id"])