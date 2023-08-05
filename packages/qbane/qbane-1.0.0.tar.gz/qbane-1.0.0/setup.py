import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

req=["requests","PySocks","bs4","mysql-connector","stem"]

setuptools.setup(
    name="qbane",
    version="1.0.0",
    author="AlaBouali",
    author_email="trap.leader.123@gmail.com",
    description="cyber security library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AlaBouali/qbane",
    python_requires=">=2.7",
    install_requires=req,
    packages=["qbane"],
    license="MIT License",
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License ",
        "Operating System :: Unix",
    ],
)
