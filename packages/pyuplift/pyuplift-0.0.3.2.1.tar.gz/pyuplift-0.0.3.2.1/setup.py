import os
from setuptools import setup, find_packages

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


def get_long_description():
    with open(os.path.join(__location__, 'README.MD'), encoding='utf8') as f:
        text = f.read()
    return text


setup(
    name='pyuplift',
    version='0.0.3.2.1',
    author='Artem Kuchumov',
    author_email='kuchumov7@gmail.com',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    url='https://github.com/duketemon/pyuplift',
    license='MIT License',
    description='Uplift modeling implementation',
    keywords=['uplift modeling', 'machine learning', 'true-response-modeling', 'incremental-value-marketing'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=["pandas>=0.23.4", "scikit-learn>=0.20.0"],
    classifiers=[
        'Intended Audience :: Science/Research',
        'Intended Audience :: Education',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
