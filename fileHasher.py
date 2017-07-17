#!/usr/bin/python

import csv
import hashlib
import os
import argparse
import progressbar
import time

def file_hash_hex(file_path, hash_func):
    with open(file_path, 'rb') as f:
        return hash_func(f.read()).hexdigest()

def recursive_file_listing(base_dir):
    for directory, subdirs, files in os.walk(base_dir):
        for filename in files:
            yield directory, filename, os.path.join(directory, filename)


if __name__ == '__main__':
	# src_dir = '/Volumes/Archive/Pictures'
	args = argparse.ArgumentParser()
	args.add_argument("-i", "--inputDir", required=True, help="The directory to hash files from.")
	args.add_argument("-o", "--output", required=True, help="The directory to hash files from.")
	args = args.parse_args()

	with open(args.output, 'w') as f:
		# Count the number of files
		numFiles = len([name for name in os.listdir(args.inputDir) if os.path.isfile(os.path.join(args.inputDir, name))])
		count = 0
		bar = progressbar.ProgressBar(max_value=numFiles)

		writer = csv.writer(f, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		for directory, filename, path in recursive_file_listing(args.inputDir):
			writer.writerow((directory, filename, file_hash_hex(path, hashlib.md5)))
			count += 1
			bar.update(count)