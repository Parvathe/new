
set -e

#configure kubernetes access
echo "*** setting up kubernetes access based on service account token ***";
gcloud auth activate-service-account ${GCP_ACCOUNTNAME} --key-file=${GCRCREDFILE} --project=${PROJECT_ID}
gcloud container clusters get-credentials ${CLUSTER_NAME} --zone ${LOCATION}

#kubernetes won't allow variables in the yaml files so using envsubst workaround so we can use them
echo "*** creating deployment yaml files ***";
env envsubst < deployment.tmpl > deployment.yaml;
env envsubst < service.tmpl > service.yaml;
env envsubst < ingress.tmpl > ingress.yaml;

echo "*** deploying docker container and setting up the service and ingress  ***";

# cat service.yaml; 
kubectl apply -f deployment.yaml --validate=false --insecure-skip-tls-verify=true;
kubectl apply -f service.yaml --validate=false --insecure-skip-tls-verify=true;
 kubectl apply -f ingress.yaml --validate=false --insecure-skip-tls-verify=true;
