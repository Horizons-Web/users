#! /bin/bash

export PROJECT_ID=crested-primacy-413823
export REGION=us-east1
export CONNECTION_NAME=crested-primacy-413823:us-central1:users

gcloud builds submit \
  --tag gcr.io/$PROJECT_ID/poll \
  --project $PROJECT_ID

gcloud run deploy users \
  --image gcr.io/$PROJECT_ID/poll \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --add-cloudsql-instances $CONNECTION_NAME \
  --project $PROJECT_ID