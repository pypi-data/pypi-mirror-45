from setuptools import setup

setup(name='isovectpy',
      version='1.3',
      description='A efficient and accurate simulator for isotope pattern in mass spectrometry',
      url='http://github.com/isovectpy',
      author='Felix Wang',
      author_email='felixwang08@hotmail.com',
      license='MIT',
      packages=['isovectpy'],
      include_package_data=True,
      install_requires=[
          'numpy',
          'matplotlib',
      ],
      zip_safe=False)
