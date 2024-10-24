from loguru import logger
import cohere
from requests.exceptions import RequestException
import time

class CohereAPI:
    def __init__(self, api_key):
        self.client = cohere.Client(api_key)
        logger.success("Cohere API client initialized.")

    def chat(self, messages):
        """Interact with the Cohere chat API."""
        try:
            response = self.client.chat(messages=messages)
            if response.generations and response.generations[0].text:
                return response.generations[0].text
            else:
                logger.error("Invalid or empty response from Cohere chat API.")
                return None
        except RequestException as e:
            logger.exception(f"Network error during chat interaction: {e}")
            raise e
        except Exception as e:
            logger.exception(f"Unexpected error during chat interaction: {e}")
            raise e

    def generate_contract(self, complexity, vulnerabilities, retries=3, delay=2):
        """Generates a Solidity contract using Cohere's language model."""
        prompt = self._build_prompt(complexity, vulnerabilities)
        logger.info(f"Generating contract with complexity '{complexity}' and vulnerabilities {vulnerabilities}.")
        
        attempt = 0
        while attempt < retries:
            try:
                response = self.client.generate(
                    model='command-r-plus-08-2024',
                    prompt=prompt,
                    max_tokens=2000,
                    temperature=0.5,
                    k=50,
                    p=0.9,
                    frequency_penalty=0.1,
                    presence_penalty=0.0,
                    stop_sequences=["END"],
                    return_likelihoods='NONE',
                    num_generations=1
                )

                if response.generations and response.generations[0].text:
                    contract_code = response.generations[0].text
                    logger.success("Contract generation successful.")
                    return contract_code
                else:
                    logger.error("Empty or invalid response from Cohere API.")
                    return None

            except RequestException as e:
                logger.warning(f"Network error during contract generation (attempt {attempt + 1}/{retries}): {e}")
                time.sleep(delay)
                attempt += 1

        logger.error("Failed to generate contract after multiple attempts.")
        raise RequestException(f"Failed to generate contract after {retries} attempts.")

    def _build_prompt(self, complexity, vulnerabilities):
        """Helper function to build the contract generation prompt."""
        # Build the vulnerability part of the prompt
        vulnerability_prompt = f"Generate a Solidity contract with the following vulnerabilities: {', '.join(vulnerabilities)}."
        logger.debug(f"Built prompt for complexity '{complexity}' with vulnerabilities {vulnerabilities}.")
        
        # Ensure no extra spaces or newlines by using strip
        return f"Complexity level: {complexity}\n{vulnerability_prompt}".strip()
