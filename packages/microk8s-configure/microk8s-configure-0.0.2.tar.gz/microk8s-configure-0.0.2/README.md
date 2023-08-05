# Microk8s-configure

Tool for setting microk8s on Ubuntu VPS over SSH

## Features

* [X] install microk8s
* [X] enabled registry microk8s
* [X] configure for external push in docker registry
* [ ] enable custom plugins in command line
* [ ] configure local kubectl for connect to microk8s on VPS
* [ ] support for other users (now only can install with root user)



## run

```bash
$ python -m mk8sconfig -p rootServerPassword -i 165.2.1.146 -d my-domain.co

```

## for push into docker registry

edit your docker-daemon.json adding:

```json
{
  "debug" : true,
  "insecure-registries" : [
    "my-domain.co:5000"
  ]
}
```

## Authors:

* Fabio Moreno <fabiomoreno@outlook.com>