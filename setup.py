import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zy-aliyun-python-sdk",
    version="0.1.1",
    author="JohnToms",
    license='MIT',
    author_email="johntoms@163.com",
    description="sdk for aliyun",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/johntoms/aliyun-sdk",
    install_requires=[
        'certifi>=2019.6.16',
        'chardet>=3.0.4',
        'decorator>=4.4.0',
        'idna>=2.8',
        'requests>=2.22.0',
        'retry>=0.9.2',
        'urllib3>=1.25.3',
        'xmltodict>=0.12.0'
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
