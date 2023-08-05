from setuptools import setup, find_packages


setup(
    name='yapatch',
    version='0.0.2',
    short_description='Python implement of patch command',
    install_requires=[
        "unidiff",
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'yapatch = yapatch.main:main',
        ]
    }
)
