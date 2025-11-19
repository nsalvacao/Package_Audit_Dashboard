"""Setup script for Package Audit Dashboard CLI."""
from setuptools import find_packages, setup

setup(
    name="audit-cli",
    version="0.1.0",
    description="Package Audit Dashboard CLI",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "typer>=0.9.0",
        "rich>=13.7.0",
    ],
    entry_points={
        "console_scripts": [
            "audit-cli=cli.audit_cli.app:app",
        ],
    },
    python_requires=">=3.10",
)
