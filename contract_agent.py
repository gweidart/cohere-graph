import cohere
from langgraph.graph import StateGraph
from loguru import logger
from cohere_api import CohereAPI
from storage import ContractStorage
from solidity_tools import compile_solidity_node, analyze_with_slither_node

class ContractAgent:
    def __init__(self, cohere_tool, compile_contract_node, analyze_contract_node, storage_tool):
        self.cohere_tool = cohere_tool
        self.compile_contract_node = compile_contract_node
        self.analyze_contract_node = analyze_contract_node
        self.storage_tool = storage_tool

    def execute(self, num_contracts=1):
        """Executes the contract workflow for the specified number of contracts."""
        for i in range(num_contracts):
            logger.info(f"Starting generation for contract {i+1}/{num_contracts}")

            try:
                # Define tasks
                generate_contract_task = self.cohere_tool.chat
                compile_contract_task = self.compile_contract_node
                analyze_contract_task = self.analyze_contract_node if self.analyze_contract_node else None
                save_contract_task = self.storage_tool.save_contract  # Use save_contract method from storage
                save_report_task = self.storage_tool.save_report      # Use save_report method from storage

                # Build the graph
                contract_graph = StateGraph(dict)
                contract_graph.add_node("generate_contract", generate_contract_task)
                contract_graph.add_node("compile_contract", compile_contract_task)
                
                if analyze_contract_task:
                    contract_graph.add_node("analyze_contract", analyze_contract_task)
                    contract_graph.add_edge("compile_contract", "analyze_contract")
                    contract_graph.add_edge("analyze_contract", "save_contract")
                else:
                    contract_graph.add_edge("compile_contract", "save_contract")

                contract_graph.add_edge("generate_contract", "compile_contract")
                contract_graph.add_node("save_contract", save_contract_task)
                contract_graph.add_node("save_report", save_report_task)  # Add report saving node if necessary

                # Execute the graph
                result = contract_graph.execute("generate_contract")
                
                if result:
                    logger.success(f"Contract {i+1}/{num_contracts} execution workflow completed successfully")
                else:
                    logger.error(f"Contract {i+1}/{num_contracts} execution workflow failed")

            except Exception as e:
                logger.exception(f"Unexpected error during workflow execution for contract {i+1}: {e}")
