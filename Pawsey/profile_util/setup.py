from setuptools import setup, Extension
from pybind11.setup_helpers import Pybind11Extension, build_ext
#from pybind11.setup_helpers import Pybind11Extension
import pybind11

# Define the extension module
ext_modules = [
    Extension(
        'profile_util',  # Module name
        ['src/profile_util_pyinterface.cpp', 'src/profile_util.cpp', 'src/mem_util.cpp', 'src/thread_affinity_util.cpp', 'src/time_util.cpp',  'src/pybind11_git_revision.cpp'],  # Source file(s)

        include_dirs=[
            pybind11.get_include(),  # Include Pybind11 headers
            'include/'
        ],
        language='c++',  # Specify the language
        extra_compile_args=['-std=c++20', '-O3'],  # Add other compiler flags if needed
        depends = ['include/profile_util.h', 'include/profile_util_gpu.h']
    ),
]

# Define the setup
setup(
    name='profile_util',
    version='0.1',
    author='Pascal Jahan Elahi',
    author_email='pascaljelahi@gmail.com',
    description='A simple profile_util Pybind11 module',
    ext_modules=ext_modules,
    # Specify the pybind11 build extension
    cmdclass={'build_ext': build_ext},
)

