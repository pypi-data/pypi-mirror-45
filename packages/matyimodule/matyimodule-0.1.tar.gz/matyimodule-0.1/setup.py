import matyimodule
import setuptools

a = matyimodule
a.sb(1)

setuptools.setup(
    name="matyimodule",
    version="0.1",
    author="matyi ONER",
    author_email="oner@matyi.com",
    description="Package amit csinaltam most",
    long_description_content_type="text/markdown",
    url="https://github.com/matyioner/pekk",
    packages=setuptools.find_packages(),
    install_requires=[
        'markdown',
    ],
    test_suite='nose.collector',
    tests_require=['nose'],
)