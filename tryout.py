import sys
import os
import win32com.client

def get_dte():
    try:
        # Get the DTE object
        dte = win32com.client.GetActiveObject("VisualStudio.DTE.16.0")
        return dte
    except Exception as e:
        print("Error getting DTE object:", e)
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
                    print("Configuration mode set to Release.")
                    return True

            print("Release configuration not found.")
            return False
        else:
            print("No solution loaded in Visual Studio.")
            return False
    except Exception as e:
        print("Error setting configuration to Release:", e)
        return False

def main():
    # Attempt to get the DTE object
    dte = get_dte()
    if not dte:
        print("Failed to get DTE object. Make sure Visual Studio is running.")
        return

    # Set configuration to Release
    if not set_configuration_to_release(dte):
        print("Failed to set configuration to Release.")
        return

if __name__ == "__main__":
    main()
