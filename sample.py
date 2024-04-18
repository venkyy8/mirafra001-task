from pywinauto.application import Application
import os
import shutil
from pywinauto import  Desktop
import time
import pyautogui
import pyperclip
import re
import re
### ###

def build_solution(muRataAppInVSCode):
    try:
            
        muRataAppInVSCode.child_window(title="Build", control_type="MenuItem").click_input()
        time.sleep(10)
        muRataAppInVSCode.child_window(title="Build Solution", control_type="MenuItem").click_input()
        customControl=muRataAppInVSCode.child_window(auto_id="WpfTextViewHost", control_type="Custom")
        buildedResultArea=customControl.child_window(control_type="Edit", found_index=0)

        ### Capture the output
        buildedResult=buildedResultArea.window_text()
        print("Output of Build:", buildedResult)
        time.sleep(10)
        if "0 failed" in buildedResult:
            print("Build is succeeded")
            muRataAppInVSCode.Output.CloseButton.click_input()
        else:
            raise Exception("Build failed. Consider it as an error.")
    except Exception as e:
        print(f"Error in build solution: {e}")

def build_process_in_release_mode(muRataAppInVSCode):

    try:
         ### Change from Debug to Release Mode ###
        muRataAppInVSCode.solutionConfigurations.select("Release")

        ######################################Laterrrrr ##################
        ### Open Folder in File Explorer ###
        solutionExplorerWindow=muRataAppInVSCode.child_window(title="Solution Explorer", auto_id="SolutionExplorer", control_type="Tree")
        solutionMuRataAppWindow=solutionExplorerWindow.child_window(title="Solution 'muRata.Applications' ‎(20 of 20 projects)", control_type="TreeItem")
        solutionMuRataAppWindow.right_click_input()

        ### Copy Devices and Plugins folders from Debug to Release ###
        sourceFolder1=r"C:\Venkatesh\Data-FEB-2024\Mirafra-Learning\Task\script\Psemi_2024-0.55.0_D1\Psemi_2024-0.55.0_D1\muratastudio\Apps\muRata\bin\Debug\Devices"
        sourceFolder2=r"C:\Venkatesh\Data-FEB-2024\Mirafra-Learning\Task\script\Psemi_2024-0.55.0_D1\Psemi_2024-0.55.0_D1\muratastudio\Apps\muRata\bin\Debug\Plugins"

        desinationFolder=r"C:\Venkatesh\Data-FEB-2024\Mirafra-Learning\Task\script\Psemi_2024-0.55.0_D1\Psemi_2024-0.55.0_D1\muratastudio\Apps\muRata\bin\Release"
        shutil.copytree(sourceFolder1,os.path.join(desinationFolder, os.path.basename(sourceFolder1)))
        shutil.copytree(sourceFolder2,os.path.join(desinationFolder,os.path.basename(sourceFolder2)))

        ### Build Solution ###
        build_solution(muRataAppInVSCode)
   
        
    except Exception as e:
        print(f"Error while building solution in release mode: {e}")

