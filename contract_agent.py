from langgraph.graph import StateGraph
from loguru import logger
from cohere_api import CohereAPI
from storage import ContractStorage
from utils import parse_assessment_result, get_params
from solidity_tools import compile_solidity_node, analyze_with_slither_node
class ContractAgent:
    def __init__(self, cohere_tool, solidity_tool, slither_tool, storage_tool):
        self.cohere_tool = cohere_tool
        self.solidity_tool = solidity_tool
        self.slither_tool = slither_tool
        self.storage_tool = storage_tool

    def execute(self, num_contracts=1):
        """Executes the contract workflow for the specified number of contracts."""
        for i in range(num_contracts):
            logger.info(f"Starting generation for contract {i+1}/{num_contracts}")

            # Define nodes for contract generation, compilation, analysis, and storage
            generate_contract_node = Node(task=self.cohere_tool.run)
            compile_contract_node = compile_solidity_node(self.solidity_tool)
            analyze_contract_node = analyze_with_slither_node(self.slither_tool)
            store_contract_node = Node(task=self.storage_tool.save)

            # Build the execution graph
            contract_graph = StateGraph()
            contract_graph.add_edge(generate_contract_node, compile_contract_node)
            contract_graph.add_edge(compile_contract_node, analyze_contract_node)
            contract_graph.add_edge(analyze_contract_node, store_contract_node)

            # Execute the graph starting from contract generation
            result = contract_graph.execute(start_node=generate_contract_node)
            if result:
                logger.success(f"Contract {i+1}/{num_contracts} execution workflow completed successfully")
            else:
                logger.error(f"Contract {i+1}/{num_contracts} execution workflow failed")
