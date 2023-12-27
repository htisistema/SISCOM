import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["os"], "includes": ["PyQt6"]}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(name="SISCOM",
      version="v231227",
      description="Automacao Comercial",
      options={"build_exe": build_exe_options},
      executaples=[Executable("siscom.py", base=base)]
      )