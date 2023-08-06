from distutils.core import setup
from setuptools import find_packages

setup(
  name = 'theama',
  packages = find_packages(),
  version = '0.0.7',
  license='apache-2.0',
  description = 'Simple interface to common computer vision algorithms.',
  author = 'David Torpey',
  author_email = 'torpey.david93@gmail.com',
  url = 'https://github.com/DavidTorpey/theama',
  download_url = 'https://github.com/DavidTorpey/theama/archive/0.0.7.tar.gz',
  keywords = ['bag-of-words', 'vlad', 'computer vision'],
  install_requires=[
          'scikit-learn',
          'numpy',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)