from setuptools import setup
setup(
  name='opportunistikapacity',
  packages=['opportunistikapacity'],
  version='0.0.1',
  license='MIT',
  description='A simple library to compute the contact capacity in mobility/contact traces',
  author='Clement Bertier',
  author_email='clement.bertier@lip6.fr',
  url='https://github.com/Bertier/OpportunistiKapacity',
  download_url='https://github.com/Bertier/OpportunistiKapacity/archive/v0.0.1.tar.gz',
  keywords=['CONTACT', 'OPPORTUNISTIC', 'CAPACITY', 'MOBILITY', 'DATA', 'TRACE', 'VANET', 'MANET'],
  install_requires=[            # I get to this in a second
          'numpy',
          'scipy',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Science/Research',
    'Topic :: Scientific/Engineering',

    'License :: OSI Approved :: MIT License',

    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
