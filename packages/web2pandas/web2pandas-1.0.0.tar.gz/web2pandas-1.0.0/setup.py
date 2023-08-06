from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="web2pandas",
    version="1.0.0",
    description="web to pandas dataframe",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/IamSantoshKumar/DeepLearning-Workouts",
    author="santhoshkumar",
    author_email="shanvsanthosh@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["webscrppandas"],
    include_package_data=True,
    install_requires=["requests"],
    entry_points={
        "console_scripts": [
            "web2pandas=webscrppandas.web2pd:main",
        ]
    },
)