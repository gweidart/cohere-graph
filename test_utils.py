import pytest
from utils import parse_assessment_result, load_prompt_from_file

# Test parse_assessment_result
def test_parse_assessment_result():
    result = """
    Complexity Level: low
    - arbitrary-send-erc20
    - abiencoderv2-array
    """
    complexity, vulnerabilities = parse_assessment_result(result)
    assert complexity == "low"
    assert vulnerabilities == ['arbitrary-send-erc20', 'abiencoderv2-array']

def test_parse_assessment_result_invalid():
    result = "Invalid Data"
    complexity, vulnerabilities = parse_assessment_result(result)
    assert complexity is None
    assert vulnerabilities == []  # Should return empty list for vulnerabilities

# Test load_prompt_from_file
def test_load_prompt_from_file(tmpdir):
    # Setup a temporary prompt file for testing
    prompt_file = tmpdir.join("prompt.txt")
    prompt_file.write("Test contract generation prompt")
    
    # Test loading a valid prompt file
    content = load_prompt_from_file(str(prompt_file))
    assert content == "Test contract generation prompt"
    
    # Test loading a non-existent file
    content = load_prompt_from_file("non_existent_file.txt")
    assert content is None
