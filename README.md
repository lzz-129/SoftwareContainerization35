# Docker Image Creation
Ensure you're in the `/SoftwareContainerization35` directory before executing the commands below to build images.
1. Command for bulding fronted image.  
```
  cd film_frontend  
  docker buildx build --platform linux/amd64 -t liuzhe2022/filmcomments-web:latest --push .
```
3. Command for building backend image.  
```
   cd film_backend   
   docker buildx build --platform linux/amd64 -t liuzhe2022/filmcomments-api:latest --push .
```
# Deploy Instructions
Make sure you are in the `\SoftwareContainerization35`
## helm install
```
helm install app-release1 ./helmcharts --namespace my-app
```
## helm scaling
```
kubectl scale deployment app-release1-filmcomments-frontend --replicas=3 --namespace my-app
kubectl get deployments -n my-app
```
## helm uninstall
```
helm uninstall app-release1 --namespace my-app
```
## helm upgrade #default:rolling upgrade
```
helm upgrade app-release1 ./helmcharts --set backend.api.container.image=liuzhe2022/filmcomments-api:test -n my-app
```
## rollout
```
kubectl rollout status deployment/app-release1-filmcomments-api-deployment -n my-app
```
