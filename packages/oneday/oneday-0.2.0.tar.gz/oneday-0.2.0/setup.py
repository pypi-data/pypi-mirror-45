from setuptools import find_packages
from setuptools import setup

setup(
    name='oneday',
    version='0.2.0',
    author='Yixian Du',
    author_email='duyixian1234@qq.com',
    classifiers=[
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description='A Python DI/component project',
    long_description=open('README.rst').read(),
    install_requires=[],
    license='BSD License',
    packages=find_packages(),
    url='https://github.com/duyixian1234/oneday',
)
