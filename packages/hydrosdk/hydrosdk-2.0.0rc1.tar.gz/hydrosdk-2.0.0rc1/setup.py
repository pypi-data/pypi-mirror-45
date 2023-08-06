from setuptools import setup, find_packages

with open("version", 'r') as v:
    version = v.read().strip()

setup(
    name='hydrosdk',
    version=version,
    description="Hydro-serving SDK",
    author="Bulat Lutfullin",
    license="Apache 2.0",
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=["hs~=2.0.4"],
    setup_requires=[
        'pytest-runner'
    ],
    test_suite='tests',
    tests_require=[
        'pytest>=3.8.0', 'requests_mock>=1.5.0', 'mock>=2.0.0'
    ]
)
