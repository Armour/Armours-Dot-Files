# This file is NOT licensed under the GPLv3, which is the license for the rest
# of YouCompleteMe.
#
# Here's the license text for this file:
#
# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# For more information, please refer to <http://unlicense.org/>

import os
import ycm_core

# These are the compilation flags that will be used in case there's no
# compilation database set (by default, one is not set).
# CHANGE THIS LIST OF FLAGS. YES, THIS IS THE DROID YOU HAVE BEEN LOOKING FOR.
flags = [
  '-Wall'            # The Wmissing-braces is useless in c++11
, '-Wextra'
#, '-Werror'          # Fucking unused parameter argc!!!
, '-Wc++98-compat'   # Well i love c++11!!!
, '-Wno-long-long'
, '-Wno-variadic-macros'
, '-fexceptions'
, '-DNDEBUG'
, '-DUSE_CLANG_COMPLETER'
# THIS IS IMPORTANT! Without a "-std=<something>" flag, clang won't know which
# language to use when compiling headers. So it will guess. Badly. So C++
# headers will be compiled as C headers. You don't want that so ALWAYS specify
# a "-std=<something>".
# For a C project, you would set this to something like 'c99' instead of 'c++11'.
, '-std=c++11'
# ...and the same thing goes for the magic -x option which specifies the
# language that the files to be compiled are written in. This is mostly
# relevant for c++ headers.
# For a C project, you would set this to 'c' instead of 'c++'.
, '-x'
, 'c++'
, '-isystem'
, '../BoostParts'
, '-isystem'
, '/System/Library/Frameworks/Python.framework/Headers' # This path will only work on OS X, but extra paths that don't exist are not harmful
, '-isystem'
, '../llvm/include'
, '-isystem'
, '../llvm/tools/clang/include'
, '-I'
, '.'
, '-I'
, './ClangCompleter'
, '-isystem'
, './tests/gmock/gtest'
, '-isystem'
, './tests/gmock/gtest/include'
, '-isystem'
, './tests/gmock'
, '-isystem'
, './tests/gmock/include'
, '-I'
, '/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib/c++/v1'
, '-I'
, '/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/include/c++/v1'
, '-I'
, '/usr/include'
, '-I'
, '/usr/local/include'
]

# Set this to the absolute path to the folder (NOT the file!) containing the
# compile_commands.json file to use that instead of 'flags'. See here for
# more details: http://clang.llvm.org/docs/JSONCompilationDatabase.html
#
# Most projects will NOT need to set this to anything; you can just change the
# 'flags' list of compilation flags. Notice that YCM itself uses that approach.
compilation_database_folder = ''

if compilation_database_folder:
  database = ycm_core.CompilationDatabase( compilation_database_folder )
else:
  database = None


def DirectoryOfThisScript():
  return os.path.dirname( os.path.abspath( __file__ ) )


def MakeRelativePathsInFlagsAbsolute( flags, working_directory ):
  if not working_directory:
    return list( flags )
  new_flags = []
  make_next_absolute = False
  path_flags = [ '-isystem', '-I', '-iquote', '--sysroot=' ]
  for flag in flags:
    new_flag = flag

    if make_next_absolute:
      make_next_absolute = False
      if not flag.startswith( '/' ):
        new_flag = os.path.join( working_directory, flag )

    for path_flag in path_flags:
      if flag == path_flag:
        make_next_absolute = True
        break

      if flag.startswith( path_flag ):
        path = flag[ len( path_flag ): ]
        new_flag = path_flag + os.path.join( working_directory, path )
        break

    if new_flag:
      new_flags.append( new_flag )
  return new_flags


def FlagsForFile( filename ):
  if database:
    # Bear in mind that compilation_info.compiler_flags_ does NOT return a
    # python list, but a "list-like" StringVec object
    compilation_info = database.GetCompilationInfoForFile( filename )
    final_flags = MakeRelativePathsInFlagsAbsolute(
      compilation_info.compiler_flags_,
      compilation_info.compiler_working_dir_ )
  else:
    relative_to = DirectoryOfThisScript()
    final_flags = MakeRelativePathsInFlagsAbsolute( flags, relative_to )

  return {
    'flags': final_flags,
    'do_cache': True
  }
# NOTE Things I marked as TODO is not nessessary means I
#      will do it myself someday. It could be a suggestion
#      for anyone interested in it.

# NOTE for Linux user
# Qt common flags
# The Qt pkg-config module in Gentoo is Qt4/Qt5, But in OS X it's splited into many sub-modules.
# Do the compatible work yourself if needed
#QtModules = ["QtCLucene", "QtDeclarative", "QtDesignerComponents", "QtHelp", "QtNetwork", "QtScript", "QtSql", "QtTest", "QtUiTools_debug", "QtXml",
#             "QtCore", "QtDesigner", "QtGui", "QtMultimedia", "QtOpenGL", "QtScriptTools", "QtSvg", "QtUiTools", "QtWebKit", "QtXmlPatterns"]

#from subprocess import Popen
#from subprocess import PIPE
#qtflags = []
# TODO just inject the flags I used but not all of them
#for module in QtModules:
#    qtflags += Popen(['pkg-config', '--cflags'] + QtModules, stdout=PIPE).communicate()[0].split()

#flags += qtflags
# NOTE since the opencv2 library will be installed in the standard include path (e.g. /usr/include)
#      So there is no need to inject external flags here
