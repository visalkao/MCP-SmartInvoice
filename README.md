# SmartInvoice MCP Server



This repository contains the **SmartInvoice MCP server**, a backend assistant for VK Tech products. Built with the [MCP framework](https://github.com/mcp-project), it's designed to be used with an MCP-compatible client like Claude to provide a virtual assistant experience.

-----

## Table of Contents

  - [Overview](https://www.google.com/search?q=%23overview)
  - [Features](https://www.google.com/search?q=%23features)
  - [Installation](https://www.google.com/search?q=%23installation)
  - [Usage](https://www.google.com/search?q=%23usage)
  - [Project Structure](https://www.google.com/search?q=%23project-structure)
  - [Tools](https://www.google.com/search?q=%23tools)
  - [License](https://www.google.com/search?q=%23license)

-----

## Overview

The **SmartInvoice MCP server** acts as a backend assistant for VK Tech products. It can:

  * Respond to user queries about product availability and pricing.
  * Generate invoices for confirmed orders.
  * List all available products.
  * Ensure professional, concise communication with customers.

The server is designed to be used with an MCP client (e.g., Claude) to provide an interactive chat experience.

-----

## Features

1.  **Invoice Assistant**: Guides users through the ordering process and handles product-related queries.
2.  **Invoice Generation Tool**: Creates a draft invoice and saves it as a JSON file.
3.  **Product Listing Tool**: Lists all available products from a catalog JSON file.
4.  **Extensible**: New tools, such as an order confirmation tool, can be easily added.
5.  **Absolute Paths**: Ensures templates and resources load correctly, regardless of the working directory.

-----

## Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/SmartInvoice-MCP.git
    cd SmartInvoice-MCP
    ```
2.  **Set up a Python virtual environment**:
    ```bash
    python -m venv venv
    # For Linux / macOS
    source venv/bin/activate
    # For Windows
    venv\Scripts\activate
    ```
3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    Make sure **mcp** is installed in your environment.

-----

## Usage

1.  **Start the MCP server**:
    ```bash
    python server.py
    ```
2.  Connect your MCP client (e.g., Claude) to the server.
3.  Interact with the assistant using natural language:
    ```
    User: Hi, I'm interested in VK Tech products. Can you tell me more?
    Assistant: Hello! We offer a variety of tech gadgets...
    ```
4.  Use the available tools via the client:
      * **invoice\_generate** – Generate a draft invoice.
      * **list\_products** – List all available products.

-----

## Project Structure

```
SmartInvoice-MCP/
├── invoices                   # Folder containing all generated invoices
├── server.py                  # MCP server entrypoint
├── smartinvoice/
│   ├── agents/                # Agents
│   ├── demo/                  # Demo videos
│   └── resources/
│       └── products.json      # Product catalog
│   ├── schema/
│   ├── templates/             # Contains Invoice template 
│   ├── tools/
│   │   └── invoice.py         # Invoice generation functions
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
```

-----

## Tools

### invoice\_generate

  * **Input**: A JSON list of items with the product and quantity.
  * **Output**: A draft invoice JSON with subtotal, total, VAT, and status.

### list\_products

  * **Input**: None
  * **Output**: A list of products from `smartinvoice/resources/products.json`.

Future tools like `confirm_invoice` can be added by following the same pattern. (Can be used to ask user for confirmation before generating an invoice.

-----

## License

This project is licensed under the MIT License—see the [LICENSE](https://www.google.com/search?q=LICENSE) file for details.
