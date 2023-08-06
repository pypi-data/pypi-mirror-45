import setuptools

from src.ptth import __version__ as version

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="post-tonal-theory-helper-mbmasuda",
    version=version,
    author="Mari Masuda",
    author_email="mbmasuda.github@gmail.com",
    description="Post-tonal music theory analysis functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mbmasuda/post-tonal-theory-helper",
    packages=setuptools.find_packages('src'),
    package_dir={'':'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
