from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="rgpython",
    version="1.0.0",
    description="A Python package to simplify daily use python code.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/Kamleshgupta1/rgpython",
    author="Kamlesh Gupta",
    author_email="kamleshguptaom@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
    ],
    packages=["regular"],
    include_package_data=True,
    #install_requires=["requests"], what package we have used to developed
    entry_points={
        "console_scripts": [
            "rgpython=regular.cli:main",
        ]
    },
)

