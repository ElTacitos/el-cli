from setuptools import setup, find_packages

setup(
    name='ElCli',
    version='0.1',
    py_modules=['aquacli'],
    install_requires=[
        'Click',
        'Inquirer'
    ],
    entry_points='''
        [console_scripts]
        elcli=elcli:cli
    '''
)