def update_folders_of_application_folder(muRataAppInVSCode, solutionMuRataAppWindow):
    try:
        ### Click File System Editor ###
        solutionMuRataAppWindow.child_window(title="muRataStudioSetup", control_type="TreeItem").click_input()
        time.sleep(5)
        muRataAppInVSCode.child_window(title="&File System", control_type="Button").click_input()

	    ###  Delete all the files from Devices of Application Folder and copy from Devices of Release Folder ###
        fileSystemWindow=muRataAppInVSCode.child_window(title="File System (muRataStudioSetup)", auto_id="D:0:0:|File System (muRataStudioSetup)||{00000000-0000-0000-0000-000000000000}|", control_type="Pane")
        applicationFolder=fileSystemWindow.child_window(title="Application Folder", control_type="TreeItem")
        applicationFolder.double_click_input()
        applicationFolder.child_window(title="Devices", control_type="TreeItem").double_click_input()
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('delete')
        deleteProcess=muRataAppInVSCode.child_window(title="Microsoft Visual Studio", control_type="Window")
        deleteProcess.YesButton.click_input()

        devicesFolderOfRelease=r"C:\Venkatesh\Data-FEB-2024\Mirafra-Learning\Task\script\Psemi_2024-0.55.0_D1\Psemi_2024-0.55.0_D1\muratastudio\Apps\muRata\bin\Release\Devices"
        pluginsFolderOfRelease=r"C:\Venkatesh\Data-FEB-2024\Mirafra-Learning\Task\script\Psemi_2024-0.55.0_D1\Psemi_2024-0.55.0_D1\muratastudio\Apps\muRata\bin\Release\Plugins"
        explorer=Application(backend="uia").start("explorer.exe")
        fileExplorer = Desktop(backend="uia").window(title='File Explorer')
        fileExplorer.wait('ready', timeout=10)

        addressBar=fileExplorer.child_window(title="Address: Quick access", auto_id="1001", control_type="ToolBar")
        addressBar.click_input()

        pyautogui.write(devicesFolderOfRelease)
        pyautogui.press('enter')
        time.sleep(10)
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('ctrl', 'c')
    
        
        muRataAppInVSCode.set_focus()
        pyautogui.hotkey('ctrl', 'v')


        ### Delete all the files from Plugins of Application Folder and copy from Plugins of Release Folder ###
        applicationFolder.child_window(title="Plugins", control_type="TreeItem").double_click_input()
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('delete')
        deleteProcess=muRataAppInVSCode.child_window(title="Microsoft Visual Studio", control_type="Window")
        deleteProcess.YesButton.click_input()

        # pyautogui.hotkey('ctrl', 'v')
        pluginsFolderOfRelease=r"C:\Venkatesh\Data-FEB-2024\Mirafra-Learning\Task\script\Psemi_2024-0.55.0_D1\Psemi_2024-0.55.0_D1\muratastudio\Apps\muRata\bin\Release\Plugins"
        time.sleep(1)
        explorer=Application(backend="uia").start("explorer.exe")
        fileExplorer = Desktop(backend="uia").window(title='File Explorer')
        fileExplorer.wait('ready', timeout=10)
        time.sleep(5)
        addressBar=fileExplorer.child_window(title="Address: Quick access", auto_id="1001", control_type="ToolBar")
        addressBar.click_input()

        pyautogui.write(pluginsFolderOfRelease)
        pyautogui.press('enter')
        time.sleep(5)
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('ctrl', 'c')
        muRataAppInVSCode.set_focus()
        pyautogui.hotkey('ctrl', 'v')


    except Exception as e:
        print(f"Error occurred while updating folders of Application Folder: {e}")
 
def delete_primary_output_and_shortcuts(fileSystemWindow,muRataAppInVSCode):
    try:
        ### Delete Primary Output from Murata ###
        fileSystemWindow.child_window(title="Primary output from muRata (Active)", control_type="Edit").click_input()
        pyautogui.press('delete')

        ### Delete muRata Studio shortcut from Application folder ###
        muRataAppInVSCode.child_window(title="muRata Studio", control_type="ListItem").click_input()
        pyautogui.press('delete')

        ###  Delete muRata Studio shortcut from User's Desktop ###
        usersDesktop=fileSystemWindow.child_window(title="User's Desktop", control_type="TreeItem")
        usersDesktop.double_click_input()
        muRataAppInVSCode.child_window(title="muRata Studio", control_type="ListItem").click_input()
        pyautogui.press('delete')

        ### Delete muRata Studio shortcut from User's Program Menu->muRata corporation ->muRata Studio ###
        usersProgramsMenu=fileSystemWindow.child_window(title="User's Programs Menu", control_type="TreeItem")
        usersProgramsMenu.double_click_input()
        usersProgramsMenu.MuRataCorporation.double_click_input()
        usersProgramsMenu.MuRataCorporation.MuRataStudio.double_click_input()
        muRataAppInVSCode.child_window(title="muRata Studio", control_type="ListItem").click_input()
        pyautogui.press('delete')

    except Exception as e:
        print(f"Error deleting primary output and shortcuts: {e}")


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
        # pyautogui.press('down') # Move down to "Primary output"
        pyautogui.press('enter')  # Select "Primary output"
        time.sleep(1)
    
        addProjectOutputGroup=muRataAppInVSCode.child_window(title="Add Project Output Group", control_type="Window")

        project=addProjectOutputGroup.child_window(title="Project:", auto_id="240", control_type="ComboBox")
        dropDownOfProject=project.child_window(title="Open", auto_id="DropDown", control_type="Button")
        dropDownOfProject.click_input()
        project.child_window(title="muRata", control_type="ListItem").click_input()

        
        time.sleep(1)
        addProjectOutputGroup.print_control_identifiers()
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
        
    except Exception as e:
        print(f"Error in creating primary output from muRata: {e}")


