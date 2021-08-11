# Environment Overview

The labs run against a Kubernetes cluster, any recent version (1.16+)
should do.

Locally, for instance, you can use:

* minikube
* microk8s

In addition, on the client side, you need Python 3.5 or above.

## Installation of a local Kubernetes

### Minikube

Minikube can be installed by following the installation step on the [Minikube Start](https://minikube.sigs.k8s.io/docs/start/) docs. The cluster can then be initiated and run using a docker driver:

```console
$ minikube start --driver docker --kubernetes-version v1.19.1
```

### Microk8s

#### Linux

```console
$ sudo snap install microk8s --classic --channel=1.19
```

#### MacOS

```console
$ brew install ubuntu/microk8s/microk8s
```

```console
$ microk8s install --channel=1.19
```

You will then receive the following which you also need to set up:

```
Support for 'multipass' needs to be set up. Would you like to do that it now? [y/N]:
```

#### Windows

We recommend following the first three installation steps on the [Microk8s](https://microk8s.io/docs/install-alternatives#heading--windows) Alternative Installation page and setting the Snap Track to "1.19/stable"

#### Add-Ons

After installing Microk8s, you will need to install a couple of add-ons for the Kubernetes cluster

```
$ microk8s.enable dns rbac
```

Please review the [microk8s documentation](https://microk8s.io/docs)
for further information.

## Installation of Kubernetes dependencies

### Prometheus

We use the [Prometheus operator](https://github.com/prometheus-operator/prometheus-operator) which will run in the `monitoring` namespace by default and expose:

* Prometheus
* Grafana
* alert manager

### Prometheus Installation

#### Minikube

```console
$ git clone https://github.com/prometheus-operator/kube-prometheus
$ kubectl apply -f kube-prometheus/manifests/setup/
$ kubectl apply -f kube-prometheus/manifests/
```

#### Microk8s

```console
$ microk8s.enable prometheus
```

### Prometheus Services
Once installed, you can view the services running

```console
$ kubectl -n monitoring get all
```

### Chaos Mesh

Chaos Mesh is a powerful fault injection tool for Kubernetes which can create
turbulences on physical and OS resources.

It is used by the Chaos Toolkit in rich Chaos Engineering experiments.

```console
$ curl -sSL https://mirrors.chaos-mesh.org/v1.0.2/install.sh | bash
```

See all its services running:

```console
$ kubectl -n chaos-testing get all
```

You can access its dashboard as follows:

```console
$ kubectl -n chaos-testing port-forward --address 0.0.0.0 service/chaos-dashboard 2333:2333
```

### Traefik

We use traefik as an ingress provider to service our application.

```console
$ kubectl apply -f manifests/traefik.yaml
```

### Installation of the Chaos Toolkit and its dependencies

The [Chaos Toolkit](https://chaostoolkit.org/) is the Chaos Engineering
automation framework from Reliably. It is an open source project written in
Python. Assuming you have a proper Python 3.5 available, you should be able to
install it as follows:

```console
$ pip install chaostoolkit
```

You can verify it is now available by running:

```console
$ chaos info core
```

In itself, Chaos Toolkit does not have any capabilities to operate systems. You
need to installation that target these systems.

```console
$ pip install chaostoolkit-kubernetes chaostoolkit-prometheus \
    chaostoolkit-addons jsonpath2
```

You can verify they are now available by running:

```console
$ chaos info extensions
```

Finally, we install a plugin to generate reports of experiment runs:

```console
$ pip install chaostoolkit-reporting
```

### Installation of experiments dependencies

The following labs are going to rely on a variety of tools.

#### Vegeta

[Vegeta](https://github.com/tsenart/vegeta) is a standalone binary that can
induce load onto a web application. We often use it for simple load during an
experiment, to understand how the traffic is impacted by an experiment.

```console
$ wget https://github.com/tsenart/vegeta/releases/download/v12.8.4/vegeta_12.8.4_linux_386.tar.gz
$ tar -zxf vegeta_12.8.4_linux_386.tar.gz
$ sudo cp ./vegeta /usr/local/bin/
$ sudo chmod +x /usr/local/bin/vegeta
```

### Installation of the applications

You can now install the application services:

```console
$ kubectl apply -f manifests/all.yaml
```
