# main.py

import json
from entity_identifier import (
    identify_entities_and_generate_gsm_symbolic,
    print_entities,
    print_gsm_symbolic
)
import time
import re

def main():
    # Path to your text file containing questions
    input_file = 'GSM8k_test_data.txt'

    # Read questions from the file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
        # Split on the separator line
        problems = content.strip().split('--------------------------------------------------')

    total_problems = len(problems)
    batch_size = 100  # Adjust the batch size as needed
    results = []

    for batch_start in range(0, total_problems, batch_size):
        batch_end = min(batch_start + batch_size, total_problems)
        batch_problems = problems[batch_start:batch_end]
        print(f"\nProcessing batch {batch_start // batch_size + 1}: Problems {batch_start + 1} to {batch_end}")

        for idx, problem in enumerate(batch_problems, start=batch_start):
            problem = problem.strip()
            if not problem:
                continue  # Skip empty lines

            print(f"\nProcessing Problem {idx + 1}:")

            # Extract the question using regular expressions
            question_match = re.search(r'Question:\s*(.*?)\s*Answer:', problem, re.DOTALL)
            if question_match:
                question = question_match.group(1).strip()
            else:
                print(f"Could not find the question in Problem {idx + 1}. Skipping.")
                continue  # Skip this problem if no question is found

            # Step 1: Identify entities and generate GSM symbolic
            entities, gsm_symbolic = identify_entities_and_generate_gsm_symbolic(question, idx + 1)

            # Check if entities and gsm_symbolic are valid
            if not entities and not gsm_symbolic:
                print(f"Skipping Problem {idx + 1} due to empty response.")
                continue  # Skip to the next problem

            # Step 2: Print entities and GSM symbolic
            print_entities(entities)
            print_gsm_symbolic(gsm_symbolic)

            # Append results
            results.append({
                'problem_number': idx + 1,
                'original_problem_text': problem,
                'question': question,
                'entities_identified': entities,
                'gsm_symbolic': gsm_symbolic
            })

            # Optional: Wait before the next API call to respect rate limits
            time.sleep(1)

        # Save results after each batch
        batch_output_file = f'output_batch_{batch_start // batch_size + 1}.json'
        with open(batch_output_file, 'w', encoding='utf-8') as json_f:
            json.dump(results, json_f, indent=4, ensure_ascii=False)

        # Clear results for the next batch
        results = []

    print("Processing completed.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProcess interrupted by user. Exiting.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
