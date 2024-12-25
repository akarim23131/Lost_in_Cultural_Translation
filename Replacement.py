import json
import random
import re

# Define regex_tokenize
def regex_tokenize(text):
    """
    Tokenizes the input text preserving hyphens and apostrophes within words.
    Also treats placeholders as single tokens.
    """
    pattern = r"\{[^}]+\}|[A-Za-z0-9']+|[-]+|\S"
    return re.findall(pattern, text)

# Define get_placeholder_type
def get_placeholder_type(placeholder_str):
    """
    Extracts the placeholder type from a placeholder string.
    For example, "{City name}" becomes "City name".
    """
    return placeholder_str.strip("{}.,?")

# Main function
def replace_placeholders_in_batch(questions_file, mappings_file, dictionary_file, output_file):
    """
    Batch process symbolic questions and mappings to replace placeholders using a dictionary.
    """
    # Load data from JSON files
    with open(questions_file, 'r', encoding='utf-8') as qf, \
         open(mappings_file, 'r', encoding='utf-8') as mf, \
         open(dictionary_file, 'r', encoding='utf-8') as df:
        questions = json.load(qf)
        mappings = json.load(mf)
        placeholder_dict = json.load(df)


    results = []

    for question_entry in questions:
        problem_number = question_entry["problem_number"]

        if "gsm_symbolic" not in question_entry:
            print(f"Warning: 'gsm_symbolic' missing for problem_number {problem_number}. Skipping.")
            continue

        # Remove "Question:\n" or "Question:\n" (with actual newline) at the start of gsm_symbolic, if it exists
        if question_entry["gsm_symbolic"].startswith("Question:\n") or question_entry["gsm_symbolic"].startswith("Question:\\n"):
            question_entry["gsm_symbolic"] = question_entry["gsm_symbolic"].lstrip("Question:").lstrip("\n").lstrip("\\n")

        symbolic_question = regex_tokenize(question_entry["gsm_symbolic"])

        mapping_entry = next((m for m in mappings if m["problem_number"] == problem_number), None)
        if not mapping_entry:
            print(f"Warning: No mapping found for problem_number {problem_number}.")
            continue

        mapping_rules = mapping_entry["mappings"]
        entity_replacements = {}
        used_placeholders = {key: [] for key in placeholder_dict.keys()}

        for mapping in mapping_rules:
            idx = mapping["index"]

            if idx >= len(symbolic_question):
                print(f"Warning: index {idx} out of range for problem_number {problem_number}.")
                continue

            placeholder = symbolic_question[idx]
            entity = mapping["entity"]
            placeholder_type = get_placeholder_type(placeholder)

            if entity in entity_replacements:
                replacement = entity_replacements[entity]
            else:
                candidates = placeholder_dict.get(placeholder_type, [])
                if candidates:
                    replacement = random.choice(candidates)
                    max_attempts = len(candidates)  # Avoid infinite loops
                    attempts = 0
                    while replacement in used_placeholders[placeholder_type] and attempts < max_attempts:
                        replacement = random.choice(candidates)
                        attempts += 1
                    used_placeholders[placeholder_type].append(replacement)
                else:
                    replacement = "DefaultEntity"
                entity_replacements[entity] = replacement

            punctuation = ''
            if placeholder.endswith('.'):
                punctuation = '.'
            elif placeholder.endswith(','):
                punctuation = ','
            elif placeholder.endswith('?'):
                punctuation = '?'

            replaced_token = replacement + punctuation
            symbolic_question[idx] = replaced_token

        final_question = " ".join(symbolic_question)
        results.append({"problem_number": problem_number, "final_question": final_question})

    with open(output_file, 'w') as of:
        json.dump(results, of, indent=4)

    print(f"Processed questions saved to {output_file}.")

# Example Usage
replace_placeholders_in_batch(
    questions_file=r'Batch of input questions json file',
    mappings_file=r'Batch of input questions' mapping rules json file',
    dictionary_file=r'Dictionary json file',
    output_file=r'output json file to store output of a batch'
)
