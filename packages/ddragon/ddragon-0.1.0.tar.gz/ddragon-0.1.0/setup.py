from setuptools import setup, find_packages
setup(
  name = 'ddragon',
  packages = find_packages(),
  version = '0.1.0',
  description = 'Host your own ddragon mirror for League of Legends static data and images, relying on dragontail',
  author = 'Canisback',
  author_email = 'canisback@gmail.com',
  url = 'https://github.com/Canisback/ddragon',
  keywords = ['python', 'ddragon'],
  classifiers = [],
  install_requires=[
    "requests"
  ],
  extras_require={
      "image_resize":[
        "pillow",
        "python-resize-image"
      ]
  }
)
