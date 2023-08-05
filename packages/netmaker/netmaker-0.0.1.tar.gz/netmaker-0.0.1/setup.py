import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="netmaker",
    version="0.0.1",
    author="Sergiy Popovych",
    author_email="sergiy.popovich@gmail.com",
    description="A tool for building deep neural networks from JSON specs in pyTorch.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/supersergiy/netmaker",
    packages=setuptools.find_packages(),
)
