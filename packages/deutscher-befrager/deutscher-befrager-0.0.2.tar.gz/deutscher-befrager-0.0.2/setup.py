import setuptools

install_requires = [
    'PyYAML',
    'Click',
]

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="deutscher-befrager",
    version="0.0.2",
    author="Travis Shears",
    author_email="t@travisshears.com",
    description="CLI Language Learning Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    include_package_data=True,
    # extras_require=extras_require,
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Operating System :: MacOS',
    ],
    entry_points={
        'console_scripts': [
            'befrager = interviewer.core:cli',
        ],
    },
    keywords='command line interface cli python language learning interactive tool',
)
