import pytest
from unittest.mock import patch, mock_open
from storage import ContractStorage

# Test saving a contract successfully
@patch("builtins.open", new_callable=mock_open)
@patch("os.makedirs")
def test_save_contract_success(mock_makedirs, mock_file_open):
    # Arrange
    storage = ContractStorage()
    contract_code = "pragma solidity ^0.8.0; contract Test {}"
    
    # Act
    result = storage.save_contract(contract_code)

    # Assert
    mock_file_open.assert_called_once_with(result, 'w')  # Ensure file was opened with correct filename
    mock_file_open().write.assert_called_once_with(contract_code)  # Ensure contract was written to file

# Test saving a contract with empty code (should raise ValueError)
@patch("os.makedirs")
def test_save_contract_empty_code(mock_makedirs):
    # Arrange
    storage = ContractStorage()
    
    # Act & Assert
    with pytest.raises(ValueError, match="Contract code is empty"):
        storage.save_contract("")

# Test saving a Slither report successfully
@patch("builtins.open", new_callable=mock_open)
@patch("os.makedirs")
def test_save_slither_report_success(mock_makedirs, mock_file_open):
    # Arrange
    storage = ContractStorage()
    contract_filepath = "/contracts/contract_20211010.sol"
    slither_report = "Slither analysis report"

    # Act
    result = storage.save_slither_report(contract_filepath, slither_report)

    # Assert
    mock_file_open.assert_called_once_with(result, 'w')  # Ensure file was opened with correct filename
    mock_file_open().write.assert_called_once_with(slither_report)  # Ensure report was written to file

# Test saving an empty Slither report (should raise ValueError)
@patch("os.makedirs")
def test_save_slither_report_empty_report(mock_makedirs):
    # Arrange
    storage = ContractStorage()
    contract_filepath = "/contracts/contract_20211010.sol"
    
    # Act & Assert
    with pytest.raises(ValueError, match="Slither report is empty"):
        storage.save_slither_report(contract_filepath, "")

# Test error handling when file save fails (e.g., permission issue)
@patch("builtins.open", side_effect=PermissionError("No write permission"))
@patch("os.makedirs")
def test_save_contract_permission_error(mock_makedirs, mock_file_open):
    # Arrange
    storage = ContractStorage()
    contract_code = "pragma solidity ^0.8.0; contract Test {}"
    
    # Act & Assert
    with pytest.raises(PermissionError, match="No write permission"):
        storage.save_contract(contract_code)

# Test error handling when saving Slither report fails (e.g., permission issue)
@patch("builtins.open", side_effect=PermissionError("No write permission"))
@patch("os.makedirs")
def test_save_slither_report_permission_error(mock_makedirs, mock_file_open):
    # Arrange
    storage = ContractStorage()
    contract_filepath = "/contracts/contract_20211010.sol"
    slither_report = "Slither analysis report"
    
    # Act & Assert
    with pytest.raises(PermissionError, match="No write permission"):
        storage.save_slither_report(contract_filepath, slither_report)
