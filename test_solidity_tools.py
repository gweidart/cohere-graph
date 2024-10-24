import pytest
from unittest.mock import patch, Mock, ANY
from solidity_tools import _compile_solidity, _analyze_with_slither

# Test Solidity compilation with solc
@patch("subprocess.run")
def test_compile_solidity_success(mock_subprocess_run):
    # Arrange
    mock_subprocess_run.return_value = Mock(returncode=0, stdout="Compiled contract", stderr="")
    
    contract_code = "pragma solidity ^0.8.0; contract Test {}"

    # Act
    result = _compile_solidity(contract_code)

    # Assert
    mock_subprocess_run.assert_called_once_with(
        ['solc', '--bin', ANY],  # Use ANY to match any temporary file path
        stdout=ANY, stderr=ANY, text=True
    )
    assert result == "Compiled contract"  # Check successful output

@patch("subprocess.run")
def test_compile_solidity_failure(mock_subprocess_run):
    # Arrange
    mock_subprocess_run.return_value = Mock(returncode=1, stdout="", stderr="Error: Invalid contract")
    
    contract_code = "invalid contract"

    # Act
    result = _compile_solidity(contract_code)

    # Assert
    mock_subprocess_run.assert_called_once_with(
        ['solc', '--bin', ANY],  # Use ANY to match any temporary file path
        stdout=ANY, stderr=ANY, text=True
    )
    assert result is None  # Check that failure returns None

# Test Slither analysis
@patch("subprocess.run")
def test_analyze_with_slither_success(mock_subprocess_run):
    # Arrange
    mock_subprocess_run.return_value = Mock(returncode=0, stdout="Slither analysis report", stderr="")
    
    contract_file_path = "/path/to/compiled_contract.sol"

    # Act
    result = _analyze_with_slither(contract_file_path)

    # Assert
    mock_subprocess_run.assert_called_once_with(
        ['slither', contract_file_path],
        stdout=ANY, stderr=ANY, text=True
    )
    assert result == "Slither analysis report"  # Check successful output

@patch("subprocess.run")
def test_analyze_with_slither_failure(mock_subprocess_run):
    # Arrange
    mock_subprocess_run.return_value = Mock(returncode=1, stdout="", stderr="Error: Slither failed")
    
    contract_file_path = "/path/to/compiled_contract.sol"

    # Act
    result = _analyze_with_slither(contract_file_path)

    # Assert
    mock_subprocess_run.assert_called_once_with(
        ['slither', contract_file_path],
        stdout=ANY, stderr=ANY, text=True
    )
    assert result is None  # Check that failure returns None
