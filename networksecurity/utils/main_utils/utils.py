import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os, sys
import numpy as np
import pickle


def read_yaml_file(file_path: str) -> dict:
    """
    Reads a YAML file and returns its content as a dictionary.
    
    :param file_path: Path to the YAML file.
    :return: Dictionary containing the YAML file content.
    """
    try:
        with open(file_path, 'r') as file:
            content = yaml.safe_load(file)
        return content
    except Exception as e:
        raise NetworkSecurityException(e, sys)

def write_yaml_file(file_path: str, content: object, replace = False) -> None:
    """
    Writes a dictionary to a YAML file.
    
    :param file_path: Path to the YAML file.
    :param content: Dictionary to write to the file.
    """
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w') as file:
            yaml.dump(content, file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)