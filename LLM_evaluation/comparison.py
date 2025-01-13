import os
import json
import pandas as pd

def load_json(file_path):
    """Load a JSON file."""
    with open(file_path, "r") as f:
        return json.load(f)

def compare_batches(original_file, symbolic_file, solved_gsm8k_file):
    """Compare a single pair of batch files across three datasets."""
    comparison_results = []
    incorrect_pakistan_count = 0
    incorrect_gsm8k_count = 0

    # Load data from all three files
    original_batch = load_json(original_file)
    symbolic_batch = load_json(symbolic_file)
    solved_gsm8k_batch = load_json(solved_gsm8k_file)

    # Compare questions within the batch
    for original, symbolic, solved_gsm8k in zip(original_batch, symbolic_batch, solved_gsm8k_batch):
        try:
            # Normalize problem identifiers
            original_problem = original["Problem"]  # E.g., "Problem 1"
            symbolic_problem = f"Problem {symbolic['problem_number']}"  # Convert number to same format
            solved_gsm8k_problem = f"Problem {solved_gsm8k['problem_number']}"

            # Ensure alignment of problems
            if original_problem != symbolic_problem or symbolic_problem != solved_gsm8k_problem:
                print(f"Problem mismatch: {original_problem}, {symbolic_problem}, {solved_gsm8k_problem}")
                continue

            # Extract and normalize answers
            ground_truth_answer = int(original["Answer"].strip('"'))  # Convert GSM8K "Answer" to int
            pakistan_answer = symbolic["answers"]["openai/gpt-4o"]["Answer"]  # Use Pakistan dataset answer directly
            solved_gsm8k_answer = solved_gsm8k["answers"]["openai/gpt-4o"]["Answer"]  # Use solved GSM8K dataset answer

            # Compare answers
            comparison = {
                "Ground Truth vs Pakistan Dataset": "Correct" if ground_truth_answer == pakistan_answer else "Incorrect",
                "Ground Truth vs Solved GSM8K": "Correct" if ground_truth_answer == solved_gsm8k_answer else "Incorrect"
            }

            # Count incorrect answers
            if comparison["Ground Truth vs Pakistan Dataset"] == "Incorrect":
                incorrect_pakistan_count += 1
            if comparison["Ground Truth vs Solved GSM8K"] == "Incorrect":
                incorrect_gsm8k_count += 1

            # Append results
            comparison_results.append({
                "Batch": os.path.basename(original_file),
                "Problem": original_problem,
                "Ground Truth Answer": ground_truth_answer,
                "Pakistan Dataset Answer": pakistan_answer,
                "GSM8K Solved Answer": solved_gsm8k_answer,
                "Comparison": comparison,
            })
        except KeyError as e:
            print(f"KeyError in batch {os.path.basename(original_file)}: {e}")
        except Exception as e:
            print(f"Error in batch {os.path.basename(original_file)}: {e}")

    return pd.DataFrame(comparison_results), incorrect_pakistan_count, incorrect_gsm8k_count

def process_all_batches(original_folder, symbolic_folder, solved_gsm8k_folder, output_folder):
    """Process all batches across three datasets and save results."""
    os.makedirs(output_folder, exist_ok=True)  # Ensure output folder exists
    master_table = pd.DataFrame()  # Initialize an empty DataFrame for all results
    total_incorrect_pakistan = 0
    total_incorrect_gsm8k = 0

    # Get all batch file names from all folders
    original_files = {f: os.path.join(original_folder, f) for f in os.listdir(original_folder) if f.startswith("batch_") and f.endswith(".json")}
    symbolic_files = {f: os.path.join(symbolic_folder, f) for f in os.listdir(symbolic_folder) if f.startswith("batch_") and f.endswith(".json")}
    solved_gsm8k_files = {f: os.path.join(solved_gsm8k_folder, f) for f in os.listdir(solved_gsm8k_folder) if f.startswith("batch_") and f.endswith(".json")}

    # Match files by batch number
    common_files = set(original_files.keys()) & set(symbolic_files.keys()) & set(solved_gsm8k_files.keys())

    for file_name in common_files:
        print(f"Processing batch: {file_name}")

        # Compare the current pair of batches
        batch_table, incorrect_pakistan, incorrect_gsm8k = compare_batches(
            original_files[file_name], symbolic_files[file_name], solved_gsm8k_files[file_name]
        )

        total_incorrect_pakistan += incorrect_pakistan
        total_incorrect_gsm8k += incorrect_gsm8k

        if not batch_table.empty:
            # Save intermediate results for the current batch
            batch_output_path = os.path.join(output_folder, f"{file_name}_comparison.csv")
            batch_table.to_csv(batch_output_path, index=False)
            print(f"Batch results saved to {batch_output_path}")

            # Append to the master table
            master_table = pd.concat([master_table, batch_table], ignore_index=True)
        else:
            print(f"Batch {file_name} produced no results.")

    # Add summary row to the final master table
    summary_row = {
        "Batch": "Summary",
        "Incorrect Pakistan Dataset Answers": total_incorrect_pakistan,
        "Incorrect GSM8K Answers": total_incorrect_gsm8k
    }
    master_table = pd.concat([master_table, pd.DataFrame([summary_row])], ignore_index=True)

    # Save the final aggregated table
    final_output_path = os.path.join(output_folder, "final_comparison_table.csv")
    if not master_table.empty:
        master_table.to_csv(final_output_path, index=False)
        print(f"Final comparison table saved to {final_output_path}")
    else:
        print("No results to save in the final comparison table.")

# Paths to the folders
original_folder = r"C:\Users\Aabid Karim\Desktop\Bias\LLMs_Evaluation\GSM8K_test_set"
symbolic_folder = r"C:\Users\Aabid Karim\Desktop\Bias\LLMs_Evaluation\Pakistan_dataset_results_ex3"
solved_gsm8k_folder = r"C:\Users\Aabid Karim\Desktop\Bias\LLMs_Evaluation\GSM8K_results"
output_folder = r"C:\Users\Aabid Karim\Desktop\Bias\LLMs_Evaluation\CSV_output_ex3"

# Process all batches
process_all_batches(original_folder, symbolic_folder, solved_gsm8k_folder, output_folder)
