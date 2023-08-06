import setuptools

# README text

with open("README.rst", "r") as f:
    long_description = f.read()

#calling setup()
setuptools.setup(
    name="stats_scraper",
    version="1.0.0",
    description="Scrapes NBA player data from basketball-reference.com and has few methods to sort the data",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/JosephJ12/stats_scraper2",
    author="Joseph Jung",
    author_email="josephjung12@gmail.com",
    license="MIT",
    classifiers = [
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=["requests",
        "contextlib2",
        "bs4",],
)