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

## Functions
### SetProjectPath(path)
Set the main project directory path in the config file.
from ProjectSystemManager import project
project.SetProjectPath("E:")
### CreateProject(ProjectName, technologies=None, summary=None, path=None)
Create a new project directory and details file.
project.CreateProject("MyProject", technologies=["Python", "Django"], summary="A web application project")
### SearchProject(keyword=None, start_date=None, end_date=None, path=None)
Search for projects based on keyword, start date, and end date.
results = project.SearchProject(keyword="web", start_date="2023-01-01", end_date="2023-12-31")

### UpdateProject(ProjectName, technologies=None, summary=None, path=None)
Update project details.
project.UpdateProject("MyProject", technologies=["React"], summary="A web application project using React")
### FetchProject(ProjectName, Key=None)
Fetch project details.
details = project.FetchProject("MyProject")

