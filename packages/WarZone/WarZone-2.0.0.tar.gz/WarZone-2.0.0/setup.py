from distutils.core import setup

with open('README') as file:
    readme = file.read()
    
setup(
    name='WarZone',
    version='2.0.0',
    packages=['wargame'],
    url='https://testpypi.python.org/WarZone/',
    licence='LICENCE.txt',
    descripton='my fantasy game',
    long_description=readme,
    author='heseltine tutu',
    author_email='heseltine@protonmail.com'
)
