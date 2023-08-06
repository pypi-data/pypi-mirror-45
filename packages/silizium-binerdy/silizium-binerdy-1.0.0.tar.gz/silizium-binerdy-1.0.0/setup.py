import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

INSTALL_REQUIRES = [
    'Click==7.0',
    'coverage==4.5.3',
    'coveralls==1.7.0',
    'pytest-bdd==3.1.0',
    'pytest-cov==2.6.1',
    'pytest==4.4.0',
    'selenium==3.141.0'
]

setuptools.setup(
    name='silizium-binerdy',
    version='1.0.0',
    author='Alan Meile',
    author_email='alan.meile@gmail.com',
    description='Source code for the wiki philosopy game in the module swt fs19',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/binerdy/swt-19fs-silizium',
    packages=setuptools.find_packages(),
    include_package_data=True,
    scripts=['silizium-cli.py'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>3.6',
    setup_requires=['setuptools==40.8.0'],
    install_requires=INSTALL_REQUIRES
)
