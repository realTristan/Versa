import sys
import os
from cx_Freeze import setup, Executable
import shiboken6
import shiboken2

# ADD FILES
files = ['icon.ico','data/', 'images/','themes/']

# TARGET
target = Executable(
    script="main.py",
    base="Win32GUI",
    icon="icon.ico"
)


# SETUP CX FREEZE
setup(
    name = "Versa Anti Cheat",
    version = "1.0",
    description = "Advanced Gaming Anti Cheat",
    author = "Versa Programs",
    options = {'build_exe': {'include_files': files}},
    executables = [target]
    
)
