YOUR_BUCKET_NAME=tip-us-east5
PATH_TO_FILE=../../assets/yelp/tip
FILENAME=4.json

# BORRAR
gsutil rm gs://$YOUR_BUCKET_NAME/$FILENAME
# COPIAR
gsutil cp $PATH_TO_FILE/$FILENAME gs://$YOUR_BUCKET_NAME/$FILENAME