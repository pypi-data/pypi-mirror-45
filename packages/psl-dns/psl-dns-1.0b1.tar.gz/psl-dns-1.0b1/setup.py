import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="psl-dns",
    version="1.0b1",
    author="Peter Thomassen",
    author_email="mail@peter-thomassen.de",
    description="Query the Public Suffix List (PSL) via DNS and check the PSL status of a domain.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/peterthomassen/psl-dns",
    packages=setuptools.find_packages(),
    install_requires=['dnspython>=1.14.0'],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Internet :: Name Service (DNS)",
    ],
    entry_points = {
        'console_scripts': ['psl-dns_check=psl.commands.check:main',
                            'psl-dns_parse=psl.commands.parse:main',
                            'psl-dns_query=psl.commands.query:main',],
    }
)

