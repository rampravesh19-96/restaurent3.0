# restaurent3.0
11 lines (8 sloc)  426 Bytes

eval $(minikube docker-env)
docker build . -t restaurant:latest
kubectl apply -f deploy.yaml
kubectl apply -f service.yaml
kubectl port-forward service/restaurant 9000:80
http://localhost:9000


kubectl port-forward service/restaurant 9000:80

eval $(minikube docker-env) && docker build . -t restaurant:latest && kubectl apply -f deploy.yaml && kubectl apply -f service.yaml && kubectl port-forward service/restaurant 9000:80
