import json
from logger import setup_logger
base_path='xx'

def increment_sub_project_version(assembly_file_paths):
    try:
        change_version = input("Do you want to increment version in any sub-projects? (y/n): ")

        if change_version.lower() == "y":
            while True:
                print("In which sub-projects, do you want to increment the version?")
                print("1. HardwareAccessFramework")
                print("2. PluginInterface")
                print("3. HardwareAccessFramework and PluginInterface")
                sub_project_choice = input("Enter the number corresponding to your choice: ")

                if sub_project_choice == "1":
                    while True:
                        print("In which project under HardwareAccessFramework do you want to increment the version?")
                        print("1. AdapterAccess")
                        print("2. DeviceAccess")
                        print("3. HardwareInterfaces")
                        print("4. AdapterAccess & DeviceAccess")
                        print("5. AdapterAccess & HardwareInterfaces")
                        print("6. DeviceAccess & HardwareInterfaces")
                        print("7. AdapterAccess & DeviceAccess & HardwareInterfaces")
                        project_choice = input("Enter the number corresponding to your choice: ")

                        if project_choice in ["1", "2", "3", "4", "5", "6", "7"]:
                            project_names = {
                                "1": "AdapterAccess",
                                "2": "DeviceAccess",
                                "3": "HardwareInterfaces",
                                "4": "AdapterAccess",
                                "5": "AdapterAccess",
                                "6": "DeviceAccess",
                                "7": "AdapterAccess"
                            }
                            while True:
                                print(f"Which version-type do you want to increment in {project_names[project_choice]}?")
                                print("1. Major version (e.g., 0.55.2 -> 1.0.0)")
                                print("2. Minor version (e.g., 0.55.2 -> 0.56.0)")
                                print("3. Patch version (e.g., 0.55.2 -> 0.55.3)")
                                version_type = input("Enter the number corresponding to your choice: ")

                                if version_type in ["1", "2", "3"]:
                                    print(f"Note: This increment version will happen in {assembly_file_paths['subProject']['hardwareAccessFrameWork'][project_names[project_choice]]['assemblyFilePath']}.")
                                    return True
                                else:
                                    print("Invalid selection. Please enter a number between 1 and 3.")
                        else:
                            print("Invalid selection. Please enter a number between 1 and 7.")

                elif sub_project_choice == "2":
                    while True:
                        print("Which version-type do you want to increment in PluginInterface?")
                        print("1. Major version (e.g., 0.55.2 -> 1.0.0)")
                        print("2. Minor version (e.g., 0.55.2 -> 0.56.0)")
                        print("3. Patch version (e.g., 0.55.2 -> 0.55.3)")
                        version_type = input("Enter the number corresponding to your choice: ")

                        if version_type in ["1", "2", "3"]:
                            print(f"Note: This increment version will happen in {assembly_file_paths['subProject']['PluginInterface']['PluginFramework']['assemblyFilePath']}.")
                            return True
                        else:
                            print("Invalid selection. Please enter a number between 1 and 3.")

                elif sub_project_choice == "3":
                    while True:
                        print("In which project under HardwareAccessFramework do you want to increment the version?")
                        print("1. AdapterAccess")
                        print("2. DeviceAccess")
                        print("3. HardwareInterfaces")
                        print("4. AdapterAccess & DeviceAccess")
                        print("5. AdapterAccess & HardwareInterfaces")
                        print("6. DeviceAccess & HardwareInterfaces")
                        print("7. AdapterAccess & DeviceAccess & HardwareInterfaces")
                        project_choice = input("Enter the number corresponding to your choice: ")

                        if project_choice in ["1", "2", "3", "4", "5", "6", "7"]:
                            project_names = {
                                "1": "AdapterAccess",
                                "2": "DeviceAccess",
                                "3": "HardwareInterfaces",
                                "4": "AdapterAccess",
                                "5": "AdapterAccess",
                                "6": "DeviceAccess",
                                "7": "AdapterAccess"
                            }
                            while True:
                                print(f"Which version-type do you want to increment in {project_names[project_choice]}?")
                                print("1. Major version (e.g., 0.55.2 -> 1.0.0)")
                                print("2. Minor version (e.g., 0.55.2 -> 0.56.0)")
                                print("3. Patch version (e.g., 0.55.2 -> 0.55.3)")
                                version_type = input("Enter the number corresponding to your choice: ")

                                if version_type in ["1", "2", "3"]:
                                    print(f"Note: This increment version will happen in {assembly_file_paths['subProject']['hardwareAccessFrameWork'][project_names[project_choice]]['assemblyFilePath']}.")
                                    return True
                                else:
                                    print("Invalid selection. Please enter a number between 1 and 3.")
                        else:
                            print("Invalid selection. Please enter a number between 1 and 7.")

                else:
                    print("Invalid selection. Please enter a number between 1 and 3.")

        return False
    except Exception as e:
        print("An error occurred:", str(e))
        return False



      

