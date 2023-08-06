import os
import sys
import datetime
import argparse
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from pageplanner.api import get_document
from pageplanner.api import get_documents

# Set up command line arguments.
parser = argparse.ArgumentParser()
parser.add_argument('urls', type=str, help='Comma delimited list of URLs to scrape.')
parser.add_argument('focus', type=str, help='Focus keyword.')
parser.add_argument('-r', '--ranks', type=str, help='Comma delimited list of ranks for the URLs.')
parser.add_argument('-v', '--variants', type=str, help='Comma delimited list of variant keywords.')
parser.add_argument('-o', '--output', type=str, help='Path to output JSON file.')
args = parser.parse_args()

# Grab arguments
urls = args.urls.split(',')
ranks = args.ranks.split(',') if args.ranks else []
focus = args.focus
variants = args.variants.split(',') if args.variants else []

# Create pages { url: url, rank: rank or None }
pages = []
for i, url in enumerate(urls):
    pages.append({
        'url': url,
        'rank': ranks[i] if i < len(ranks) else None
    })

# Run once or run multiple depending on the passed arguments.
if len(pages) == 1:
    output = get_document(pages[0]['url'], focus, variants=variants, rank=pages[0]['rank'])
else:
    output = get_documents(pages, focus, variants=variants)

# Output to file if output path given, else print to stdout.
if args.output and os.path.exists(args.output):
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    filename = "{0}_{1}.json".format(timestamp, focus.replace(' ', '-').lower())
    with open(filename, 'w') as outFile:
        outFile.write(output)
else:
    print(output)