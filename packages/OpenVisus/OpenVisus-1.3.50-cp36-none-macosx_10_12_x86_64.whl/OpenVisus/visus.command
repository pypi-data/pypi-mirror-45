#!/bin/bash
this_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
export PYTHON_EXECUTABLE=/usr/local/opt/python36/bin/python3.6
export PYTHON_PATH=${this_dir}:/Users/travis/build/sci-visus/OpenVisus/build/RelWithDebInfo/site-packages/OpenVisus:/usr/local/Cellar/python36/3.6.8_2/Frameworks/Python.framework/Versions/3.6/lib/python36.zip:/usr/local/Cellar/python36/3.6.8_2/Frameworks/Python.framework/Versions/3.6/lib/python3.6:/usr/local/Cellar/python36/3.6.8_2/Frameworks/Python.framework/Versions/3.6/lib/python3.6/lib-dynload:/usr/local/lib/python3.6/site-packages
export DYLD_LIBRARY_PATH=/usr/local/Cellar/python36/3.6.8_2/Frameworks/Python.framework/Versions/3.6/lib
${this_dir}/bin/visus.app/Contents/MacOS/visus $@
