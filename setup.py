# coding=utf8
from setuptools import setup
__author__ = 'hellflame'


setup(
    name='YoudaoDict',
    version="2.0.2",
    keywords=('Youdao', 'youdao', 'dict', 'youdao api'),
    description="适用于在linux or mac 终端通过有道api查询单词或者翻译词句",
    license='MIT',
    author='hellflame',
    author_email='hellflamedly@gmail.com',
    url="https://github.com/hellflame/youdao",
    packages=[
        'youdao'
    ],
    install_requires=[
        'instantDB>=0.0.8'
    ],
    platforms="linux, mac os",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        "Environment :: Console",
        "Operating System :: MacOS",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux"
    ],
    entry_points={
        'console_scripts': [
            'youdao=youdao.youdao:main'
        ]
    }
)


