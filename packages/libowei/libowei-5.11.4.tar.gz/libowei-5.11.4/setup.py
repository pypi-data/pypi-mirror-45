from setuptools import setup, find_packages

setup(
    name = "libowei",
    version = "5.11.4",
    keywords = "math",
    description = "数学工程库",
    long_description = "基础数学,统计学,物理",
    license = "MIT Licence",
    url="https://github.com/",
    author = "Libowei",
    author_email = "913911037@qq.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["sympy"]
)