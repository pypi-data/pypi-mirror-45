from setuptools import setup

setup(
    name='loadneptun',
    version='0.3',    
    description='loadneptun(versionNumber): returns a pandas dataframe with the neptun_db of the correct version',
    py_modules=['loadneptun'],
    package_dir={'': 'src'},
)