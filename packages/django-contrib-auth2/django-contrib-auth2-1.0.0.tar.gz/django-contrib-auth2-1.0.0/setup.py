from setuptools import setup, find_packages

setup(
    name='django-contrib-auth2',
    version='1.0.0',
    url='https://github.com/mixkorshun/django-contrib-auth2',

    author='Vladislav Bakin',
    author_email='vladislav@bakin.me',
    maintainer='Vladislav Bakin',
    maintainer_email='vladislav@bakin.me',

    license='MIT',

    install_requires=[
        'django>=2.0',
        'requests',
    ],

    packages=find_packages(exclude=['tests.*', 'tests']),

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
