from setuptools import setup

version = '1.1'


setup(
    name='tt_cli',
    version=version,
    packages=[
        'tt_cli',
        'tt_cli.commands',
    ],
    url='https://github.com/a1fred/tt',
    entry_points={
        'console_scripts': ['tt=tt_cli.cli:main'],
    },
    license='MIT',
    author='a1fred',
    author_email='demalf@gmail.com',
    description='Simple commandline timetracker',
    classifiers=[
        'Environment :: Console',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite="tests",
)