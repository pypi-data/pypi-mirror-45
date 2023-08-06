#
from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='reusegen',
    version='0.1.2',
    description='Cache generator\'s results and reuse them',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Topic :: Utilities',
    ],
    url='http://github.com/whoiscc/reusegen',
    author='Correctizer',
    author_email='correctizer@gmail.com',
    license='MIT',
    packages=['reusegen'],
    test_suite='nose.collector',
    tests_require=['nose'],
)
