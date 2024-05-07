import os
import shutil
import subprocess
import re
import time
from pywinauto.application import Application

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


def move_folders(source_dir, dest_dir):
    # Check if the source directory exists
    if not os.path.exists(source_dir):
        print(f"Source directory '{source_dir}' not found.")
        return

    # Create the destination directory if it doesn't exist
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # Move folders from source to destination
    for item in os.listdir(source_dir):
        source_item = os.path.join(source_dir, item)
        dest_item = os.path.join(dest_dir, item)
        if os.path.isdir(source_item):
            shutil.move(source_item, dest_item)

def build_vdproj(vdproj_path):
    # Move folders from Debug to Release
    move_folders(r"C:\Venkatesh\Data-FEB-2024\Mirafra-Learning\Task\Psemi_2024-0.55.0_D1\Psemi_2024-0.55.0_D1\muratastudio\Apps\muRata\bin\Debug\Devices", r"C:\Venkatesh\Data-FEB-2024\Mirafra-Learning\Task\Psemi_2024-0.55.0_D1\Psemi_2024-0.55.0_D1\muratastudio\Apps\muRata\bin\Release\Devices")
    move_folders(r"C:\Venkatesh\Data-FEB-2024\Mirafra-Learning\Task\Psemi_2024-0.55.0_D1\Psemi_2024-0.55.0_D1\muratastudio\Apps\muRata\bin\Debug\Plugins", r"C:\Venkatesh\Data-FEB-2024\Mirafra-Learning\Task\Psemi_2024-0.55.0_D1\Psemi_2024-0.55.0_D1\muratastudio\Apps\muRata\bin\Release\Plugins")

    # Build the deployment project in Release configuration using devenv
    devenv_path = r"c:\Program Files (x86)\Microsoft Visual Studio\2019\Community\Common7\IDE\devenv.com"  # Adjust the path as needed
    command = [devenv_path, vdproj_path, "/build", "Release"]

    result = subprocess.run(command, capture_output=True)

    # Save the build output to a file
    with open("build_output.txt", "wb") as f:
        f.write(result.stdout)
        f.write(result.stderr)

    if result.returncode == 0:
        print("Project built successfully in Release mode.")
    else:
        print("Build failed. Check the output for errors in 'build_output.txt'.")





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



def extract_properties_version(vdproj_path):
    # Regular expression pattern to match the ProductVersion line
    version_pattern = re.compile(r'\"ProductVersion\" = \"\d+:(\d+\.\d+\.\d+)\"')

    # Read the content of the .vdproj file
    with open(vdproj_path, 'r') as file:
        for line in file:
            match = version_pattern.search(line)
            if match:
                return match.group(1)  # Return the captured version value

    return None  # Return None if ProductVersion not found

def properties_version_increment_logic(properties_version, version_type):
    # Split the current version into major, minor, and patch segments
    major, minor, patch = map(int, properties_version.split('.'))
    
    if version_type == 1:  # Increment major version
        major += 1
        minor = 0
        patch = 0
    elif version_type == 2:  # Increment minor version
        minor += 1
        patch = 0
    elif version_type == 3:  # Increment patch version
        patch += 1
    
    # Return the incremented version
    return f"{major}.{minor}.{patch}"

def updating_properties_version_in_file(vdproj_path, properties_new_version):

    try:
        # Read the content of the .vdproj file
        with open(vdproj_path, 'r') as file:
            lines = file.readlines()

        # Regular expression pattern to match the ProductVersion line
        version_pattern = re.compile(r'(\"ProductVersion\" = \"\d+:)(\d+\.\d+\.\d+)(\")')

        # Update the version in memory
        updated_lines = []
        for line in lines:
            match = version_pattern.search(line)
            if match:
                # Replace the old version with the new version
                updated_lines.append(f"{match.group(1)}{properties_new_version}{match.group(3)}\n")
            else:
                updated_lines.append(line)

        # Write the updated content back to the file
        with open(vdproj_path, 'w') as file:
            file.writelines(updated_lines)
        
        print("Properties version updated successfully.")
    except FileNotFoundError:
        print(f"File '{vdproj_path}' not found.")
    except Exception as e:
        print(f"An error occurred while updating properties version: {e}")




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




def update_version(assembly_version, properties_version, version_type,base_path,assembly_info_path,vdproj_path,sub_projects_list):

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
        properties_new_version = properties_version_increment_logic(properties_version, version_type)
        updating_properties_version_in_file(vdproj_path, properties_new_version)
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


def main():
    vdproj_path = r"C:\Venkatesh\Data-FEB-2024\Mirafra-Learning\Task\Psemi_2024-0.55.0_D1\Psemi_2024-0.55.0_D1\muratastudio\Solutions\muRata.Applications\muRataStudioSetup\muRataStudioSetup.vdproj"

    assembly_info_path = r"C:\Venkatesh\Data-FEB-2024\Mirafra-Learning\Task\Psemi_2024-0.55.0_D1\Psemi_2024-0.55.0_D1\muratastudio\Apps\muRata\Properties\AssemblyInfo.cs"
    msi_path=r"C:\Venkatesh\Data-FEB-2024\Mirafra-Learning\Task\Psemi_2024-0.55.0_D1\Psemi_2024-0.55.0_D1\muratastudio\Solutions\muRata.Applications\muRataStudioSetup\Release\muRataStudioSetup.msi"
    version_type = get_version_type()
    
    
    base_path=get_base_path_from_user()
    sub_projects = {
        "AdapterAccess": rf"{base_path}\Apps\AdapterAccess\Properties\AssemblyInfo.cs",
        "DeviceAccess": rf"{base_path}\Apps\DeviceAccess\Properties\AssemblyInfo.cs",
        "HardwareInterfaces": rf"{base_path}\Apps\HardwareInterfaces\Properties\AssemblyInfo.cs",
        "PluginFramework": rf"{base_path}\Apps\PluginFramework\Properties\AssemblyInfo.cs"
        # Add more sub-projects here if needed
    }
    
    update_sub_projects, sub_projects_list = prompt_update_sub_projects(sub_projects)
    #update_specific_sub_projects_version(base_path, version_type)
    assembly_version = get_assembly_version(assembly_info_path)
    properties_version = extract_properties_version(vdproj_path)
    
    
    
    update_version(assembly_version, properties_version, version_type, base_path, assembly_info_path, vdproj_path, sub_projects_list)
    
    #install_muRata_studio_setup(msi_path)


if __name__ == "__main__":
    main()