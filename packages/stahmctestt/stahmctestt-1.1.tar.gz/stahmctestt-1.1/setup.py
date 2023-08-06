from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='stahmctestt',
      version='1.1',
      description='testversion',
      url='https://github.com/RihuiOu95/HMC.git',
      author='Flying Circus',
      author_email='thuizhou@outlook.com',
      license='DUKE',
      packages=['stahmctestt'],
      py_modules = ['stahmctestt.oned', 'stahmctestt.vec'],
      zip_safe=False)
