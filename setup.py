from setuptools import find_packages, setup
setup(
    name='manga_scraper',
    packages=find_packages(
        include=[
            'requests',
            'beautifulsoup4'
        ]
    ),
    version='0.1',
    description='Library to download manga images from https://ww5.manganelo.tv/',
    author='Ruben Araiza',
    license='MIT',
)