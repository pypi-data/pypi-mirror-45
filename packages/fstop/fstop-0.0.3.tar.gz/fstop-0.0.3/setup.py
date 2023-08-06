import setuptools


with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='fstop',
    version='0.0.3',
    author='Noel Kaczmarek',
    author_email='noel.kaczmarek@gmail.com',
    description='The f-stop Engine',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/NoelKaczmarek/fstop',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
