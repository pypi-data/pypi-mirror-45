from setuptools import setup, find_packages

setup(
    name='simple-gen',
    version='2019.4.22.2',
    description='gen files',
    author='buglan',
    author_email='1831353087@qq.com',
    packages=find_packages(),
    scripts=['gen.py'],
    entry_points={
        'console_scripts': [
            'gen = gen:main',
        ]
    }
)