def create_muRata_shortcut(applicationFolder, fileSystemWindow):
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

    except Exception as e:
        print(f"Error in creating muRata shortcut: {e}")

def create_primary_output_and_shortcuts(muRataAppInVSCode,applicationFolder,fileSystemWindow ):
    try:
        create_primary_output_from_muRata(muRataAppInVSCode,applicationFolder)
        create_muRata_shortcut(applicationFolder, fileSystemWindow)

        ## Copy file from Application Folder to User's Desktop
        muRataAppInVSCode.child_window(title="muRata Studio", control_type="Edit").click_input()
        muRataAppInVSCode.type_keys("^x")
        usersDesktop=fileSystemWindow.child_window(title="User's Desktop", control_type="TreeItem")
        usersDesktop.double_click_input()
        muRataAppInVSCode.type_keys("^v")

        create_muRata_shortcut(applicationFolder, fileSystemWindow)

        ## Copy file from Application Folder to usersProgramsMenu
        muRataAppInVSCode.child_window(title="muRata Studio", control_type="Edit").click_input()
        muRataAppInVSCode.type_keys("^x")
        usersProgramsMenu=fileSystemWindow.child_window(title="User's Programs Menu", control_type="TreeItem")
        usersProgramsMenu.double_click_input()
        usersProgramsMenu.MuRataCorporation.double_click_input()
        usersProgramsMenu.MuRataCorporation.MuRataStudio.double_click_input()
        muRataAppInVSCode.type_keys("^v")

        create_muRata_shortcut(applicationFolder, fileSystemWindow)

    
        
    except Exception as e:
        print(f"Error creating primary output and shortcuts: {e}")

#def increment_version(version_string):
    """
    Increments the version string.

    Args:
        version_string: The version string to increment.

    Returns:
        The incremented version string.
    """
    major, minor, patch = map(int, version_string.split("."))
    patch += 1


    return f"{major}.{minor}.{patch}"



