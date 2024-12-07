# LLM_config.py

import openai
import time
import logging
from openai.error import APIError, Timeout, RateLimitError, ServiceUnavailableError

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

# Set your OpenAI API key securely
openai.api_key = <api_key>  # Make sure to set the environment variable 'OPENAI_API_KEY'

def call_llm(prompt, model='gpt-4o', temperature=0, max_retries=5):
    """
    Calls the OpenAI API with the given prompt and returns the response.
    Implements retry logic to handle transient API errors.
    """
    retries = 0
    backoff_factor = 2  # Exponential backoff factor

    while retries < max_retries:
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=prompt,
                temperature=temperature
            )
            return response['choices'][0]['message']['content'].strip()
        except (APIError, Timeout, ServiceUnavailableError) as e:
            retries += 1
            wait_time = backoff_factor ** retries
            logging.warning(f"API error encountered: {e}. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
        except RateLimitError as e:
            retries += 1
            wait_time = backoff_factor ** retries
            logging.warning(f"Rate limit error encountered: {e}. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
        except KeyboardInterrupt:
            logging.info("Process interrupted by user.")
            raise
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            break  # Exit the loop and raise the exception

    logging.error("Max retries exceeded. Exiting.")
    return None  # Return None or raise an exception if preferred
