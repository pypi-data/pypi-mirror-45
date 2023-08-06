from setuptools import setup, find_packages

setup(name='mindconnectiot',
      version='0.1',
      description='Wrapper around the MindConnect IoT Extention.',
      url='https://gitlab.com/Addono/mindconnect-iot-extention-python',
      author='Adriaan Knapen',
      author_email='hi@aknapen.nl',
      license='MIT',
      packages=find_packages(),
      zip_safe=False,
      install_requires=['paho-mqtt'])
