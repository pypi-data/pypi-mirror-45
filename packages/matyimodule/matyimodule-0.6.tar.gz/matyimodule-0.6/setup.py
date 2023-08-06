import setuptools
import codecs
ld = codecs.open('README.md','r','utf-8').read()

setuptools.setup(
    name="matyimodule",
    version="0.6",
    description="Egy minta, hogy hogyan kell Pip csomagot csinálni.",
    long_description=ld,
    long_description_content_type="text/markdown",
    author="Matyi",
    author_email="mmatyi1999@gmail.com",
    url="https://github.com/matyifkbt/matyimodule",
    packages=setuptools.find_packages(),
    install_requires=[
        'markdown',
    ],
    test_suite='nose.collector',
    tests_require=['nose'],
    entry_points={
        'console_scripts': ['matyicommand=matyimodule.app:main'],
    },
)