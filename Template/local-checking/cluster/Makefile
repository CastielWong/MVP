
SHELL := /bin/bash

POD_NAME = checking-pod

start:
	kubectl apply -f ck_pod.yaml

run:
	kubectl exec -it $(POD_NAME) -- bash

check:
	kubectl get pod | grep $(POD_NAME) || true

end:
	kubectl delete pod/$(POD_NAME)
