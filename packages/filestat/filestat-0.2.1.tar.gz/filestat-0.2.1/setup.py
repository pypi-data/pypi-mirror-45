from setuptools import setup


def readme():
    with open('README.rst', 'r') as w:
        return w.read()


setup(name='filestat',
      version='0.2.1',
      description='A command line library for file monitoring',
      long_description=readme(),
      url='https://github.com/zxalif/filestat/',
      author='Alif Jahan',
      keywords='filestat stats file monitoring details',
      author_email='sajeeb162537@gmail.com',
      license='MIT',
      packages=['filestat'],
      include_package_data=True,
      zip_safe=False)
