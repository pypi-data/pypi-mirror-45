from setuptools import setup

setup(name='plotly_charts',
      version='0.3',
      description='Helper functions for plotly charts',
      url='http://github.com/walkerlangley/plotly-charts#v0.3',
      author='Walker Langley',
      author_email='flyingcircus@example.com',
      license='MIT',
      packages=['plotly_charts'],
      install_requires=[
          'plotly',
          'pandas',
          'datetime',
          'cufflinks',
          'json',
          'numpy',
      ],
      zip_safe=False)
