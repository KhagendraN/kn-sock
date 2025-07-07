from setuptools import setup, find_packages

setup(
    name="kn-sock",
    version="0.2.3",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'kn-sock=kn_sock.cli:run_cli',
        ],
    },
    install_requires=[
        "opencv-python",
        "numpy",
        "pyaudio",
        "ffmpeg-python"
    ],
    author="Khagendra Neupane",
    author_email="nkhagendra1@gmail.com",
    description="A simplified socket programming toolkit for Python",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/KhagendraN/kn-sock",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
