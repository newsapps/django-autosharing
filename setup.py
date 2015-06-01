from setuptools import find_packages, setup

# PyPI only supports nicely-formatted README files in reStructuredText.
# Newsapps seems to prefer Markdown.  Use a version of the pattern from
# https://coderwall.com/p/qawuyq/use-markdown-readme-s-in-python-modules
# to convert the Markdown README to rst if the pypandoc package is
# present.
try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError, OSError):
    long_description = open('README.md').read()

# Load the version from the version module
exec(open('autosharing/version.py').read())

setup(
    name='django-autosharing',
    version=__version__,
    description=("Simple Django app for periodically sharing Django models using "
        "social media"),
    long_description=long_description,
    author="Geoff Hing for Chicago Tribune News Applications",
    author_email="newsapps@tribune.com",
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires=[
        'Django',
        'tweepy',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Framework :: Django',
    ],
    test_suite='runtests.runtests',
)
