from setuptools import setup, find_packages

setup(
    name="kfmd",
    version="0.1.1",
    packages=find_packages(),
    install_requires=['ml_metadata>=0.13.2'],
    #tests_require=TESTS_REQUIRES,
    author="kfmd",
    description="Prototype kfmd SDK",
)