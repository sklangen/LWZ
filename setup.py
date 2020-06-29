import setuptools

with open('README.md') as f:
    long_description = f.read()

setuptools.setup(
    name='lwz',
    version='0.0.1',
    author='Schachklub Langen e. V. ',
    author_email='Turnierleiter@sklangen.de',
    description='https://github.com/sklangen/',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/sklangen/lwz/',
    packages=setuptools.find_packages(),
    classifiers=[],
    python_requires='>=3.8',
)
