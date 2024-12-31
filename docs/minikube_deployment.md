### Build image locally and deploy on Minikube

1. Build image for platform
```sh
cd platform
docker build -t axon-api .
```

2. Load image from local docker into minikube.
```sh
minikube start
eval $(minikube docker-env)
minikube image load axon-api
```

3. Apply k8s manifests
```sh
kubectl apply -f infrastructure/manifests
```

4. Install Platform Ingres + NGINX helm chart
```sh
helm install axon ./infrastructure/helm/
```

If you want to uninstall the platform-api helm chart and purge its resources, run this:
```sh
helm uninstall axon  
```
