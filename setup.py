from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines() # reading line by line

setup(
    name="mlops_project_1",
    version="0.1",
    author="Syed Musharraf Ali",
    author_email="musharrafleo94@gmail.com",
    packages=find_packages(), # automatically find packages in utils, config, src
    install_requires=requirements
)