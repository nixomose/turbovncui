#!/usr/bin/env python3
"""
Setup script for TurboVNC UI
"""

from setuptools import setup, find_packages

setup(
    name="turbovncui",
    version="2.0.0",
    description="A graphical frontend for TurboVNC",
    author="TurboVNC UI Developer",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "PyQt5>=5.15.0",
    ],
    entry_points={
        "console_scripts": [
            "turbovncui=turbovncui.main:main",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
) 