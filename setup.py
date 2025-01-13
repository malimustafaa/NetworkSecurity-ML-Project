'''
The setup.py file is an essential part of packaging and distributing python project.
It is used by setuptools to define the configurations off your project, such as its metadata ,depedencies etc.
'''

from setuptools import find_packages,setup # find packages scan all folders and wherever there is __init__ file it cosiders it as package 
from typing import List

def get_requirements() -> List[str]: # type casting it that it will return string
    """
    this function will return list of requirements

    """
    requirement_lst :List[str] = []
    try:
        with open('requirements.txt','r') as file:
            # read lines from file
            lines = file.readlines()
            #process each line
            for line in lines:
                requirement = line.strip() # removing white spaces
                # ignore the empty lines and -e .
                if requirement and requirement != '-e .':
                    requirement_lst.append(requirement)





       
    except FileNotFoundError:
        print("requirements.txt file not found")
    return requirement_lst

setup(

    name = "NetworkSecurity",
    version = "0.0.1",
    author = "M Ali Mustafa",
    author_email="malimustafaa0@gmail.com",
    packages = find_packages(),
    install_requirements = get_requirements()
)
   
 


