from setuptools import find_packages, setup
from ptrait import __version__

setup(name='ptrait',
      version=__version__,
      description='trait',
      long_description='',
      url='https://github.com/xyloon/ptrait',
      author='xyloon',
      author_email='xyloon@gmail.com',
      license='MIT',
      packages=find_packages(),
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      zip_safe=False)
