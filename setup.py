from setuptools import setup, find_packages

setup(name='kampuan',
      version='0.0.1',
      description='Thai language tricks',
      long_description=open('README.md').read().strip(),
      author='Tanawat Chiewhawan',
      author_email='poom_tanawat@hotmail.com',
      url='',
      package_dir={'': 'src'},
      packages=find_packages('src'),
      package_data={"kampuan": ["py.typed"]},
      py_modules=['kampuan'],
      install_requires=[
          "numpy",
          "pandas",
          "pythainlp"
      ],
      extras_require={
          'dev': [
              'ipykernel',
              'mypy',
              'autopep8'
          ],
          'test': [
              'pytest',
              'pytest-xdist',
              "pytest-cov",
              "pytest-mypy"
          ]
      },
      license='Private',
      zip_safe=False,
      keywords='',
      classifiers=[''])
