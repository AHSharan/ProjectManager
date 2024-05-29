**My Project Manager**
My Project Manager is a Python package that helps you manage your projects by providing functionalities such as creating projects, updating project details, searching for projects based on various criteria, and fetching project details.

Installation
You can install My Project Manager via pip:

pip install my_project_manager

Usage
Setting the Project Directory Path
Before using any functionalities, you need to set the main project directory path. This is done using the SetProjectPath() function.

from my_project_manager import SetProjectPath

SetProjectPath('/path/to/your/project/directory')

Creating a New Project
You can create a new project using the CreateProject() function.

from my_project_manager import CreateProject

CreateProject("MyProject", technologies=["Python", "Django"], summary="A web development project")

Searching for Projects
You can search for projects based on various criteria such as keywords, start date, and end date using the SearchProject() function.

from my_project_manager import SearchProject

results = SearchProject(keyword="Web", start_date="2023-01-01", end_date="2023-12-31")
print(results)

Updating Project Details
You can update the details of an existing project using the UpdateProject() function.

from my_project_manager import UpdateProject

UpdateProject("MyProject", technologies=["Python", "Django", "REST API"], summary="A web development project with REST API integration")

Fetching Project Details
You can fetch the details of a specific project using the FetchProject() function.

from my_project_manager import FetchProject

details = FetchProject("MyProject")
print(details)

Contributing
Contributions are welcome! If you find any bugs or have suggestions for improvements, please open an issue or submit a pull request on the GitHub repository.

License
This project is licensed under the MIT License - see the LICENSE file for details.

