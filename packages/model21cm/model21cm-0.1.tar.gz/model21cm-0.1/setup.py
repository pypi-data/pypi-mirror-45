from setuptools import setup

setup(name='model21cm',
      version='0.1',
      description='Infer parameters of a 21cm cosmology model.',
      url='http://github.com/phys201/model21cm',
      author='I. Davenport, N. DePorzio',
      author_email='iandavenport@g.harvard.edu, nicholasdeporzio@g.harvard.edu',
      license='GNU GPL-3.0',
      packages=['model21cm'],
      install_requires = ['numpy'],
      zip_safe=False)
