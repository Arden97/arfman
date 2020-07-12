import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="arfman",
    version="0.0.1",
    author="Denisov Artem",
    author_email="arden2545@gmail.com",
    description="A CLI tree-like file manager written in Python",
    url="https://github.com/Arden97/arfman",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "arfman = arfman:main.main",
        ]
    },
    python_requires='>=3.6',
)