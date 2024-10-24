import pytest
from unittest.mock import patch, Mock
from cohere_api import CohereAPI
from requests.exceptions import RequestException

# Mock API key for testing
API_KEY = "test_api_key"

# Test the chat functionality
@patch("cohere_api.cohere.Client")
def test_chat(mock_cohere_client):
    # Arrange
    mock_client_instance = mock_cohere_client.return_value
    mock_client_instance.chat.return_value = Mock(generations=[Mock(text="Chat response")])

    api = CohereAPI(api_key=API_KEY)
    messages = ["Hello Cohere"]

    # Act
    response = api.chat(messages)

    # Assert
    assert response == "Chat response"
    mock_client_instance.chat.assert_called_once_with(messages=messages)

# Test contract generation with a successful response
@patch("cohere_api.cohere.Client")
def test_generate_contract_success(mock_cohere_client):
    # Arrange
    mock_client_instance = mock_cohere_client.return_value
    mock_client_instance.generate.return_value = Mock(generations=[Mock(text="Generated contract code")])

    api = CohereAPI(api_key=API_KEY)
    complexity = "medium"
    vulnerabilities = ["arbitrary-send-erc20", "reentrancy"]

    # Act
    contract_code = api.generate_contract(complexity, vulnerabilities)

    # Assert
    assert contract_code == "Generated contract code"
    assert mock_client_instance.generate.called
    assert mock_client_instance.generate.call_args[1]["prompt"] == "Complexity level: medium\nGenerate a Solidity contract with the following vulnerabilities: arbitrary-send-erc20, reentrancy."

# Test contract generation with an empty response
@patch("cohere_api.cohere.Client")
def test_generate_contract_empty_response(mock_cohere_client):
    # Arrange
    mock_client_instance = mock_cohere_client.return_value
    mock_client_instance.generate.return_value = Mock(generations=[Mock(text="")])

    api = CohereAPI(api_key=API_KEY)
    complexity = "high"
    vulnerabilities = ["overflow", "underflow"]

    # Act
    contract_code = api.generate_contract(complexity, vulnerabilities)

    # Assert
    assert contract_code is None  # Should return None for empty responses
    assert mock_client_instance.generate.called

@patch("cohere_api.cohere.Client")
def test_generate_contract_network_error(mock_cohere_client):
    # Arrange
    mock_client_instance = mock_cohere_client.return_value
    mock_client_instance.generate.side_effect = RequestException("Network error")

    api = CohereAPI(api_key=API_KEY)
    complexity = "low"
    vulnerabilities = ["race-condition"]

    # Act & Assert
    with pytest.raises(RequestException):
        api.generate_contract(complexity, vulnerabilities)

    assert mock_client_instance.generate.call_count == 3  # Should retry 3 times before failing

# Test the prompt builder
def test_build_prompt():
    api = CohereAPI(api_key=API_KEY)
    prompt = api._build_prompt("low", ["reentrancy", "arbitrary-send-erc20"])

    assert prompt == "Complexity level: low\nGenerate a Solidity contract with the following vulnerabilities: reentrancy, arbitrary-send-erc20."
