import setuptools

with open('requirements.txt') as f:
    required = f.read().splitlines()

with open('README.md') as f:
    long_description = f.read()

setuptools.setup(
    name='lwz',
    packages=setuptools.find_packages(),
    install_requires=required,
    version='0.0.1',
    author='Schachklub Langen e. V. ',
    author_email='Turnierleiter@sklangen.de',
    description='CLI-Tool to manage club intern, monthly tournaments.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/sklangen/lwz/',
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Development Status :: 1 - Planning',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Natural Language :: German',
    ],
    python_requires='>=3.8',
    scripts=['bin/lwz'],
    package_data={
       'lwz': ['templates/*.html'],
    },
)
