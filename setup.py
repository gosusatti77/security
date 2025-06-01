'''
The setup.py file is used to package the Python project ad used in the distribution of the project.
it is used by setyptools to install the package and its dependencies such as metadata, dependencies, and other configurations.
'''

from setuptools import setup, find_packages
from typing import List

def get_requirements() -> List[str]:
    """This function is used to read the requirements from the requirements.txt file.
    """
    requirement_lst = []
    try:
        with open('requirements.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                requirement=line.strip()
                if requirement and requirement!='-e .':
                    requirement_lst.append(requirement)
    
    except FileNotFoundError:
        print("requirements.txt file not found. Please ensure it exists in the project directory.")

    return requirement_lst

setup(
    name='Security',
    version='0.0.1',
    author='Satish Kumar',
    author_email='satishgosu@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements()
)
