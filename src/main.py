from ai_client import client
from config import MODEL_NAME, INPUT_FOLDER, OUTPUT_FOLDER, data_extraction_prompt
from google.genai import types

for filepath in INPUT_FOLDER.glob("*.pdf"): # Iterate over all .pdf files

    print(f"\n--- Processing file: {filepath.name} ---")

    try:
        response = client.aio.models.generate_content(
          model=MODEL_NAME,
          contents=[
              types.Part.from_bytes(
                data=filepath.read_bytes(),
                mime_type='application/pdf',
              ),
              data_extraction_prompt
          ]
        )
        print(response.text)

    except Exception as e:
        print(f"An error occurred while processing {filepath.name}: {e}")

