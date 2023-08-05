
from setuptools import setup, find_packages

setup(
    name='terminaltranslator',
    version='1.0',
    packages=find_packages(),
    py_modules=['terminaltranslator'],
    author="Veelion",
    author_email="veelion@gmail.com",
    license='MIT',
    url='https://github.com/veelion/tt',
    description=("Linux terminal translating tool implemented in Python"),
    # scripts=['t', 'tt', 'terminaltranslator.py'],
    entry_points={
        'console_scripts': [
            't = terminaltranslator:main',
            'tt = terminaltranslator:main',
        ],
    }
)

