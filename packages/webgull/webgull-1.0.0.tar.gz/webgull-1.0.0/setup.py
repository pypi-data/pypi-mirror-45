from setuptools import setup

setup(name='webgull',
      version='1.0.0',
      license='GPL3',
      packages=[
          'webgull'
      ],
      entry_points = {
          'console_scripts': ['webgull=webgull.main:entry']
      },
      zip_safe=False
)
