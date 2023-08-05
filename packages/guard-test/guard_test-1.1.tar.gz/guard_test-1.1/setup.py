import setuptools

setuptools.setup(
    name="guard_test",
    version="1.1",
    author="hy",
    description="a androguard test",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'androguard_test = guardtest.cli.entry_points:entry_point'
        ]
    }
)
