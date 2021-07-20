# Kubernetes 101

Kubernetes 101 is an introductory Kubernetes workshop for folks without prior knowledge or experience.

## Goal

Consolidate a baseline of Kubernetes theoretical knowledge and practical experience for the interested audience.

## Pre-requisites

Some basic linux commands will be used during this workshop. Moreover, it is recommended to have some working knowledge or general overview of containers, micro-services architecture, and distributed systems.

## Installation (before workshop)

In order to participate in this workshop you will need to setup some tooling:

- Docker Desktop. Follow this [instructions](https://docs.docker.com/docker-for-mac/install/)
- Bash or Zsh.
- Visual Studio Code, vim, or similar editor

## Workshop

### Verify setup

Let's start by verifying that docker and kubernetes are correctly installed in your local environment.

- Open up your terminal
- Verify that Docker Desktop is running on your laptop.

<img src="./img/docker-desktop.png" alt="drawing" width="200"/>

- Execute `docker --version`. You should see an output similar to the following

```
Docker version 20.10.7, build f0df350
```
- Execute `kubectl version --short`. The output now should look like this:

```
Client Version: v1.21.2
Server Version: v1.19.7
```

### Containers

As we saw in the theory section, containers are standardized units of development, shipment, and deployment that contain application code and its dependencies.

Let's take a look now at spinning up a simple nginx server via its docker image.

- Pull the Docker image from the Dockerhub repository:

`docker pull nginx:latest`

- Spin up locally a running container from this image:

`docker run --name nginx-server -d -p 8080:80 nginx`

You should see as output a long id:

```
c838b80e0ea2d354cbce534110c3d7f7d7315d127f64fe4c0aa0a67225699483
```

and you should be able to see your container up and running:

`docker ps | grep nginx-server`

```
c838b80e0ea2   nginx   "/docker-entrypoint.…"   11 seconds ago   Up 6 seconds   0.0.0.0:8080->80/tcp, :::8080->80/tcp   nginx-server
```

At this point if you hit your localhost at port 8080 you should see nginx default page.

- Open up a browser and go to `localhost:8080`
- Execute on your terminal `curl localhost:8080`

The outcome should be the same

<img src="./img/nginx-default.png" alt="drawing" width="200"/>

By following these steps we have started a container from an image that fires up an nginx server.

<img src="./img/k8s_1.png" alt="drawing"/>

Make sure you kill the container created in this section before moving into the next one

`docker kill <CONTAINER_ID>`

### Pod

The Pod is the fundamental unit of work in Kubernetes, specifying a single container or group of communicating containers that are scheduled together. Pods are defined by a specification that contains details about the container image, port to run in, etc.

Following up with our nginx example from previously, we can specify the desired state we want to achieve, and we do that with a **pod specification**:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
spec:
  containers:
    - name: nginx
      image: nginx:latest
      ports:
      - containerPort: 80
```

You can see that we are defining a Kubernetes object, a Pod specifically, that will be created out of the nginx image, and will run on port 80. We can now apply this configuration:

```
kubectl apply -f pod.yaml
kubectl get pods
kubectl port-forward pod/nginx-pod 8080:80
```

At this point, if you try to hit the endpoint again as we previously did, you should get the same nginx default page in your browser/client. Something has changed though. The server as before is running within its container, however, this container now is running inside a pod. You can see more information about this pod by executing:

`kubectl describe pod nginx-pod`

<details>
<summary>See output</summary>

```yaml
Name:         nginx-pod
Namespace:    default
Priority:     0
Node:         docker-desktop/192.168.65.4
Start Time:   Wed, 14 Jul 2021 19:07:36 +0200
Labels:       <none>
Annotations:  <none>
Status:       Running
IP:           10.1.1.209
IPs:
  IP:  10.1.1.209
Containers:
  nginx:
    Container ID:   docker://25fcfd5b60e8c88a4da0c181605f42d0eb57536b5babe83eaa4f263048cc2c49
    Image:          nginx:latest
    Image ID:       docker-pullable://nginx@sha256:353c20f74d9b6aee359f30e8e4f69c3d7eaea2f610681c4a95849a2fd7c497f9
    Port:           80/TCP
    Host Port:      0/TCP
    State:          Running
      Started:      Wed, 14 Jul 2021 19:07:41 +0200
    Ready:          True
    Restart Count:  0
    Environment:    <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from default-token-h6cdl (ro)
Conditions:
  Type              Status
  Initialized       True
  Ready             True
  ContainersReady   True
  PodScheduled      True
Volumes:
  default-token-h6cdl:
    Type:        Secret (a volume populated by a Secret)
    SecretName:  default-token-h6cdl
    Optional:    false
QoS Class:       BestEffort
Node-Selectors:  <none>
Tolerations:     node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
                 node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
Events:
  Type    Reason     Age    From               Message
  ----    ------     ----   ----               -------
  Normal  Scheduled  2m16s  default-scheduler  Successfully assigned default/nginx-pod to docker-desktop
  Normal  Pulling    2m14s  kubelet            Pulling image "nginx:latest"
  Normal  Pulled     2m12s  kubelet            Successfully pulled image "nginx:latest" in 1.6311278s
  Normal  Created    2m12s  kubelet            Created container nginx
  Normal  Started    2m12s  kubelet            Started container nginx
```
</details>


### Deployment

Deployment objects exist to manage the release of new versions. It sits in front of a replica set that manages the desired state of your system.

<img src="./img/k8s_2.png" alt="drawing"/>


A Deployment object is created out of this specification and will create and configure pods accordingly.


```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  selector:
    matchLabels:
      app: nginx
  replicas: 1
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:latest
        ports:
        - containerPort: 80
```

```
kubectl apply -f deployment.yaml
kubectl get pods
kubectl get deployments
```

It could be the case that your use case requires multiple pods running the container image, and for that you need to specify it in the deployment YAML by using the replicas parameter. Let's try to modify the number of pods in which our nginx container will be running in from 1 to 3.

Now if you apply again this configuration and query for the running pods you'll see a different amount of them in the output.

```
kubectl apply -f deployment.yaml
kubectl get pods
```

```
NAME                                READY   STATUS    RESTARTS   AGE
nginx-deployment-68c7f5464c-ptc4k   1/1     Running   0          18s
nginx-deployment-68c7f5464c-vwwtk   1/1     Running   0          50m
nginx-deployment-68c7f5464c-w92x2   1/1     Running   0          18s
```

Let's bring it back to 2 instances now, by manually executing:

`kubectl scale deployments/<DEPLOYMENT_NAME> --replicas=2`


### Service

As we mentioned before, Kubernetes handles the lifecycle of the pods you declare in your manifest. If we want to connect 2 applications running on different ports, or wanted to reach to a specific pod we could do it by targeting the pod IP address. The problem is that those might change as the pod supervision takes place, therefore, it would be an unreliable way of communicating with the pod. That's when Services become useful. A Service is an abstraction of a pod (or set of pods) in order to provide consumers of this application with a single interface and an unchanging IP address. It acts like a proxy to this logical set of pods, that under the hood might undergo through a series of restart, reallocate, etc. operations.

<img src="./img/k8s_3.png" alt="drawing"/>

In this example you can see that the service is the entry point or proxy to a set of pods that we abstract ourselves from when communicating. One of the pods might be restarted for some reason and its IP might change, or might be reallocated to another node, etc. However, this is transparent to consumers of this service.

Following up on our example with nginx, we could define a Service configuration parameters like this:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-nginx-service
spec:
  selector:
    app: nginx
  ports:
    - protocol: TCP
      port: 80
```

We can also expose a service based on a Deployment object.

```
kubectl get deployments
kubectl expose deployment nginx-deployment --type=LoadBalancer
kubectl get services
```

You should see an output like this:

```
service “nginx-deployment” exposed
```