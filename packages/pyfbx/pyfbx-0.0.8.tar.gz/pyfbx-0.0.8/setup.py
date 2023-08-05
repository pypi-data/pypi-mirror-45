import pathlib
from setuptools import setup, find_packages

setup(
    name="pyfbx",
    version="0.0.8",
    description="Freebox thin client",
    long_description=(pathlib.Path(__file__).parent / "README.md").read_text(),
    long_description_content_type='text/markdown',
    author_email="teebeenator@gmail.com",
    url='https://framagit.org/sun/pyfbx',
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    packages=find_packages(),
    install_requires=["zeroconf", "requests"],
    include_package_data=True,
    entry_points={'console_scripts': ['pyfbx = pyfbx.__main__:main', ]},
)
