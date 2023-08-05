from setuptools import setup

setup(name='model21cm',
      version='0.3',
      description='Infer parameters of a 21cm cosmology model.',
      url='http://github.com/phys201/model21cm',
      author='I. Davenport, N. DePorzio',
      author_email='iandavenport@g.harvard.edu, nicholasdeporzio@g.harvard.edu',
      license='GNU GPL-3.0',
      packages=['model21cm'],
      install_requires = ['numpy','pandas','matplotlib.pyplot','os'],
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose'], 
      include_package_data=False)
