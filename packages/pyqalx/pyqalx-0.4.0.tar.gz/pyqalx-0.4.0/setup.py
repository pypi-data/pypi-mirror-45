import os

from setuptools import setup


with open('README.rst', 'r') as f:
    readme = f.read()

about = {}
here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'pyqalx', '__version__.py'), 'r') as f:
    exec(f.read(), about)

setup(name='pyqalx',
      version=about['__version__'],
      description='High-level interfaces to the qalx API',
      long_description=readme,
      classifiers=[
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Development Status :: 4 - Beta',
          'Intended Audience :: Manufacturing',
          'Intended Audience :: Science/Research',
          'Intended Audience :: Telecommunications Industry',
          'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
          'Natural Language :: English',
          'Operating System :: OS Independent'
      ],
      url='https://docs.qalx.io',
      keywords='qalx engineering simulation',
      author='AgileTek Engineering',
      author_email='',
      license='GNU',
      packages=['pyqalx', 'pyqalx.core', 'pyqalx.config', 'pyqalx.config.defaults',
                'pyqalx.core.entities', 'pyqalx.bot','pyqalx.transport',
                'tests', 'tests.unittests'],
      install_requires=['requests', 'boto3', 'dill'],
      setup_requires=["pytest-runner", ],
      tests_require=['pytest', 'pytest-mock'],
      include_package_data=True,
      zip_safe=False)
