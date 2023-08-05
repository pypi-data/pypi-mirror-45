from setuptools import setup, find_packages


def readfile(name):
    with open(name) as f:
        return f.read()


readme = readfile('README.rst')
changes = readfile('CHANGES.rst')

requires = [
    'pyramid',
    'wired >= 0.2',  # container.register_singleton
    'zope.interface',
]

tests_require = requires + ['pytest', 'pytest-cov', 'webtest']

setup(
    name='pyramid_services',
    version='2.2',
    description='A service layer abstraction for the Pyramid Web Framework.',
    long_description=readme + '\n\n' + changes,
    # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Pyramid',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    keywords=','.join(
        ['pyramid', 'services', 'service layer', 'ioc container']
    ),
    author='Michael Merickel',
    author_email='pylons-discuss@googlegroups.com',
    url='https://github.com/mmerickel/pyramid_services',
    license='MIT',
    packages=find_packages('src', exclude=['tests']),
    package_dir={'': 'src'},
    include_package_data=True,
    python_requires='>=3.3',
    zip_safe=False,
    install_requires=requires,
    extras_require={'testing': tests_require},
    tests_require=tests_require,
    test_suite='pyramid_services',
    entry_points={},
)
