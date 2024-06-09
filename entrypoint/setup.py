from setuptools import setup, find_packages

setup(
    name="inspector_scan",
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'boto3',
    ],
    entry_points={
        'console_scripts': [
            'inspector-scan=entrypoint.main:main',
        ],
    },
)
