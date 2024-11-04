from setuptools import setup, find_packages

setup(
    name='flytrap_flask',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
      'Flask',
      'requests',
    ],
    python_requires='>=3.6'
)