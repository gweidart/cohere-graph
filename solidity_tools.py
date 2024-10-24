import subprocess
import tempfile
import os
from loguru import logger

def _compile_solidity(contract_code):
    """Compiles Solidity contract code using solc."""
    try:
        with tempfile.NamedTemporaryFile(suffix=".sol", delete=False) as temp_contract_file:
            temp_contract_file.write(contract_code.encode('utf-8'))
            temp_contract_file_path = temp_contract_file.name

        # Run solc compiler on the temp contract file
        result = subprocess.run(
            ['solc', '--bin', temp_contract_file_path],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

        if result.returncode == 0:
            logger.info(f"Solidity compilation successful for {temp_contract_file_path}.")
            return result.stdout  # Return compilation output
        else:
            logger.error(f"Solidity compilation failed for {temp_contract_file_path}: {result.stderr}")
            return None  # Compilation failed

    except Exception as e:
        logger.exception(f"Error during Solidity compilation: {e}")
        raise e
    finally:
        try:
            if os.path.exists(temp_contract_file_path):
                os.remove(temp_contract_file_path)  # Clean up temp file
        except Exception as cleanup_error:
            logger.warning(f"Error cleaning up temp file {temp_contract_file_path}: {cleanup_error}")

def _analyze_with_slither(contract_file_path):
    """Runs Slither analysis on a compiled contract using Slither."""
    try:
        result = subprocess.run(
            ['slither', contract_file_path],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

        if result.returncode == 0:
            logger.info(f"Slither analysis successful for {contract_file_path}.")
            return result.stdout  # Return analysis output
        else:
            logger.error(f"Slither analysis failed for {contract_file_path}: {result.stderr}")
            return None  # Slither analysis failed

    except Exception as e:
        logger.exception(f"Error during Slither analysis: {e}")
        raise e

def compile_solidity_node(contract_code):
    """Node wrapper for compiling Solidity contract using solc."""
    return lambda: _compile_solidity(contract_code)

def analyze_with_slither_node(compiled_contract_file):
    """Node wrapper for analyzing compiled contract with Slither."""
    return lambda: _analyze_with_slither(compiled_contract_file)
