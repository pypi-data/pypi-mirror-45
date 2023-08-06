import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='pyvacy',
    version='0.0.31',
    author='Chris Waites',
    author_email='cwaites10@gmail.com',
    description='Privacy preserving deep learning for PyTorch',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='http://github.com/ChrisWaites/pyvacy',
    packages=setuptools.find_packages(),
)
