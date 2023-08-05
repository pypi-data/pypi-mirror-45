from setuptools import setup
import pathlib
from setuptools import setup
from microk8s_configure.main import __version__

# The directory containing this file
HERE = pathlib.Path(__file__).parent
# The text of the README file
README = (HERE / "README.md").read_text()
setup(
    name='microk8s-configure',
    version=__version__,
    packages=['microk8s_configure'],
    url='https://github.com/netsaj/microk8s-configure',
    license='MIT',
    description='Tool for configure microk8s on Ubuntu VPS',
    long_description=README,
    long_description_content_type='text/markdown',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    author='Fabio Moreno',
    author_email='fabiomoreno@outlook.com',
    entry_points={
        'console_scripts': [
            'mk8sconfig = microk8s_configure.main:main',
            'microk8s-configure= microk8s_configure.main:main',
        ],
    },
    scripts=['mk8sconfig.py']
)
