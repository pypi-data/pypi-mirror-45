from setuptools import setup, find_packages

setup(
    name='simple-gen',
    version='2019.4.22.1',
    description='gen files',
    author='buglan',
    author_email='1831353087@qq.com',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'gen = gen:main',
        ]
    },
    scripts=['gen.py']
)
