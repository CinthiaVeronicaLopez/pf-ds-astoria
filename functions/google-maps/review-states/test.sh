YOUR_BUCKET_NAME=review-states-us-east5
PATH_TO_FILE=../../../assets/review-states/florida
FILENAME=0.json

# BORRAR
gsutil rm gs://$YOUR_BUCKET_NAME/$FILENAME
# COPIAR
gsutil cp $PATH_TO_FILE/$FILENAME gs://$YOUR_BUCKET_NAME/$FILENAME