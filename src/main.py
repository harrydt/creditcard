import shelve
import argparse
import csv
from processor import Processor

# Set argument
parser = argparse.ArgumentParser()
parser.add_argument("input_file", help="the path of input file")
args = parser.parse_args()

commands = []
# Read input file
with open(args.input_file, 'r') as f:
    reader = csv.reader(f, delimiter=' ')
    for row in reader:
        commands.append(row)

# Since input file could include multiple operations on one account,
# writeback is set to True to allow persistent operations.
accounts = shelve.open(filename='accounts', flag='c', writeback=True)

processor = Processor(accounts)
summary = processor.process(commands)

# Sync and close shelve
accounts.close()    

# Print output
print(summary)
