#from distutils.core import setup

#setup(
#    name='PyCDTS',
#    version='0.1.0',
#    author='Abdul Rawoof Shaik',
#    author_email='arshaik@asu.edu',
#    packages=['pycdts', 'pycdts.test'],
##    scripts=['bin/stowe-towels.py','bin/wash-towels.py'],
#    url='http://pypi.python.org/pypi/PyCDTS/',
#    license='LICENSE.txt',
#    description='A Python based Carrier and Defect Transport Solver',
#    long_description=open('README.txt').read(),
#    install_requires=[
#        "PyQt5  >=5.9.2",
#        "scikit-umfpack >=0.3.1"
#    ],
#)

import setuptools

with open("README.txt", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyCDTS",
    version="0.1.1",
    author="Abdul Rawoof Shaik",
    author_email="arshaik@asu.edu",
    description="A Python based Carrier and Defect Transport Solver",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/abdul529/pycdts",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
         'PyQt5  >= 5.9.2',
         'scikit-umfpack >= 0.3.1',
    ],  
)
