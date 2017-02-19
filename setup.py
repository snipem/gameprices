from setuptools import setup
try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()

setup(
    name='psnprices',
    packages=['psnprices', 'psnprices.psn', 'psnprices.cli', 'psnprices.test', 'psnprices.utils'],
    version='1.0',
    description='An interface for the undocumented Sony PlayStation Store PSN Api',
    long_description=long_description,
    author='Matthias Kuech',
    author_email='halde@matthias-kuech.de',
    url='https://github.com/snipem/psnprices',
    download_url='https://github.com/snipem/psnprices/archive/1.0.tar.gz',
    keywords=['playstation', 'store', 'prices'],
    license='GPL2',
    test_suite='nose.collector',
    tests_require=['nose'],
    entry_points={
        'console_scripts': ['psncli=psnprices.cli.psncli:main',
                            'psndealsmailalert=psnprices.cli.psndealsmailalert:main',
                            'psnmailalert=psnprices.cli.psnmailalert:main'],
        }
    )
