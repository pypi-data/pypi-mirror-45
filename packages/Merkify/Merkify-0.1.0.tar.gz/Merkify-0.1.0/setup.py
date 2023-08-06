from distutils.core import setup
import setuptools

setup(
  name = 'Merkify',
  version = '0.1.0',
  license='MIT',
  description = 'Simple Merkle Tree implementation',
  author = 'Bani Singh',
  author_email = 'banihns@gmail.com',
  url = 'https://github.com/user/reponame',
  download_url = 'https://github.com/banisingh/Merkify/archive/0.1.0.tar.gz',
  keywords = ['merkletree', 'bitcoin', 'binarytree'],
  packages = setuptools.find_packages(),
  install_requires=[],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)
