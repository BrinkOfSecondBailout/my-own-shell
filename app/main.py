import sys
import os
import subprocess

def find_file(paths, command):
    for path in paths:
        current_path = os.path.join(path, command)
        if os.path.exists(current_path):
            return current_path
    return None

def process_cd_path(path):
    if path == "~":
        return os.path.expanduser("~")
    
    if os.path.isabs(path):
        return path
    
    return os.path.normpath(os.path.join(os.getcwd(), path))

def main():
    builtins_cmd = ["echo", "exit", "type", "pwd", "cd"]
    PATH = os.environ.get("PATH")
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        command_line = input().strip()

        if not command_line:
            continue

        command_parts = command_line.split()
        command = command_parts[0]
        args = command_parts[1:]

        if command == "exit" and "0" in args:
            break
        elif command == "echo":
            print(" ".join(args))
        elif command == "type":
            cmd = args[0] if args else ""
            cmd_path = None
            paths = PATH.split(":")
            for path in paths:
                if os.path.isfile(f"{path}/{cmd}"):
                    cmd_path = f"{path}/{cmd}"
            if cmd in builtins_cmd:
                print(f"{cmd} is a shell builtin")
            elif cmd_path:
                print(f"{cmd} is {cmd_path}")
            else:
                print(f"{cmd}: not found")
        elif command == "pwd":
            print(f"{os.getcwd()}")
        elif command == "cd":
            new_path = args[0] if args else os.path.expanduser("~")
            target_path = process_cd_path(new_path)
            if os.path.isdir(target_path):
                try:
                    os.chdir(target_path)
                except OSError as e:
                    print(f"cd: {new_path}: {str(e)}")
            else:
                print(f"cd: {new_path}: No such file or directory")
        else:
            paths = PATH.split(":")
            executable = find_file(paths, command)
            if executable:
                try:
                    result = subprocess.run([executable] + args, capture_output=True, text=True)
                    sys.stdout.write(result.stdout)
                    sys.stderr.write(result.stderr)
                except Exception as e:
                    print(f"Error executing command: {e}")
            else:
                print(f"{command}: command not found")
            continue




if __name__ == "__main__":
    main()
