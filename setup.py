# -----------------------------------------------------------------------------
# imports
# -----------------------------------------------------------------------------
from setuptools import setup, find_packages
# -----------------------------------------------------------------------------
# helpers
# -----------------------------------------------------------------------------
with open("README.md", "r") as fh:
    long_description = fh.read()
# -----------------------------------------------------------------------------
# setup
# -----------------------------------------------------------------------------
setup(
    name='toolsar',  
    version='0.5',
    author="Luis Monteiro",
    author_email="monteiro.lcm@gmail.com",
    description="ToolSar",
    long_description=long_description,
    url="",
    packages=[
        'toolsar'
    ],
    install_requires=[
        'boltons',
        'flask',
        'colorlog'
    ],
	entry_points={
	  'console_scripts': [
		  'toolsar   = toolsar.__main__:main'
	  ]
	}
 )
 # ----------------------------------------------------------------------------
 # end
 # ----------------------------------------------------------------------------
