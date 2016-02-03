from distutils.core import setup
import py2exe
import sys

#include = ["encodings", "encodings.*"]
sys.argv.append("py2exe")

option = {"py2exe": {"bundle_files": 1}}
setup(options = option, 
        zipfile = None,
        windows = [{"script": "gas_tool.py",
            "icon_resources": [(1, "resource\hk.ico")]}],
        data_files = [("resource", ["resource\hk.ico"])]
        )
		
