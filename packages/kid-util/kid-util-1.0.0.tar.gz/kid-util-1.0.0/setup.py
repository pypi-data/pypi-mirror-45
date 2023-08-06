from setuptools import setup, find_packages


setup(
    name='kid-util',
    version='1.0.0',
    author='Halvor Holsten Strand',
    author_email='halvor.holsten.strand@gmail.com',
    url='https://github.com/Ondkloss/kid-util',
    description='Module for making and verifying KID numbers',
    license='WTFPL',
    packages=find_packages(exclude=['test']),
)
