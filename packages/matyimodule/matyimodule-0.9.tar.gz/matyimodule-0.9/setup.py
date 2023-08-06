import setuptools
import codecs
ld = codecs.open('README.md','r','utf-8').read()
print(ld)
setuptools.setup(
    name="matyimodule",
    version="0.9",
    description="Egy minta, hogy hogyan kell Pip csomagot csinálni.",
    long_description=open('README.md', encoding='UTF-8').read(),
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
    include_package_data=True,
)