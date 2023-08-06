import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(name='mindconnectiot',
      version='0.1.2',
      description='Wrapper around the MindConnect IoT Extention.',
	  long_description=README,
	  long_description_content_type="text/markdown",
      url='https://gitlab.com/Addono/mindconnect-iot-extention-python',
      author='Adriaan Knapen',
      author_email='hi@aknapen.nl',
      license='MIT',
      packages=find_packages(),
      zip_safe=False,
      install_requires=['paho-mqtt'])
