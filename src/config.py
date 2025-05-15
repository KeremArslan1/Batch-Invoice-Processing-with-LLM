import pathlib
MODEL_NAME = "gemini-2.5-flash-04-17"

current_directory = pathlib.Path.cwd()
INPUT_FOLDER = current_directory / "input_files"
OUTPUT_FOLDER = current_directory / "output_data"

data_extraction_prompt = """
You are a data extraction assistant. Your task is to extract specific information from the provided text.
"""