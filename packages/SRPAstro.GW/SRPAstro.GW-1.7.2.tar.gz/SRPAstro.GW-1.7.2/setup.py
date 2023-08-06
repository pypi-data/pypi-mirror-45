
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



import SRPGW as GW
durl = 'http://www.me.oa-brera.inaf.it/utenti/covino/SRPAstro.GW-%s.tar.gz' % GW.__version__



setup(
    name='SRPAstro.GW',
    version=GW.__version__,
    description='Tools for handling GW EM transient search under SRP',
    packages = find_packages('.'),
    include_package_data = False,
    long_description='Set of tools to handle GW EM transient search.',
    author='Stefano Covino', 
    author_email='stefano.covino@brera.inaf.it', 
    url='http://www.me.oa-brera.inaf.it/utenti/covino/SRPAstro.GW.pdf',
    download_url=durl,    
    install_requires=['SRPAstro >= 4.2.13','PyPrind','mysql-connector-python','sep >= 0.5', 'photutils', 'astropy >= 1.1.1', 'aplpy', 'pyds9', 'SRPAstro.FITS >= 2.4.3',
        'astlib', 'feets'],
    scripts=lscrex,
    zip_safe = False,
    package_data={'SRPGW':['Data/*',]},
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

