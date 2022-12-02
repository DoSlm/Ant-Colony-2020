from cx_Freeze import setup, Executable
base = None
executables = [Executable("interface.py", base=base)]
packages = ["idna", "pygame", "math", "random"]
options = {
    'build_exe': {    
        'packages':packages,
    },
}
setup(
    name = "Ant_Colony_Optimisation",
    options = options,
    version = "1.0",
    description = '',
    executables = executables
)