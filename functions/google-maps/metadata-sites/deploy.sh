REGION=us-east5
YOUR_BUCKET_NAME=metadata-sites-us-east5
YOUR_FUNCTION_NAME=metadata-sites-finalize
ENTRY_POINT=main_gcs

gcloud functions deploy $YOUR_FUNCTION_NAME \
--gen2 \
--runtime=python310 \
--region=$REGION \
--source=. \
--entry-point=$ENTRY_POINT \
--trigger-event-filters="type=google.cloud.storage.object.v1.finalized" \
--trigger-event-filters="bucket=$YOUR_BUCKET_NAME"