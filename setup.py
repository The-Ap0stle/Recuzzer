from setuptools import setup, find_packages

setup(
    name="Recuzzer",
    version="1.0.0",
    author="Ap0stle",
    description="A tool for recursive sub-directory fuzzing.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/The-Ap0stle/Recuzzer",
    license="GPL",
    packages=find_packages(),
    install_requires=[
        "requests",  
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "recuzzer=Recuzzer.main:main",  
        ],
    },
)
