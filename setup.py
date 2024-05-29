from setuptools import setup, find_packages

setup(
    name='my_project_manager',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'configparser',  # For parsing configuration files
        # Add any other dependencies you're using here
    ],
)