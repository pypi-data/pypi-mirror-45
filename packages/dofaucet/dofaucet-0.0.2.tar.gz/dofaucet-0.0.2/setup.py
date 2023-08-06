import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dofaucet",
    version='0.0.2',
    author="Aljoscha Vollmerhaus",
    author_email='pydev@aljoscha.vollmerhaus.net',
    description="read ansible yaml inventory, create droplets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/avollmerhaus/dofaucet",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Environment :: Console"
    ],

    install_requires=['python-digitalocean', 'pyyaml'],
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    entry_points={'console_scripts': ['dofaucet = dofaucet.cli:open_faucet']},

)
