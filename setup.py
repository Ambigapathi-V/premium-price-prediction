from setuptools import find_packages, setup
from typing import List

HYPEN_E_DOT = "-e ."

def get_requirements(file_path: str) -> List[str]:
    """
    Reads the requirements from a given file and returns a list of requirements.

    Args:
        file_path (str): The path to the requirements file.

    Returns:
        List[str]: A list of required packages.
    """
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n", "") for req in requirements]
        
        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    
    return requirements

setup(
    name="Premium-Price-Prediction",
    version="0.0.1",
    author="Ambigapathi",
    author_email="ambigapathikavin2@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)
