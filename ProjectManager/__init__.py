import configparser
import os

# Define the path to the configuration file
config_file_path = os.path.join(os.path.dirname(__file__), 'config.ini')


# Check if the file exists
if not os.path.exists(config_file_path):
    try:
        # Create a ConfigParser object
        config = configparser.ConfigParser()

        # Add the [settings] section
        config.add_section('settings')

        # Set the main_project_directory key
        config.set('settings', 'main_project_directory', 'D:')

        # Write the configuration to a file
        with open(config_file_path, 'w') as configfile:
            config.write(configfile)
        print(f"Configuration file '{config_file_path}' created successfully.")
    except Exception as e:
        print(f"Unable to create '{config_file_path}': {e}")
else:
    print(f"Configuration file '{config_file_path}' already exists.")
