# evaluate.py

import json
import csv
import time
import os
from llm_config import call_llm
from prompt_config import get_evaluation_prompt
import logging

def main():
    # Directory where your batch JSON files are stored
    input_directory = 'Entities Evaluation\input'  # Use raw string to handle backslashes

    # Output directory for CSV files
    output_directory = 'Entities Evaluation\output'  # You can set a different directory if you prefer

    # Ensure output directory exists
    os.makedirs(output_directory, exist_ok=True)

    # Collect all JSON files
    json_files = [f for f in os.listdir(input_directory) if f.endswith('.json')]

    # Process each JSON file individually
    for json_file in json_files:
        json_path = os.path.join(input_directory, json_file)
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Prepare the output CSV file name (same as JSON file but with .csv extension)
        csv_file_name = os.path.splitext(json_file)[0] + '.csv'
        output_csv_path = os.path.join(output_directory, csv_file_name)

        print(f"Processing {json_file}...")

        # Prepare the CSV file
        with open(output_csv_path, 'w', encoding='utf-8', newline='') as csvfile:
            fieldnames = ['problem_number', 'original_question', 'gsm_symbolic', 'evaluation_result']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for item in data:
                problem_number = item.get('problem_number')
                original_question = item.get('question')
                gsm_symbolic = item.get('gsm_symbolic')

                # Prepare the prompt for GPT-4o
                prompt = get_evaluation_prompt(original_question, gsm_symbolic)

                # Call GPT-4o to evaluate
                evaluation_result = call_llm(prompt, model='gpt-4o')

                # Check if response is None due to API errors
                if evaluation_result is None:
                    evaluation = 'Error'
                else:
                    # Process the response to get 'Yes' or 'No'
                    evaluation = extract_evaluation(evaluation_result)

                # Write to CSV
                writer.writerow({
                    'problem_number': problem_number,
                    'original_question': original_question,
                    'gsm_symbolic': gsm_symbolic,
                    'evaluation_result': evaluation
                })

                # Optional: Wait before the next API call to respect rate limits
                time.sleep(1)

        print(f"Finished processing {json_file}. Results saved to {csv_file_name}")

    print("All files processed.")

def extract_evaluation(response_text):
    """
    Extracts the 'Yes' or 'No' evaluation from the GPT-4 response.
    """
    response_text = response_text.strip().lower()
    if 'yes' in response_text:
        return 'Yes'
    elif 'no' in response_text:
        return 'No'
    else:
        return 'Unclear'

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')
    main()
