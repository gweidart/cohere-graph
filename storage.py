from loguru import logger
import os
from datetime import datetime

class ContractStorage:
    def __init__(self):
        self._create_directories()

    def _create_directories(self):
        try:
            os.makedirs('contracts', exist_ok=True)
            os.makedirs('reports', exist_ok=True)
            logger.success("Output directories created or already exist.")
        except Exception as e:
            logger.exception(f"Error creating directories: {e}")
            raise e

    def save_contract(self, contract_code: str):
        """Saves the generated Solidity contract to the output directory."""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"contract_{timestamp}.sol"
        filepath = os.path.join('contracts', filename)
        try:
            with open(filepath, 'w') as f:
                f.write(contract_code)
            logger.success(f"Contract saved at {filepath}")
            return filepath
        except Exception as e:
            logger.exception(f"Error saving contract: {e}")
            return None

    def save_slither_report(self, contract_filepath: str, slither_report: str):
        """Saves the Slither analysis report."""
        report_filename = os.path.splitext(os.path.basename(contract_filepath))[0] + "_SlitherReport.txt"
        report_filepath = os.path.join('reports', report_filename)
        try:
            with open(report_filepath, 'w') as f:
                f.write(slither_report)
            logger.success(f"Slither report saved at {report_filepath}")
            return report_filepath
        except Exception as e:
            logger.exception(f"Error saving Slither report: {e}")
            return None
