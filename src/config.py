import pathlib
MODEL_NAME = "gemini-2.5-flash-preview-04-17"

current_directory = pathlib.Path.cwd()
INPUT_FOLDER = current_directory / "input_files"
OUTPUT_FOLDER = current_directory / "output_data"

data_extraction_prompt = """
Extract structured data from the provided invoice.
Adhere strictly to the provided schema for the output.
If a value for a field does not exist or cannot be found in the document, use null for that field remember to keep key values and if value does not exist it will be null.
For the 'issue_date' in 'invoice_metadata', first identify the date in any format present in the document, then convert it to YYYY-MM-DD format.
The 'description' in 'invoice_metadata' should be a natural language summary of the invoice including the invoice number, order ID, date, entities involved, and total price.
Ensure the output is only the structured data as per the schema.
"""