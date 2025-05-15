import pathlib
MODEL_NAME = "gemini-2.5-flash-preview-04-17"

current_directory = pathlib.Path.cwd()
INPUT_FOLDER = current_directory / "input_files"
OUTPUT_FOLDER = current_directory / "output_data"

data_extraction_prompt = """
Invoice OCR JSON Extraction Specification 

Use this specification to extract structured data from invoices like the one provided.  
If a value does not exist or cannot be found in the document text, use null.
Do not infer missing fields. Output only the JSON object — no extra start or in the and of output AND DO NOT SAY ITS JSONOR DO NOT WRITE ''' IN THE AND OR START.

JSON Output Format:

{{
  "invoice_metadata": {{
    "issue_date": "<YYYY-MM-DD>" (first get the date in whatever format it is in the document, then convert to YYYY-MM-DD),
    "order_id": "<string>",
    "document_type": "Invoice",
    "description": "<natural language summary of the invoice> (include invoice number, order id, date, entites, total price), e.g., 'Invoice for Allen Goldenen with order ID CA-2012-AG10390140-41017, including 11 Xerox 232 for a total of $790.88.')"
  }},
  "seller_details": {{
    "name": "<string>"
  }},
  "customer_details": {{
    "bill_to.name": "<string>",
    "ship_to.city": "<string>",
    "ship_to.region": "<string>",
    "ship_to.country": "<string>"
  }},
  "shipping_details": {{
    "ship_mode": "<string>",
    "shipping_cost": <float>
  }},
  "financials": {{
    "subtotal": <float>,
    "shipping_total": <float>,
    "total_amount_due": <float>,
    "balance_due": <float>,
    "line_items": [
      {{
        "description": "<string>",
        "quantity": <int>,
        "unit_price": <float>,
        "item_total": <float>
      }}
    ]
  }},
  "additional_info": {{}} (like notes, terms, etc.),
}}

Return accurate and complete JSON data not any other format or additional text.

Example JSON Output:

{
  "invoice_metadata": {
    "issue_date": "2012-03-06",
    "order_id": "CA-2012-AB10015140-40974",
    "document_type": "Invoice",
    "description": "Invoice #36258 for Aaron Bergman with order ID CA-2012-AB10015140-40974, dated 2012-03-06, including 1 Global Push Button Manager's Chair, Indigo for a total of $50.10."
  },
  "seller_details": {
    "name": "SuperStore"
  },
  "customer_details": {
    "bill_to.name": "Aaron Bergman",
    "ship_to.city": "Seattle",
    "ship_to.region": "Washington",
    "ship_to.country": "United States"
  },
  "shipping_details": {
    "ship_mode": "First Class",
    "shipping_cost": 11.13
  },
  "financials": {
    "subtotal": 48.71,
    "shipping_total": 11.13,
    "total_amount_due": 50.10,
    "balance_due": 50.10,
    "line_items": [
      {
        "description": "Global Push Button Manager's Chair, Indigo",
        "quantity": 1,
        "unit_price": 48.71,
        "item_total": 48.71
      }
    ]
  },
  "additional_info": {
    "Notes": "Thanks for your business!",
    "Terms": "Order ID : CA-2012-AB10015140-40974",
    "Discount (20%)": 9.74
  }
}



"""