# Project 4 — Observability platform

Version-controlled dashboards, Prometheus rules, Loki and Alloy values, and a local query tool. The local tool parses Prometheus text, queries JSON logs, and evaluates three example alerts. Prometheus, Grafana, Loki, and Alloy were not installed on a cluster.

## Samajh lo, Hinglish mein

Metrics numbers hain: kitne request, kitne error, kitni der. Logs lines hain: kis request ne kya kiya. Alert ek rule hai jo number threshold ke paar jaaye to message banata hai. Dashboard un numbers ka chart hai.

Is project ka local lab Python mein hai. Woh Prometheus server nahi hai. Woh sample text padh kar wahi sawal poochta hai jo baad mein Grafana mein poochoge. Isse bina cluster ke test hota hai.

Cluster wala hissa Helm values mein hai. Woh tab kaam karega jab tum kube-prometheus-stack, Loki, aur Alloy install karo. Woh install yahan nahi hua.

## Architecture

```mermaid
flowchart LR
  app[Demo app] --> metrics[/metrics]
  app --> logs[stdout JSON]
  metrics --> prom[Prometheus]
  logs --> alloy[Grafana Alloy]
  alloy --> loki[Loki]
  prom --> graf[Grafana]
  prom --> am[Alertmanager]
  am --> slack[Optional Slack file]
  lab[Local lab] --> evidence[test-alert.log]
```

## Example SLI and SLO

These are design examples, not measured results.

| Signal | SLI | Example SLO | Assumption |
| --- | --- | --- | --- |
| Availability | Non-5xx requests divided by all requests | 99 percent over 30 days | No traffic means the SLI is undefined. It is not treated as 100 percent. |
| Latency | Average of the demo duration sum divided by count | Under 0.5 seconds | This is an average, not p95 or p99. |
| Saturation | One minus idle CPU | Below 80 percent for 15 minutes | Node exporter metrics must exist. They were not scraped here. |

## Local test

From the repository root:

```bash
python3 -m pytest projects/04-observability-platform/observability_lab/tests -q
```

The test writes `evidence/test-alert.log`. That file is the reproducible alert scenario.

Log query used by the test:

```text
level=error contains "simulated failure"
```

## Optional cluster install

Chart versions are listed in `helm/chart-versions.txt`. Confirm them before install. Do not install unless you approve the cluster cost.

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm upgrade --install kube-prometheus-stack prometheus-community/kube-prometheus-stack \
  -n monitoring --create-namespace \
  -f projects/04-observability-platform/helm/values/kube-prometheus-stack.yaml
```

Loki and Alloy commands belong in the same namespace only after the values match the current chart schema. The values files were not rendered against the upstream charts in the initial local run unless `scripts/verify-helm-charts.sh` says they were.

Slack stays empty until you mount `/etc/alertmanager/secrets/slack-webhook-url`.

## Retention and resources

Committed example retention is 7 days for Prometheus and 168 hours for Loki. Example requests are 100m CPU and 256Mi memory for Prometheus and Loki, and 50m CPU and 64Mi for Alloy. These are starting points for a lab, not a capacity test. A real cluster needs disk, remote storage, and a review of cardinality.

Production hardening that is not implemented here: authentication on Grafana, TLS on Loki, multi-replica Prometheus, object storage, and paging rules with an owned on-call rotation.

## Troubleshooting

| Symptom | Local meaning |
| --- | --- |
| No alert on an empty file | The lab refuses to call empty traffic healthy. |
| Alert log has three lines | Error ratio, latency, and CPU sample all crossed example thresholds. |
| Grafana panel is empty on a cluster | The app metric names or the scrape label do not match the dashboard. |

## Teardown

```bash
helm uninstall alloy -n monitoring
helm uninstall loki -n monitoring
helm uninstall kube-prometheus-stack -n monitoring
```

Run that only on your own cluster. It was not run here.

## Limitations

- Metrics and logs were queried in the Python lab, not in Prometheus or Loki.
- Dashboards and rules are valid JSON and YAML. They were not loaded into Grafana.
- No Slack message was sent.
