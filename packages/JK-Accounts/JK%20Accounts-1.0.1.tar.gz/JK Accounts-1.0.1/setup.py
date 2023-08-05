import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="JK Accounts",
    version="1.0.1",
    author="jackkillian",
    description="Make accounts for JK apps with this module. Just run jk-accounts.main()",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Jackkillian/JK-Accounts",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)"
    ],
)
