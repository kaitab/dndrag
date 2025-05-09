from setuptools import setup, find_packages

setup(
    name='dnd_rag',
    version='0.1',
    description='RAG tool for DnD SRD Data',
    packages=find_packages(where='src'), 
    package_dir={'': 'src'},          
    install_requires=[
        'numpy',
        'pandas',
    ],
)