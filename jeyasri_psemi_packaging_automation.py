# import os
# import shutil
# import subprocess

# def move_folders(source_dir, dest_dir):
#     # Check if the source directory exists
#     if not os.path.exists(source_dir):
#         print(f"Source directory '{source_dir}' not found.")
#         return

#     # Create the destination directory if it doesn't exist
#     if not os.path.exists(dest_dir):
#         os.makedirs(dest_dir)

#     # Move folders from source to destination
#     for item in os.listdir(source_dir):
#         source_item = os.path.join(source_dir, item)
#         dest_item = os.path.join(dest_dir, item)
#         if os.path.isdir(source_item):
#             shutil.move(source_item, dest_item)

# def build_vdproj(vdproj_path):
#     # Move folders from Debug to Release
#     move_folders(r"c:\Users\jeyasri\Downloads\Psemi_packaging_automation\Psemi_2024-0.55.0_D1\import os
# import shutil
# import subprocess

# def move_folders(source_dir, dest_dir):
#     # Check if the source directory exists
#     if not os.path.exists(source_dir):
#         print(f"Source directory '{source_dir}' not found.")
#         return

#     # Create the destination directory if it doesn't exist
#     if not os.path.exists(dest_dir):
#         os.makedirs(dest_dir)

#     # Move folders from source to destination
#     for item in os.listdir(source_dir):
#         source_item = os.path.join(source_dir, item)
#         dest_item = os.path.join(dest_dir, item)
#         if os.path.isdir(source_item):
#             shutil.move(source_item, dest_item)

# def build_vdproj(vdproj_path):
#     # Move folders from Debug to Release
#     move_folders(r"c:\Users\jeyasri\Downloads\Psemi_packaging_automation\Psemi_2024-0.55.0_D1\muratastudio\Apps\muRata\bin\Debug\Devices", r"c:\Users\jeyasri\Downloads\Psemi_packaging_automation\Psemi_2024-0.55.0_D1\muratastudio\Apps\muRata\bin\Release\Devices")
#     move_folders(r"c:\Users\jeyasri\Downloads\Psemi_packaging_automation\Psemi_2024-0.55.0_D1\muratastudio\Apps\muRata\bin\Debug\Plugins", r"c:\Users\jeyasri\Downloads\Psemi_packaging_automation\Psemi_2024-0.55.0_D1\muratastudio\Apps\muRata\bin\Release\Plugins")

#     # Build the deployment project in Release configuration using devenv
#     devenv_path = r"c:\Program Files (x86)\Microsoft Visual Studio\2019\Community\Common7\IDE\devenv.com"  # Adjust the path as needed
#     command = [devenv_path, vdproj_path, "/build", "Release"]

#     result = subprocess.run(command, capture_output=True)
#  # Save the build output to a file
#     with open("build_output.txt", "wb") as f:
#         f.write(result.stdout)
#         f.write(result.stderr)

#     if result.returncode == 0:
#         print("Project built successfully in Release mode.")
#     else:
#         print("Build failed. Check the output for errors in 'build_output.txt'.")

# if __name__ == "__main__":
#     vdproj_path = r"c:\Users\jeyasri\Downloads\Psemi_packaging_automation\Psemi_2024-0.55.0_D1\muratastudio\Solutions\muRata.Applications\muRataStudioSetup\muRataStudioSetup.vdproj"
#     build_vdproj(vdproj_path)
#     move_folders(r"c:\Users\jeyasri\Downloads\Psemi_packaging_automation\Psemi_2024-0.55.0_D1\muratastudio\Apps\muRata\bin\Debug\Plugins", r"c:\Users\jeyasri\Downloads\Psemi_packaging_automation\Psemi_2024-0.55.0_D1\muratastudio\Apps\muRata\bin\Release\Plugins")

#     # Build the deployment project in Release configuration using devenv
#     devenv_path = r"c:\Program Files (x86)\Microsoft Visual Studio\2019\Community\Common7\IDE\devenv.com"  # Adjust the path as needed
#     command = [devenv_path, vdproj_path, "/build", "Release"]

#     result = subprocess.run(command, capture_output=True)
#  # Save the build output to a file
#     with open("build_output.txt", "wb") as f:
#         f.write(result.stdout)
#         f.write(result.stderr)

#     if result.returncode == 0:
#         print("Project built successfully in Release mode.")
#     else:
#         print("Build failed. Check the output for errors in 'build_output.txt'.")

# if __name__ == "__main__":
#     vdproj_path = r"c:\Users\jeyasri\Downloads\Psemi_packaging_automation\Psemi_2024-0.55.0_D1\muratastudio\Solutions\muRata.Applications\muRataStudioSetup\muRataStudioSetup.vdproj"
#     build_vdproj(vdproj_path)



# import clr
# import System
# clr.AddReference("EnvDTE")
# from EnvDTE import DTE

# def change_to_release_mode(solution_file_path):
#     try:
#         # Create an instance of DTE
#         dte = DTE()

