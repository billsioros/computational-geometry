
import csv
import logging
import re
from pathlib import Path

logger = logging.getLogger(__name__.replace('_', ' ').strip().upper())

logging.basicConfig(
    format='[%(asctime)s] %(name)s:%(levelname)s: %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)

csv_file = 'benchmark.csv'
base = Path('images/kdtree/')
force, tree = base / 'force', base / 'tree'

regex = r'([0-9]+)_([0-9]+)_([0-9]+)\.png'

counts = {
    '01': 80,
    '005': 160,
    '001': 800,
    '0005': 1600
}

data = {
    'force': [],
    'tree': []
}

headers = ['type', 'neighbors', 'predictions', 'time', 'efficiency']

for t, p in {'force': tree, 'tree': force}.items():
    logger.info('Processing %s files' % (t,))

    for file in p.iterdir():
        logger.info('Processing file %s' % (file.name,))

        match = re.match(regex, file.name)
        neighbors = match.group(1)
        meshgrid_step = match.group(2)
        time = match.group(3)

        neighbors = int(neighbors)
        predictions = int(counts[meshgrid_step])
        time = float(f'{time[:-4]}.{time[-4:]}')

        if t == 'force':
            efficiency = 1
        else:
            counterpart = None
            for row in data['force']:
                if row['predictions'] == predictions and row['neighbors'] == neighbors:
                    counterpart = row
                    break

            efficiency = counterpart['time'] / time

        data[t].append(
            {
                'neighbors': neighbors,
                'predictions': predictions,
                'time': time,
                'efficiency': efficiency
            }
        )


logger.info('Writing to %s file' % (csv_file,))
try:
    with open(csv_file, 'w') as file:
        writer = csv.DictWriter(file, fieldnames=headers, lineterminator='\n')
        writer.writeheader()
        for t, rows in data.items():
            for row in rows:
                writer.writerow({'type': t, **row})
except IOError as e:
    logger.error(e)
