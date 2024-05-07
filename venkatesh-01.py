from pywinauto.application import Application
import os
import shutil
from pywinauto import  Desktop
import time
import pyautogui
import pyperclip
import re
import subprocess
from logger import setup_logger
import threading
import win32com.client

     

def get_base_path_from_user():
    """
    Prompts the user to input the base path.

    Returns:
        str: The base path provided by the user.
    """
    print() 
    print("Please provide the path where your project is located.")
    print("For example, if your project is located at 'C:\\Downloads\\Psemi_2024-0.55.0_D1\\muratastudio',")
    print("you should enter 'C:\\Download\\Psemi_2024-0.55.0_D1\\muratastudio'.")
    print() 

    # Prompt the user to input the base path
    base_path = input("Enter the Project Path: ")   
    return base_path



def get_version_type():
    while True:
        print("Which version type do you want to upgrade?")
        print("1. Major")
        print("2. Minor")
        print("3. Patch")
        choice = input("Enter the number corresponding to your choice: ")

        if choice in ["1", "2", "3"]:
            return int(choice)
        else:
            print("Invalid choice. Please enter 1, 2, or 3 for 'major', 'minor', or 'patch' respectively.")


def connect_or_open_vscode(vsCodePath, solution_path):
    try:
        # Try to connect to an existing instance of Visual Studio Code
        app = Application(backend="uia").connect(path=vsCodePath, timeout=10)
        logger.debug('Connected to the existing instance of Visual Studio Code')
        # Activate and focus the window
        app.window().set_focus()
        return app.window()
    except Exception as e:
        logger.debug(f'There is no Visual Studio Code instance existing... {e}')
        logger.debug('Opening a new instance of Visual Studio Code...')

        try:
            subprocess.Popen([vsCodePath, solution_path])
            logger.debug('New Visual Studio Code opened successfully')
            # Wait for the new instance to start
            time.sleep(20)  # Adjust the sleep time as needed
            app = Application(backend="uia").connect(path=vsCodePath, timeout=10)
            return app.window()
        except Exception as e:
            logger.critical('An error occurred while opening Visual Studio Code')            
            raise

def open_solution_explorer(muRataAppInVSCode):
    try:
        logger.debug('Opening Solution Explorer window')
        # Check if Solution Explorer is already open
        solution_explorer = muRataAppInVSCode.child_window(title="Solution Explorer", control_type="Pane", found_index=0)
        if solution_explorer.exists():
            logger.debug('Solution Explorer is already opened')
            solution_explorer.set_focus()
            return
        else:
            # Find the parent menu containing the "View" menu item
            
            #Find and click on the "View" menu item
            view_menu = muRataAppInVSCode.child_window(title="View", control_type="MenuItem")
            view_menu.click_input()
            time.sleep(2)

            # Find and click on the "Solution Explorer" menu item under the "View" menu
            solution_explorer_menu = muRataAppInVSCode.child_window(title="Solution Explorer", control_type="MenuItem")
            solution_explorer_menu.click_input()
            logger.debug('Solution Explorer is Opened')
    except Exception as e:
        logger.critical('An error occurred while opening Solution Explorer')            
        raise
    
     

def get_dte():
    try:
        # Get the DTE object
        dte = win32com.client.GetActiveObject("VisualStudio.DTE.16.0")
        return dte
    except Exception as e:
        logger.critical("Error getting DTE object:", e)
        return None

def set_configuration_to_release(dte):
    try:
        # Get solution
        solution = dte.Solution

        if solution:
            # Get configurations
            solution_configs = solution.SolutionBuild.SolutionConfigurations

            # Iterate over configurations
            for config in solution_configs:
                if config.Name == "Release":
                    config.Activate()
                    logger.debug("Configuration mode set to Release.")
                    return

            # If the Release configuration is not found, raise an exception
            raise Exception("Release configuration not found.")
        else:
            # If no solution is loaded in Visual Studio, raise an exception
            raise Exception("No solution loaded in Visual Studio.")
    except Exception as e:
    
        logger.critical("Error setting configuration to Release")
        raise

   

def build_solution_with_devenv(solution_path,devEnvPath, configuration="Release"):
    try:


        # Construct the devenv command
        devenv_command = [
            devEnvPath,
            solution_path,
            "/build", configuration
        ]
        
        # Run devenv command
        result = subprocess.run(devenv_command, capture_output=True, text=True)
        
        # Check the build result
        if result.returncode == 0:
            logger.debug("Build successful.")
            logger.debug(result.stdout)
        else:
            logger.debug("Build failed.")
            logger.debug("Error output:")
            logger.debug(result.stderr)
    except Exception as e:
        logger.critical("Error during build process")
        raise

def build_process_in_release_mode(dte, sourceFolder1, sourceFolder2, desinationFolderRelease, solution_path, vsCodePath):
    try:
        set_configuration_to_release(dte)
        build_solution_with_devenv(solution_path, vsCodePath)
    except Exception as e:
        logger.critical('Error while building solution in release mode')
        raise


