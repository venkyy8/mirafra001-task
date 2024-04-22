from pywinauto.application import Application
import pyautogui
from pywinauto import  Desktop
import time
import os

def get_last_folder_name(path):
    # Split the path by the directory separator
    folders = path.split(os.path.sep)
    # Get the last folder name
    last_folder = folders[-1]
    return last_folder

def start_file_explorer():
        explorer=Application(backend="uia").start("explorer.exe")
    
def open_folder_in_file_explorer(folderPath, currentWindowTitle):
        fileExplorer = Desktop(backend="uia").window(title=currentWindowTitle)
        fileExplorer.set_focus()
        fileExplorer.wait('ready', timeout=10)

        addressBar=fileExplorer.child_window(title="Address: Quick access",  control_type="ToolBar")
        addressBar.click_input()

        pyautogui.write(folderPath)
        pyautogui.press('enter')
        last_folder_name = get_last_folder_name(folderPath)
        time.sleep(10)
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('ctrl', 'c')
        currentWindowTitle= last_folder_name
        return currentWindowTitle

def close_file_explorer(currentWindowTitle):
        fileExplorer = Desktop(backend="uia").window(title=currentWindowTitle)
        fileExplorer.CloseButton.click_input()