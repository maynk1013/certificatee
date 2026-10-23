# High latency

The example alert uses average latency from a sum and a count. It is not a percentile. A single slow request can move the average.

## Checks

1. Compare the latency panel with request rate. A tiny amount of traffic makes the average noisy.
2. Check CPU and memory panels before changing application code.
3. Check whether the readiness probe is passing while requests are slow. Readiness does not measure latency in this demo.

## Mitigation

Scale the demo only after you know the process is CPU bound. This repository has no measured capacity number.
