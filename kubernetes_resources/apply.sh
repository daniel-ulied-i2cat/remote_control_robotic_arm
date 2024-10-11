echo "Launching General K8s-Related Resources!"
echo "-----------------------------"
echo ' '

#kubectl create namespace v2x
kubectl apply -f docker_pull.yaml
echo ' '

echo "Launching Niryo Ned 2 Remote Controller"
kubectl apply -f niryo_ned_service.yaml
kubectl apply -f niryo_ned_deployment.yaml
echo ' '

echo "Launching Prometheus Monitoring"
kubectl apply -f prometheus_service.yaml
kubectl apply -f prometheus_deployment.yaml
echo ' '

echo 'Everything Deployed!'