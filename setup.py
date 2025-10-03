import os
from setuptools import setup, find_packages

# Get absolute path to the directory containing this file
this_dir = os.path.abspath(os.path.dirname(__file__))

# Read the long description from docs/index.md
with open(os.path.join(this_dir, "docs", "index.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="kn-sock",
    version="v0.3.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "kn-sock=kn_sock.cli:run_cli",
        ],
    },
    install_requires=["opencv-python", "numpy", "pyaudio", "ffmpeg-python"],
    author="Khagendra Neupane",
    author_email="nkhagendra1@gmail.com",
    description="Modern Python networking library with comprehensive protocol support and developer-friendly APIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KhagendraN/kn-sock",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
