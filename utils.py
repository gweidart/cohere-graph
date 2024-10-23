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
        complexity_match = re.search(r"Complexity Level: (\\w+)", assessment_result)
        complexity = complexity_match.group(1) if complexity_match else None
        vulnerabilities_match = re.findall(r"- (\\w+-\\w+)", assessment_result)
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
        return ""
    except Exception as e:
        logger.exception(f"Error loading prompt from {filename}: {e}")
        return ""

def get_params() -> str:
    """Generates contract complexity level and a set of vulnerabilities."""
    try:
        complexity = random.choice(COMPLEXITY)
        selected_vulnerabilities = random.sample(VULNERABILITIES, k=random.randint(1, 5))

        result = f"Complexity Level: {complexity.capitalize()}\n"
        if selected_vulnerabilities:
            result += "Identified Vulnerabilities:\n" + "\n".join(f"- {vuln}" for vuln in selected_vulnerabilities)
        else:
            result += "No vulnerabilities identified."

        logger.success(f"Complexity: '{complexity}', Vulnerabilities: {selected_vulnerabilities}")
        return result.strip()
    except Exception as e:
        logger.exception(f"Error generating complexity and vulnerabilities: {e}")
        return f"Error: {e}"
