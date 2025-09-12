from mcp.server.fastmcp import FastMCP
import os
import sys
import json
from pathlib import Path

# Always set working dir to the project root (where server.py lives)
BASE_DIR = ((os.path.dirname(__file__)))
print(BASE_DIR)
os.chdir(BASE_DIR)

# Optional: make sure the project root is in sys.path so imports work
sys.path.insert(0, BASE_DIR)

from smartinvoice.tools import invoice
from pydantic import BaseModel
from typing import List

# -------------------------
# Input schema for the tool
# -------------------------
class InvoiceItem(BaseModel):
    product: str
    quantity: int

class InvoiceGenerateSchema(BaseModel):
    items: List[InvoiceItem]

class InvoiceConfirmSchema(BaseModel):
    invoice_id: str

# -------------------------
# Initialize MCP server
# -------------------------
mcp = FastMCP("SmartInvoice")

# -------------------------
# Prompt handler
# -------------------------
@mcp.prompt()
def invoice_assistant(user_input: str) -> str:
    """
    This function handles user input and returns a response.
    """
    response = f"""# Invoice Generation Assistant

You are a virtual assistant that answers questions regarding VK Tech products, their availability, prices, and generates invoices once an order is confirmed.

**Preferences:**
- Keep communications clear and concise
- Always ask for confirmation before placing an order
- Ensure product names, quantities, prices, delivery location, and total amount are acquired before generating an invoice
- Use polite and professional language

**Instructions:**
- Greet the user and offer assistance
- Provide product availability and pricing
- Summarize order details and ask for confirmation before generating an invoice
- Generate a simple invoice upon confirmation

**Example Interaction:**
User: Hi, I'm interested in VK Tech products. Can you tell me more?
Assistant: Hello! We offer a variety of tech gadgets including smartphones, laptops, and accessories. Which product are you interested in?
User: I'd like a smartphone. What models do you have?
Assistant: We have VK Tech X1, VK Tech Pro, and VK Tech Lite. Prices range from $299 to $999. Which one would you like?
User: I'll go with the VK Tech Pro. Can you place an order?
Assistant: Great choice! Just to confirm, you want 1 VK Tech Pro smartphone. Is that correct?
User: Yes
Assistant: Thank you! Here is your invoice:
Product: VK Tech Pro Smartphone
Quantity: 1
Price: $699
Total Amount: $699
Thank you for your business!"""
    return response

# -------------------------
# Register the single tool
# -------------------------
# Only the tool name is required; input schema is inferred from type hints
# @mcp.tool()
# mcp.tool("invoice_generate", file=sys.stderr)(invoice.generate_invoice)

# -------------------------
# Register the tool
# -------------------------
print("before tool", file=sys.stderr)
@mcp.tool()
def invoice_generate(data: InvoiceGenerateSchema):
    return invoice.generate_invoice([item.dict() for item in data.items])

# print("before tool", file=sys.stderr)
# @mcp.tool()
# def confirm_invoice(invoice_id: InvoiceConfirmSchema):
#     return invoice.confirm_invoice(invoice_id)


CATALOG_FILE = Path("smartinvoice/resources/products.json")

@mcp.tool()
def list_products():
    """
    List all available products from the catalog.
    """
    if not CATALOG_FILE.exists():
        return {"error": f"Catalog file not found at {CATALOG_FILE}"}
    with open(CATALOG_FILE, "r") as f:
        catalog = json.load(f)
    return {"products": catalog}


print("after tool", file=sys.stderr)

# -------------------------
# Run the MCP server
# -------------------------
if __name__ == "__main__":
    mcp.run()
