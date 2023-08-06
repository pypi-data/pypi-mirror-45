from setuptools import setup, find_packages

setup(
    name = "django-admin-auto",
    version = "0.1.1",
    keywords = ("pip", "django", "admin"),
    description = "To automate the Django Admin displaying.",
    long_description = open('README.rst').read(),
    license = "Apache-2.0 Licence",
    url = "https://github.com/excelwang/django-admin-auto",
    author = "Excel Wang",
    author_email = "wanghj@cnic.com",
    packages = find_packages(),
    include_package_data = True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires = ['django']
)