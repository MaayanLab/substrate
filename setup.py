"""Installs Python package.
"""


from setuptools import setup, find_packages


setup(
    name='substrate',
    url='https://github.com/MaayanLab/substrate',
    author='Gregory Gundersen',
    author_email='avi.maayan@mssm.edu',
    version='1.0',
    packages=find_packages(),
    install_requires=['flask', 'flask-sqlalchemy']
)