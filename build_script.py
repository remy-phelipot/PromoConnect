import sys
from cx_Freeze import setup, Executable

build_exe_options = {}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "PromoHack",
        version = "0.1",
        description = "Connect to the Promolo network",
        options = {"build_exe": build_exe_options},
        executables = [Executable("promoHack.py",base=base)])
