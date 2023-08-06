from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name = 'workfrankomik',
    version = '1.5',
    packages = find_packages(),
    long_description = open(join(dirname(__file__), 'README.rst')).read(),
    scripts=['worker.py'],
    url='https://github.com/mik62/workfrankomik',
    download_url ='https://github.com/mik62/workfrankomik/blob/master/workfrankomik-1.5.tar.gz',
    entry_points = {
       'console_scripts':
        ['worker = worker:main'],
    }
)        
