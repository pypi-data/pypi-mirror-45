from setuptools import setup


def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name='ungleich-cli',
    version='1.0.0',
    description="A Python package for ungleich dns administration.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="William Colmenares",
    author_email="colmenares.william@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],

    py_modules=['ungleichcli'],
    install_requires=[
        'Click',
        'requests',
    ],
    entry_points={
        "console_scripts": [
            "ungleich-cli=ungleichcli:cli"
        ]
    },
)
