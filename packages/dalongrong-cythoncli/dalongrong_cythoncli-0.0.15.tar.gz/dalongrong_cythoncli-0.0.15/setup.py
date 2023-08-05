import setuptools
from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize
from distutils import extension as distutils_extension
from distutils.command import build as distutils_build
from distutils.command import build_ext as distutils_build_ext

import subprocess
with open("README.md", "r") as fh:
    long_description = fh.read()

add_extension = Extension(
    name="add_app",
    sources=["cli/app.pyx"],
    libraries=["add"],
    library_dirs=["cli/ext"],
    include_dirs=["cli/ext"]
)
class build_ext_Library(distutils_build_ext.build_ext):
    def run(self):
        command = "cd cli/ext && make"
        process = subprocess.Popen(command, shell=True)
        process.wait()
        distutils_build_ext.build_ext.run(self)
setuptools.setup(
    name="dalongrong_cythoncli",
    version="0.0.15",
    author="dalongrong",
    package_data={
        'cli': ['*.pyx',"ext/add.c","ext/add.h","ext/Makefile"]
    },    
    author_email="1141591465@qq.com",
    description="a simple cli project",
    long_description=long_description,
    install_requires=['click',"Cython==0.29.7"],
    ext_modules= cythonize([add_extension]),
    long_description_content_type="text/markdown",
    packages = [
        "cli"
    ],
    cmdclass ={
         "build_ext":build_ext_Library
      },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    project_urls={
        'Documentation': 'https://github.com/rongfengliang/cython-c-pip-demo.git',
        'Say Thanks!': 'https://github.com/rongfengliang/cython-c-pip-demo.git',
        'Source': 'https://github.com/rongfengliang/cython-c-pip-demo.git',
        'Tracker': 'https://github.com/rongfengliang/cython-c-pip-demo.git',
    },
    entry_points={
        'console_scripts': [
            'podcli=cli:apply',
        ],
    }
)