from setuptools import setup

requires = [
    "flake8 > 3.0.0",
]


def get_version(fname='flake8_mock.py'):
    with open(fname) as f:
        for line in f:
            if line.startswith('__version__'):
                return eval(line.split('=')[-1])


def get_long_description():
    descr = []
    for fname in ('README.rst',):
        with open(fname) as f:
            descr.append(f.read())
    return '\n\n'.join(descr)


setup(
    name='verve-flake8-mock',
    version=get_version(),
    description="Provides checking for non-existent mock methods and properties",
    long_description=get_long_description(),
    keywords=['flake8', 'mock', 'testing'],
    author='Anna Warzecha',
    author_email='anna.warzecha@gmail.com',
    url='https://github.com/aniav/flake8-mock',
    license='GNU',
    py_modules=['flake8_mock'],
    install_requires=requires,
    setup_requires=['pytest-runner'],
    tests_require=[
        'pytest==4.0.1',
        'pytest-flake8dir==1.3.0'
    ],
    test_suite="tests",
    python_requires='>=3.0',
    zip_safe=False,
    entry_points={
        'flake8.extension': [
            'M2 = flake8_mock:MockChecker',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Quality Assurance',
    ],
)
