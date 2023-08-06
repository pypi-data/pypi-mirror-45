from setuptools import setup, find_packages

setup(
    name = "easysql2pd",
    version = "0.0.1.9",
    keywords = ("pip", "sql","pandas", "pd"),
    description = "sql for pandas",
    long_description = "a simple tools for pandas to use sql",
    license = "GPL Licence",

    url = "https://github.com/StevenSunnySun/JT",
    author = "SSS",
    author_email = "steven_sunny_316@163.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ['pandas','numpy','sqlalchemy']
    
)