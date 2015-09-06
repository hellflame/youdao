__author__ = 'hellflame'

from setuptools import setup, find_packages

setup(
    name='Youdao',
    version="1.0",
    keywords=('Youdao', 'youdao', 'dict', 'youdao api'),
    description="simply deploy youdao web api , translate the words you don't know, specially for console users",
    license='MIT License',
    author='hellflame',
    author_email='hellflamedly@gmail.com',
    url="https://github.com/hellflame/youdao",
    packages=find_packages(),
    platforms="linux, mac os",
    entry_points={
        'console_scripts': [
            'youdao_test=youdao.youdao:main'
        ]
    }
)


