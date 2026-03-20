# Project Scope

## Intended intervention

This project explores privacy-safe, interpretable public-health signal monitoring in a deliberately limited research setting. The intended intervention is not operational surveillance. It is a cautious analytic workflow for studying whether broad aggregate indicators can be monitored in a way that is explainable, privacy-aware, and evaluable.

## Intended users

At a high level, the work is aimed at:

- researchers studying health AI, anomaly detection, or privacy-preserving analytics
- public-health analysts interested in benign early-warning-style evaluation
- technical teams thinking about responsible deployment boundaries and governance

## Why the current version is deliberately limited

The current version uses only synthetic data and a simple baseline model because the point at this stage is to clarify assumptions, inspect model behaviour, and document boundaries. It is easier to reason about safety, interpretability, and failure modes in a narrow prototype than in a broad platform with unclear claims.

## Success in a first prototype

For this repository, success means:

- a working end-to-end demo exists
- the workflow is transparent and easy to inspect
- outputs are interpretable enough for discussion
- safety and scope boundaries are explicit
- the next research steps are concrete

## Success in a later funded version

A stronger, funded version would still remain safely scoped, but success would look like:

- better evaluation on appropriate public or synthetic benchmark-style datasets
- multiple benign baselines with clearer calibration and uncertainty handling
- stronger reproducibility, documentation, and experiment tracking
- a lightweight interface for reviewing alerts and explanations
- a more mature governance and deployment-boundary framework

## Out of scope

The following are explicitly out of scope for this repository:

- medical advice
- real patient deployment
- pathogen design
- wet-lab support
- exploit identification
- sensitive threat modelling
- operational surveillance of individuals
