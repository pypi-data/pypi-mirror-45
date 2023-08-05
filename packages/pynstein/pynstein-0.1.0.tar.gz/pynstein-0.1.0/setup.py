from setuptools import setup

setup(name='pynstein',
      version='0.1.0',
      description='Basic functions for doing Special Relativity in Python',
      url='https://github.com/jbredall/pynstein',
      author='John Bredall',
      author_email='jbredall@hawaii.edu',
      packages=['pynstein'],
      install_requires=[
          'numpy',
          'astropy',
      ],
      license='MIT',
      zip_safe=False,
      classifiers=('Development Status :: 1 - Planning',
                   'Intended Audience :: Science/Research',
                   'License :: OSI Approved :: MIT License',
                   'Natural Language :: English',
                   'Programming Language :: Python :: 3.6',
                   'Topic :: Scientific/Engineering :: Physics',
                   )
      )
