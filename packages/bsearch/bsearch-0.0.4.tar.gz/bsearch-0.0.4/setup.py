from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="bsearch",
    version="0.0.4",
    description="Binary search - bisect_left and bisect_right with more flexible comparison",
    author='Dominic Slee',
    author_email='domslee1@gmail.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=[
        'bsearch',
    ],
    package_dir={'':'bsearch'},
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    url='https://github.com/domsleee/bsearch',
    license='BSD'
)