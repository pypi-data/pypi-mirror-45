
from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages 
import glob, os.path, sys


# Path check
def which(command):
    percorso = os.getenv("PATH")
    directories = percorso.split(os.pathsep)
    for path_dir in directories:
        real_dir = os.path.expanduser(path_dir)
        try:
            lista_dir = os.listdir(real_dir)
        except OSError:
            lista_dir = []
        if os.path.exists(real_dir) and command in lista_dir:
            return os.path.join(real_dir, command)
    return None


# Look for script files
lscr = glob.glob(os.path.join('Scripts', 'SRP*'))
lscrex = []
for i in lscr:
    if os.path.splitext(i)[1] == '':
        lscrex.append(i)


# Look for data files
lsdt = glob.glob(os.path.join('SRPFITS/Data', '*'))
lsdtex = []
for i in lsdt:
    if os.path.splitext(i)[1] == '':
        lsdtex.append(i)



import SRPFITS as FITS


setup(
    name='SRPAstro.FITS',
    version=FITS.__version__,
    description='Tools for handling FITS files under SRP',
    packages = find_packages('.'),
    include_package_data = True,
    long_description='Set of tools to handle FITS files.',
    author='Stefano Covino', 
    author_email='stefano.covino@brera.inaf.it', 
    url='https://pypi.python.org/pypi/SRPAstro.FITS',
    install_requires=['SRPAstro > 4.2', 'sep', 'photutils', 'astropy'],
    scripts=lscrex,
    zip_safe = False,
    package_data={'SRPFITS':lsdtex},
    classifiers=[ 
        'Development Status :: 5 - Production/Stable', 
        'Environment :: Console', 
        'Intended Audience :: Science/Research', 
        'License :: Freely Distributable', 
        'Operating System :: MacOS :: MacOS X', 
        'Operating System :: POSIX', 
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Scientific/Engineering :: Astronomy', 
        ], 
    ) 

