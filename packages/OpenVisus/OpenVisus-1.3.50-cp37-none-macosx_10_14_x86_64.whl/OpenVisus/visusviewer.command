#!/bin/bash
this_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
export PYTHON_EXECUTABLE=/usr/local/opt/python37/bin/python3.7
export PYTHON_PATH=${this_dir}:/Users/travis/build/sci-visus/OpenVisus/build/RelWithDebInfo/site-packages/OpenVisus:/usr/local/Cellar/python37/3.7.3/Frameworks/Python.framework/Versions/3.7/lib/python37.zip:/usr/local/Cellar/python37/3.7.3/Frameworks/Python.framework/Versions/3.7/lib/python3.7:/usr/local/Cellar/python37/3.7.3/Frameworks/Python.framework/Versions/3.7/lib/python3.7/lib-dynload:/usr/local/lib/python3.7/site-packages:/usr/local/lib/python3.7/site-packages/geos:/usr/local/Cellar/numpy/1.16.2/libexec/nose/lib/python3.7/site-packages:/usr/local/Cellar/protobuf/3.7.1/libexec/lib/python3.7/site-packages
export DYLD_LIBRARY_PATH=/usr/local/Cellar/python37/3.7.3/Frameworks/Python.framework/Versions/3.7/lib
if [ -d ${this_dir}/bin/Qt ]; then 
   echo "Using internal Qt5" 
   export Qt5_DIR=${this_dir}/bin/Qt
else
   echo "Using external PyQt5" 
   export Qt5_DIR=$(${PYTHON_EXECUTABLE} -c "import os,PyQt5; print(os.path.dirname(PyQt5.__file__))")/Qt 
fi
export QT_PLUGIN_PATH=${Qt5_DIR}/plugins
cd ${this_dir}
${this_dir}/bin/visusviewer.app/Contents/MacOS/visusviewer $@
