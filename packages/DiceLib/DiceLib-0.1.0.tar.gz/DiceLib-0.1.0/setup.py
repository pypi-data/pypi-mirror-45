from setuptools import setup, find_packages

setup(
    name='DiceLib',
    version="0.1.0",
    url='https://github.com/rolecraft/DiceLib',
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    author="CMSteffen",
    author_email="cmsteffen@protonmail.com",
    description="A dice-rolling library for RPGs.",
    packages=["DiceLib"],
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    zip_safe=False,
)
