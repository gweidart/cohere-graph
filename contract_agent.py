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
                analyze_contract_task = self.analyze_contract_node
                save_contract_task = self.storage_tool.save_contract
                save_slither_report_task = self.storage_tool.save_slither_report

                # Build the graph
                contract_graph = StateGraph(dict)
                contract_graph.add_node("generate_contract", generate_contract_task)
                contract_graph.add_node("compile_contract", compile_contract_task)

                # Ensure proper flow with Slither analysis and saving of contract/report
                contract_graph.add_node("analyze_contract", analyze_contract_task)
                contract_graph.add_edge("compile_contract", "analyze_contract")
                contract_graph.add_edge("analyze_contract", "save_contract")

                contract_graph.add_edge("generate_contract", "compile_contract")
                contract_graph.add_node("save_contract", save_contract_task)
                contract_graph.add_node("save_slither_report", save_slither_report_task)
                contract_graph.add_edge("save_contract", "save_slither_report")

                # Initialize the state that will be passed between nodes
                state = {"messages": []}

                # Execute the graph starting from the first node
                logger.info("Executing contract generation workflow...")
                result = contract_graph.execute("generate_contract", state)

                # Debugging: Log the state after each major step
                logger.debug(f"Graph execution result: {result}")
                logger.debug(f"Current state: {state}")

                if result:
                    logger.success(f"Contract {i+1}/{num_contracts} execution workflow completed")

                    # Check if save_contract and save_slither_report are called
                    save_contract_result = contract_graph.get_node_result("save_contract", state)
                    logger.debug(f"save_contract_result: {save_contract_result}")

                    if save_contract_result:
                        save_slither_report_result = contract_graph.get_node_result("save_slither_report", state)
                        logger.debug(f"save_slither_report_result: {save_slither_report_result}")

                        if save_slither_report_result:
                            logger.success(f"Slither report saved for contract {i+1}")
                        else:
                            logger.error(f"Slither report not saved for contract {i+1}")
                    else:
                        logger.error(f"Contract {i+1} was not saved")
                else:
                    logger.error(f"Contract {i+1} workflow failed")

            except Exception as e:
                logger.exception(f"Error in workflow execution for contract {i+1}: {e}")