def update_folders_of_application_folder(muRataAppInVSCode, solutionMuRataAppWindow, devicesFolderOfRelease, pluginsFolderOfRelease):
    try:
        ### Click File System Editor ###
        solutionMuRataAppWindow.child_window(title="muRataStudioSetup", control_type="TreeItem").click_input()
        time.sleep(5)
        muRataAppInVSCode.child_window(title="&File System", control_type="Button").click_input()
        logger.debug('File system sditor button is clicked')

	    ###  Delete all the files from Devices of Application Folder and copy from Devices of Release Folder ###
        fileSystemWindow=muRataAppInVSCode.child_window(title="File System (muRataStudioSetup)", auto_id="D:0:0:|File System (muRataStudioSetup)||{00000000-0000-0000-0000-000000000000}|", control_type="Pane")
        applicationFolder=fileSystemWindow.child_window(title="Application Folder", control_type="TreeItem")
        applicationFolder.double_click_input()
        applicationFolder.child_window(title="Devices", control_type="TreeItem").double_click_input()
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('delete')
        deleteProcess=muRataAppInVSCode.child_window(title="Microsoft Visual Studio", control_type="Window")
        deleteProcess.YesButton.click_input()
        logger.debug('All files are deleted from devices folder (File System on Targer Machine-> Application Folder->Devices)')


        explorer=Application(backend="uia").start("explorer.exe")
        fileExplorer = Desktop(backend="uia").window(title='File Explorer')
        fileExplorer.wait('ready', timeout=10)
        logger.debug('File Explorer is Opened')

        addressBar=fileExplorer.child_window(title="Address: Quick access", auto_id="1001", control_type="ToolBar")
        addressBar.click_input()

        pyautogui.write(devicesFolderOfRelease)
        pyautogui.press('enter')
        time.sleep(10)
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('ctrl', 'c')
        muRataAppInVSCode.set_focus()
        pyautogui.hotkey('ctrl', 'v')
        logger.debug(f'All files are copied from {devicesFolderOfRelease} to Devices (File System on Targer Machine-> Application Folder->Devices)')   


        ### Delete all the files from Plugins of Application Folder and copy from Plugins of Release Folder ###
        applicationFolder.child_window(title="Plugins", control_type="TreeItem").double_click_input()
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('delete')
        deleteProcess=muRataAppInVSCode.child_window(title="Microsoft Visual Studio", control_type="Window")
        deleteProcess.YesButton.click_input()
        logger.debug('All files are deleted from plugins folder (File System on Targer Machine-> Application Folder->Plugins)')
        

        # pyautogui.hotkey('ctrl', 'v')
        time.sleep(1)
        explorer=Application(backend="uia").start("explorer.exe")
        fileExplorer = Desktop(backend="uia").window(title='File Explorer')
        fileExplorer.wait('ready', timeout=10)
        time.sleep(5)
        logger.debug('File Explorer is Opened')
        addressBar=fileExplorer.child_window(title="Address: Quick access", auto_id="1001", control_type="ToolBar")
        addressBar.click_input()

        pyautogui.write(pluginsFolderOfRelease)
        pyautogui.press('enter')
        time.sleep(5)
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('ctrl', 'c')
        muRataAppInVSCode.set_focus()
        pyautogui.hotkey('ctrl', 'v')
        logger.debug(f'All files are copied from {pluginsFolderOfRelease} to plugins folder (File System on Targer Machine-> Application Folder->Plugins)')


    except Exception as e:
        logger.critical('Error occurred while updating folders of Application Folder')
        raise


def delete_primary_output_and_shortcuts(fileSystemWindow,muRataAppInVSCode,applicationFolder):
    try:
        ### Delete Primary Output from Murata ###
        applicationFolder.double_click_input()
        fileSystemWindow.child_window(title="Primary output from muRata (Active)", control_type="Edit").click_input()
        pyautogui.press('delete')
        logger.debug('Deleted Primary Output from Murata (File System on Targer Machine-> Application Folder)')

        ### Delete muRata Studio shortcut from Application folder ###
        muRataAppInVSCode.child_window(title="muRata Studio", control_type="ListItem").click_input()
        pyautogui.press('delete')
        logger.debug('Deleted muRata Studio shortcut from Murata (File System on Targer Machine-> Application Folder)')


        ###  Delete muRata Studio shortcut from User's Desktop ###
        usersDesktop=fileSystemWindow.child_window(title="User's Desktop", control_type="TreeItem")
        usersDesktop.double_click_input()
        muRataAppInVSCode.child_window(title="muRata Studio", control_type="ListItem").click_input()
        pyautogui.press('delete')
        logger.debug("Deleted muRata Studio shortcut from Murata (File System on Targer Machine-> User's Desktop)")


        ### Delete muRata Studio shortcut from User's Program Menu->muRata corporation ->muRata Studio ###
        usersProgramsMenu=fileSystemWindow.child_window(title="User's Programs Menu", control_type="TreeItem")
        usersProgramsMenu.double_click_input()
        usersProgramsMenu.MuRataCorporation.double_click_input()
        usersProgramsMenu.MuRataCorporation.MuRataStudio.double_click_input()
        muRataAppInVSCode.child_window(title="muRata Studio", control_type="ListItem").click_input()
        pyautogui.press('delete')
        logger.debug("Deleted muRata Studio shortcut from Murata (File System on Targer Machine->User's Program Menu->muRata corporation)")


    except Exception as e:
        logger.critical('Error while deleting primary output and shortcuts')
        raise


