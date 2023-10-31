import os
import subprocess
import tkinter.colorchooser as colorchooser
import tkinter as tk
import sys

print("Welcome to the SupCommandPrompt!")
print("Copyright (c) SupCommandPrompt, All rights reserved.")

operators = ["/", "*", "+", "-"]
numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
integer1 = True
integer2 = True
operator = False
operated = False


def write(text):
    print(text)


def mkdir(args):
    if len(args) < 1:
        write(f"The command 'mkdir' requires at least 1 argument. Usage: mkdir <directory_name>")
    else:
        directory_name = " ".join(args)
        try:
            os.mkdir(directory_name)
            write(f"Directory '{directory_name}' created successfully.")
        except FileExistsError:
            write(f"Directory '{directory_name}' already exists.")
        except Exception as e:
            write(f"An error occurred: {str(e)}")


def mkfile(args):
    if len(args) < 1:
        write(f"The command 'mkfile' requires at least 1 argument. Usage: mkfile <file_name>")
    else:
        file_name = " ".join(args)
        try:
            with open(file_name, 'w'):
                pass
            write(f"File '{file_name}' created successfully.")
        except FileExistsError:
            write(f"File '{file_name}' already exists.")
        except Exception as e:
            write(f"An error occurred: {str(e)}")


def cd(args):
    if not args:
        os.chdir(os.path.expanduser("~"))
    else:
        new_directory = " ".join(args)
        try:
            os.chdir(new_directory)
        except FileNotFoundError:
            write(f"Directory '{new_directory}' not found.")
        except Exception as e:
            write(f"An error occurred: {str(e)}")


def colorpicker():
    root = tk.Tk()
    color = colorchooser.askcolor()
    write(f"Selected color: {color[1]}")
    root.withdraw()


def start(args):
    if not args:
        write("Usage: start <file_path>")
    else:
        file_path = " ".join(args)
        if os.path.isfile(file_path):
            try:
                subprocess.Popen([file_path], shell=False)
            except Exception as e:
                write(f"An error occurred: {str(e)}")
        else:
            write(f"'{file_path}' not found.")


def execute_command(command):
    global numbers, operators, integer1, integer2, operator, operated
    inputs = command.split()
    current_directory = os.getcwd()
    current_directory_files = os.listdir(current_directory)

    if command in current_directory_files:
        return os.path.abspath(command)

    path_dirs = os.environ["PATH"].split(os.pathsep)
    for path_dir in path_dirs:
        try:
            path_dir_files = os.listdir(path_dir)
            for file in path_dir_files:
                if file.lower() == command.lower():
                    return os.path.abspath(os.path.join(path_dir, file))
        except FileNotFoundError:
            pass

    for extension in [".exe", ".bat"]:
        executable = f"{command}{extension}"
        if executable in current_directory_files:
            return os.path.abspath(executable)
        for path_dir in path_dirs:
            try:
                path_dir_files = os.listdir(path_dir)
                for file in path_dir_files:
                    if file.lower() == executable.lower():
                        return os.path.abspath(os.path.join(path_dir, file))
            except FileNotFoundError:
                pass

    if len(inputs) == 3 and inputs[1] in operators:
        try:
            first = int(inputs[0])
            second = int(inputs[2])
            operation = inputs[1]
            if operation == "+":
                print(first + second)
                operated = True
            elif operation == "-":
                print(first - second)
                operated = True
            elif operation == "*":
                print(first * second)
                operated = True
            elif operation == "/":
                if second != 0:
                    print(first / second)
                    operated = True
                else:
                    print("Undefined.")
                    operated = False
            else:
                operated = False
            return None  # Added to prevent further processing
        except ValueError:
            operated = False

    if len(inputs) == 1 and inputs[0].isnumeric():
        print(inputs[0])
        return None  # Added to prevent further processing

    return None


while True:
    current_directory = os.getcwd()
    command = input(f"{current_directory}> ")
    executable = execute_command(command)

    if executable:
        subprocess.Popen([executable], shell=False)
    elif command.lower() == "exit":
        sys.exit(0)
    elif command.lower().startswith("mkfile"):
        mkfile(command.split()[1:])
    elif command.lower().startswith("mkdir"):
        mkdir(command.split()[1:])
    elif command.lower().startswith("cd"):
        cd(command.split()[1:])
    elif command.lower() == "colorpicker":
        colorpicker()
    elif command.lower().startswith("start"):
        start(command.split()[1:])
    elif operated:
        operated = False
    else:
        print(f'"{command}" is an unknown command, executable, path file, or a math operation.')
