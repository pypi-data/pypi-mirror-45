from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='stahmctestt',
      version='1.2',
      description='testversion',
      url='https://github.com/RihuiOu95/HMC.git',
      author='Tianhui',
      author_email='thuizhou@outlook.com',
      license='MIT',
      packages=['one','high'],
      zip_safe=False)
