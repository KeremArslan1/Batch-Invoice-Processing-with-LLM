import asyncio
import time # For timer
from pathlib import Path # For path operations
from google.genai import types # For types.Part
from schema import InvoiceSchema

from ai_client import client
from config import MODEL_NAME, INPUT_FOLDER, OUTPUT_FOLDER, data_extraction_prompt

async def extract_data_from_pdf(filepath: Path, current_client, current_model_name, current_prompt):
    print(f"--- [START] Processing: {filepath.name} ---")

    try:
        pdf_bytes = filepath.read_bytes()
        response = await current_client.aio.models.generate_content(
            model=current_model_name,
            
            config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0),
            response_schema=InvoiceSchema,
            response_mime_type="application/json"
            ),
            contents=[
                types.Part.from_bytes( # or types.Part.from_data
                    data=pdf_bytes,
                    mime_type='application/pdf',
                ),
                current_prompt
            ]
        )
        print(f"--- [SUCCESS] Finished processing: {filepath.name} ---")
        return filepath.name, response.text
    except FileNotFoundError:
        error_msg = f"File not found: {filepath.name}"
        print(f"!!! [ERROR] {error_msg} !!!")
        return filepath.name, error_msg
    except Exception as e:
        error_msg = f"An error occurred while processing {filepath.name}: {e}"
        print(f"!!! [ERROR] {error_msg} !!!")
        return filepath.name, error_msg

async def main_async_processing():
    """
    Finds all PDF files in the INPUT_FOLDER, processes them in parallel
    to extract data using the Gemini API, saves results to OUTPUT_FOLDER,
    and times the entire operation.
    """
    if not client:
        print("Critical Error: GenAI client is not initialized. Check ai_client.py.")
        return
    if not all([MODEL_NAME, INPUT_FOLDER, OUTPUT_FOLDER, data_extraction_prompt]):
        print("Critical Error: One or more configurations (MODEL_NAME, INPUT_FOLDER, OUTPUT_FOLDER, data_extraction_prompt) are missing from config.py.")
        return

    start_time = time.perf_counter()

    input_path = Path(INPUT_FOLDER)
    output_path = Path(OUTPUT_FOLDER)

    try:
        output_path.mkdir(parents=True, exist_ok=True)
        print(f"Output will be saved to: {output_path.resolve()}")
    except Exception as e:
        print(f"Critical Error: Could not create or access output folder '{output_path}': {e}")
        return

    if not input_path.is_dir():
        print(f"Critical Error: Input folder '{input_path}' does not exist or is not a directory.")
        return

    pdf_files = list(input_path.glob("*.pdf"))

    if not pdf_files:
        print(f"No PDF files found in '{input_path}'. Please check the INPUT_FOLDER configuration.")
        end_time_no_files = time.perf_counter()
        duration_no_files = end_time_no_files - start_time
        print(f"Total time taken: {duration_no_files:.2f} seconds.")
        return

    print(f"Found {len(pdf_files)} PDF files to process in parallel from '{input_path.resolve()}'.")

    tasks = []
    for filepath in pdf_files:
        task = asyncio.create_task(extract_data_from_pdf(filepath, client, MODEL_NAME, data_extraction_prompt))
        tasks.append(task)

    all_files_saved_successfully = True
    files_processed_count = 0

    print("\n--- Batch Processing Results ---")
    for completed_task in asyncio.as_completed(tasks):
        filename, result_text = await completed_task
        files_processed_count += 1

        output_filename = f"{Path(filename).stem}_extracted.json"
        output_filepath = output_path / output_filename

        try:
            with open(output_filepath, "w", encoding="utf-8") as f:
                f.write(result_text)
            print(f"Data for '{filename}' saved to '{output_filepath.name}'")
        except IOError as e:
            print(f"!!! [SAVE ERROR] Could not write file {output_filepath.name} for {filename}: {e} !!!")
            all_files_saved_successfully = False
        except Exception as e:
            print(f"!!! [UNEXPECTED SAVE ERROR] while handling output for {filename}: {e} !!!")
            all_files_saved_successfully = False

    end_time = time.perf_counter()
    duration = end_time - start_time

    print(f"\n--- All {files_processed_count}/{len(pdf_files)} PDF processing tasks complete. ---")
    if all_files_saved_successfully and files_processed_count == len(pdf_files):
        print(f"All extracted data successfully saved to '{output_path.resolve()}'.")
    else:
        print(f"Some data may not have been saved correctly to '{output_path.resolve()}'. Please check logs above.")
    print(f"Total processing time: {duration:.2f} seconds.")

if __name__ == "__main__":
    # This is the standard way to run an asyncio program from a script.
    # main_processor.py
    asyncio.run(main_async_processing())
