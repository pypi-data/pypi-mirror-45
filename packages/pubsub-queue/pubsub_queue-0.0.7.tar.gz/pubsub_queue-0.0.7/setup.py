import setuptools

try:
    with open("README.md", "r") as fh:
        long_description = fh.read()
except:
    long_description = "PubSub Queue Manager"

setuptools.setup(
    name="pubsub_queue",
    version="0.0.7",
    author="Samuel Heinrichs",
    author_email="samuel@n2bbrasil.com",
    description="PubSub Queue Manager",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    url="https://github.com/N2BBrasil/pubsub-queue",
    install_requires=[r for r in open("requirements.txt").read().split("\n")],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)