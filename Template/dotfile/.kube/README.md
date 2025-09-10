
This is for reference when there are multiple K8S clusters to manage.

## AWS EKS
Prerequisite:
1. config `cluster`, `user`, `context` under ".kube"
2. set env `AWS_REGION`, `AWS_PROFILE`, `AWS_ACCOUNT_ID`

In case cluster is recreated, it's better to ensure the __API server endpoint__
matches to avoid unexpected behavior.

```sh
kubectl config use-context {CONTEXT}
```

Config the cluster for the first time:
```sh
export AWS_PROFILE={profile}

export AWS_REGION={region}
export CLUSTER_NAME={cluster}

aws eks update-kubeconfig \
--region ${AWS_REGION}  \
--name ${CLUSTER_NAME} \
--profile ${AWS_PROFILE}
```
