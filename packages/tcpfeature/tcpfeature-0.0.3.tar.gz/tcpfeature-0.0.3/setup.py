import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tcpfeature",
    version="0.0.3",
    author="dzokha",
    author_email="dzokha1010@gmail.com",
    description="extraction feature from tcp/ip for machine learning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/tcpfeature",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

# python3 setup.py sdist bdist_wheel
# twine upload dist/*

