# coding=utf8
__author__ = 'hellflame'

from setuptools import setup, find_packages

setup(
    name='YoudaoDict',
    version="1.1.2",
    keywords=('Youdao', 'youdao', 'dict', 'youdao api'),
    description="适用于在linux or mac 终端通过有道api查询单词或者翻译词句",
    license='MIT License',
    author='hellflame',
    author_email='hellflamedly@gmail.com',
    url="https://github.com/hellflame/youdao",
    packages=find_packages(),
    platforms="linux, mac os",
    entry_points={
        'console_scripts': [
            'youdao=youdao.youdao:main'
        ]
    }
)


