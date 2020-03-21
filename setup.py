from setuptools import setup, find_packages

setup(
    name='discordbotjp',
    version='2020.3.21',
    py_modules=find_packages(),
    install_requires=[
        'discord.py >= 1.2.5',
        'dispander >= 0.3.0',
        'echidna >= 0.2.1',
    ],
)
