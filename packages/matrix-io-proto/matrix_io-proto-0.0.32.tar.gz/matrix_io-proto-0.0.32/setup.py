""" Setup module for MATRIX Labs protos

See:
https://github.com/matrix-io/protocol-buffers
"""
from setuptools import setup, find_packages

install_requires = [
  'protobuf>=3.6.0',
]

extras_require = {
  'grpc': ['grpcio>=1.12.0']
}

setup(
  name='matrix_io-proto',
  version='0.0.32',
  author='MATRIX Labs',
  author_email='devel@matrixlabs.ai',
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
  description='Protobufs used MATRIX ecosystem',
  long_description='Protobuf message definition for MATRIX Labs boards and services',
  install_requires=install_requires,
  extras_require=extras_require,
  license='GPLv3',
  namespace_packages=[
    'matrix_io',
  ],
  packages=find_packages(),
  url='https://github.com/matrix-io/protocol-buffers'
)
