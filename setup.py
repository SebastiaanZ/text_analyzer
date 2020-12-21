"""This file is used to install this package using pip."""

from setuptools import find_packages, setup


setup(
    name="word_frequency_analyzer",
    version="1.0.0",
    description="Analyze a text for word frequencies.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Sebastiaan Zeeff",
    author_email="sebastiaan.zeeff@gmail.com",
    url="https://github.com/SebastiaanZ/text_analyzer",
    license="MIT",
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    install_requires=[],
    python_requires='~=3.9',
    extras_require={},
    include_package_data=False,
    zip_safe=False
)
