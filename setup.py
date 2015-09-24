# coding=utf8
__author__ = 'hellflame'

from setuptools import setup, find_packages

setup(
    name='YoudaoDict',
    version="1.1.5.1",
    keywords=('Youdao', 'youdao', 'dict', 'youdao api'),
    description="适用于在linux or mac 终端通过有道api查询单词或者翻译词句",
    license='MIT',
    author='hellflame',
    author_email='hellflamedly@gmail.com',
    url="https://github.com/hellflame/youdao",
    packages=find_packages(),
    platforms="linux, mac os",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7'
    ],
    entry_points={
        'console_scripts': [
            'youdao=youdao.youdao:main'
        ]
    }
)


