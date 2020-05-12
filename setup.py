from setuptools import setup, find_packages

setup(
    name='discordbotjp',
    version='2020.5.13',
    py_modules=find_packages(),
    install_requires=[
        'discord.py >= 1.3.3',
        'dispander >= 0.4.0',
        'echidna >= 0.2.1',
    ],
)
