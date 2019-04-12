#!/usr/bin/env python

# Read distance matrix
# Read arg X - average dist cutoff
# Read arg Y - median dist cutoff
# Read arg Z - Higher than Z std.dev

import csv, argparse, statistics
#from statistics import median, mean, stdev

__version__ = '0.1b'

parser = argparse.ArgumentParser(description='dist-outlier - identify distance outliers')
parser.add_argument("-v", "--version", help="Installed version", action="version", version="%(prog)s " + str(__version__))
parser.add_argument("-d", "--dist", help="Identify all items with an average distance to other items d or higher", type=int, dest="dist", default=float('Inf'))
parser.add_argument("-m", "--median", help="Instead of average distance, use the median", default=False, action="store_true")
parser.add_argument("-s", "--stddev", dest="stddev", type=float, help="Identify items that have distance to others more than X standard deviations higher than the rest",default=0.0)
parser.add_argument("--delimiter", help="Cell separator in input file (Default comma ',')",default=",")
parser.add_argument("file", help="CSV file of distances")
args = parser.parse_args()

with open(args.file,"rU") as myfile:
	reader = csv.reader(myfile,delimiter=args.delimiter)
	header = next(reader)
	dists = {}
	for line in reader:
		dists[line[0]] = [int(i) for i in line[1:]]
		dists[line[0]].sort()

	# Return results
	Results = []
	meandistlist = {}
	if args.median:
		mean = statistics.median
		#statistics.mean = statistics.median
	else:
		mean = statistics.mean
	
	for item in dists:
		meandist = mean(dists[item])
		meandistlist[item] = meandist
		if meandist >= args.dist:
			print("Isolate %s \t Distance: %s" % (item,meandist))
			Results.append(item)

	if not args.stddev == 0.0:
		average_average = statistics.mean(meandistlist.values())
		average_stdev = statistics.stdev(meandistlist.values())
		threshold = average_average + args.stddev * average_stdev
		Results = []
		for item in meandistlist:
			if meandistlist[item] >= threshold:
				Results.append(item)

	# Write results
	print(Results)








