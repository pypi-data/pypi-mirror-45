import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='yetu',
    version='1.0',
    url="https://johnnes-smarts.ch",
    license='License :: OSI Approved :: MIT License',
    author='David Johnnes',
    author_email='david.johnnes@gmail.com',
    description='General purpose software development frame-work.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='Type checking and input validation already integrated, attributes, methods, classes, decorators and metaclasses.',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
