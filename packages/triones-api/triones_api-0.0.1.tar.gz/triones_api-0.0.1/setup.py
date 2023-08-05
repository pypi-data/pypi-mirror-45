import setuptools

with open("description.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="triones_api",
    version="0.0.1",
    author="fankailun",
    author_email="kailunfan@163.com",
    description="api methods for Triones.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.chengfayun.net/implementation/TrionesAPI",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
