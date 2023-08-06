from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="skhk",
    version="1.0.0",
    description=".",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="",
    author="",
    author_email="",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3"
    ],
    packages=["skhk"],
    include_package_data=True
)
