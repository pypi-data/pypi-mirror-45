from setuptools import setup, find_packages

setup(name='wranglepy',
      version='0.01',
      url='https://github.com/pmugenyi/wranglepy-0.1',
     # license='MIT',
      author='Peter Mugenyi',
     # author_email='the.gigi@gmail.com',
      description='A python package containing some easy-to-use tools for data cleaning / Exploration and ML.',
      #packages=find_packages(exclude=['tests']),
      #long_description=open('README.md').read(),
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
      ],
      zip_safe=False)