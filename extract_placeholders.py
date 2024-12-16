import os
import json
import re

# Input JSON file
INPUT_FILE = r"C:\Users\Aabid Karim\Desktop\Bias\Extracting Unique Placeholders\input\Batch_output_batch_2.json"
# Output JSON file
OUTPUT_FILE = r"C:\Users\Aabid Karim\Desktop\Bias\Extracting Unique Placeholders\output\unique_placeholders.json"

def main():
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    # Regex to find placeholders like {name}, {place}, etc.
    placeholder_pattern = re.compile(r"\{(.*?)\}")

    all_placeholders = set()

    # Process the single input file
    print(f"Processing {INPUT_FILE}...")

    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Data is expected to be a list of dictionaries
        for item in data:
            gsm_symbolic = item.get("gsm_symbolic", "")
            # Find all placeholders in the gsm_symbolic string
            found_placeholders = placeholder_pattern.findall(gsm_symbolic)
            all_placeholders.update(found_placeholders)

        # Convert the set to a sorted list for consistency
        all_placeholders_list = sorted(list(all_placeholders))

        # Save the unique placeholders to a JSON file
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as out_f:
            json.dump({"unique_placeholders": all_placeholders_list}, out_f, indent=4, ensure_ascii=False)

        print(f"Extraction complete. Unique placeholders saved to {OUTPUT_FILE}")

    except FileNotFoundError:
        print(f"Error: The file '{INPUT_FILE}' does not exist.")
    except json.JSONDecodeError:
        print(f"Error: The file '{INPUT_FILE}' is not a valid JSON file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
