from setuptools import find_packages, setup

setup(
    name="script.sh",
    version="0.0.1",
    description="",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Nikita Tsvetkov",
    author_email="nikitanovosibirsk@yandex.com",
    url="https://github.com/nikitanovosibirsk/script.sh",
    license="Apache 2",
    packages=find_packages(exclude=("tests",)),
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
    ],
)
