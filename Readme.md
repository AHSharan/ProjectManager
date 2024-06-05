# ProjectSystemManager

ProjectSystemManager is a Python library designed to manage projects by creating, updating, searching, and fetching project details. It allows you to organize projects in a specified directory and store relevant information such as project name, creation date, technologies used, and a summary.

## Features

- **Set Project Path**: Define the main directory where projects will be stored.
- **Create Project**: Create a new project directory with a details file.
- **Search Projects**: Search for projects based on keywords, creation dates, and technologies.
- **Update Project**: Update project details such as technologies and summary.
- **Fetch Project Details**: Retrieve details of a specific project.

## Installation

Use pip install ProjectSystemManager

## Usage
The configuration file (config.ini) should be located inside the ProjectSystemManager directory. This file defines the main project directory where all projects will be stored. If the file doesn't exist, it will be created with default settings.

### Functions
**SetProjectPath(path)**
Set the main project directory path in the config file.
from ProjectSystemManager import project
project.SetProjectPath("E:")
