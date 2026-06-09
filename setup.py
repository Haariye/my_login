from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

setup(
    name="my_login",
    version="1.0.0",
    description="Elegant per-site login page for Dagaar Technology",
    author="Dagaar Technology",
    author_email="info@dagaartech.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires,
)