#         # Open the solution
#         dte.Solution.Open(solution_file_path)

#         # Get the solution object
#         solution = dte.Solution
#         # Get the configurations for the solution
#         configurations = solution.SolutionBuild.SolutionConfigurations

#         # Find the Release configuration
#         for configuration in configurations:
#             # print ("configuration one by one", configuration)
#             if configuration.Name == "Release":
#                 # Change the active configuration to Release
#                 solution.SolutionBuild.ActiveConfiguration = configuration

#                 print("Changed solution configuration to Release mode.")
#                 return

#         print("Release configuration not found for the solution.")
#         return f"Changed project '{project_name}' to Release mode."

  
#     except Exception as e:
#         return str(e)

# # Example usage:
# solution_file_path = r"c:\Users\jeyasri\Downloads\Psemi_packaging_automation\Psemi_2024-0.55.0_D1\muratastudio\Solutions\muRata.Applications\muRata.Applications.sln"
# project_name = "YourProjectName"

# print(change_to_release_mode(solution_file_path))




import clr

# Add a reference to the Visual Studio type library
clr.AddReference("EnvDTE")

# Now import the types from the EnvDTE namespace
import EnvDTE


class VisualStudioAutomation:
    def change_to_release_mode(self, solution_file_path):
        # Create an instance of DTE
        dte = DTE()

        # Open the solution
        dte.Solution.Open(solution_file_path)

        # Get the solution object
        solution = dte.Solution
        
        configurations = solution.SolutionBuild.SolutionConfigurations

  
        for configuration in configurations:
                if configuration.ConfigurationName == "Release":
                    # Change the active configuration to Release
                    solution.SolutionBuild.ActiveConfiguration = configuration

                    print("Changed solution configuration to Release mode.")

# Example usage:
vs_automation = VisualStudioAutomation()
vs_automation.change_to_release_mode(r"c:\Users\jeyasri\Downloads\Psemi_packaging_automation\Psemi_2024-0.55.0_D1\muratastudio\Solutions\muRata.Applications\muRata.Applications.sln")



# Example usage:
# solution_file_path =r"c:\Users\jeyasri\Downloads\Psemi_packaging_automation\Psemi_2024-0.55.0_D1\muratastudio\Solutions\muRata.Applications\muRata.Applications.sln"





import win32com.client
import time

def delete_shortcut_from_setup_project(solution_path, shortcut_name):
    try:
        # Create instance of Visual Studio 2019
        dte = win32com.client.Dispatch("VisualStudio.DTE.16.0")
        print("Visual Studio instance created successfully.")

        # Open the solution
        dte.Solution.Open(solution_path)
        print(f"Solution '{solution_path}' opened successfully.")

        # Wait for the solution to load
        time.sleep(10)

        # Access the solution object
        solution = dte.Solution
        if not solution:
            print("Failed to access the Solution object.")
            return

        # Check if the solution is open and contains projects
        if not solution.Projects:
            print("The solution contains no projects or failed to retrieve project list.")
            return

        # Find the setup project
        setup_project = None
        for project in solution.Projects:
            if project.Name == "muRataStudioSetup":
                setup_project = project
                break

        if not setup_project:
            print("The solution does not contain a setup project named 'muRataStudioSetup'.")
            return

        print(f"Setup project '{setup_project.Name}' found.")

        # Check if the ProjectItems property is available
        project_items = setup_project.ProjectItems
        if not project_items:
            print("The 'Application Folder' is not found in the setup project or the ProjectItems property is not available.")
            return

        # Find the Application Folder item
        application_folder = None
        for item in project_items:
            if item.Name == "Application Folder":
                application_folder = item
                break

        if not application_folder:
            print("The 'Application Folder' is not found in the setup project.")
            return

        # Access the project items directly from the setup project
        if not application_folder.ProjectItems:
            print("The 'Application Folder' does not contain any project items.")
            return

        # Print sub-items of the Application Folder
        print("Sub-items of the 'Application Folder':")
        for sub_item in application_folder.ProjectItems:
            print(sub_item.Name)
            if sub_item.ProjectItems:
                for sub_sub_item in sub_item.ProjectItems:
                    if sub_sub_item.Name == shortcut_name:
                        sub_sub_item.Delete()
                        print(f"Shortcut '{shortcut_name}' deleted successfully.")
                        return

        print(f"Shortcut '{shortcut_name}' not found in the 'Application Folder' or its subfolders.")
        
    except win32com.client.pywintypes.com_error as com_err:
        print("COM error occurred:", com_err)
    except Exception as e:
        print("An error occurred:", e)

# Example usage
solution_path = r"c:\Users\jeyasri\Downloads\Psemi_packaging_automation\Psemi_2024-0.55.0_D1\muratastudio\Solutions\muRata.Applications\muRata.Applications.sln"
shortcut_name = "murata-web.url"
delete_shortcut_from_setup_project(solution_path, shortcut_name)