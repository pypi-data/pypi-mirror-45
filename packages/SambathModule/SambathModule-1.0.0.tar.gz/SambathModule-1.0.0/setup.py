from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="SambathModule",
    version="1.0.0",
    description="This is for assignment purpose. This package contains weather report and a language translator",
    long_description=readme(),
    long_description_content_type="text/markdown",
    py_modules=["SambathModule"],
    package_dir={'': 'src'},
    install_requires=['googletrans','feedparser'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
)
