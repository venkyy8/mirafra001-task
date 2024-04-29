import os
import shutil
import subprocess

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
    move_folders(r"c:\Users\jeyasri\Downloads\Psemi_packaging_automation\Psemi_2024-0.55.0_D1\muratastudio\Apps\muRata\bin\Debug\Devices", r"c:\Users\jeyasri\Downloads\Psemi_packaging_automation\Psemi_2024-0.55.0_D1\muratastudio\Apps\muRata\bin\Release\Devices")
    move_folders(r"c:\Users\jeyasri\Downloads\Psemi_packaging_automation\Psemi_2024-0.55.0_D1\muratastudio\Apps\muRata\bin\Debug\Plugins", r"c:\Users\jeyasri\Downloads\Psemi_packaging_automation\Psemi_2024-0.55.0_D1\muratastudio\Apps\muRata\bin\Release\Plugins")

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

if __name__ == "__main__":
    vdproj_path = r"c:\Users\jeyasri\Downloads\Psemi_packaging_automation\Psemi_2024-0.55.0_D1\muratastudio\Solutions\muRata.Applications\muRataStudioSetup\muRataStudioSetup.vdproj"
    build_vdproj(vdproj_path)
