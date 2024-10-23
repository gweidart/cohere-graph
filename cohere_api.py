from loguru import logger
import cohere
from requests.exceptions import RequestException

class CohereAPI:
    def __init__(self, api_key):
        self.client = cohere.Client(api_key)
        logger.success("Cohere API client initialized.")

    def generate_contract(self, complexity, vulnerabilities):
        """Generates a Solidity contract using Cohere's language model."""
        try:
            prompt = self._build_prompt(complexity, vulnerabilities)
            logger.info(f"Generating contract with complexity '{complexity}' and vulnerabilities {vulnerabilities}.")

            response = self.client.generate(
                model='command-r-plus-08-2024',
                prompt=prompt,
                max_tokens=1250,
                temperature=0.5,
                stop_sequences=["END"],
                return_likelihoods="NONE"
            )
            contract_code = response.generations[0].text
            logger.success("Contract generation successful.")
            return contract_code
        except RequestException as e:
            logger.exception(f"Error during contract generation: {e}")
            return None

    def _build_prompt(self, complexity, vulnerabilities):
        """Helper function to build the contract generation prompt."""
        vulnerability_prompt = f"Generate a Solidity contract with the following vulnerabilities: {', '.join(vulnerabilities)}."
        logger.debug(f"Built prompt for complexity '{complexity}' with vulnerabilities {vulnerabilities}.")
        return f"Complexity level: {complexity}\n{vulnerability_prompt}"
