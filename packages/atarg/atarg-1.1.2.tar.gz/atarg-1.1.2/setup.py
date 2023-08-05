from setuptools import setup, find_packages
from os import path

root_dir = path.abspath(path.dirname(__file__))

setup(
        name='atarg',
        version='1.1.2',
        description='Utility tools for AtCoder',
        author='Ittoh Kimura',
        author_email='kimura.itto.kd3@gmail.com',
        url='https://github.com/itto-ki/Atarg/',
        license='MIT',
        install_requires=[
            'requests',
            'beautifulsoup4'
            ],
        packages=find_packages(exclude=('tests')),
        scripts=['scripts/atarg'],
        test_suite='tests',
        classifiers=[
                    'Development Status :: 4 - Beta',
                    'Environment :: Console',
                    'License :: OSI Approved :: MIT License',
                    'Programming Language :: Python :: 3',
                    'Topic :: Internet :: WWW/HTTP',
                    'Topic :: Software Development',
                    'Topic :: Utilities',
        ],
    )
