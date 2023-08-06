import os.path
from setuptools import setup, find_packages

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

setup(
      name='mindconnectiot',
      version='0.1.7',
      description='Wrapper around the MindConnect IoT Extention.',
	  long_description=README,
	  long_description_content_type='text/markdown',
      url='https://gitlab.com/Addono/mindconnect-iot-extension-python',
      author='Adriaan Knapen',
      author_email='hi@aknapen.nl',
      license='MIT',
      packages=find_packages(),
	  include_package_data=True,
	  classifiers=[
          "License :: OSI Approved :: MIT License",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.7",
      ],
      zip_safe=False,
      install_requires=['paho-mqtt'])
