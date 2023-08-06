from setuptools import setup, find_packages
with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
    name="short-chn-yn",
    version="0.0.2",
    author="cltian",
    author_email="cl.tian@live.com",
    description="Short Chinses literal YES or NO recognition by logic",
    long_description=long_description,
    url="https://github.com/foowaa/short-chn-yn/",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: Chinese (Simplified)",
        "Development Status :: 3 - Alpha",
        "Topic :: Scientific/Engineering :: Artificial Intelligence"
    ],
    package_data = {
    '': ['*.txt', '*.rst'],

    },
    keywords = "Chinese, NLP"
)