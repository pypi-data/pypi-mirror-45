from setuptools import setup


def readme():
    with open('README.md', 'r') as w:
        return w.read()


setup(name='filestat',
      version='0.1',
      description='A command line library for file monitoring',
      long_description=readme(),
      url='https://github.com/zxalif/filestat.git',
      author='Alif Jahan',
      keywords='filestat stats file monitoring details',
      author_email='sajeeb162537@gmail.com',
      license='MIT',
      packages=['filestat'],
      include_package_data=True,
      zip_safe=False)