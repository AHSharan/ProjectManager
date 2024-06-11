import os 
import json
from datetime import datetime
import configparser
import shutil

config_file_path = os.path.join(os.path.dirname(__file__), 'config.ini')

# Initialize configuration
config = configparser.ConfigParser()

# Define the default details structure
details = {
    "Project Name": "",
    "Date Created On": "",
    "Technologies": "",
    "Summary": "",
    "Diffculty":"",
    "Tags":""
    }

# Define the path to the configuration file inside the ProjectSystemManager directory

# Check if the config file exists
if not os.path.exists(config_file_path):
    # Create the config file with default settings if it doesn't exist
    config['Settings'] = {
        'main_project_directory': 'D:'
    }
    with open(config_file_path, 'w') as configfile:
        config.write(configfile)
else:
    # Read the existing config file
    config.read(config_file_path)

# Ensure the 'Settings' section exists
if 'Settings' not in config:
    config['Settings'] = {
        'main_project_directory': 'D:'
    }
    with open(config_file_path, 'w') as configfile:
        config.write(configfile)

# Initialize PARENTPATH with the value from the config file
PARENTPATH = config.get('Settings', 'main_project_directory')
templates_str = config.get('Settings', 'Templates')
TEMPLATES = dict(item.split(':') for item in templates_str.split(','))

def SetProjectPath(path):
    """
    Set the main project directory path in the config file.

    Args:
        path (str): The path to set as the main project directory.

    Returns:
        str: A success message if the path is set successfully.
    """
    config.read(config_file_path)
    
    if 'Settings' not in config:
        config['Settings'] = {}
    
    config['Settings']['main_project_directory'] = str(path)
    
    with open(config_file_path, 'w') as configfile:
        config.write(configfile)
    return "Path set successfully"

def GetProjectPath():
    """
    Get the Project path from config.ini

    Returns:
        str: The Main path form the config.ini."""
    with open(config_file_path, 'r') as configfile:
        config.read(configfile)
    ProjectPath = config['Settings']['main_project_directory'] 
    return ProjectPath

def CreateTemplate(TemplateName,PROJECTLOCATION):
    if TemplateName in TEMPLATES:
        SourceFile = os.path.join(os.path.dirname(__file__), f'Templates/{TEMPLATES[TemplateName]}')
        DestinationFolder = PROJECTLOCATION
        shutil.copy(SourceFile, DestinationFolder)
        return f"{TemplateName} Template successfully created"
    else:
        return f"Template '{TemplateName}' does not exist in the configuration."
def CreateProject(ProjectName, technologies=None, summary=None, path=None, difficulty="Undefined",tags=[],templates=[]):
    """
    Create a new project directory and details file.

    Args:
        ProjectName (str): The name of the project.
        technologies (list, optional): List of technologies used in the project. Defaults to None.
        summary (str, optional): Summary of the project. Defaults to None.
        path (str, optional): Path where the project directory will be created. Defaults to None.

    Returns:
        str: A success message if the project is created successfully.
    """
    if os.path.exists(os.path.join(PARENTPATH,ProjectName)):
        exit( "Folder already exsits")
        
    if path is None:
        PROJECTLOCATION = os.path.join(PARENTPATH, ProjectName)
    else:
        PROJECTLOCATION = os.path.join(path, ProjectName)
    
    # Create the project directory
    try:
        os.mkdir(PROJECTLOCATION)
    except FileExistsError:
        pass

    # Populate project details
    details = {
        "Project Name": ProjectName,
        "Date Created On": datetime.now().strftime("%Y-%m-%d"),
        "Technologies": technologies if technologies else [],
        "Summary": summary if summary else "",
        "Diffculty":difficulty if difficulty else "",
        "Tags":tags if tags else []
    }

    # Write details to JSON file
    with open(os.path.join(PROJECTLOCATION, 'details.json'), 'w') as fp:
        json.dump(details, fp, indent=4)

    for TemplateName in templates:
        CreateTemplate(TemplateName, PROJECTLOCATION)

        
    return "Project created successfully"

