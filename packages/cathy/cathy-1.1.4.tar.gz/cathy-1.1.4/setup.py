from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='cathy',
    version='1.1.4',
    description='Discord chat bot using AIML artificial intelligence.',
    long_description=open('README.rst').read(),
    url='https://github.com/DevDungeon/ChattyCathy',
    author='DevDungeon',
    author_email='nanodano@devdungeon.com',
    license='GPL-3.0',
    packages=['cathy'],
    scripts=[
        'bin/cathy',
        'bin/cathy.bat',
    ],
    package_data={
        'cathy': [
            'std-startup.xml',
            'aiml/alice/*.aiml',
            'aiml/custom/*.aiml'
        ],
    },
    zip_safe=False,
    install_requires=requirements,
    python_requires='<3.7',
)
