from loguru import logger
import cohere
from requests.exceptions import RequestException

class CohereAPI:
    def __init__(self, api_key):
        self.client = cohere.Client(api_key)
        logger.success("Cohere API client initialized.")

    def chat(self, messages):
        """Interact with the Cohere chat API."""
        response = self.client.chat(messages=messages)
        return response.generations[0].text  # Adjust based on response structure

    def generate_contract(self, complexity, vulnerabilities):
        """Generates a Solidity contract using Cohere's language model."""
        try:
            prompt = self._build_prompt(complexity, vulnerabilities)
            logger.info(f"Generating contract with complexity '{complexity}' and vulnerabilities {vulnerabilities}.")
            
            # Generate contract using the Cohere API with the recommended parameters
            response = self.client.generate(
                model='command-r-plus-08-2024',
                prompt=prompt,
                max_tokens=2000,  # Increased token limit for larger contracts
                temperature=0.5,  # Balance between creativity and determinism
                k=50,  # Top-k sampling to limit token selection to the top 50 tokens
                p=0.9,  # Cumulative probability threshold to limit token selection
                frequency_penalty=0.1,  # Penalizes repeated tokens to reduce redundancy
                presence_penalty=0.0,  # No penalty for repeated ideas (good for contract structure)
                stop_sequences=["END"],  # Stop generation at "END"
                return_likelihoods='NONE',  # Do not return likelihoods
                num_generations=1  # Generate one contract per request
            )

            # Check if the response is valid
            if response.generations and response.generations[0].text:
                contract_code = response.generations[0].text
                logger.success("Contract generation successful.")
                return contract_code
            else:
                logger.error("Empty or invalid response from Cohere API.")
                return None

        except RequestException as e:
            logger.exception(f"Network error during contract generation: {e}")
            raise e
        except Exception as e:
            logger.exception(f"Unexpected error during contract generation: {e}")
            raise e

def _build_prompt(self, complexity, vulnerabilities):
        """Helper function to build the contract generation prompt."""
        vulnerability_prompt = f"Generate a Solidity contract with the following vulnerabilities: {', '.join(vulnerabilities)}."
        logger.debug(f"Built prompt for complexity '{complexity}' with vulnerabilities {vulnerabilities}.")
        return f"Complexity level: {complexity}\\n{vulnerability_prompt}"
