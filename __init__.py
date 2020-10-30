import os, sys

print(f"os.getcwd() is {os.getcwd()}")
print(f"os.pardir = {os.pardir}")

if os.name == "nt": # If windows use backslash
    sys.path.append(os.path.abspath("..") + "\\tic_tac_toe")
    for subdirectory in os.scandir(".."):
        print(f"subdirectory.name is {subdirectory.name}")
        print(f"os.path.abspath(subdirectory.name) = {os.path.abspath(subdirectory.name)}")
        sys.path.append(os.path.abspath(subdirectory.name + "\\"))
        print(f"appended to path: {subdirectory.name}")
else: # TravisCI default environment os.name = str "posix"
    for subdirectory in os.scandir():
        sys.path.append(os.path.abspath(subdirectory.name + "/"))
print(f"parent __init__ updated sys.path to:")
for entry in sys.path:
    print(f"\t{entry}")

print("parent __init__ ok")
