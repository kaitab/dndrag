from setuptools import setup, find_packages

requirements = []
with open('requirements.txt', 'r') as file:
    for line in file:
        line = line.strip()
        if line and not line.startswith('#') and not line.startswith('-'):
            requirements.append(line)

setup(
    name='dnd_rag',
    version='0.1',
    description='RAG tool for DnD SRD Data',
    packages=find_packages(where='src'), 
    package_dir={'': 'src'},          
    install_requires=requirements
)