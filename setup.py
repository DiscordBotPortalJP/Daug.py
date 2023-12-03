from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='Daug',
    version='2023.12.3.2',
    author='Discord Bot Portal JP',
    author_email='discordbot.jp@gmail.com',
    description='discord.py を利用した Discord Bot 向け機能拡張ライブラリ',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/DiscordBotPortalJP/Daug.py',
    packages=find_packages(),
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'discord.py >= 2.3.2',
        'python-dotenv >= 1.0.0',
    ],
)
