#!/usr/bin/env python
"""TIQS: Translational Invariant Quantum Solver

TIQS is an open-source Python solver to study the exact Lindbladian dynamics of open quantum systems on translationally invariant lattices. 
It implements Linbladian diagonalisation, master equaiton resolution, and quantum trajectories. 
"""
from setuptools import setup


DOCLINES = __doc__.split('\n')


DESCRIPTION = DOCLINES[0]
LONG_DESCRIPTION = "\n".join(DOCLINES[2:])



setup(name='tiqs',
      version='0.1.1',
      url='https://github.com/fminga/tiqs',
      author='Fabrizio Minganti, Nathan Shammah',
      license='BSD 3 New',
      packages = ['tiqs'],
      description = DESCRIPTION,
      long_description = LONG_DESCRIPTION,
     )