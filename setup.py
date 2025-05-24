#!/usr/bin/env python3
"""
Setup script for Financial Risk Assessment System
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

# Get version
def get_version():
    version_file = os.path.join("project code", "config", "settings.py")
    if os.path.exists(version_file):
        with open(version_file, "r") as f:
            for line in f:
                if line.startswith("APP_VERSION"):
                    return line.split("=")[1].strip().strip("'\"")
    return "2.0.0"

setup(
    name="financial-risk-assessment-system",
    version=get_version(),
    author="ViktorFu",
    author_email="viktoru@example.com",
    description="Enterprise-grade financial risk assessment and management platform",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/ViktorFu/Financial-Risk-Assessment-System",
    project_urls={
        "Bug Reports": "https://github.com/ViktorFu/Financial-Risk-Assessment-System/issues",
        "Source": "https://github.com/ViktorFu/Financial-Risk-Assessment-System",
        "Documentation": "https://github.com/ViktorFu/Financial-Risk-Assessment-System/wiki",
    },
    packages=find_packages(where="project code"),
    package_dir={"": "project code"},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Environment :: X11 Applications :: Qt",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=22.0",
            "flake8>=5.0",
            "isort>=5.0",
            "mypy>=1.0",
            "pre-commit>=2.20",
        ],
        "security": [
            "bandit>=1.7",
            "safety>=2.0",
        ],
        "monitoring": [
            "prometheus-client>=0.15",
            "grafana-api>=1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "financial-risk-system=main:main",
            "fras=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.csv", "*.sql", "*.json", "*.yml", "*.yaml"],
    },
    keywords=[
        "finance",
        "risk assessment",
        "credit scoring",
        "banking",
        "financial analysis",
        "risk management",
        "compliance",
        "Basel III",
        "PyQt5",
        "desktop application"
    ],
    zip_safe=False,
) 