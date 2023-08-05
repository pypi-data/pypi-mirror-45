from distutils.core import setup
import os

setup(
    name="commentSql",
    version="0.1",
    author="chenminhua",
    author_email="chenmhgo@gmail.com",
    license="GPL3",
    description="generate add comment sql",
    url="https://github.com/chenminhua/commentSql",
    packages=[

    ],
    scripts=['bin/commentSql'],
    install_requires=[
        'pymysql'
    ]
)
