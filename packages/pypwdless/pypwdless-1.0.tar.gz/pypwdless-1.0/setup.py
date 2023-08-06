from setuptools import setup

setup(name='pypwdless',
      version='1.0',
      description='Password less authentication in Python',
      url='https://github.com/narayan8291/pypwdless',
      author='Narayan Gowraj',
      author_email='gowrajn@gmail.com',
      license='MIT',
      packages=['pypwdless'],
      install_requires=[
          'PyJWT',
      ],
      zip_safe=False)