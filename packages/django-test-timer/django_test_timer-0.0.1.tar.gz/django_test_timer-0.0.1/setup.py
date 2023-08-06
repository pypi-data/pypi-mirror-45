import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django_test_timer",
    version="0.0.1",
    author="Matt Shaw",
    author_email="m@ttshaw.com",
    description="Print the amount of time that each unit test took",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/unformatt/django-test-timer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
