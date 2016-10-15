from setuptool import setup, find_packages

import gogowidget

setup(
    name='gogowidget',
    version='1.0.0',
    packages=find_packages(),
    author='Cheikhrouhou Yacine',
    author_email='yacine.cheikhrouhou@yahoo.fr',
    description='Utilitary library',
    long_description=open('README.md').read(),
    install_requires=['rsa'],
    include_package_data=True,
    url=''
)
