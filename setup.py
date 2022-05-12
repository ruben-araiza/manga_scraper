from setuptools import find_packages, setup

setup(
    name='mangascraper',
    packages=find_packages(
        include=[
            'requests',
            'beautifulsoup4'
        ]
    ),
    version='0.1',
    description='Tools to download manga images from https://ww5.manganelo.tv/',
    author='Ruben Araiza',
    license='MIT',
)
