import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cal_event_search",
    version="1.0.8",
    author="Pol Monroig",
    author_email="polmonroig@gmail.com",
    description="Calendar Event Search",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/polmonroig/calendar_api",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)