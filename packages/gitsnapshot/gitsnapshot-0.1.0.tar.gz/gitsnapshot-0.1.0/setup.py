from setuptools import setup, find_packages

setup(
    name='gitsnapshot',
    version='0.1.0',
    description='Python module to simplify loading of snapshot of git repository',
    author='Kirill Sulim',
    author_email='kirillsulim@gmail.com',
    license='MIT',
    url='https://github.com/kirillsulim/gitsnapshot',
    packages=find_packages(include=[
        'gitsnapshot',
    ]),
    test_suite='tests',
    install_requires=[
    ],
    classifiers=[
    ],
    keywords='git snapshot load download delivery config',
)
