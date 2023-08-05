import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='shopify-converter',
    version='1.2.2',
    author='UPINUS',
    author_email='dev@upinus.com',
    description='A tool which converts Shopify data to Upinus data.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://git.upinus.com/upinus/shopify-api-converter.git',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
