#!/bin/bash
this_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
export PYTHON_EXECUTABLE=/usr/local/opt/python37/bin/python3.7
export PYTHON_PATH=${this_dir}:/Users/travis/build/sci-visus/OpenVisus/build/RelWithDebInfo/site-packages/OpenVisus:/usr/local/Cellar/python37/3.7.3/Frameworks/Python.framework/Versions/3.7/lib/python37.zip:/usr/local/Cellar/python37/3.7.3/Frameworks/Python.framework/Versions/3.7/lib/python3.7:/usr/local/Cellar/python37/3.7.3/Frameworks/Python.framework/Versions/3.7/lib/python3.7/lib-dynload:/usr/local/lib/python3.7/site-packages:/usr/local/lib/python3.7/site-packages/geos:/usr/local/Cellar/numpy/1.16.2/libexec/nose/lib/python3.7/site-packages:/usr/local/Cellar/protobuf/3.7.1/libexec/lib/python3.7/site-packages
export DYLD_LIBRARY_PATH=/usr/local/Cellar/python37/3.7.3/Frameworks/Python.framework/Versions/3.7/lib
${this_dir}/bin/visus.app/Contents/MacOS/visus $@
