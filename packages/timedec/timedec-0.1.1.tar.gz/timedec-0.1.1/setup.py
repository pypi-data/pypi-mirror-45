from distutils.core import setup
setup(
  name = 'timedec',
  packages = ['timedec'],
  version = '0.1.1',
  license='MIT',
  description = 'Simple decorator for measuring execution time of a function.',
  author = 'Bohdan Dubas',
  author_email = 'bogdan.dubas@gmail.com',
  url = 'https://github.com/BDubas',
  download_url = 'https://github.com/BDubas/timedec/archive/v_0.1.1.tar.gz',
  keywords = ['timeit', 'timer', 'profiling', 'decorator'],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: System :: Benchmark',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.6',
  ],
)
