# Environment Overview

The labs run against a Kubernetes cluster, supported by the `kubectl` package.

Locally, for instance, you can use:

* `minikube`
* `microk8s`

In addition, on the client side, you need Python 3.5 or above.

## Installation of a local Kubernetes

### Kubectl

For both `minikube` and `microk8s`, `kubectl` is required. Even if you have `kubectl` installed, for the purpose of this demonstration, a specific version (v1.19.1) is required so following the installation steps is necessary to replace the current version. You can check the current version, if installed, using:

```console
$ kubectl version --client
```

#### Linux

You can install Kubectl v1.19.1 using:

```console
$ curl -LO https://dl.k8s.io/release/v1.19.1/bin/linux/amd64/kubectl
```

```console
$ sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```

For further instructions, and for information about downloading the latest `kubectl` version for Linux after completing the demonstration, consult the [Kubernetes Installation Documentation](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)

#### Mac OS

You can install Kubectl v1.19.1 for Intel macOS using:

```console
$ curl -LO "https://dl.k8s.io/release/v1.19.1/bin/darwin/amd64/kubectl"
```

And for Apple Silicon macOS using:

```console
$ curl -LO "https://dl.k8s.io/release/v1.19.1/bin/darwin/arm64/kubectl"
```

Once installed, the `kubectl` binary needs to be made executable and its path rooted:

```console
$ chmod +x ./kubectl
```

```console
$ sudo mv ./kubectl /usr/local/bin/kubectl
```

```console
$ sudo chown root: /usr/local/bin/kubectl
```

For further instructions, and for information about downloading the latest `kubectl` version for Mac OS after completing the demonstration, consult the [Kubernetes Installation Documentation](https://kubernetes.io/docs/tasks/tools/install-kubectl-macos/)

#### Windows

You can install Kubectl v1.19.1 by running the Command Prompt as Administrator and using:

```console
$ curl -LO https://dl.k8s.io/release/v1.19.1/bin/windows/amd64/kubectl.exe
```

```console
$ move kubectl.exe C:\Windows\System32
```

For further instructions, and for information about downloading the latest `kubectl` version for Windows after completing the demonstration, consult the [Kubernetes Installation Documentation](https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/)

### Minikube

Minikube can be installed by following the installation steps on the [Minikube Start](https://minikube.sigs.k8s.io/docs/start/) docs. The cluster can then be initiated and run using the docker driver:

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

```console
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
```

```console
$ kubectl apply -f kube-prometheus/manifests/setup/
```

```console
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

## Chaos Mesh

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

You can setup the dashboard as follows:

```console
$ kubectl -n chaos-testing port-forward --address 0.0.0.0 service/chaos-dashboard 2333:2333
```

And access it by going to <http://localhost:2333/>

## Traefik

We use traefik as an ingress provider to service our application.

```console
$ kubectl apply -f manifests/traefik.yaml
```

## Installation of the Chaos Toolkit and its dependencies

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
$ pip install chaostoolkit-kubernetes chaostoolkit-prometheus chaostoolkit-addons jsonpath2
```

You can verify they are now available by running:

```console
$ chaos info extensions
```

Finally, we install a plugin to generate reports of experiment runs:

```console
$ pip install chaostoolkit-reporting
```

## Installation of experiment dependencies

### Vegeta

[Vegeta](https://github.com/tsenart/vegeta) is a standalone binary that can
induce load onto a web application. We often use it for simple load during an
experiment to understand how the traffic is impacted by an experiment.

#### Linux

You will first need to install `wget` using:

```console
$ apt-get install wget
```

You can then install Vegeta v12.8.3 for Linux AMD64 using:

```console
$ wget https://github.com/tsenart/vegeta/releases/download/v12.8.3/vegeta-12.8.3-linux-amd64.tar.gz
```

```console
$ tar -zxf vegeta-12.8.3-linux-amd64.tar.gz
```

Or for Linux ARM64 using:

```console
$ wget https://github.com/tsenart/vegeta/releases/download/v12.8.3/vegeta-12.8.3-linux-arm64.tar.gz
```

```console
$ tar -zxf vegeta-12.8.3-linux-arm64.tar.gz
```

Once installed, the `vegeta` binary needs to be moved and rooted

```console
$ sudo mv ./vegeta /usr/local/bin/
```

```console
$ sudo chmod +x /usr/local/bin/vegeta
```

#### MacOS

For macOS, you can install Vegeta via the Homebrew package manager:

```console
$ brew install vegeta
```

#### Windows

You will first need to install `wget` by running the Command Prompt as Administrator and using:

```console
$ curl -LO https://eternallybored.org/misc/wget/1.21.1/64.wget.exe
```

```console
$ move wget.exe C:\Windows\System32
```

You will also need to install `unzip` by running the Command Prompt as Administrator and using:

```console
$ curl -LO www.stahlworks.com/dev/unzip.exe
```

```console
$ move unzip.exe C:\Windows\System32
```

You can then install Vegeta v12.8.3 into a temporary directory by running the Command Prompt as Administrator and using:

```console
$ mkdir vegeta && cd vegeta
```

```console
$ wget https://github.com/tsenart/vegeta/releases/download/v12.8.3/vegeta-12.8.3-windows-amd64.zip
```

```console
$ unzip vegeta-12.8.3-windows-amd64.zip
```

```console
$ move vegeta.exe C:\Windows\System32
```

The temporary directory can then be deleted which will ask for a confirmation:

```console
$ cd .. && rmdir /s vegeta
```

## Installation of the applications

You can now install the application services:

```console
$ kubectl apply -f manifests/all.yaml
```
