from setuptools import setup, find_packages

setup(
	name="minilogger",
	version="1.0.2",
	packages=find_packages(), # permet de récupérer tout les fichiers 
	description="Mini pretty logger for Python3",
	author="Nofix",
	author_email="contact@no-fix.fr",
	license="MIT",
	python_requires=">=3.3"
	)
