# entity_identifier.py

import re
import json
from LLM_config import call_llm
from prompt_config import get_few_shot_prompt
import logging

def identify_entities_and_generate_gsm_symbolic(question, question_idx=None):
    """
    Identifies entities and generates the GSM symbolic version of the question.
    """
    prompt = [
        {"role": "user", "content": get_few_shot_prompt(question)}
    ]

    # Call the LLM
    response = call_llm(prompt)

    if response is None:
        logging.error(f"Failed to get a response for Question {question_idx}.")
        return [], ''  # Return empty entities and GSM symbolic

    # Debug: Print the LLM response
    # logging.info(f"LLM Response for Question {question_idx}:\n")
    # logging.info(response)
    # logging.info("\n" + "="*50 + "\n")

    # Extract entities and GSM symbolic from the response
    entities = extract_entities(response)
    gsm_symbolic = extract_gsm_symbolic(response)

    return entities, gsm_symbolic

def extract_entities(response_text):
    """
    Extracts entities from the LLM response.
    """
    try:
        entities_section = re.search(r'Entities Identified:\s*(.*?)\s*GSM Symbolic:', response_text, re.DOTALL)
        if entities_section:
            entities_text = entities_section.group(1).strip()
            entities = [line.strip('- ').strip() for line in entities_text.strip().split('\n') if line.strip()]
            return entities
        else:
            logging.warning("No entities found.")
            return []
    except Exception as e:
        logging.error(f"Error extracting entities: {e}")
        return []

def extract_gsm_symbolic(response_text):
    """
    Extracts the GSM symbolic question from the LLM response.
    """
    try:
        gsm_section = re.search(r'GSM Symbolic:\s*(.*)', response_text, re.DOTALL)
        if gsm_section:
            gsm_symbolic = gsm_section.group(1).strip()
            return gsm_symbolic
        else:
            logging.warning("No GSM symbolic found.")
            return ''
    except Exception as e:
        logging.error(f"Error extracting GSM symbolic: {e}")
        return ''

def print_entities(entities):
    print("Entities Identified:")
    for entity in entities:
        print(f"- {entity}")

def print_gsm_symbolic(gsm_symbolic):
    print("\nGSM Symbolic:")
    print(gsm_symbolic)
