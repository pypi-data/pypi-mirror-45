from setuptools import setup

setup(name='code2read',
      version='0.2.1.2',
      description='Converts your code with comments into a workable README.md: Code more. Write less.',
      url='https://github.com/SubhadityaMukherjee/code_to_readme',
      author='Subhaditya Mukherjee',
      author_email='mukherjeesubhaditya001@gmail.com',
      license='MIT',
      packages=['code2read'],
      entry_points={
          'console_scripts': [
              'code2read = code2read.__main__:main'
          ]
      },
      zip_safe=False)
