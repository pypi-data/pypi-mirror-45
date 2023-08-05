#!/usr/bin/python
import os.path
from setuptools import setup

with open("README.md", "r") as handle:
	long_description = handle.read()

setup(
		name='bdflib',
		version='1.1.3',
		description="Library for working with BDF font files.",
		long_description=long_description,
		long_description_content_type="text/markdown",
		author="Timothy Allen",
		author_email="screwtape@froup.com",
		url='https://gitlab.com/Screwtapello/bdflib/',
		packages=['bdflib', 'bdflib.test'],
		entry_points={
			'console_scripts': [
				"bdflib-embolden = bdflib.tools:embolden",
				"bdflib-fill = bdflib.tools:fill",
				"bdflib-merge = bdflib.tools:merge",
				"bdflib-passthrough = bdflib.tools:passthrough",
			]
		}
	)
