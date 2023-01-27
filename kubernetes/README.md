# Uso en Kubernetes


Dentro del Directorio lanzamos los yml
```
$ kubectl apply -f kubernetes-nrpe.yml 
deployment.apps/nrpe-ubuntu-portal-deployment created
$ kubectl apply -f nrpe-service.yml 
service/nrpe-service-portal created
$ kubectl apply -f loadbalancer-nrpe.yml 
service/nrpe-service-portal-loadbalancer created
```

Para comprobar:


```
$ kubectl get all
NAME                                                 READY   STATUS    RESTARTS   AGE
pod/nrpe-ubuntu-portal-deployment-74f4785854-6t755   1/1     Running   0          30m

NAME                                       TYPE           CLUSTER-IP       EXTERNAL-IP    PORT(S)          AGE
service/kubernetes                         ClusterIP      10.96.0.1        <none>         443/TCP          28h
service/nrpe-service-portal                ClusterIP      10.96.159.10     <none>         5666/TCP         60m
service/nrpe-service-portal-loadbalancer   LoadBalancer   10.103.127.183   10.52.38.200   5666:32434/TCP   44m

NAME                                            READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/nrpe-ubuntu-portal-deployment   1/1     1            1           30m

NAME                                                       DESIRED   CURRENT   READY   AGE
replicaset.apps/nrpe-ubuntu-portal-deployment-74f4785854   1         1         1       30m
```
## Las imagenes estan en Docker HUB

https://hub.docker.com/r/wexmaster/nrpe-ubuntu-portal
