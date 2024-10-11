echo "Deleting General K8s-Related Resources!"
echo "-----------------------------"
echo ' '

#kubectl create namespace v2x
kubectl delete -f docker_pull.yaml
echo ' '

echo "Deleting Niryo Ned 2 Remote Controller"
kubectl delete -f niryo_ned_service.yaml
kubectl delete -f niryo_ned_deployment.yaml
echo ' '

echo "Deleting Prometheus Monitoring"
kubectl delete -f prometheus_service.yaml
kubectl delete -f prometheus_deployment.yaml
echo ' '

echo 'Everything Deleted!'