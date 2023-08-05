from setuptools import setup
# read the contents of README file
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='cwlbrowser',
      version='5.0',
      description='Python library that browses and analyses workflows in CWL',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://gitlab.cs.man.ac.uk/mbaxasp7/cwlbrowser',
      author='Sean Pertet',
      author_email='sean.pertet@student.manchester.ac.uk',
      packages=['cwlbrowser'],
      install_requires=[
          'pyyaml',
          'requests',
          'cwlref-runner',
          'IPython'
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      include_package_data=True,
      zip_safe=False,
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
      ],)
      