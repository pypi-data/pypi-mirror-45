from setuptools import setup, find_packages

setup(
    name='ShareMount',
    version='0.6b.0dev',
    author='Darryl lane',
    author_email='DarrylLane101@gmail.com',
    packages=['ShareMount'],
    include_package_data=True,
    license='LICENSE',
    description='''
    Mount shares on Linux and OSX.
    ''',
    long_description=open('README.md').read(),
    
    scripts=['ShareMount/ShareMount.py']
)

