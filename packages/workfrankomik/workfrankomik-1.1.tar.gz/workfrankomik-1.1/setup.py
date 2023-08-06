from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='workfrankomik',
    version='1.1',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.rst')).read(),
    scripts=['worker.py'],
    url='https://github.com/mik62/workfrankomik',
    download_url ='https://github.com/mik62/workfrankomik/blob/master/workfrankomik-1.1.tar.gz'        
)