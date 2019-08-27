from setuptools import setup

from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='yamconv',
    version='0.1.2',
    description='yamconv converts the file formats of machine learning datasets',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    keywords='machine learning',
    url='https://github.com/yam-ai/yamconv',
    author='Thomas Lee',
    author_email='thomaslee@yam.ai',
    pymodule='yamconv',
    include_page_data=True,
    zip_safe=True
)
