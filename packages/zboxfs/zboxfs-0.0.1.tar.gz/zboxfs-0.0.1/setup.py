import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zboxfs",
    version="0.0.1",
    author="Bo Lu",
    author_email="support@zbox.io",
    description="ZboxFS binding for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zboxfs/zbox",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