def SearchProject(keyword=None, start_date=None, end_date=None, path=PARENTPATH):
    """
    Search for projects based on keyword, start date, and end date.

    Args:
        keyword (str, optional): Keyword to search for in project names, creation dates, or technologies. Defaults to None.
        start_date (str, optional): Start date to filter projects. Defaults to None.
        end_date (str, optional): End date to filter projects. Defaults to None.
        path (str, optional): Path to search for projects. Defaults to PARENTPATH.

    Returns:
        list: List of project names matching the search criteria.
    """
    results = []
    ProjectPath = path

    if start_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
    if end_date:
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
    
    for project_name in os.listdir(ProjectPath):
        project_path = os.path.join(ProjectPath, project_name)
        if os.path.isdir(project_path):
            details_file = os.path.join(project_path, 'details.json')
            if os.path.exists(details_file):
                with open(details_file, 'r') as fp:
                    details = json.load(fp)
                    project_date_str = details.get("Date Created On", "")
                    project_date = datetime.strptime(project_date_str, "%Y-%m-%d") if project_date_str else None
                    matches_keyword = (
                        keyword is None or 
                        keyword.lower() in project_name.lower() or 
                        keyword.lower() in details.get("Date Created On", "").lower() or 
                        keyword.lower() in details.get("Diffculty", "").lower() or 
                        any(keyword.lower() in tech.lower() for tech in details.get("Technologies", [])) or 
                        any(keyword.lower() in tech.lower() for tech in details.get("Tags", []))
                    )

                    matches_date = True
                    if start_date and project_date:
                        matches_date = matches_date and project_date >= start_date
                    if end_date and project_date:
                        matches_date = matches_date and project_date <= end_date
                    
                    if matches_keyword and matches_date:
                        results.append(project_name)
    
    return results if results else ["No matching projects found"]

def UpdateProject(ProjectName, technologies=None, summary=None, path=None, difficulty="Undefined",tags=[]):
    """
    Update project details.

    Args:
        ProjectName (str): Name of the project to update.
        technologies (list, optional): List of new technologies to add. Defaults to None.
        summary (str, optional): New summary for the project. Defaults to None.
        path (str, optional): Path of the project. Defaults to None.

    Returns:
        str: A success message if the project details are updated successfully.
    """
    ProjectLocation = os.path.join(PARENTPATH, ProjectName)
    if os.path.isdir(ProjectLocation):
        details_file = os.path.join(ProjectLocation, 'details.json')
        if os.path.exists(details_file):
            with open(details_file, 'r') as fp:
                details = json.load(fp)
                
            if technologies:
                details["Technologies"].extend(technologies)
                details["Technologies"] = list(set(details["Technologies"]))
                
            if summary:
                details["Summary"] = summary
            if tags:
                details["Tags"].extend(tags)
                details["Tags"] = list(set(details["Tags"]))
                
            if difficulty:
                details["Difficulty"] = difficulty
            
            with open(details_file, 'w') as fp:
                json.dump(details, fp, indent=4)
            return "Project details updated successfully"
        else:
            return "details.json not found"
    else:
        return "Project directory not found"

def FetchProject(ProjectName, Key=None):
    """
    Fetch project details.

    Args:
        ProjectName (str): Name of the project to fetch details for.
        Key (str, optional): Specific detail to fetch. Defaults to None.

    Returns:
        str or dict: The value of the requested key if provided, else the entire project details.
    """
    ProjectLocation = os.path.join(PARENTPATH, ProjectName)
    DetailsFile = os.path.join(ProjectLocation, "details.json")  

    if os.path.exists(DetailsFile):
        with open(DetailsFile, "r") as fp:
            details = json.load(fp)

        if Key:
            return details.get(Key, "Key not found")
        else:
            return details  
    else:
        return "details.json not found"
