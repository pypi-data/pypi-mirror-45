from setuptools import setup


setup(
    name='yapatch',
    version='0.0.1',
    short_description='Python implement of patch command',
    install_requires=[
        "unidiff",
    ],
    entry_points={
        'console_scripts': [
            'yapatch = yapatch.main:main',
        ]
    }
)
