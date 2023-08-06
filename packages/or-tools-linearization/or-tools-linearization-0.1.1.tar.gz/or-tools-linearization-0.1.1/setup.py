import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='or-tools-linearization',
    version='0.1.1',
    description='This package allows you to linearize non-linear functions and make use of them with or-tools in '
                'constraints or the objective function',
    author='Usiel Riedl',
    author_email='usiel.riedl@gmail.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Usiel/or-tools-linearization",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
)
