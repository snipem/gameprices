from setuptools import setup
try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()

setup(
    name='psnprices',
    packages=['psnprices', 'psnprices.shops', 'psnprices.cli', 'psnprices.test', 'psnprices.utils'],
    version='1.0',
    description='An interface for the undocumented Sony PlayStation Store PSN Api',
    long_description=long_description,
    author='Matthias Kuech',
    author_email='halde@matthias-kuech.de',
    url='https://github.com/snipem/psnprices',
    download_url='https://github.com/snipem/psnprices/archive/1.0.tar.gz',
    keywords=['playstation', 'store', 'prices'],
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
            'eshopcli=psnprices.cli.psncli:eshop_main',
            'psncli=psnprices.cli.psncli:psn_main',
            'psndealsmailalert=psnprices.cli.psndealsmailalert:main',
            'psnmailalert=psnprices.cli.psnmailalert:main',
            'dealsmailalert=psnprices.cli.psnmailalert:main']
        }
    )
