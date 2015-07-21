from distutils.core import setup
import py2exe
import sys

#include = ["encodings", "encodings.*"]
sys.argv.append("py2exe")

option = {"py2exe": {"bundle_files": 1}}
setup(options = option, 
        zipfile = None,
        windows = [{"script": "pm25_tool.py"}]
        )
		