def create_primary_output_from_muRata(muRataAppInVSCode,applicationFolder):
    try:
         ### Create Primary Output from MuRata in Application folder ###
        applicationFolder.right_click_input()

       # Send keys to navigate the context menu
        pyautogui.press('down')  # Move down to "Add" option
        pyautogui.press('enter')  # Select "Add" option
        time.sleep(1)

        # Send keys to navigate to "Primary output"
        pyautogui.press('down') 
        # pyautogui.press('down') # Move down to "Project output"
        pyautogui.press('enter')  # Select "Project output"
        time.sleep(1)
    
        addProjectOutputGroup=muRataAppInVSCode.child_window(title="Add Project Output Group", control_type="Window")

        project=addProjectOutputGroup.child_window(title="Project:", auto_id="240", control_type="ComboBox")
        dropDownOfProject=project.child_window(title="Open", auto_id="DropDown", control_type="Button")
        dropDownOfProject.click_input()
        project.child_window(title="muRata", control_type="ListItem").click_input()

        
        time.sleep(1)
        outputGroups=addProjectOutputGroup.child_window(title="Output Groups:", auto_id="241", control_type="List")
        # outputGroups.child_window(title="Localized resources", control_type="Text").click_input()
        # time.sleep(1)
        outputGroups.child_window(title="Primary output", control_type="Text").click_input()

        time.sleep(1)
        configuration=addProjectOutputGroup.child_window(title="Configuration:", auto_id="242", control_type="ComboBox")
        dropDownOfConfiguration=configuration.child_window(title="Open", auto_id="DropDown", control_type="Button")
        dropDownOfConfiguration.click_input()
        configuration.child_window(title="(Active)", control_type="ListItem").click_input()


        time.sleep(1)
        addProjectOutputGroup.OKButton.click_input()
        logger.debug('Created primary output from muRata')
        
    except Exception as e:
        logger.critical('Error in creating primary output from muRata')
        raise


def create_muRata_shortcut(applicationFolder, fileSystemWindow, muRataAppInVSCode):
    try:
        applicationFolder.double_click_input()
        primaryOutputFromMuRataActive=fileSystemWindow.child_window(title="Primary output from muRata (Active)", control_type="Edit")

        primaryOutputFromMuRataActive.right_click_input()

        time.sleep(1)
        pyautogui.press('down')  # Move down to "Add" option
        time.sleep(1)
        pyautogui.press('enter')  # Select "Add" option
        time.sleep(1)

        shortcutToPrimaryOutputFromMuRataActive=fileSystemWindow.child_window(title="Shortcut to Primary output from muRata (Active)", control_type="Edit")
        shortcutToPrimaryOutputFromMuRataActive.right_click_input()
        time.sleep(1)
        pyautogui.press('down')
        pyautogui.press('down')
        pyautogui.press('down')  
        pyautogui.press('down')
        pyautogui.press('enter')

        properties = muRataAppInVSCode.child_window(title="Properties", control_type="Window")


        properties.child_window(title="(Name)", control_type="TreeItem").double_click_input()
        name=properties.child_window(title="(Name)", control_type="Edit")
        name.type_keys('muRata{SPACE}Studio')
        time.sleep(1)


        icon=properties.child_window(title="Icon", control_type="TreeItem")
        icon.double_click_input()
        time.sleep(0.5)


        iconWindow=muRataAppInVSCode.child_window(title="Icon", control_type="Window")
        time.sleep(0.5)
        iconWindow.child_window(title="Browse...", control_type="Button").click_input()

        time.sleep(0.5)
        selectItemInProject=muRataAppInVSCode.child_window(title="Select Item in Project", control_type="Window")
        selectItemInProject.child_window(title="Application Folder", control_type="ListItem").double_click_input()
        time.sleep(0.5)
        selectItemInProject.child_window(title="muRata.ico", control_type="ListItem").click_input()
        time.sleep(0.5)
        selectItemInProject.OKButton.click_input()


        currentIcon=iconWindow.child_window(title="Current icon:", control_type="List")
        currentIcon.child_window(title="0", control_type="ListItem").click_input()
        time.sleep(0.5)
        iconWindow.OKButton.click_input()


        properties.CloseButton.click_input()  
        logger.debug('Created muRata shortcut with name as muRata and selected icon as muRata.ico')  

    except Exception as e:
        logger.critical('Error in creating muRata shortcut')
        raise
 

