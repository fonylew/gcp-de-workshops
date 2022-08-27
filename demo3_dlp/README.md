# Demo 3: Event-based pipeline with Cloud Functions and Cloud DLP
Create event-based pipeline with Cloud Functions with Object Notification to create Cloud DLP (Data Loss Prevention) job.

## Create 3 Cloud Storage buckets
- Raw data
- Sensitive data
- Non-sensitive data

## Create Pub/Sub Topic and Subscription
```
gcloud pubsub topics create classify-topic
gcloud pubsub subscriptions create classify-sub --topic classify-topic
```

## Add IAM role to App Engine default service account 
Add permission for service account `Project_ID@gcp-de-dryrun@appspot.gserviceaccount.com`
- DLP Administrator 
- DLP API Service Agent 

## Set up environment variables
Change the content in `env.yaml` coresponsing to project ID and bucket names.

## Deploy Cloud Functions 1: Create DLP Job
Before deploy, check that you're in `demo3_dlp` otherwise `cd gcp-de-workshops/demo3_dlp`.
```
gcloud functions deploy create_DLP_job --runtime python37 \
--trigger-event google.storage.object.finalize \
--trigger-resource [YOUR_RAW_BUCKET] \
--env-vars-file env.yaml
```

### Deploy Cloud Functions 2: Resolve DLP
Before deploy, check that you're in `demo3_dlp` otherwise `cd gcp-de-workshops/demo3_dlp`.
```
gcloud functions deploy resolve_DLP --runtime python37 \
--trigger-topic classify-topic \
--env-vars-file env.yaml
```
### References
- Cloud DLP demo: https://cloud.google.com/dlp/demo/#!/
- Cloud DLP docs: https://cloud.google.com/dlp/docs/examples
- Google Code labs: https://codelabs.developers.google.com/codelabs/cloud-storage-dlp-functions#0
- Original GitHub repository: https://github.com/GoogleCloudPlatform/dlp-cloud-functions-tutorials/tree/master/gcs-dlp-classification-python
