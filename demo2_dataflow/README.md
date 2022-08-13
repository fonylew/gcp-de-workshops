# Demo 2: Streaming pipeline with Cloud Dataflow

Install requirements with
```
pip3 install -r requirements.txt
```

The source data can be generated with `message_generator_pubsub.py`.
Run with command:
```
python3 message_generator_pubsub.py
```

Set up the local variables in terminal:
```
export PROJECT_ID='enter your project_id'
export REGION='enter your region e.g. us-central1'
export BUCKET_NAME='enter your bucket name'
```

### Demo 2.1: Use Dataflow Job Template
Follow the instruction on the Console UI

### Demo 2.2: Beam Python SDK
The source code is `demo2_streaming_python.py`

Run with command:
```
python gcp-de-workshops/demo2_dataflow/demo2_streaming_python.py \
  --project=$PROJECT_ID \
  --region=$REGION \
  --input_subscription=projects/$PROJECT_ID/subscriptions/sales-sub \
  --output_table=$PROJECT_ID:testrun_workshop.sales_stat \
  --runner=DataflowRunner \
  --temp_location=gs://$BUCKET_NAME/temp
```
