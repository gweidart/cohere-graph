import argparse
import os
from contract_agent import ContractAgent
from cohere_api import CohereAPI
from solidity_tools import compile_solidity_node, analyze_with_slither_node
from storage import ContractStorage
from loguru import logger

def main():
    # Set up argument parsing for the number of contracts
    parser = argparse.ArgumentParser(description="Generate and analyze Solidity contracts.")
    parser.add_argument('-c', '--contracts', type=int, default=1, help='Number of contracts to generate')
    
    # Parse the arguments
    args = parser.parse_args()
    num_contracts = args.contracts

    # Read the Cohere API key from the environment
    cohere_api_key = os.getenv("COHERE_API_KEY")
    if not cohere_api_key:
        logger.error("Cohere API key is not set. Please set the COHERE_API_KEY environment variable.")
        return

    # Initialize the tools
    cohere_tool = CohereAPI(api_key=cohere_api_key)
    storage_tool = ContractStorage()

    # Pass the node functions (compile and analyze) directly to the agent
    agent = ContractAgent(
        cohere_tool=cohere_tool,
        compile_contract_node=compile_solidity_node,
        analyze_contract_node=analyze_with_slither_node,
        storage_tool=storage_tool
    )
    
    agent.execute(num_contracts=num_contracts)

if __name__ == "__main__":
    main()
