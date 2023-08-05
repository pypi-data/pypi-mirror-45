from setuptools import setup

setup(name='learnfuntest',
      version='0.1',
      description='The funniest joke in the world to beginner',
      url='http://github.com/storborg/funniest',
      author='Flying Circus',
      author_email='flyingcircus@example.com',
      license='MIT',
      packages=['learnfuntest'],
      install_requires=[
          'markdown',
          ],
      zip_safe=False)
