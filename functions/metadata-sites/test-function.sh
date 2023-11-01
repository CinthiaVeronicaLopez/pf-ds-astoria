YOUR_BUCKET_NAME=metadata-sites-us-east5
PATH_TO_FILE=../../assets/metadata-sites
FILENAME=4.json

# BORRAR
gsutil rm gs://$YOUR_BUCKET_NAME/$FILENAME
# COPIAR
gsutil cp $PATH_TO_FILE/$FILENAME gs://$YOUR_BUCKET_NAME/$FILENAME