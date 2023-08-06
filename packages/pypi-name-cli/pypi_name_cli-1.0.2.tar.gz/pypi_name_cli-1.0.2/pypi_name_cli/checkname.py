from pypi_name import pypiName
import sys

def main():
	if (len(sys.argv) == 2):
		if (pypiName(sys.argv[1])):
			print('😊 This name is available to use')
		else:
			print('😞 This name is already taken')
	else:
		print("Usage: pypi <package_name>")
