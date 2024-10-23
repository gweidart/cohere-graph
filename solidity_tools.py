from loguru import logger
import subprocess
import os

def compile_solidity_node(contract_code: str):
    """Compiles Solidity code using solc."""
    return Node(task=lambda: _compile_solidity(contract_code))

def _compile_solidity(contract_code: str):
    """Helper function to compile Solidity contract using solc."""
    try:
        # Write the contract to a temporary file
        with tempfile.NamedTemporaryFile(suffix=".sol", delete=False) as tmp_file:
            tmp_file.write(contract_code.encode())
            contract_file = tmp_file.name

        logger.debug(f"Compiling contract located at {contract_file}")

        # Compile the contract with solc
        result = subprocess.run(
            ["solc", "--bin", contract_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode != 0:
            logger.error(f"Compilation failed: {result.stderr}")
            return None

        logger.success(f"Contract compiled successfully.")
        return contract_file
    except Exception as e:
        logger.exception(f"Error during contract compilation: {e}")
        return None

def analyze_with_slither_node(contract_file: str):
    """Generates a LangGraph node to analyze Solidity code with Slither."""
    return Node(task=lambda: _run_slither_analysis(contract_file))

def _run_slither_analysis(contract_file: str):
    """Helper function to run Slither analysis on the contract."""
    try:
        logger.info(f"Running Slither analysis on contract: {contract_file}")

        result = subprocess.run(
            ["slither", contract_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode != 0:
            logger.error(f"Slither analysis failed: {result.stderr}")
            return None

        logger.success("Slither analysis completed successfully.")
        return result.stdout
    except Exception as e:
        logger.exception(f"Error running Slither analysis: {e}")
        return None
