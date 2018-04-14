from setuptools import setup
try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()

setup(
    name='gameprices',
    packages=['gameprices', 'gameprices.shops', 'gameprices.cli', 'gameprices.test', 'gameprices.utils'],
    version='1.0',
    description='An interface for the undocumented Sony PlayStation Store PSN and Nintendo Eshop Apis',
    long_description=long_description,
    author='Matthias Kuech',
    author_email='halde@matthias-kuech.de',
    url='https://github.com/snipem/psnprices',
    download_url='https://github.com/snipem/psnprices/archive/1.0.tar.gz',
    keywords=['playstation', 'eshop', 'store', 'prices'],
    license='GPL2',
    install_requires=[
        'requests',
    ],
    test_suite='nose.collector',
    tests_require=[
        'pytest-cov'
        ],
    entry_points={
        'console_scripts': [
            'eshopcli=gameprices.cli.cli:eshop_main',
            'psncli=gameprices.cli.cli:psn_main',
            'psndealsmailalert=gameprices.cli.psndealsmailalert:main',
            'psnmailalert=gameprices.cli.mailalert:main',
            'dealsmailalert=gameprices.cli.mailalert:main']
        }
    )
