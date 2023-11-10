REGION=us-east5
YOUR_FUNCTION_NAME=yelp
ENTRY_POINT=main

gcloud functions deploy $YOUR_FUNCTION_NAME \
--gen2 \
--runtime=python310 \
--region=$REGION \
--source=. \
--entry-point=$ENTRY_POINT \
--trigger-http \
--env-vars-file .env.yaml \
--memory 512MB