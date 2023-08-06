"""
PyPI setup file
"""

from setuptools import setup


setup(
    name='dndbuddy',
    packages=['dndbuddy'],
    version='0.0.1',
    author='Matt Cotton',
    author_email='matthewcotton.cs@gmail.com',
    url='https://github.com/MattCCS/DnDBuddy',

    description='It\'s DnDBuddy!',
    long_description=open("README.md").read(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],

    entry_points={
        "console_scripts": [
            "dndbuddy=dndbuddy.main:main",
        ]
    },
    install_requires=[
        "dndbuddy_core"
    ],
)
