import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Common django setup without context
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bulletnews.settings')

import django
django.setup()

import bbc
import nytimes


# The only purpose of this script is to
# invoke all crawlers; It gets executed
# periodically though cron
if __name__ == '__main__':
    c = nytimes.NyTimesWorld()
    c.crawl()