def get_initial_version_from_file(filepath):
    """
    Reads the initial version from the specified file.

    Args:
        filepath: The path to the file containing the initial version.

    Returns:
        The initial version string.
    """
    try:
        with open(filepath, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if "AssemblyVersion" in line:
                    version_string = re.search(r'\d+\.\d+\.\d+\.\d+', line)
                    if version_string:
                        return version_string.group()
    except Exception as e:
        print(f"Error reading version from file: {e}")
    return None

# Example usage:
assembly_version_file_path = r"C:\Venkatesh\Data-FEB-2024\Mirafra-Learning\Task\script\Psemi_2024-0.55.0_D1\Psemi_2024-0.55.0_D1\muratastudio\Apps\muRata\Properties\AssemblyInfo.cs"
assembly_version = get_initial_version_from_file(assembly_version_file_path)

if assembly_version:
    print("Initial version:", assembly_version)
else:
    print("Failed to retrieve initial version.")

def update_version_in_file(filepath, version_string):
    """
    Updates the version number in the specified file.

    Args:
        filepath: The path to the file.
        version_string: The new version number to be inserted.
    """
    try:
        with open(filepath, 'r') as file:
            lines = file.readlines()
        with open(filepath, 'w') as file:
            for line in lines:
                if "AssemblyVersion" in line or "AssemblyFileVersion" in line:
                    line = re.sub(r'\d+\.\d+\.\d+\.\d+', version_string, line)
                file.write(line)
        print(f"Version number updated to {version_string} in {filepath}")
    except Exception as e:
        print(f"Error updating version number in file: {e}")


def change_version_in_assembly_info(solutionExplorerWindow, muRataAppInVSCode):
    try:
        gui_directory = solutionExplorerWindow.child_window(title="GUI", control_type="TreeItem")
        gui_directory.double_click_input()  # Double click to expand

        # Find and select the tree item for "muRata" directory under "GUI" directory
        muRata_directory = gui_directory.child_window(title="muRata", control_type="TreeItem")
        muRata_directory.double_click_input()  # Double click to expand

        # Find and select the tree item for "Properties" directory under "muRata" directory
        properties_directory = muRata_directory.child_window(title="Properties", control_type="TreeItem")

        # Right-click on "Properties" directory
        properties_directory.right_click_input()

        # Wait for the context menu to appear
        time.sleep(1)

        # Simulate keyboard inputs to move down to the desired option (assuming it's the 4th option)
        for _ in range(3):  # Move down 3 times (zero-indexed)
            muRataAppInVSCode.type_keys('{DOWN}')

        # Select the "New Solution Explorer View" option
        muRataAppInVSCode.type_keys('{ENTER}')

        # Activate the search box in the Solution Explorer
        muRataAppInVSCode.type_keys("^;")  # Press Ctrl+;

        # Type the file name to search for AssemblyInfo.cs
        muRataAppInVSCode.type_keys("AssemblyInfo.cs")

        # Wait for a short moment to ensure the search results appear
        time.sleep(1)

        # Press Enter to open the file
        muRataAppInVSCode.type_keys("{ENTER}")
        ##
        # Double-click on the searched AssemblyInfo.cs file to open it
        assembly_info_file = muRataAppInVSCode.child_window(title="AssemblyInfo.cs", control_type="TreeItem")
        assembly_info_file.click_input(double=True)

        # Wait for a short moment to ensure the file opens
        time.sleep(1)

        # Path to the file containing the initial version
        file_path = r"C:\Venkatesh\Data-FEB-2024\Mirafra-Learning\Task\script\Psemi_2024-0.55.0_D1\Psemi_2024-0.55.0_D1\muratastudio\Apps\muRata\Properties\AssemblyInfo.cs"

        # Get the initial version from the file
        initial_version = get_initial_version_from_file(file_path)

        if initial_version:
            print(f"Initial version: {initial_version}")

            # Increment the version
            new_version = increment_versionInFile(initial_version)

            # Update the version in the file
            update_version_in_file(file_path, new_version)
    except Exception as e:
        print(f"Error changing version in AssemblyInfo.cs file: {e}")

def get_initial_version_from_muRata_studio_properties(muRataAppInVSCode, solutionMuRataAppWindow ):

    try:
               # Open the Properties window using the F4 key shortcut
        muRataAppInVSCode.type_keys("{F4}")
        time.sleep(2)
        solutionMuRataAppWindow.child_window(title="muRataStudioSetup", control_type="TreeItem").click_input()
        time.sleep(2)

        propertiesWindow=muRataAppInVSCode.child_window(title="Properties", control_type="Window")
        # propertiesWindow=muRataAppInVSCode.child_window(title="Properties Window", control_type="Table")
        propertiesWindow.child_window(title="Version", control_type="TreeItem").click_input()
        propertiesWindow.child_window(title="Version",  control_type="Edit").double_click_input()

        # propertiesWindow.print_control_identifiers()

        # Copy the selected text to the clipboard
        pyautogui.hotkey('ctrl', 'c')

        # Wait briefly for the clipboard to update
        time.sleep(0.5)

        # Retrieve the selected text from the clipboard
        initialVersion = pyperclip.paste()
        print("initialVersion is", initialVersion)
        propertiesWindow.CloseButton.click_input()
        return initialVersion
    
    except Exception as e:
        print(f"Error occurred while getting initial version from muRata Studio properties: {e}")

def compare_versions(assembly_version, initial_version):
    """
    Compare the assembly_version with the initial_version,
    ignoring the last segment of the assembly_version.

    Args:
        assembly_version: The version obtained from AssemblyInfo.cs.
        initial_version: The initial version.

    Returns:
        True if the versions match, False otherwise.
    """
    # Split the versions into segments
    assembly_segments = assembly_version.split('.')
    initial_segments = initial_version.split('.')

    # Ignore the last segment of the assembly_version
    assembly_segments = assembly_segments[:-1]

    # Compare the versions
    if assembly_segments == initial_segments:
        return True
    else:
        return False

# Example usage:
assembly_version = "0.55.1.0"
initial_version = "0.55.1"

# Compare the versions
if compare_versions(assembly_version, initial_version):
    print("Versions match.")
else:
    print("Versions do not match.")



def change_version_in_muRata_studio_properties(muRataAppInVSCode, solutionMuRataAppWindow ):
    try:
        initialVersion=get_initial_version_from_muRata_studio_properties(muRataAppInVSCode, solutionMuRataAppWindow )

        muRataAppInVSCode.type_keys("{F4}")

        solutionMuRataAppWindow.child_window(title="muRataStudioSetup", control_type="TreeItem").click_input()
        time.sleep(10)

        propertiesWindow=muRataAppInVSCode.child_window(title="Properties", control_type="Window")
        # propertiesWindow=muRataAppInVSCode.child_window(title="Properties Window", control_type="Table")
        propertiesWindow.child_window(title="Version", control_type="TreeItem").click_input()
        propertiesWindow.child_window(title="Version",  control_type="Edit").double_click_input()

        newVersion=increment_version(initialVersion)
        version=propertiesWindow.child_window(title="Version",  control_type="Edit")
        version.type_keys(newVersion)
        print("new version is", newVersion)
        time.sleep(1)

        propertiesWindow.CloseButton.click_input()
        time.sleep(0.5)
        muRataAppInVSCode.MicrosoftVisualStudio.YesButton.click_input()
        time.sleep(1)
        propertiesWindow.CloseButton.click_input()

    except Exception as e:
        print(f"Error changing version in muRata Studio properties: {e}")



def change_version(muRataAppInVSCode, solutionMuRataAppWindow, solutionExplorerWindow):
    try:
        filepath = r"C:\Venkatesh\Data-FEB-2024\Mirafra-Learning\Task\script\Psemi_2024-0.55.0_D1\Psemi_2024-0.55.0_D1\muratastudio\Apps\muRata\Properties\AssemblyInfo.cs"
        initial_version = get_initial_version_from_muRata_studio_properties(muRataAppInVSCode, solutionMuRataAppWindow)
        assembly_version= get_initial_version_from_file(filepath)
        
        if compare_versions(assembly_version, initial_version):
            change_version_in_muRata_studio_properties(muRataAppInVSCode, solutionMuRataAppWindow)
            change_version_in_assembly_info(solutionExplorerWindow, muRataAppInVSCode)
        else:
            raise Exception("Versions do not match.")

    except Exception as e:
        print(f"Error in changing version: {e}")





def install_muRata_studio_setup(solutionMuRataAppWindow):
    try:
        solutionMuRataAppWindow.child_window(title="muRataStudioSetup", control_type="TreeItem").right_click_input()
        for _ in range(5):
            pyautogui.press("down")
        pyautogui.press("enter")
        fileExplorer=Application(backend="uia").connect(title="Release")
        releaseFolderInFileExplorer=fileExplorer.Release
        releaseFolderInFileExplorer.set_focus()
        releaseFolderInFileExplorer.child_window(title="muRataStudioSetup",  control_type="ListItem").double_click_input()

        time.sleep(1)
        muRataStudioWindow=Application(backend="uia").connect(title="muRata Studio")
        muRataStudioInstallationWindow=muRataStudioWindow.MuRataStudio
        muRataStudioInstallationWindow.set_focus()
        muRataStudioInstallationWindow.child_window(title="Next >", control_type="Button").click_input()
        time.sleep(1)
        muRataStudioInstallationWindow.child_window(title="I Agree", control_type="RadioButton").click_input()
        time.sleep(1)
        muRataStudioInstallationWindow.child_window(title="Next >",  control_type="Button").click_input()
        time.sleep(1)
        muRataStudioInstallationWindow.child_window(title="Next >", control_type="Button").click_input()
        time.sleep(1)
        muRataStudioInstallationWindow.child_window(title="Next >", control_type="Button").click_input()
        time.sleep(10)
        message='muRata Studio has been successfully installed.\r\n\r\nClick "Close" to exit.'
        successResponse=muRataStudioInstallationWindow.child_window(title=message,  control_type="Text")
        if successResponse.exists():

            muRataStudioInstallationWindow.print_control_identifiers()
            muRataStudioInstallationWindow.CloseButton2.click_input()
            response=message.split('.', 1)[0].strip() + "." 
            print(response)
        else:
             raise Exception("Erro in the Installation of muRata Studio")
    except Exception as e:
        print(f"Error installing muRata Studio setup: {e}")

def muRata_studio_installer_packaging(muRataAppInVSCode, solutionMuRataAppWindow):
    try:
        build_solution(muRataAppInVSCode)
        install_muRata_studio_setup(solutionMuRataAppWindow)

    except Exception as e:
        print(f"Error in muRataStudio installer packaging: {e}")

def main(vsCodePath, filePath):

    try:
        ### Open and Connect with Visual Studio Code ###
        app=Application(backend="uia").start(vsCodePath + ' ' + filePath )

        ### Capturing Window
        muRataAppInVSCode=app.window(title="muRata.Applications - Microsoft Visual Studio")
        time.sleep(25)

        solutionExplorerWindow=muRataAppInVSCode.child_window(title="Solution Explorer", auto_id="SolutionExplorer", control_type="Tree")
        solutionMuRataAppWindow=solutionExplorerWindow.child_window(title_re=".*Solution 'muRata.Applications'*.", control_type="TreeItem")
        
        get_initial_version_from_muRata_studio_properties(muRataAppInVSCode, solutionMuRataAppWindow)
        filepath = r"C:\Venkatesh\Data-FEB-2024\Mirafra-Learning\Task\script\Psemi_2024-0.55.0_D1\Psemi_2024-0.55.0_D1\muratastudio\Apps\muRata\Properties\AssemblyInfo.cs"
        get_initial_version_from_file(filepath)
        
        # build_process_in_release_mode(muRataAppInVSCode)
        # update_folders_of_application_folder(muRataAppInVSCode, solutionMuRataAppWindow)

        ### Capturing Window
        fileSystemWindow=muRataAppInVSCode.child_window(title="File System (muRataStudioSetup)", auto_id="D:0:0:|File System (muRataStudioSetup)||{00000000-0000-0000-0000-000000000000}|", control_type="Pane")
        compare_versions(assembly_version, initial_version)
        # delete_primary_output_and_shortcuts(fileSystemWindow,muRataAppInVSCode)
        change_version(muRataAppInVSCode, solutionMuRataAppWindow, solutionExplorerWindow)
        ### Capturing Window
        applicationFolder=fileSystemWindow.child_window(title="Application Folder", control_type="TreeItem")

        # create_primary_output_and_shortcuts(muRataAppInVSCode,applicationFolder,fileSystemWindow )

        # change_version(muRataAppInVSCode, solutionMuRataAppWindow, solutionExplorerWindow)

        # muRata_studio_installer_packaging(muRataAppInVSCode, solutionMuRataAppWindow)
    
    except Exception as e:
          print(f"An error occurred: {e}")


if __name__=="__main__":

    ### Delcare VScode path and File Path ###
    vsCodePath=r"C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\Common7\IDE\devenv.exe"
    filePath=r"C:\Venkatesh\Data-FEB-2024\Mirafra-Learning\Task\script\Psemi_2024-0.55.0_D1\Psemi_2024-0.55.0_D1\muratastudio\Solutions\muRata.Applications\muRata.Applications.sln"
    main (vsCodePath, filePath)
