import pytest
from unittest.mock import patch, Mock
from contract_agent import ContractAgent

# Test the full workflow (contract generation, compilation, analysis, saving)
@patch("contract_agent.StateGraph")
@patch("contract_agent.ContractStorage.save_contract")  # Mocking save_contract method in the ContractStorage class
@patch("contract_agent.ContractStorage.save_slither_report")  # Mocking save_slither_report method in the ContractStorage class
@patch("contract_agent.compile_solidity_node")
@patch("contract_agent.analyze_with_slither_node")
@patch("contract_agent.CohereAPI")
def test_full_workflow(mock_cohere_api, mock_compile_node, mock_analyze_node, mock_save_contract, mock_save_slither_report, mock_state_graph):
    # Arrange
    mock_state_graph_instance = mock_state_graph.return_value
    mock_state_graph_instance.execute.return_value = True  # Simulate successful workflow execution

    mock_cohere_tool = mock_cohere_api.return_value
    mock_compile_tool = mock_compile_node
    mock_analyze_tool = mock_analyze_node

    mock_save_contract.return_value = "contract saved"  # Simulate successful contract saving
    mock_save_slither_report.return_value = "report saved"  # Simulate successful report saving

    # Initialize the agent with mock components
    agent = ContractAgent(
        cohere_tool=mock_cohere_tool,
        compile_contract_node=mock_compile_tool,
        analyze_contract_node=mock_analyze_tool,  # Ensure Slither analysis is included
        storage_tool=Mock()  # Create a mock for storage_tool to handle saving methods
    )

    # Act
    agent.execute(num_contracts=1)

    # Assert
    mock_state_graph_instance.execute.assert_called_once_with("generate_contract", {'messages': []})
    mock_save_contract.assert_called_once()  # Ensure save_contract is called
    mock_save_slither_report.assert_called_once()  # Ensure save_slither_report is called

# Test the workflow without analysis node
@patch("contract_agent.StateGraph")
@patch("contract_agent.ContractStorage.save_contract")  # Mocking save_contract method in the ContractStorage class
@patch("contract_agent.ContractStorage.save_slither_report")  # Mocking save_slither_report method in the ContractStorage class
@patch("contract_agent.compile_solidity_node")
@patch("contract_agent.CohereAPI")
def test_workflow_without_analysis(mock_cohere_api, mock_compile_node, mock_save_contract, mock_save_slither_report, mock_state_graph):
    # Arrange
    mock_state_graph_instance = mock_state_graph.return_value
    mock_state_graph_instance.execute.return_value = True  # Simulate successful workflow execution

    mock_cohere_tool = mock_cohere_api.return_value
    mock_compile_tool = mock_compile_node

    mock_save_contract.return_value = "contract saved"  # Simulate successful contract saving
    mock_save_slither_report.return_value = "report saved"  # Simulate successful report saving

    # Initialize the agent without the analysis node, passing None explicitly
    agent = ContractAgent(
        cohere_tool=mock_cohere_tool,
        compile_contract_node=mock_compile_tool,
        analyze_contract_node=None,  # Pass None when analysis is skipped
        storage_tool=Mock()  # Create a mock for storage_tool to handle saving methods
    )

    # Act
    agent.execute(num_contracts=1)

    # Assert
    mock_state_graph_instance.execute.assert_called_once_with("generate_contract", {'messages': []})
    mock_save_contract.assert_called_once()  # Ensure save_contract is called
    mock_save_slither_report.assert_called_once()  # Ensure save_slither_report is called