def create_primary_output_and_shortcuts(muRataAppInVSCode,applicationFolder,fileSystemWindow ):
    try:
        create_primary_output_from_muRata(muRataAppInVSCode,applicationFolder)
        create_muRata_shortcut(applicationFolder, fileSystemWindow, muRataAppInVSCode)

        ## Move file from Application Folder to User's Desktop
        muRataAppInVSCode.child_window(title="muRata Studio", control_type="Edit").click_input()
        muRataAppInVSCode.type_keys("^x")
        usersDesktop=fileSystemWindow.child_window(title="User's Desktop", control_type="TreeItem")
        usersDesktop.double_click_input()
        muRataAppInVSCode.type_keys("^v")
        logger.debug("Moved muRata Studio shortcut file from Application folder to User's Desktop")

        create_muRata_shortcut(applicationFolder, fileSystemWindow, muRataAppInVSCode)

        ## Copy file from Application Folder to usersProgramsMenu
        muRataAppInVSCode.child_window(title="muRata Studio", control_type="Edit").click_input()
        muRataAppInVSCode.type_keys("^x")
        usersProgramsMenu=fileSystemWindow.child_window(title="User's Programs Menu", control_type="TreeItem")
        # usersProgramsMenu.double_click_input()
        # usersProgramsMenu.MuRataCorporation.double_click_input()
        usersProgramsMenu.MuRataCorporation.MuRataStudio.double_click_input()
        muRataAppInVSCode.type_keys("^v")
        logger.debug("Moved muRata Studio shortcut file from Application folder to User's Programs Menu->MuRataCorporation-> muRataStudio")

        create_muRata_shortcut(applicationFolder, fileSystemWindow, muRataAppInVSCode)

    
        
    except Exception as e:
        logger.critical('Error creating primary output and shortcuts')
        raise


########################################


def fetch_product_code(vdproj_path):
    try:
        with open(vdproj_path, 'r') as file:
            content = file.read()
            # Regular expression pattern to match the ProductCode line
            product_code_pattern = re.compile(r'"ProductCode" = "8:{(.*?)}"')
            # Search for ProductCode line
            match = product_code_pattern.search(content)
            if match:
                return match.group(1)  # Return the captured product code value
            else:
                print("Product code not found in the file.")
                return None
    except FileNotFoundError:
        print(f"File '{vdproj_path}' not found.")
        return None

def fetch_upgrade_code(vdproj_path):
    try:
        with open(vdproj_path, 'r') as file:
            content = file.read()
            # Regular expression pattern to match the UpgradeCode line
            upgrade_code_pattern = re.compile(r'"UpgradeCode" = "8:{(.*?)}"')
            # Search for UpgradeCode line
            match = upgrade_code_pattern.search(content)
            if match:
                return match.group(1)  # Return the captured upgrade code value
            else:
                print("Upgrade code not found in the file.")
                return None
    except FileNotFoundError:
        print(f"File '{vdproj_path}' not found.")
        return None


