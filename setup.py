from setuptools import setup, find_packages

setup(
    name="kn_sock",
    version="0.2.0",
    author="Khagendra Neupane",
    author_email="nkhagendra1@gmail.com",
    description="A simplified socket programming toolkit for Python.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/KhagendraN/easy-socket",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        # List of dependencies
    ],
    entry_points={
        'console_scripts': [
            'easy-socket=easy_socket.cli:run_cli',
        ],
    },
)
