CLUSTER_NAME=observability-cluster
CLUSTER_EXISTS = $(shell kind get clusters -q | grep $(CLUSTER_NAME))
export KIND_CONFIG_FILE_NAME=kind.config.yaml

COLOR_RESET = \033[0m
COLOR_GREEN = \033[32m
COLOR_YELLOW = \033[33m
COLOR_BLUE = \033[34m


# HELP
# This will output the help for each task
# thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.PHONY: help grafana create-cluster delete-cluster

help: ## Help command
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

create-cluster: ## Create cluster k8s with cert-manager e metrics-server
    ifneq ($(CLUSTER_EXISTS), $(CLUSTER_NAME))
		kind create cluster --config config/kind-cluster-config.yaml --name $(CLUSTER_NAME) --wait 10s
    else
		kubectl config use-context kind-$(CLUSTER_NAME)
		kubectl cluster-info --context kind-$(CLUSTER_NAME)
    endif
    
	@echo "#### Installing metrics-server ####"
	helm repo add metrics-server https://kubernetes-sigs.github.io/metrics-server/
	helm upgrade --install -n kube-system metrics-server metrics-server/metrics-server --set image.repository=bitnami/metrics-server --set image.tag=latest
	@echo

	@echo "#### Installing CertManager ####"
	kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.15.3/cert-manager.yaml
	@echo

	@echo "#### Get pods ####"
	kubectl get pods -n kube-system
	@echo
