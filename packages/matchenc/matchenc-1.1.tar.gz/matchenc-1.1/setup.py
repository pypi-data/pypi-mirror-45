from setuptools import setup, find_packages


# read the contents of your README file
from os import path
with open('README.md', 'r') as f:
    long_description = f.read()

setup(name='matchenc',
      version='1.1',
      description='Checks which standard encoding can open the given file, and if contains the expected terms are encoded as such.',
      long_description=long_description,
      long_description_content_type='text/x-rst',
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Information Analysis',
      ],
      keywords='Standard Encoding Decoding',
      url='https://github.com/gythaogg/matchenc',
      author='Gytha Ogg',
      author_email='gythaoggscat@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'markdown',
      ],
      include_package_data=True,
      zip_safe=False)
