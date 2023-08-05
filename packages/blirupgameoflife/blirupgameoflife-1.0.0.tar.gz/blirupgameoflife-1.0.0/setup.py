from setuptools import setup

setup(
    name='blirupgameoflife',
    version='1.0.0',
    description='Conway\'s Game of Life implemented with PyGame',
    url='',
    author='Blirup',
    author_email='martin.blirup@gmail.com',
    license='GPL-3.0',
    packages=['blirupgameoflife'],
    scripts=[
        'bin/blirupgameoflife',
        'bin/blirupgameoflife.bat',
    ],
    zip_safe=False,
    install_requires=[
        'pygame'
    ]
)