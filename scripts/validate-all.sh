#!/usr/bin/env bash
# Run the local checks that do not create cloud resources.
set -eu
cd "$(dirname "$0")/.."

if [[ -x .venv/bin/python ]]; then
  PY=".venv/bin/python"
else
  PY="python3"
fi

"$PY" -m pytest -q
"$PY" tools/secret_scan.py
terraform fmt -check -recursive projects

roots=(
  projects/01-gitops-eks-platform/terraform/envs/dev
  projects/03-terraform-multi-environment/envs/dev
  projects/03-terraform-multi-environment/envs/staging
  projects/03-terraform-multi-environment/envs/prod
  projects/06-disaster-recovery/terraform
  projects/07-secrets-management/terraform
)
for dir in "${roots[@]}"; do
  terraform -chdir="$dir" init -backend=false -input=false
  terraform -chdir="$dir" validate
done

terraform -chdir=projects/03-terraform-multi-environment/tests/fixtures/invalid-syntax init -backend=false -input=false
if terraform -chdir=projects/03-terraform-multi-environment/tests/fixtures/invalid-syntax validate; then
  echo "invalid fixture was accepted"
  exit 1
fi

helm lint projects/01-gitops-eks-platform/helm/demo-web
helm lint projects/02-progressive-delivery/helm/demo-rollout
echo "local validation finished"
