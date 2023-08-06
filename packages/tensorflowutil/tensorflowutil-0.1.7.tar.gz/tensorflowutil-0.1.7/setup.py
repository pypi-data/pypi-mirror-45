import os
from setuptools import setup, find_packages

README = 'PYPI_README.md'
PACKAGENAME = 'tensorflowutil'
MAIN_ENTRYPOINT = "tfutil"

# __version__ = x.x.x
with open(os.path.join(os.path.dirname(__file__),
                       PACKAGENAME,
                       'version.py')) as f:
    exec(f.read())


with open('requirements.txt') as f:
    requirements = f.readlines()


def long_desc():
    with open(README) as f:
            return f.read()

setup(
    name=PACKAGENAME,
    version=__version__,
    description='Collection of some useful tensorflow util functions.',
    author='Ashish Sharma',
    author_email='accssharma@gmail.com',
    url='https://github.com/accssharma/{}'.format(PACKAGENAME),
    license='MIT',
    long_description=long_desc(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    test_suite='tests',
    install_requires=requirements,
    setup_requires=["setuptools"],
    entry_points={
      'console_scripts': ['{}={}.main:main'.format(MAIN_ENTRYPOINT,
                                                   PACKAGENAME)]
    },
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)
