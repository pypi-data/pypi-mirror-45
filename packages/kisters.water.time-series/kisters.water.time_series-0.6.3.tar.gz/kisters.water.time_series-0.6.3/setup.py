"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from codecs import open
from os import path

from setuptools import setup

from xml.etree.ElementTree import parse


def getversion():
    pomfile = parse('pom.xml')
    root = pomfile.getroot()
    version = root.findall("{http://maven.apache.org/POM/4.0.0}version")
    if len(version) == 1:
        return version[0].text.replace("-", "+")
    raise Exception("No version found in pom")


# To use a consistent encoding
here = path.abspath(path.dirname(__file__))

if __name__ == "__main__":
    # Get the long description from the README file
    with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
        long_description = f.read()

    with open(path.join(here, "requirements.txt"), encoding='utf-8') as req:
        requirements = [l for l in req.read().splitlines() if not l.startswith('--')]

    setup(
        name='kisters.water.time_series',

        # Versions should comply with PEP440.  For a discussion on single-sourcing
        # the version across setup.py and the project code, see
        # https://packaging.python.org/en/latest/single_source_version.html
        # version='0.2',
        # get version from scm (see https://pypi.python.org/pypi/setuptools_scm)
        version=getversion(),
        python_requires='>=3.5, <4',

        description='KISTERS WATER Time Series Access library',
        long_description=long_description,

        # The project's main homepage.
        url='https://gitlab.com/kisters/kisters.water.time_series',

        # Author details
        author='Rudolf Strehle',
        author_email='rudolf.strehle@kisters.net',

        # Choose your license
        license='LGPL',

        # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
        classifiers=[
            # How mature is this project? Common values are
            #   3 - Alpha
            #   4 - Beta
            #   5 - Production/Stable
            'Development Status :: 4 - Beta',

            # Indicate who your project is intended for
            'Intended Audience :: Developers',

            # Pick your license as you wish (should match "license" above)
            'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',

            # Specify the Python versions you support here. In particular, ensure
            # that you indicate whether you support Python 2, Python 3 or both.
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
        ],

        # What does your project relate to?
        keywords='kisters water time series',

        # You can just specify the packages manually here if your project is
        # simple. Or you can use find_packages().
        package_dir={'': '.'},
        packages=['kisters.water.time_series.store_decorators',
                  'kisters.water.time_series.file_io',
                  'kisters.water.time_series.kiwis',
                  'kisters.water.time_series.kiwis._support.auth',
                  'kisters.water.time_series.tso',
                  'kisters.water.time_series.core'],

        # Alternatively, if you want to distribute just a my_module.py, uncomment
        # this:
        #   py_modules=["my_module"],

        # List run-time dependencies here.  These will be installed by pip when
        # your project is installed. For an analysis of "install_requires" vs pip's
        # requirements files see:
        # https://packaging.python.org/en/latest/requirements.html
        zip_safe=False,
        install_requires=requirements,
        setup_requires=['pytest-runner', 'wheel'],
        extras_require={
            'test': ['pytest', 'coverage', 'nbformat', 'nbconvert', 'statsmodels',
                     'matplotlib', 'jupyter_client', 'ipykernel', 'scipy', 'patsy']
        }

        # List additional groups of dependencies here (e.g. development
        # dependencies). You can install these using the following syntax,
        # for example:
        # $ pip install -e .[dev,test]
        # extras_require={
        #    'dev': ['check-manifest'],
        #    'test': ['coverage'],
        # },

        # If there are data files included in your packages that need to be
        # installed, specify them here.  If using Python 2.6 or less, then these
        # have to be included in MANIFEST.in as well.
        # package_data={
            # 'water_python_timeseries': ['package_data.dat'],
        # },

        # Although 'package_data' is the preferred approach, in some case you may
        # need to place data files outside of your packages. See:
        # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
        # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
        # data_files=[('my_data', ['data/data_file'])],

        # To provide executable scripts, use entry points in preference to the
        # "scripts" keyword. Entry points provide cross-platform support and allow
        # pip to create the appropriate form of executable for the target platform.
        # entry_points={'console_scripts': [
        #     ],
        # },
    )
