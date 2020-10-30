"""Modifies sys.path according to the OS of the environment in which Pytest
is attempting to run the tests."""

import os, sys

if os.name == "nt": # If windows use backslash
    for subdirectory in os.scandir():
        sys.path.append(os.path.abspath(subdirectory.name + "\\"))
    else: # TravisCI default environment os.name = str "posix"
        for subdirectory in os.scandir():
            sys.path.append(os.path.abspath(subdirectory.name + "/"))

print("Pytest discovery helper ok")
