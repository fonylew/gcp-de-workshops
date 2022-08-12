#!/usr/bin/env python
# Code modified from https://cloud.google.com/dataflow/docs/samples/join-streaming-data-with-sql#expandable-3
# Original code from https://gist.github.com/antoniocachuan/9862a7662a22d201718cb08fb0066e23

import datetime, json, os, random, time

# Set the `project` variable to a Google Cloud project ID.
project = 'acoustic-racer-358817'

BRANCH = ['LIM', 'BOG', 'SFO', 'LAX', 'PEK', 'ATL', 'CDG', 'AMS',
        'HKG', 'ICN', 'FRA', 'MAD', 'SEA', 'LAS', 'SIN', 'BKK', 'DFW',
        'DXB', 'LHR', 'DEL', 'BCN', 'SZX', 'KUL', 'JFK']
TRANSACTION = ['A00001', 'B00001', 'C00001', 'D00001', 'E00001', 'F00001', 'G00001',
        'H00001', 'I00001', 'F00001', 'G00001', 'H00001', 'I00001', 'J00001', 'K00001', 'L00001',
        'M00001', 'N00001', 'O00001', 'P00001', 'Q00001', 'R00001', 'S00001', 'T00001', 'U00001']

while True:
    data = {
            'tr_time_str': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'branch_txn': random.choice(BRANCH),
            'transaction_id': random.choice(TRANSACTION),
            'price': float(random.randrange(50000, 70000)) / 100,
            }

    # For a more complete example on how to publish messages in Pub/Sub.
    # https://cloud.google.com/pubsub/docs/publisher
    message = json.dumps(data)
    command = "gcloud --project={} pubsub topics publish sales --message='{}'".format(project, message)
    print(command)
    os.system(command)
    time.sleep(random.randrange(1, 5))
