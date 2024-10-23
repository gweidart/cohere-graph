from loguru import logger
import os
import re
import random
from config import LOG_FILE, LOG_LEVEL, LOGURU_FORMAT
import sys

# Setting up Loguru based on config.py
logger.remove()  # Remove the default logger to customize

# Add the file handler (for logging to a file)
logger.add(LOG_FILE, rotation="10 MB", retention="10 days", level=LOG_LEVEL, format=LOGURU_FORMAT)

# Add the stdout handler (for logging to console with colors)
logger.add(sys.stdout, level=LOG_LEVEL, format=LOGURU_FORMAT, colorize=True)

# List of vulnerabilities and complexities
VULNERABILITIES = [
    'abiencoderv2-array', 'arbitrary-send-erc20', 'arbitrary-send-erc20-permit', 'arbitrary-send-eth',
    # ... (complete vulnerability list as you had before)
]
COMPLEXITY = ['low', 'medium', 'high']

def parse_assessment_result(assessment_result: str):
    """Parses the string output from the assessment tool and extracts the complexity and vulnerabilities."""
    try:
        # Match complexity, e.g., "Complexity Level: low"
        complexity_match = re.search(r"Complexity Level: (\w+)", assessment_result)
        complexity = complexity_match.group(1) if complexity_match else None
        
        # Match vulnerabilities, e.g., "- arbitrary-send-erc20"
        vulnerabilities_match = re.findall(r"- ([a-zA-Z0-9-_]+)", assessment_result)
        vulnerabilities = vulnerabilities_match if vulnerabilities_match else None

        return complexity, vulnerabilities
    except Exception as e:
        logger.exception(f"Error parsing assessment result: {e}")
        return None, None

def load_prompt_from_file(filename="prompt.txt"):
    """Loads the contract generation prompt from a .txt file."""
    try:
        with open(filename, 'r') as file:
            return file.read()
    except FileNotFoundError:
        logger.error(f"The prompt file {filename} was not found.")
        return None  # Return None instead of an empty string for better error handling
    except Exception as e:
        logger.exception(f"Error loading prompt from {filename}: {e}")
        return None

def get_params() -> str:
    """Generates contract complexity level and a set of vulnerabilities."""
    try:
        complexity = random.choice(COMPLEXITY)

        # Generate a random set of vulnerabilities (between 1 and 3)
        num_vulnerabilities = random.randint(1, 3)
        vulnerabilities = random.sample(VULNERABILITIES, num_vulnerabilities)

        # Validate that the combination of complexity and vulnerabilities makes sense for the contract
        if complexity == 'low' and 'arbitrary-send-erc20' in vulnerabilities:
            logger.warning("Low complexity contracts should not include 'arbitrary-send-erc20'. Removing it.")
            vulnerabilities.remove('arbitrary-send-erc20')

        return complexity, vulnerabilities
    except Exception as e:
        logger.exception(f"Error generating parameters: {e}")
        return None, None