assembly_file_paths = {
                    "mainProject": {
                        "assemblyFilePath": rf"{base_path}\Apps\muRata\Properties\AssemblyInfo.cs"
            },
            "subProject": {
            "hardwareAccessFrameWork": {
            "adapterAccess": {
            "assemblyFilePath": rf"{base_path}\Apps\AdapterAccess\Properties\AssemblyInfo.cs"
            },
            "deviceAccess": {
            "assemblyFilePath": rf"{base_path}\Apps\DeviceAccess\Properties\AssemblyInfo.cs"
            },
            "hardwareInterfaces": {
            "assemblyFilePath": rf"{base_path}\Apps\HardwareInterfaces\Properties\AssemblyInfo.cs"
            }
            },
            "PluginInterface": {
            "PluginFramework": {
            "assemblyFilePath": rf"{base_path}\Apps\PluginFramework\Properties\AssemblyInfo.cs"
            }
            },
            "Plugins": {
            "AdapterControl": {
            "assemblyFilePath": rf"{base_path}\Apps\Plugins\AdapterControl\Properties\AssemblyInfo.cs"
            },
            "ARC1C0608Control": {
            "assemblyFilePath": rf"{base_path}\Apps\Plugins\ARC1C0608Control\Properties\AssemblyInfo.cs"
            },
            "ARCxCCxxControl": {
            "assemblyFilePath": rf"{base_path}\Apps\Plugins\ARCxCCxxControl\Properties\AssemblyInfo.cs"
            },
            "DocumentViewerControl": {
            "assemblyFilePath": rf"{base_path}\Apps\Plugins\DocumentViewerControl\Properties\AssemblyInfo.cs"
            },
            "HelpViewerControl": {
            "assemblyFilePath": rf"{base_path}\Apps\Plugins\HelpViewerControl\Properties\AssemblyInfo.cs"
            },
            "MPQ7920Control": {
            "assemblyFilePath": rf"{base_path}\Apps\Plugins\MPQ7920Control\Properties\AssemblyInfo.cs"
            },
            "MPQChartControl": {
            "assemblyFilePath": rf"{base_path}\Apps\Plugins\MPQChartControl\Properties\AssemblyInfo.cs"
            },
            "MPQControl": {
            "assemblyFilePath": rf"{base_path}\Apps\Plugins\MPQControl\Properties\AssemblyInfo.cs"
            },
            "PE24103Control": {
            "assemblyFilePath": rf"{base_path}\Apps\Plugins\PE24103Control\Properties\AssemblyInfo.cs"
            },
            "PE24103i2cControl": {
            "assemblyFilePath": rf"{base_path}\Apps\Plugins\PE24103i2cControl\Properties\AssemblyInfo.cs"
            },
            "PE24106Control": {
            "assemblyFilePath": rf"{base_path}\Apps\Plugins\PE24106Control\Properties\AssemblyInfo.cs"
            },
            "PE26100Control": {
            "assemblyFilePath": rf"{base_path}\Apps\Plugins\PE26100Control\Properties\AssemblyInfo.cs"
            },
            "RegisterControl": {
            "assemblyFilePath": rf"{base_path}\Apps\Plugins\RegisterControl\Properties\AssemblyInfo.cs"
            },
            "VADERControl": {
            "assemblyFilePath": rf"{base_path}\Apps\Plugins\VADERControl\Properties\AssemblyInfo.cs"
            }
            }
            }
}
      
isChangeVersion = increment_sub_project_version(assembly_file_paths)
print("isChangeVersion:", isChangeVersion)




# import os
# import json

# def increment_version(version, increment_type):
#     major, minor, patch = version.split('.')
#     if increment_type == 1:  # Major version
#         major = str(int(major) + 1)
#         minor = '0'
#         patch = '0'
#     elif increment_type == 2:  # Minor version
#         minor = str(int(minor) + 1)
#         patch = '0'
#     elif increment_type == 3:  # Patch version
#         patch = str(int(patch) + 1)
#     return f"{major}.{minor}.{patch}"

# def update_version_file(file_path, new_version):
#     with open(file_path, 'r') as file:
#         data = file.readlines()
#     for i, line in enumerate(data):
#         if line.strip().startswith('Version'):
#             data[i] = f"[assembly: AssemblyVersion(\"{new_version}\")]\n"
#             data[i+1] = f"[assembly: AssemblyFileVersion(\"{new_version}\")]\n"
#             break
#     with open(file_path, 'w') as file:
#         file.writelines(data)

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

