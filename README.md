# DevSecOps Lab — projet volontairement vulnérable

> ⚠️ Application **intentionnellement vulnérable**, uniquement pour apprendre et tester vos outils DevSecOps.
> Ne la déployez jamais sur Internet ni en production. Tous les secrets sont **factices**.

## Contenu

| Dossier / fichier | Type d'analyse | Exemples de findings attendus |
|---|---|---|
| `app/app.py` | SAST (Bandit, Semgrep, SonarQube) | SQLi, injection de commande, XSS/SSTI, path traversal, SSRF, pickle/yaml, MD5, debug=True |
| `app/requirements.txt` | SCA (pip-audit, Trivy, Snyk, Dependabot) | CVE sur Flask, Jinja2, Werkzeug, PyYAML, requests, urllib3, Pillow |
| `app/app.py`, `terraform/main.tf`, `Dockerfile` | Secrets (Gitleaks, TruffleHog) | Clés AWS, token GitHub, mots de passe en dur |
| `Dockerfile`, `docker-compose.yml` | Container / Dockerfile (Trivy, Hadolint) | Image `python:3.6` obsolète, root, ADD, secrets en ENV |
| `terraform/`, `k8s/` | IaC (Checkov, tfsec, kube-linter) | S3 public, SG 0.0.0.0/0, RDS non chiffrée, pod privilégié |
| lancement de l'app | DAST (OWASP ZAP, Nikto) | XSS, headers manquants, injections |
| `.github/workflows/devsecops.yml` | Pipeline CI complet | Tous les scans ci-dessus |

## Utilisation rapide

```bash
git init && git add . && git commit -m "init"   # nécessaire pour Gitleaks

# Secrets
gitleaks detect --source . -v

# SAST
pip install bandit semgrep
bandit -r app
semgrep --config auto app

# SCA
pip install pip-audit
pip-audit -r app/requirements.txt
trivy fs --scanners vuln,secret,misconfig .

# IaC
pip install checkov
checkov -d .

# Conteneur
docker build -t vulnerable-lab .
trivy image vulnerable-lab
hadolint Dockerfile

# DAST
docker run -d -p 5000:5000 vulnerable-lab
docker run --network host -t ghcr.io/zaproxy/zaproxy:stable zap-baseline.py -t http://localhost:5000
```

## Test CI

Poussez le dépôt sur GitHub : le workflow `.github/workflows/devsecops.yml` lance les 6 jobs
(secrets, SAST, SCA, IaC, conteneur, DAST). Pour faire **échouer** le pipeline, retirez les `|| true`,
`soft_fail` et passez `exit-code: "1"`.

## Exercices

1. Corrigez chaque vulnérabilité et relancez les scans pour voir les alertes disparaître.
2. Ajoutez un *quality gate* : le pipeline échoue si sévérité HIGH/CRITICAL.
3. Ajoutez un `.gitleaksignore` / `.trivyignore` et gérez les faux positifs.
4. Comparez les résultats de Bandit vs Semgrep vs SonarQube.
