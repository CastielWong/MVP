#!/bin/bash
# # set proxy if needed
# export http_proxy="http://xxx:8080"
# export https_proxy="http://xxx:8080"
# export no_proxy="*.com,vdi*,sso.com*""

# =============================================================================
export WORKING_DIRECTORY="tools"

# set environment variables
export TERRAFORM_VERSION="1.9.5"
export K9S_VERSION="v0.50.2"
export KUBECTL_VERSION=$(curl -L -s https://dl.k8s.io/release/stable.txt)
export HELM_SCRIPT="install_helm.sh"

export URL_AWSCLI="https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip"
export URL_TERRAFORM="https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_386.zip"
export URL_KUBECTL="https://dl.k8s.io/release/${KUBECTL_VERSION}/bin/linux/amd64/kubectl"
export URL_HELM="https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3"
export URL_K9S="https://github.com/derailed/k9s/releases/download/${K9S_VERSION}/k9s_Linux_amd64.tar.gz"

export UNZIP_AWSCLI="unzip_aws"
export UNZIP_TERRAFORM="unzip_terraform"
export UNZIP_K9S="unzip_k9s"

# -----------------------------------------------------------------------------
# place all tools inside a dedicated place
if [[ ! -d "${WORKING_DIRECTORY}" ]]; then
  # Create the directory
  mkdir "${WORKING_DIRECTORY}"
  echo "LOGGING: Directory '${WORKING_DIRECTORY}' is created."
else
  echo "LOGGING: Directory '${WORKING_DIRECTORY}' already exists."
fi

cd "${WORKING_DIRECTORY}/"

# -----------------------------------------------------------------------------
# Downloading
# AWS CLI
if [[ ! -f $(basename ${URL_AWSCLI}) ]]; then
  curl ${URL_AWSCLI} -o $(basename ${URL_AWSCLI})
fi

# Terraform
if [[ ! -f $(basename ${URL_TERRAFORM}) ]]; then
  curl -LO ${URL_TERRAFORM}
fi

# kubectl
if [[ ! -f $(basename ${URL_KUBECTL}) ]]; then
  curl -LO ${URL_KUBECTL}

  # verify the download
  curl -LO "${URL_KUBECTL}.sha256"
  echo "LOGGING: $(cat kubectl.sha256)  kubectl" | sha256sum --check
fi

# Helm
if [[ ! -f "${HELM_SCRIPT}" ]]; then
  curl -fsSL -o ${HELM_SCRIPT} ${URL_HELM}
fi

# K9S
if [[ ! -f $(basename ${URL_k9s}) ]]; then
  curl -LO ${URL_K9S} -o $(basename ${URL_K9S})
fi

# -----------------------------------------------------------------------------

# Installing
# AWS CLI
if ! command -v aws > /dev/null 2>&1; then
  unzip $(basename ${URL_AWSCLI}) -d ${UNZIP_AWSCLI}
  sudo ./${UNZIP_AWSCLI}/aws/install
fi

# Terraform
if ! command -v terraform > /dev/null 2>&1; then
  unzip $(basename ${URL_TERRAFORM}) -d ${UNZIP_TERRAFORM}
  sudo cp ${UNZIP_TERRAFORM}/terraform /usr/local/bin/
fi

# kubectl
if ! command -v kubectl > /dev/null 2>&1; then
  sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
fi

# Helm
if ! command -v helm > /dev/null 2>&1; then
  chmod 700 ${HELM_SCRIPT}
  ./${HELM_SCRIPT}
fi

# K9S
if ! command -v k9s > /dev/null 2>&1; then
  mkdir ${UNZIP_K9S}; tar -xzvf $(basename ${URL_K9S}) -C ${UNZIP_K9S}
  sudo mv ${UNZIP_K9S}/k9s /usr/local/bin/
fi

# -----------------------------------------------------------------------------

# Cleaning
direcotires=(
  "${UNZIP_AWSCLI}"
  "${UNZIP_TERRAFORM}"
  "${UNZIP_K9S}"
)

for dir in "${direcotires[@]}"; do
  if [ -d "${dir}" ]; then
    echo "LOGGING: Deleting files inside: ${dir}"
    rm -rf "${dir}"/*
    rmdir "${dir}"
  else
    echo "LOGGING: There is no ${dir} found"
  fi
done

rm "$(basename ${URL_KUBECTL}).sha256"

cd -
