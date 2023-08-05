from setuptools import setup
import os
import platform

version = '0.4.9'

print("seting up for " + platform.system() + " " + platform.architecture()[0] + " platform")
if platform.system() == 'Windows' and platform.architecture()[0] == '32bit':
    os.rename("./ICS_IPA/_DataFileIOLibraryInterface32.pyd", "./ICS_IPA/_DataFileIOLibraryInterface.pyd")
elif platform.system() == 'Windows' and platform.architecture()[0] == '64bit':
    os.rename("./ICS_IPA/_DataFileIOLibraryInterface64.pyd", "./ICS_IPA/_DataFileIOLibraryInterface.pyd")
elif platform.system() == 'Linux':
    os.rename("./ICS_IPA/_DataFileIOLibraryInterface64.so", "./ICS_IPA/_DataFileIOLibraryInterface.so")
else:
    raise "Platform is not supported"

setup(
    name='ICS_IPA',
    packages=['ICS_IPA'],
    version=version,
    description='API used for DataMining mdf data files using DataSpy',
    long_description='This repo is designed to manage the library functions used \
                      for DataMining through mdf data files using the DataSpy \
                      product made by Intrepid Control System. The library \
                      contains a bunch of File I/O functions in a dll that \
                      allow users to parse through mdf data files using their \
                      own applications like Python, Excel, Matlab, C# etc. \
                      This library of functions is duplicated on Intrepids \
                      wireless data server (Wireless NeoVI) allowing users to \
                      develop scripts on their PC and then run those scripts \
                      on the Wireless Neo VI data server without requiring \
                      the data to be downloaded.',
    maintainer='Zaid Nackasha',
    maintainer_email='ZNackasha@intrepidcs.com',
    url='https://github.com/intrepidcs/ICS_IPA',
    download_url='https://github.com/intrepidcs/ICS_IPA/archive/' +
                 version + '.tar.gz',
    package=['DataFileIOLibrary'],
    package_data={'DataFileIOLibrary':
                  ['ICS_IPA/_DataFileIOLibraryInterface32.pyd',
                   'ICS_IPA/_DataFileIOLibraryInterface64.pyd',
                   'ICS_IPA/_DataFileIOLibraryInterface64.so']},
    include_package_data=True,
    classifiers=['Operating System :: Microsoft :: Windows',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 3.6']
)
