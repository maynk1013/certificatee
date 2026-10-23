# Resource pressure

The example CPU alert fires when the idle ratio leaves less than 20 percent idle for the local evaluator, or when the PromQL expression stays above 0.8 for 15 minutes on a real Prometheus.

## Checks

1. Identify the node and the pod with the highest CPU request.
2. Check whether a deployment is missing requests and limits.
3. Check eviction events before adding nodes.

## Mitigation

Add requests and limits first. Add nodes only when the workload is expected and the requests are already set. This was not executed on a cluster.
