import setuptools

def readme():
    with open('README.md') as f:
        return f.read()

setuptools.setup(
    name="matyimodule",
    version="0.2",
    description="Egy minta, hogy hogyan kell Pip csomagot csinálni.",
    long_description=readme(),
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