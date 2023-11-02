REGION=us-east5
YOUR_FUNCTION_NAME=review-states-finalize

gcloud beta functions logs read $YOUR_FUNCTION_NAME --gen2 --region=$REGION --limit=100