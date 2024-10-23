import cohere
import argparse
import os
from contract_agent import ContractAgent
from cohere_api import CohereAPI
from solidity_tools import compile_solidity_node, analyze_with_slither_node
from storage import ContractStorage
from loguru import logger
from config import LOG_FILE, LOG_LEVEL, LOGURU_FORMAT
import sys

# Configure logging from config.py
logger.remove()  # Remove default logger
logger.add(LOG_FILE, rotation="10 MB", retention="10 days", level=LOG_LEVEL, format=LOGURU_FORMAT)
logger.add(sys.stdout, level=LOG_LEVEL, format=LOGURU_FORMAT, colorize=True)

def main():
    parser = argparse.ArgumentParser(description="Generate and analyze Solidity contracts.")
    parser.add_argument('-c', '--contracts', type=int, default=1, help='Number of contracts to generate')
    parser.add_argument('--log-level', type=str, default=LOG_LEVEL, help='Log level (e.g., DEBUG, INFO, WARNING)')
    parser.add_argument('--output-dir', type=str, default='contracts', help='Directory to store generated contracts')
    parser.add_argument('--skip-analysis', action='store_true', help='Skip the analysis step (Slither)')
    
    # Parse the arguments
    args = parser.parse_args()
    num_contracts = args.contracts
    output_dir = args.output_dir
    log_level = args.log_level
    skip_analysis = args.skip_analysis

    # Set log level based on argument
    logger.remove()  # Remove existing handlers
    logger.add(LOG_FILE, rotation="10 MB", retention="10 days", level=log_level, format=LOGURU_FORMAT)
    logger.add(sys.stdout, level=log_level, format=LOGURU_FORMAT, colorize=True)

    # Read the Cohere API key from the environment
    cohere_api_key = os.getenv("COHERE_API_KEY")
    if not cohere_api_key:
        logger.error("Cohere API key is not set. Please set the COHERE_API_KEY environment variable.")
        return

    # Initialize the tools
    try:
        cohere_tool = CohereAPI(api_key=cohere_api_key)
        storage_tool = ContractStorage()
    except Exception as e:
        logger.exception(f"Error initializing tools: {e}")
        return

    # Build the contract agent with or without analysis based on the skip-analysis flag
    if skip_analysis:
        agent = ContractAgent(
            cohere_tool=cohere_tool,
            compile_contract_node=compile_solidity_node,
            analyze_contract_node=None,  # Skip analysis
            storage_tool=storage_tool
        )
    else:
        agent = ContractAgent(
            cohere_tool=cohere_tool,
            compile_contract_node=compile_solidity_node,
            analyze_contract_node=analyze_with_slither_node,
            storage_tool=storage_tool
        )
    
    agent.execute(num_contracts=num_contracts)

if __name__ == "__main__":
    main()
