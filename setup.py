from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='Daug',
    version='2020.11.19.1',
    author='1ntegrale9',
    author_email='1ntegrale9uation@gmail.com',
    description='discord.py を利用した Discord Bot 向け機能拡張ライブラリ',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/DiscordBotPortalJP/Daug.py',
    packages=find_packages(),
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'discord.py >= 1.5.0',
        'dispander >= 0.4.0',
    ],
)
