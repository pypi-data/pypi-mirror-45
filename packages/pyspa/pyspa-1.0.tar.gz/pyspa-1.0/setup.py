import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pyspa',
    version='1.0',
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy',
        'pandas'
    ],
    url='https://github.com/hybridlca/pyspa',
    license='GNU General Public License v3.0',
    author='André Stephan & Paul-Antoine Bontinck',
    author_email='stephan.andre@gmail.com',
    description='An object-oriented python package for structural path analysis',
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_data={
    'template_input_files':['*.csv']
    }
)
