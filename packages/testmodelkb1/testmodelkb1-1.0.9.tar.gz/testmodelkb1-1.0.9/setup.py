import botocore

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

files = ["static/css/*", "rawdata/*", "templates/*", "static/js/*", "static/scss/*", "static/vendor/bootstrap/*",
         "static/vendor/chart.js/*", "static/vendor/datatables/*", "static/vendor/fontawesome-free/*", "static/vendor/jquery/*"
         ,"static/vendor/jquery-easing/*"]

setuptools.setup(
    name="testmodelkb1",
    version="1.0.9",
    author="Sirisha Rella",
    author_email="srnk2@mail.umkc.edu",
    description="ModelKB",
    long_description="ModelKB",
    long_description_content_type="text/markdown",
    url="https://github.com/SirishaRella/Xsequential_package",
    package_data={'Xsequential': files},
    packages=['Xsequential'],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
)