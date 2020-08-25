from setuptools import setup, find_packages

setup(
    name='Daug',
    version='2020.8.25',
    py_modules=find_packages(),
    install_requires=[
        'discord.py >= 1.4.1',
        'dispander >= 0.4.0',
        'echidna >= 0.2.1',
    ],
)
