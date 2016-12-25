# coding=utf8
from setuptools import setup, find_packages
__author__ = 'hellflame'


setup(
    name='YoudaoDict',
    version="3.2.0",
    keywords=('Youdao', 'youdao', 'dict', 'youdao api', 'partly offset dict'),
    description="终端通过有道api查询单词或者翻译词句",
    license='MIT',
    author='hellflame',
    author_email='hellflamedly@gmail.com',
    url="https://github.com/hellflame/youdao",
    packages=find_packages(),
    platforms="UNIX like",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        "Environment :: Console",
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX'
    ],
    entry_points={
        'console_scripts': [
            'youdao=youdao.run:main'
        ]
    }
)


