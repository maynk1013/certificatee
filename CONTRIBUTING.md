# Contributing

Run the checks from the repository root before opening a pull request:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest -q
terraform fmt -check -recursive projects
python3 tools/secret_scan.py
```

Terraform validation also needs `terraform init -backend=false` in each root module. The script `scripts/validate-all.sh` lists those commands.

Do not add real account IDs, tokens, or state files. Keep `create_compute`, `create_backup_resources`, and `create_secret_resource` false in committed examples.

Branch names can be `feature/<short-description>`. Commit subjects should say what changed and why, in one line under 72 characters.
