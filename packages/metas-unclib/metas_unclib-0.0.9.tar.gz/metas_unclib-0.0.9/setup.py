import setuptools


with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="metas_unclib",
	version="0.0.9",
	author="Michael Wollensack",
	author_email="michael.wollensack@metas.ch",
	description="An advanced measurement uncertainty calculator",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://www.metas.ch/unclib",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3.6",
		"License :: Other/Proprietary License",
		"Operating System :: OS Independent",
	],
	#install_requires=[
	#	'numpy',
	#	'scipy',
	#	'matplotlib',
	#	'pythonnet',
	#],
	include_package_data=True,
	zip_safe=False
)

