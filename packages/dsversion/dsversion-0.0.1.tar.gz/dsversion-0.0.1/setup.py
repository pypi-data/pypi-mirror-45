from setuptools import setup, find_packages

package_name = 'dsversion'

with open('README.md', 'rt') as fh:
    long_description = fh.read()

setup(name=package_name,
      version='0.0.1',
      description='Helper for defining package version strings.',
      author='YvesPy',
      author_email='grazhopper+pypi@gmail.com',
      packages=find_packages('.'),
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='',
      python_requires='>=3',
      install_requires=[],
      extras_require={},
      license='MIT',
      classifiers=[
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Build Tools',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
      ],
      keywords='version versioning',
      )
