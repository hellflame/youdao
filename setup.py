# coding=utf8
from setuptools import setup, find_packages
__author__ = 'hellflame'


setup(
    name='YoudaoDict',
    version="4.0.6",
    keywords=('youdao', 'dict', 'partly offline dict', 'web spider'),
    description="通过有道爬虫查询单词",
    license='MIT',
    author='hellflame',
    author_email='hellflamedly@gmail.com',
    url="https://github.com/hellflame/youdao",
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4',
        'requests',
        'gevent'
    ],
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
            'youdao=youdao.run:main',
            'service.youdao=youdao.service.run:main'
        ]
    }
)


