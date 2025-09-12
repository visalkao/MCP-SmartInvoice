schema_list_products = {
    "type": "object",
    "properties": {
        "query": {"type": "string"}
    },
    "required": ["query"]
}


schema_invoice_generate = {
    "type": "object",
    "properties": {
        "items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "product": {"type": "string"},
                    "quantity": {"type": "integer"}
                },
                "required": ["product", "quantity"]
            }
        }
    },
    "required": ["items"]
}

schema_invoice_confirm = {
    "type": "object",
    "properties": {
        "invoice_id": {"type": "string"}
    },
    "required": ["invoice_id"]
}

