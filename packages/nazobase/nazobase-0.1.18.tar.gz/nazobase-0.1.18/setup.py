#############################################
# File Name: setup.py
# Author: WEN
# Created Time:  2019-05-05 23:29:00
#############################################

from setuptools import setup

setup(
    name            ='nazobase',
    version         ='0.1.18',
    py_modules      =['nazobase'],
    author          = 'WEN',
    license         = "LGPLv3",
    description     = "NAZOrip's basement",
    url             = "https://www.nazorip.site",
    # install_requires=[
    #     '',
    # ],
    entry_points='''
        [console_scripts]
        nazobase=nazobase:nazobase
    ''',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)