
#!/usr/bin/env python
"""
Copyright (c) 2019 Joshua W.
"""


version = '0.0.1a'

from setuptools import setup
setup(name='nsurl',
      install_requires=["ezurl==0.1.3.25"],
      version=version,
      description='Nationstates API URL generator',
      author='Joshua W',
      author_email='DolphDevgithub@gmail.com',
      keywords=["nationstates URL Generator"],
      packages=["nsurl"],
      classifiers=["License :: OSI Approved :: MIT License",
                   "Operating System :: OS Independent",
                   "Topic :: Utilities",
                   "Programming Language :: Python :: 3.2",
                   "Programming Language :: Python :: 3.3",
                   "Programming Language :: Python :: 3.4",
                   "Programming Language :: Python :: 3.5",
                   "Programming Language :: Python :: 3.6"]
                    )
