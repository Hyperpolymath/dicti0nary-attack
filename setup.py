from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dicti0nary-attack",
    version="0.1.0",
    author="Security Research Team",
    description="A security research utility for testing non-dictionary passwords",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Hyperpolymath/dicti0nary-attack",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.10",
    install_requires=[
        "click>=8.1.0",
        "pyyaml>=6.0",
        "rich>=13.0.0",
        "tqdm>=4.66.0",
        "colorama>=0.4.6",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
        ],
        "web": [
            "flask>=3.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "dicti0nary=dicti0nary_attack.cli:main",
        ],
    },
)
