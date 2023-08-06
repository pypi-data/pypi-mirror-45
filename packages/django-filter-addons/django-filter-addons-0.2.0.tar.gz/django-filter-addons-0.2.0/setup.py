from setuptools import find_packages, setup

__all__ = ()

with open('README.md') as readme:
    _README = readme.read()

setup(
    name='django-filter-addons',
    version='0.2.0',
    description='A collection of addons for django-filter',
    long_description=_README,
    long_description_content_type='text/markdown',
    author='Xavier Dutreilh',
    author_email='xavier@dutreilh.com',
    maintainer='Xavier Dutreilh',
    maintainer_email='xavier@dutreilh.com',
    url='https://github.com/xavierdutreilh/django-filter-addons',
    packages=find_packages(exclude=('tests',)),
    include_package_data=True,
    license='MIT',
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ),
    python_requires='>=3.5',
    install_requires=(
        'django-filter>=2.0',
    ),
)
