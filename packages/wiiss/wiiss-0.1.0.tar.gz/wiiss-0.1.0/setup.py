from setuptools import setup, find_packages

long_description = """# wiiss
 -- short for 'where is iss' - provides the current location of the ISS based on data from the open-notify and nominatim osm apis

Just call `wiis.wiis()` to print the location information."""

setup(
    name='wiiss',
    version='0.1.0',
    packages=find_packages(),
    url='https://github.com/RoW171/wiiss',
    license='MIT',
    author="Robin 'r0w' Weiland",
    author_email='robinweiland@gmx.de',
    description='Provides the current location of the ISS',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='iss location api',
    py_modules=["wiiss"],
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
