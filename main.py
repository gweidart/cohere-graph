import argparse
from contract_agent import ContractAgent
from cohere_api import CohereAPI
from solidity_tools import compile_solidity_node, analyze_with_slither_node
from storage import ContractStorage

def main():
    # Argument parser for number of contracts
    parser = argparse.ArgumentParser(description="Smart contract generation and analysis.")
    parser.add_argument('-c', '--contracts', type=int, default=1, help="Number of contracts to generate")
    
    args = parser.parse_args()
    num_contracts = args.contracts
    
    # Initialize components
    cohere_tool = CohereAPI(api_key="your_cohere_api_key")
    storage_tool = ContractStorage()
    
    # Create and execute the contract agent
    agent = ContractAgent(
        cohere_tool=cohere_tool,
        compile_contract_node=compile_solidity_node,
        analyze_contract_node=analyze_with_slither_node,
        storage_tool=storage_tool
    )
    
    # Execute the agent's workflow
    agent.execute(num_contracts=num_contracts)

if __name__ == "__main__":
    main()
