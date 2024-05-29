import os 
import json
from datetime import datetime
import configparser

# Define the default details structure
details = {
    "Project Name": "",
    "Date Created On": "",
    "Technologies": "",
    "Summary": ""
}

# Read configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

# Initialize PARENTPATH with the value from the config file
PARENTPATH = config.get('Settings', 'main_project_directory')

def SetProjectPath(path):
    """
    Set the main project directory path in the config file.

    Args:
        path (str): The path to set as the main project directory.

    Returns:
        str: A success message if the path is set successfully.
    """
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    if 'Settings' not in config:
        config['Settings'] = {}
    
    config['Settings']['main_project_directory'] = str(path)
    
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    return "Path Set successfully"

def CreateProject(ProjectName, technologies=None, summary=None, path=None):
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
        "Summary": summary if summary else ""
    }

    # Write details to JSON file
    with open(os.path.join(PROJECTLOCATION, 'details.json'), 'w') as fp:
        json.dump(details, fp, indent=4)

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
                        any(keyword.lower() in tech.lower() for tech in details.get("Technologies", []))
                    )

                    matches_date = True
                    if start_date and project_date:
                        matches_date = matches_date and project_date >= start_date
                    if end_date and project_date:
                        matches_date = matches_date and project_date <= end_date
                    
                    if matches_keyword and matches_date:
                        results.append(project_name)
    
    return results if results else ["No matching projects found"]

def UpdateProject(ProjectName, technologies=None, summary=None, path=None):
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

