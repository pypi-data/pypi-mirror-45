import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="openstock",
    version="0.0.5",
    author="Chanson Shaw",
    author_email="lovezww2011@gmail.com",
    description="A python util for US stock market",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/openstock/",
    packages=setuptools.find_packages(),
    install_requires=[
        'requests>=2.18.1',
    ],
    dependency_link=[
      'https://files.pythonhosted.org/packages/7d/e3/20f3d364d6c8e5d2353c72a67778eb189176f08e873c9900e10c0287b84b/requests-2.21.0-py2.py3-none-any.whl'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)