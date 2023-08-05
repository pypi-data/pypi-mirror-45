from setuptools import setup, find_packages


setup(
    name='lammps_tools',
    version='1.0.8',
    author='Roy-Kid',
    author_email='lijichen365@126.com',
    packages=find_packages(),
    #scripts=['bin/stowe-towels.py','bin/wash-towels.py'],
    url='https://github.com/Roy-Kid/lammps-tools',
    license='LICENSE',
    description='lammps data process tools.',
    long_description=open('README').read(),
    python_requires='>=3',
    #install_requires=[    ],

)