def get_initial_versions_of_assembly_file_paths(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()

            # Regular expression pattern to match AssemblyVersion and AssemblyFileVersion lines
            version_pattern = re.compile(r'\[assembly: AssemblyVersion\("(.*?)"\)\]\s*\[assembly: AssemblyFileVersion\("(.*?)"\)\]')

            # Search for AssemblyVersion and AssemblyFileVersion lines
            match = version_pattern.search(content)

            if match:
                assembly_version = match.group(1)
                file_version = match.group(2)
                return assembly_version, file_version
            else:
                print("No AssemblyVersion or AssemblyFileVersion found in the file.")
                return None, None
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None, None



def assembly_file_update_version_logic(initial_version, version_type):
    if initial_version and '.' in initial_version:
        version_parts = initial_version.split(".")
        if len(version_parts) == 4:
            major, minor, patch, build = map(int, version_parts)
            
            if version_type == 1:  # Major update
                major += 1
                minor = 0
                patch = 0
                build = 0
            elif version_type == 2:  # Minor update
                minor += 1
                patch = 0
                build = 0
            elif version_type == 3:  # Patch update
                patch += 1
                build = 0
            else:
                print("Invalid version type. Must be 1, 2, or 3 for 'major', 'minor', or 'patch' respectively.")
                return None
            
            new_version = f"{major}.{minor}.{patch}.{build}"
            return new_version
        else:
            print("Invalid initial version format.")
            return None
    else:
        print("Initial version not found or does not follow the expected format.")
        return None



#############################

def get_initial_version_from_muRata_studio_properties(muRataAppInVSCode, solutionMuRataAppWindow ):

    try:
        # Open the Properties window using the F4 key shortcut
        muRataAppInVSCode.type_keys("{F4}")

        solutionMuRataAppWindow.child_window(title="muRataStudioSetup", control_type="TreeItem").click_input()
        time.sleep(2)

        propertiesWindow=muRataAppInVSCode.child_window(title="Properties", control_type="Window")
        # propertiesWindow=muRataAppInVSCode.child_window(title="Properties Window", control_type="Table")
        propertiesWindow.child_window(title="Version", control_type="TreeItem").click_input()
        propertiesWindow.child_window(title="Version",  control_type="Edit").double_click_input()

        # Copy the selected text to the clipboard
        pyautogui.hotkey('ctrl', 'c')

        # Wait briefly for the clipboard to update
        time.sleep(0.5)

        # Retrieve the selected text from the clipboard
        initialVersion = pyperclip.paste()
        print()
        print("Initial Version in MuRata Studio Property is", initialVersion)
        propertiesWindow.CloseButton.click_input()
        return initialVersion
    
    except Exception as e:
        print()
        print(f"Error occurred while getting initial version from muRata Studio properties: {e}")
        raise


def change_version_in_muRata_studio_properties(muRataAppInVSCode, solutionMuRataAppWindow, version_type):
    try:
        initial_version = get_initial_version_from_muRata_studio_properties(muRataAppInVSCode, solutionMuRataAppWindow)

        muRataAppInVSCode.type_keys("{F4}")

        solutionMuRataAppWindow.child_window(title="muRataStudioSetup", control_type="TreeItem").click_input()
        time.sleep(10)

        properties_window = muRataAppInVSCode.child_window(title="Properties", control_type="Window")
        properties_window.child_window(title="Version", control_type="TreeItem").click_input()
        properties_window.child_window(title="Version", control_type="Edit").double_click_input()

        major, minor, patch = map(int, initial_version.split("."))

        if version_type == 1 or version_type == "major":  # Major update
            major += 1
            minor = 0
            patch = 0
        elif version_type == 2 or version_type == "minor":  # Minor update
            minor += 1
            patch = 0
        elif version_type == 3 or version_type == "patch":  # Patch update
            patch += 1
        else:
            print()
            print("Invalid version type. Must be 1, 2, or 3 for 'major', 'minor', or 'patch' respectively, or their string representations.")
            return

        new_version = f"{major}.{minor}.{patch}"

        version_edit = properties_window.child_window(title="Version", control_type="Edit")
        version_edit.type_keys(new_version)
        print()
        print(f" Updated {'Major' if version_type == 1 or version_type == 'major' else 'Minor' if version_type == 2 or version_type == 'minor' else 'Patch'} version in MuRata Studio Property is {new_version}")
        time.sleep(1)

        properties_window.CloseButton.click_input()
        time.sleep(0.5)
        muRataAppInVSCode.MicrosoftVisualStudio.YesButton.click_input()
        time.sleep(1)
        properties_window.CloseButton.click_input()

    except Exception as e:
        print()
        print(f"Error changing version in muRata Studio properties: {e}")
        raise


###########################


def compare_versions(assembly_version, properties_version):
    # Split the versions into segments
    assembly_segments = assembly_version.split('.')
    initial_segments = properties_version.split('.')

    # Ignore the last segment of the assembly_version
    assembly_segments = assembly_segments[:-1]

    # Compare the versions
    return assembly_segments == initial_segments




def update_version_in_file(file_path, new_version):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        with open(file_path, 'w') as file:
            for line in lines:
                if line.strip().startswith("[assembly: AssemblyVersion("):
                    line = f'[assembly: AssemblyVersion("{new_version}")]\n'
                elif line.strip().startswith("[assembly: AssemblyFileVersion("):
                    line = f'[assembly: AssemblyFileVersion("{new_version}")]\n'
                file.write(line)
        print(f"Version updated to {new_version} in {file_path}")
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")


def get_assembly_version(assembly_info_path):
    # Regular expression to match AssemblyVersion line not preceded by //
    version_pattern = re.compile(r'^(?!//).*?\[assembly: AssemblyVersion\("(.*?)"\)\]')

    # Read the AssemblyInfo.cs file
    with open(assembly_info_path, 'r') as file:
        for line in file:
            match = version_pattern.search(line)
            if match:
                return match.group(1)  # Return the AssemblyVersion value

    return None  # Return None if AssemblyVersion not found

def prompt_update_sub_projects(sub_projects):
    """
    Prompt the user whether they want to update any sub-projects.

    Args:
        sub_projects (dict): Dictionary containing sub-project names and paths.

    Returns:
        tuple: A tuple containing a boolean indicating if user wants to update sub-projects,
               and a list of selected sub-projects to update.
    """
    print("Do you want to update any sub-projects? (yes/no)")
    update_choice = input("Enter your choice: ").lower().strip()

    if update_choice == "yes":
        print("Which sub-projects do you want to update?")
        print("Enter the numbers separated by commas (e.g., 1, 2, 3, 4) or 'all' to update all sub-projects.")

        # Print the list of sub-projects
        for i, (project_name, _) in enumerate(sub_projects.items(), start=1):
            print(f"{i}. {project_name}")

        user_choice = input("Enter your choice: ").lower().replace(" ", "")

        if user_choice == "all":
            return True, list(sub_projects.values())
        else:
            user_choice = user_choice.split(",")
            selected_projects = []
            for choice in user_choice:
                if choice.isdigit() and 1 <= int(choice) <= len(sub_projects):
                    selected_projects.append(list(sub_projects.values())[int(choice) - 1])
                else:
                    print(f"Invalid choice: {choice}")

            return True, selected_projects
    elif update_choice == "no":
        print("No sub-projects will be updated.")
        return False, []
    else:
        print("Invalid choice. Please enter 'yes' or 'no'.")
        return False, []

def update_specific_sub_projects_version(base_path, version_type,sub_projects_list):
    for project_path in sub_projects_list:
            initial_version = get_initial_versions_of_assembly_file_paths(project_path)
            if initial_version:
                print(f"Initial version of {project_path}: {initial_version[0]}")
                new_version = assembly_file_update_version_logic(initial_version[0], version_type)
                if new_version:
                    update_version_in_file(project_path, new_version)
            else:
                print(f"Initial version not found for {project_path}.")



def plugins_related_updation(base_path, version_type):
    plugins_file_paths = {
        "AdapterControl": rf"{base_path}\Apps\Plugins\AdapterControl\Properties\AssemblyInfo.cs",
        "ARC1C0608Control": rf"{base_path}\Apps\Plugins\ARC1C0608Control\Properties\AssemblyInfo.cs",
        "ARCxCCxxControl": rf"{base_path}\Apps\Plugins\ARCxCCxxControl\Properties\AssemblyInfo.cs",
        "DocumentViewerControl": rf"{base_path}\Apps\Plugins\DocumentViewerControl\Properties\AssemblyInfo.cs",
        "HelpViewerControl": rf"{base_path}\Apps\Plugins\HelpViewerControl\Properties\AssemblyInfo.cs",
        "MPQ7920Control": rf"{base_path}\Apps\Plugins\MPQ7920Control\Properties\AssemblyInfo.cs",
        "MPQChartControl": rf"{base_path}\Apps\Plugins\MPQChartControl\Properties\AssemblyInfo.cs",
        "MPQControl": rf"{base_path}\Apps\Plugins\MPQControl\Properties\AssemblyInfo.cs",
        "PE24103Control": rf"{base_path}\Apps\Plugins\PE24103Control\Properties\AssemblyInfo.cs",
        "PE24103i2cControl": rf"{base_path}\Apps\Plugins\PE24103i2cControl\Properties\AssemblyInfo.cs",
        "PE24106Control": rf"{base_path}\Apps\Plugins\PE24106Control\Properties\AssemblyInfo.cs",
        "PE26100Control": rf"{base_path}\Apps\Plugins\PE26100Control\Properties\AssemblyInfo.cs",
        "RegisterControl": rf"{base_path}\Apps\Plugins\RegisterControl\Properties\AssemblyInfo.cs",
        "VADERControl": rf"{base_path}\Apps\Plugins\VADERControl\Properties\AssemblyInfo.cs",
    }

    for plugin_name, plugin_path in plugins_file_paths.items():
        initial_version = get_initial_versions_of_assembly_file_paths(plugin_path)
        if initial_version:
            new_version = assembly_file_update_version_logic(initial_version[0], version_type)
            if new_version:
                update_version_in_file(plugin_path, new_version)
        else:
            print(f"Initial version not found for {plugin_name} plugin.")

def update_main_assembly_info(assembly_info_path, version_type):
    initial_version = get_initial_versions_of_assembly_file_paths(assembly_info_path)
    if initial_version:
        new_version = assembly_file_update_version_logic(initial_version[0], version_type)
        if new_version:
            update_version_in_file(assembly_info_path, new_version)
    else:
        print(f"Initial version not found for AssemblyInfo.cs file at {assembly_info_path}.")




def update_version(muRataAppInVSCode,solutionMuRataAppWindow,assembly_version, properties_version, version_type,base_path,assembly_info_path,vdproj_path,sub_projects_list):

    if compare_versions(assembly_version, properties_version):
        major, minor, patch = map(int, properties_version.split("."))

        if version_type == 1:  # Major update
            major += 1
            minor = 0
            patch = 0
        elif version_type == 2:  # Minor update
            minor += 1
            patch = 0
        elif version_type == 3:  # Patch update
            patch += 1
        else:
            print("Invalid version type. Must be 1, 2, or 3 for 'major', 'minor', or 'patch' respectively.")
            return

        new_version = f"{major}.{minor}.{patch}"

        # Print the updated version
        print()
        print(f"Updated {'Major' if version_type == 1 else 'Minor' if version_type == 2 else 'Patch'} version in MuRata Studio Property is {new_version}")

        # Fetch product codes before updating
        before_updating_MSI_version_Product_code = fetch_product_code(vdproj_path)
        print("Product code before updating:", before_updating_MSI_version_Product_code)

        # Fetch upgrade codes before updating
        before_updating_MSI_version_upgrade_code = fetch_upgrade_code(vdproj_path)
        print("Upgrade code before updating:", before_updating_MSI_version_upgrade_code)

        # Update properties version
        
        
        change_version_in_muRata_studio_properties(muRataAppInVSCode, solutionMuRataAppWindow, version_type)
        time.sleep(1)
        # Fetch product codes after updating
        after_updating_MSI_version_Product_code = fetch_product_code(vdproj_path)
        print("Product code after updating:", after_updating_MSI_version_Product_code)

        # Fetch upgrade codes after updating
        after_updating_MSI_version_upgrade_code = fetch_upgrade_code(vdproj_path)
        print("Upgrade code after updating:", after_updating_MSI_version_upgrade_code)

        # Ensure product codes before and after updating are different
        if before_updating_MSI_version_Product_code != after_updating_MSI_version_Product_code:
            # Ensure upgrade codes before and after updating are the same
            if before_updating_MSI_version_upgrade_code == after_updating_MSI_version_upgrade_code:
                print("Error: Upgrade codes before and after updating are the same.")
                return
        else:
            print("Error: Product codes before and after updating are the same. Aborting further steps.")
            return

        # If both conditions are met, proceed to next steps

        
        update_specific_sub_projects_version(base_path, version_type,sub_projects_list)
        plugins_related_updation(base_path, version_type)
        update_main_assembly_info(assembly_info_path, version_type)
    else:
        print("Assembly version and properties version are different. No update needed.")




def install_muRata_studio_setup(msi_path):
    try:
        # Check if the MSI file exists
        if not os.path.exists(msi_path):
            raise FileNotFoundError(f"MSI file not found at: {msi_path}")

        # Launch the MSI installer
        app = Application().start(cmd_line=f"msiexec /i \"{msi_path}\" /passive")

        # Wait for the installation window to appear
        muRataStudioInstallationWindow = app.window(title_re="muRata Studio.*")

        # Perform UI actions
        muRataStudioInstallationWindow.wait('ready', timeout=30)
        muRataStudioInstallationWindow.Next.click_input()
        time.sleep(1)
        muRataStudioInstallationWindow.IAgree.click_input()
        time.sleep(1)
        muRataStudioInstallationWindow.Next.click_input()
        time.sleep(1)
        muRataStudioInstallationWindow.Next.click_input()
        time.sleep(1)
        muRataStudioInstallationWindow.Next.click_input()
        time.sleep(10)

        # Check for success message
        successResponse = muRataStudioInstallationWindow.window(title="muRata Studio has been successfully installed.")
        if successResponse.exists():
            successResponse.close_click()
            print("muRata Studio has been successfully installed.")
        else:
            raise Exception("Error in the installation of muRata Studio")
    except FileNotFoundError as e:
        print('File not found error:', e)
    except Exception as e:
        print('Error in installing muRata Studio setup:', e)




###########################################

def build_muRata_studio_Setup(muRataAppInVSCode, solutionMuRataAppWindow, solutionExplorerWindow):
    try:
        ### Build muRata Studio Setup ###
        solutionExplorerWindow.child_window(title="Collapse All", control_type="Button").click_input()
        solutionMuRataAppWindow.child_window(title="muRataStudioSetup", control_type="TreeItem").right_click_input()
        pyautogui.press("down")
        time.sleep(0.3)
        pyautogui.press("enter")
        logger.debug('Build muRata Studio Setup project is started ')
        capture_the_result_of_build(muRataAppInVSCode)
        logger.debug('Build muRata Studio Setup project is completed')

    except Exception as e:
        logger.critical('Error in building muRataStudio Setup')
        raise

def muRata_studio_installer_packaging(muRataAppInVSCode, solutionMuRataAppWindow, solutionExplorerWindow, solution_path,devEnvPath):
    try:
        build_solution_with_devenv(solution_path,devEnvPath)
        build_muRata_studio_Setup(muRataAppInVSCode, solutionMuRataAppWindow, solutionExplorerWindow)
        install_muRata_studio_setup(solutionMuRataAppWindow, solutionExplorerWindow, )

    except Exception as e:
        logger.critical('Error in muRataStudio installer packaging')
        raise
  

def main():

    try:
        
         ### Delcare VScode path and File Path ###
        vsCodePath=r"C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\Common7\IDE\devenv.exe"
        devEnvPath=r"C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\Common7\IDE\devenv.com"
        
        

        logger.info('Initial Message of Packaging Process !!!')

        ###  Get Project Location Path
        base_path = get_base_path_from_user()
        update_sub_projects, sub_projects_list = prompt_update_sub_projects(sub_projects)
        # Construct the full paths using the provided base path
        sourceFolder1 = fr"{base_path}\Apps\muRata\bin\Debug\Devices"
        sourceFolder2 = fr"{base_path}\Apps\muRata\bin\Debug\Plugins"
        desinationFolderRelease = fr"{base_path}\Apps\muRata\bin\Release"
        # devicesFolderOfRelease = fr"{base_path}\Apps\muRata\bin\Release\Devices"
        devicesFolderOfRelease = os.path.join(base_path, "Apps", "muRata", "bin", "Release", "Devices")
        pluginsFolderOfRelease = fr"{base_path}\Apps\muRata\bin\Release\Plugins"
        assemblyInfosolution_path = fr"{base_path}\Apps\muRata\Properties\AssemblyInfo.cs"
        solution_path = fr"{base_path}\Solutions\muRata.Applications\muRata.Applications.sln"
        ###################
        vdproj_path = fr"{base_path}\Solutions\muRata.Applications\muRataStudioSetup\muRataStudioSetup.vdproj"
        assembly_info_path = fr"{base_path}\Apps\muRata\Properties\AssemblyInfo.cs"
        msi_path= fr"{base_path}\Solutions\muRata.Applications\muRataStudioSetup\Release\muRataStudioSetup.msi"
        sub_projects = {
        "AdapterAccess": rf"{base_path}\Apps\AdapterAccess\Properties\AssemblyInfo.cs",
        "DeviceAccess": rf"{base_path}\Apps\DeviceAccess\Properties\AssemblyInfo.cs",
        "HardwareInterfaces": rf"{base_path}\Apps\HardwareInterfaces\Properties\AssemblyInfo.cs",
        "PluginFramework": rf"{base_path}\Apps\PluginFramework\Properties\AssemblyInfo.cs"
        # Add more sub-projects here if needed
    }
        ################
        ### Get Version Type
        version_type = get_version_type()

        logger.debug(f'Project Folder is, {base_path}')
        logger.debug(f'Version Type is {version_type}')

        logger.info('Packaging Process is Started')

        
        muRataAppInVSCode = connect_or_open_vscode(vsCodePath, solution_path)
        open_solution_explorer(muRataAppInVSCode)
  
  
        
        dte = get_dte()
        
        if not dte:
            logger.debug("Failed to get DTE object. Make sure Visual Studio is running.")
            return

        
        
        build_process_in_release_mode(dte, sourceFolder1, sourceFolder2, desinationFolderRelease, solution_path, devEnvPath)

       

        solutionExplorerWindow=muRataAppInVSCode.child_window(title="Solution Explorer", control_type="Window")
        solutionMuRataAppWindow=solutionExplorerWindow.child_window(title_re=".*Solution 'muRata.Applications'.*", control_type="TreeItem")
        
        
        
        update_folders_of_application_folder(muRataAppInVSCode, solutionMuRataAppWindow, devicesFolderOfRelease, pluginsFolderOfRelease)

        ### Capturing Window
        fileSystemWindow=muRataAppInVSCode.child_window(title="File System (muRataStudioSetup)", auto_id="D:0:0:|File System (muRataStudioSetup)||{00000000-0000-0000-0000-000000000000}|", control_type="Pane")

        

        ### Capturing Window
        applicationFolder=fileSystemWindow.child_window(title="Application Folder", control_type="TreeItem")

        delete_primary_output_and_shortcuts(fileSystemWindow,muRataAppInVSCode,applicationFolder)

        create_primary_output_and_shortcuts(muRataAppInVSCode,applicationFolder,fileSystemWindow )

        ###################
        
        assembly_version = get_assembly_version(assembly_info_path)
        properties_version = extract_properties_version(vdproj_path)
    
    
    
        
        update_version(muRataAppInVSCode,solutionMuRataAppWindow,assembly_version, properties_version, version_type,base_path,assembly_info_path,vdproj_path,sub_projects_list)
        ########################
        
        
        
        install_muRata_studio_setup(msi_path)
        muRata_studio_installer_packaging(muRataAppInVSCode, solutionMuRataAppWindow, solutionExplorerWindow, solution_path,devEnvPath)

        muRataAppInVSCode.CloseButton.click_input()
        devicesWindowInfileExplorer = Desktop(backend="uia").window(title='Devices')
        logger.debug('Visual Studio Code is closed')
        devicesWindowInfileExplorer.set_focus()
        devicesWindowInfileExplorer.CloseButton.click_input()
        pluginsWindowInfileExplorer = Desktop(backend="uia").window(title='Devices')
        pluginsWindowInfileExplorer.set_focus()
        pluginsWindowInfileExplorer.CloseButton.click_input()
   


    except Exception as e:
            logger.critical(f'An error occurred: {e}')
            # fileExplorer.set_focus()
            # fileExplorer.close_file_explorer()
            muRataAppInVSCode.set_focus()
            muRataAppInVSCode.CloseButton.click_input()
            muRataAppInVSCode.MicrosoftVisualStudio.print_control_identifiers()
            muRataAppInVSCode.MicrosoftVisualStudio.DontSave.click_input()
            pyautogui.hotkey('ctrl', 'f4')
            return




if __name__=="__main__":

     # Set up logging
    logger = setup_logger('psemi_packagaing_automation.log')
   
    # Run the main function in a separate thread
    threading.Thread(target=main).start()

 
