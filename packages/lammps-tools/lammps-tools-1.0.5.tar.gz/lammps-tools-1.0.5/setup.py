from setuptools import setup, find_packages

setup(
    name='lammps-tools',
    version='1.0.5',
    author='Roy-Kid',
    author_email='lijichen365@126.com',
    #packages=['data-processing', 'model-builder','test'],
    #scripts=['bin/stowe-towels.py','bin/wash-towels.py'],
    url='https://github.com/Roy-Kid/lammps-tools',
    license='LICENSE',
    description='lammps data process tools.',
    long_description=open('README').read(),
    python_requires='>=3',
    #install_requires=[    ],
    packages=find_packages()
)
