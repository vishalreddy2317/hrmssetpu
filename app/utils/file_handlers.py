"""
File handling utilities
"""

import csv
import json
from typing import List, Dict, Any
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class FileHandler:
    """File handling utilities"""
    
    @staticmethod
    def read_csv(file_path: Path) -> List[Dict[str, Any]]:
        """Read data from CSV file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                return list(reader)
        except Exception as e:
            logger.error(f"Error reading CSV file {file_path}: {e}")
            return []
    
    @staticmethod
    def write_csv(file_path: Path, data: List[Dict[str, Any]], fieldnames: List[str]) -> bool:
        """Write data to CSV file"""
        try:
            with open(file_path, 'w', encoding='utf-8', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            return True
        except Exception as e:
            logger.error(f"Error writing CSV file {file_path}: {e}")
            return False
    
    @staticmethod
    def read_json(file_path: Path) -> Dict[str, Any]:
        """Read data from JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except Exception as e:
            logger.error(f"Error reading JSON file {file_path}: {e}")
            return {}
    
    @staticmethod
    def write_json(file_path: Path, data: Dict[str, Any]) -> bool:
        """Write data to JSON file"""
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            logger.error(f"Error writing JSON file {file_path}: {e}")
            return False
    
    @staticmethod
    def ensure_directory(directory: Path) -> bool:
        """Ensure directory exists"""
        try:
            directory.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            logger.error(f"Error creating directory {directory}: {e}")
            return False
