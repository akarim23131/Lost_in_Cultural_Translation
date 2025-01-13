import os
import json
from openrouter_config import get_openai_client
from prompt_config import generate_prompt

def query_model(question, model_name, openai_client):
    """Query the specified model with the given question."""
    try:
        # Generate prompt using the defined function
        prompt = generate_prompt(question)
        
        # Non-streaming response
        completion = openai_client.ChatCompletion.create(
            model=model_name,
            messages=prompt
        )
        return completion["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {e}"

def process_batch(batch_file, models, output_folder):
    """Process a single batch file and save the results."""
    openai_client = get_openai_client()

    # Load questions from the batch file
    with open(batch_file, "r") as f:
        questions = json.load(f)

    # Prepare output structure
    batch_results = []

    # Process each question in the batch
    for question_data in questions:
        problem_number = question_data["problem_number"]
        question = question_data["final_question"]

        # Extract the problem number as an integer
        #problem_number = int(question_data["Problem"].replace("Problem ", "").strip())
        #question = question_data["Question"]  # Extract question text
        model_results = {"problem_number": problem_number, "question": question, "answers": {}}

        # Query each model
        for model in models:
            print(f"Processing Problem {problem_number} with model {model}...")
            answer = query_model(question, model, openai_client)

            # Extract and clean the final "Answer" tag from the model's response
            def extract_answer(response_text):
                """Extract the final numerical answer from the model's response."""
                import re
                # Match the Answer tag with a number, allowing optional quotes or formatting
                match = re.search(r'"Answer":\s*"?(\d+[,.\d]*)"?', response_text)
                if match:
                    # Remove commas and convert to a number
                    return float(match.group(1).replace(',', '')) if '.' in match.group(1) else int(match.group(1).replace(',', ''))
                return None
                

            # Extract final numerical answer
            final_answer = extract_answer(answer)

            # Add extracted answer and reasoning to the model's results
            model_results["answers"][model] = {
                "reasoning": answer,
                "Answer": final_answer
            }

        batch_results.append(model_results)

    # Save results to a file in the output folder
    batch_name = os.path.basename(batch_file).replace(".json", "_results.json")
    output_file = os.path.join(output_folder, batch_name)
    with open(output_file, "w") as f:
        json.dump(batch_results, f, indent=4)
    print(f"Results saved to {output_file}")

def process_all_batches(data_folder, models, output_folder):
    """Process all batch files in the given folder and save results."""
    os.makedirs(output_folder, exist_ok=True)  # Create the output folder if it doesn't exist

    # Load all batch files
    batch_files = [
        os.path.join(data_folder, f) for f in os.listdir(data_folder) if f.endswith(".json")
    ]

    for batch_file in batch_files:
        print(f"Processing batch: {batch_file}")
        process_batch(batch_file, models, output_folder)
