Steps to Automate Psemi Packaging:
1. Change from debug to release mode
2. Copy files from ..\Apps\muRata\bin\Debug\Devices  to  ..\Apps\muRata\bin\Release\Devices
3. Copy files from ..\Apps\muRata\bin\Debug\Plugins  to  ..\Apps\muRata\bin\Release\Plugins
4. Build solution in Release mode
If Build is Succeeded,
5. Delete all files from devices folder (File System on Targer Machine-> Application Folder->Devices)
6. Copy files from ..\Apps\muRata\bin\Release\Devices to File System on Targer Machine-> Application Folder->Devices
7.  Delete all files from plugins folder (File System on Targer Machine-> Application Folder->Plugins)
8.  Copy files from ..\Apps\muRata\bin\Release\Plugins to File System on Targer Machine-> Application Folder->Plugins
9. Delete Primary Output from Murata (File System on Targer Machine-> Application Folder)
10. Delete muRata Studio shortcut from Murata (File System on Targer Machine-> Application Folder)
11. Delete muRata Studio shortcut from Murata (File System on Targer Machine-> User's Desktop)
12. Delete muRata Studio shortcut from Murata (File System on Targer Machine->User's Program Menu->muRata corporation)
13. Create primary output from muRata (By rightclick application folder it done)...Here
    addProjectOutputGroup = muRata,
    outputGroups= Primary output, 
    configurations=(Active),
14. Create muRata shortcut (from-primary output from muRata) 3 times. Here
        name=muRata Studio
        icon=muRata.ico (which was under application folder)    
 keep one muRata Studio shortcut file in Application folder
15. Move muRata Studio shortcut file from Application folder to User's Desktop
16. Move muRata Studio shortcut file from Application folder to User's Programs Menu->MuRataCorporation-> muRataStudio
if want to  change main project version, 
    17. Compare version of main project assembly info file and muratastudio project properties and check the upgrade code
    18. Change version of muratastudio project properties according to the main project version type
    19. Change version of main project assembly info file according to the main project version type
    20. Change version of 14 assembly info files under Plugins folder according to the  main project version type
if want to change any sub-project version,
according to the input 
    21. Change version in AdapterAccess of HardwareAccessFramework according to the version type
    22. Change version in DeviceAccess of HardwareAccessFramework according to the version type
    23. Change version in HardwareInterfaces of HardwareAccessFramework according to the version type
    24. Change version in PluginFramework of PluginInterface according to the version type

25. Build solution
26. Build Muratastudio setup
27. Install Muratastudio  (If version is changed means, it automatically uninstall the previous one and install new muratastudio...if we done everything without changing the version means, we want to first uninstall and then want to install it)