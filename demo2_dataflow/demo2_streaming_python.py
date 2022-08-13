#!/usr/bin/env python
# Doc: https://cloud.google.com/pubsub/docs/stream-messages-dataflow
# Ref code: https://github.com/GoogleCloudPlatform/python-docs-samples/blob/main/dataflow/flex-templates/streaming_beam/streaming_beam.py

"""An Apache Beam streaming pipeline example.
It reads JSON encoded messages from Pub/Sub, transforms the message data and
writes the results to BigQuery.
"""

import argparse
import json
import logging
import time
from typing import Any, Dict, List

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import apache_beam.transforms.window as window

# Defines the BigQuery schema for the output table.

SCHEMA = ",".join(
    [
        "timestamp:TIMESTAMP",
        "branch:STRING",
        "transactions:INTEGER",
        "average_price:FLOAT",
    ]
)

def run(
    input_subscription: str,
    output_table: str,
    window_interval_sec: int = 60,
    beam_args: List[str] = None,
) -> None:
    """Build and run the pipeline."""
    options = PipelineOptions(beam_args, save_main_session=True, streaming=True)

    with beam.Pipeline(options=options) as pipeline:
        messages = (
            pipeline
            | "Read from Pub/Sub" >> beam.io.ReadFromPubSub(subscription=input_subscription)
            | "Parse JSON messages" >> beam.Map(json.loads)
            | "Fixed-size windows" >> beam.WindowInto(window.FixedWindows(window_interval_sec, 0))
            | "Add branch_txn keys" >> beam.WithKeys(lambda msg: msg["branch_txn"])
            | "Group by branch_txn" >> beam.GroupByKey()
            | "Get statistics" >> beam.MapTuple(
                lambda branch_txn, messages: {
                    "timestamp": max(msg["tr_time_str"] for msg in messages),
                    "branch": branch_txn,
                    "transactions": len(messages),
                    "average_price": sum(msg["price"] for msg in messages) / len(messages),
                }
            )
        )

        # Output the results into BigQuery table.
        _ = messages | "Write to Big Query" >> beam.io.WriteToBigQuery(
            output_table, schema=SCHEMA
        )


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output_table",
        help="Output BigQuery table for results specified as: "
        "PROJECT:DATASET.TABLE or DATASET.TABLE.",
    )
    parser.add_argument(
        "--input_subscription",
        help="Input PubSub subscription of the form "
        '"projects/<PROJECT>/subscriptions/<SUBSCRIPTION>."',
    )
    parser.add_argument(
        "--window_interval_sec",
        default=60,
        type=int,
        help="Window interval in seconds for grouping incoming messages.",
    )
    args, beam_args = parser.parse_known_args()

    run(
        input_subscription=args.input_subscription,
        output_table=args.output_table,
        window_interval_sec=args.window_interval_sec,
        beam_args=beam_args,
    )
