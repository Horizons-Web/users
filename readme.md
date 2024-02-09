

gcloud builds submit --tag gcr.io/crested-primacy-413823/users


gcloud run deploy users --image gcr.io/crested-primacy-413823/users --platform managed --allow-unauthenticated --region us-east1
