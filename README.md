# Privacy-Safe AI for Early Public-Health Signal Monitoring

*A cautious prototype for interpretable, privacy-aware early warning analytics on synthetic data.*

## Overview

This repository is an early research/demo artifact for a narrow question: can simple, interpretable models help flag unusual public-health-style signal patterns without relying on sensitive personal data or making operational claims?

The current prototype uses only synthetic, non-sensitive data. It demonstrates a small end-to-end workflow for generating benign time-series signals, fitting a baseline anomaly detector, scoring new observations, attaching lightweight explanations, and saving outputs for review. The emphasis is on careful scoping, privacy-aware design choices, and evaluation thinking rather than deployment.

## Status

This is an early prototype. It is intentionally small, non-operational, and incomplete. The point is to show a serious start: a working baseline, explicit safety framing, and a concrete path for deeper research if resources become available.

## Why This Project Exists

Public-health preparedness often depends on noticing weak signals before they become obvious. That sounds straightforward, but in practice it raises hard questions about privacy, governance, interpretability, and overclaiming. A system that produces alerts without clear reasoning, clear boundaries, or clear data provenance is not especially helpful.

This project exists to explore a safer starting point:

- synthetic or clearly public non-sensitive data only
- interpretable alert logic instead of opaque scoring
- privacy-aware defaults from the outset
- evaluation and governance questions treated as first-class work

The goal is not to build an operational monitoring platform. The goal is to create a careful research scaffold for studying what a responsible early-warning workflow could look like.

## Why Cautious Early Public-Health Signal Monitoring Could Be Useful

Benign early-warning-style analytics can be useful for preparedness research because they help clarify:

- what kinds of broad aggregate signals are even worth monitoring
- how much transparency is needed for analysts to trust an alert
- what privacy-preserving design choices should be built in early
- how to evaluate false alarms, missed events, and deployment boundaries

Even a small prototype can be useful if it makes these questions concrete.

## Why Privacy, Governance, and Interpretability Matter

For this kind of work, model quality is only one part of the problem. Privacy, governance, and interpretability matter because:

- public-health signal work can drift into collecting more detail than is justified
- uninterpretable alerts are hard to assess or contest
- weak governance can encourage misuse or scope creep
- a research prototype should make its limits visible rather than hiding them

This repository therefore keeps the technical design modest and the documentation explicit.

## What This Prototype Currently Does

- generates synthetic daily public-health-style signals with a few benign anomalous periods
- fits a simple robust baseline using reference-window medians and median absolute deviations
- produces a scalar risk score and alert flag for each day
- attaches a short explanation field showing the strongest contributors to each alert
- saves predictions to CSV and creates one lightweight plot
- includes project-scope, safety, and grant-use notes

## What It Explicitly Does Not Do

- use private patient data or individual-level surveillance data
- provide medical advice or clinical decision support
- operate as a real-world monitoring system
- perform pathogen-specific modelling or biological optimisation
- support laboratory work, wet-lab design, or offensive capability development
- perform exploit identification, red-team analysis, or adversarial misuse work

## Why The Project Is Intentionally Narrow

This first pass is narrow on purpose. A broader system would need much stronger evaluation, careful governance, better uncertainty handling, and expert review. Starting small makes it easier to inspect assumptions, document boundaries, and avoid implying capabilities that do not yet exist.

## Current Prototype Scope

This first version currently focuses on:

- synthetic or public non-sensitive data only
- basic anomaly detection baselines
- interpretable outputs
- privacy-aware design choices
- evaluation thinking rather than deployment
- responsible scoping and documentation

## Example Workflow

```mermaid
flowchart LR
    accTitle: Prototype Workflow
    accDescr: Synthetic signals are generated, a simple baseline is fit, risk scores are computed, explanations are attached, and outputs are saved for review.

    synth_data["Synthetic Signals<br/>daily aggregated indicators"]
    baseline["Baseline Fit<br/>robust medians and dispersion"]
    scoring["Scoring<br/>risk score and alert flag"]
    explain["Interpretability<br/>top contributing features"]
    outputs["Outputs<br/>CSV, plot, evaluation summary"]
    docs["Docs<br/>scope, safety, grant plan"]

    synth_data --> baseline
    baseline --> scoring
    scoring --> explain
    explain --> outputs
    baseline --> docs

    classDef data fill:#e0f2fe,stroke:#0369a1,stroke-width:1.5px,color:#0f172a
    classDef model fill:#ecfccb,stroke:#4d7c0f,stroke-width:1.5px,color:#1f2937
    classDef out fill:#fef3c7,stroke:#b45309,stroke-width:1.5px,color:#1f2937

    class synth_data data
    class baseline,scoring,explain model
    class outputs,docs out
```

1. Generate a small synthetic dataset of daily aggregate indicators.
2. Fit a deliberately simple baseline on an initial reference window.
3. Score each day with a transparent anomaly score.
4. Attach a short explanation based on the largest standardized deviations.
5. Save predictions, a plot, and a basic evaluation summary.

## Sample CLI Usage

```bash
python3 -m src.generate_data
python3 -m src.train_baseline
python3 -m src.score_signals
python3 -m src.evaluate
```

The repository already includes sample outputs generated from this workflow.

## Reproducibility

The demo is meant to be rerunnable in a few commands from a clean checkout:

```bash
python3 -m src.generate_data
python3 -m src.train_baseline
python3 -m src.score_signals
python3 -m src.evaluate
```

If you rerun the pipeline with the default seed, it will regenerate the synthetic dataset, baseline summary, predictions CSV, plot, and evaluation summary shipped in the repository.

## Current Sample Output

The checked-in sample run is intentionally modest:

- 180 synthetic daily rows
- 13 alert days flagged
- precision `1.00` and recall `0.54` against synthetic labels only

Those figures are included as a transparent demo artifact, not as a claim about real-world performance.

## Repository Structure

```text
privacy-safe-ai-public-health-signal-monitoring/
├── data/
│   └── synthetic_signals.csv
├── docs/
│   ├── grant_use_plan.md
│   ├── project_scope.md
│   └── safety_note.md
├── notebooks/
│   └── exploratory_demo.ipynb
├── outputs/
│   ├── baseline_summary.json
│   ├── evaluation_summary.json
│   ├── sample_plot.png
│   └── sample_predictions.csv
├── src/
│   ├── __init__.py
│   ├── evaluate.py
│   ├── generate_data.py
│   ├── score_signals.py
│   ├── train_baseline.py
│   └── utils.py
├── .gitignore
├── LICENSE
├── pyproject.toml
├── README.md
└── requirements.txt
```

## Roadmap

- improve evaluation beyond a single synthetic scenario
- compare several benign baseline methods
- add uncertainty estimates and alert calibration checks
- prototype a small review-oriented dashboard
- expand interpretability outputs without increasing operational scope
- test on better public benchmark-style datasets where appropriate
- formalize governance, documentation, and deployment boundaries

## Done So Far / Next Steps

### Done so far

- [x] defined project scope
- [x] built synthetic data generator
- [x] implemented first baseline model
- [x] created initial scoring pipeline
- [x] added sample outputs
- [x] wrote safety framing
- [x] set up repo structure

### Next

- [ ] improve evaluation metrics
- [ ] compare multiple benign baselines
- [ ] add uncertainty estimates
- [ ] prototype a simple dashboard
- [ ] expand interpretability methods
- [ ] test on better public benchmark-style datasets
- [ ] formalize governance and evaluation criteria
- [ ] document deployment boundaries
- [ ] seek expert feedback

### Grant-enabled

- [ ] run larger safe experiments
- [ ] improve reproducibility
- [ ] host a demo
- [ ] improve documentation and usability
- [ ] create a stronger public research artifact

## Grant-Enabled Next Steps

With modest support, the next stage would focus on making the work more rigorous and more reproducible rather than making stronger claims.

- run larger safe experiments on synthetic and appropriate public datasets
- improve reproducibility, experiment tracking, and evaluation infrastructure
- support project-specific software or tooling where justified
- host a lightweight demo or dashboard if that becomes useful
- improve public-facing documentation and usability
- turn the prototype into a stronger, inspectable research artifact

## What Grant Support Would Unlock

Grant support would mainly accelerate the infrastructure around the research:

- compute for larger but still safe experiments on non-sensitive datasets
- project-specific software or tooling where justified
- lightweight hosting for a simple demo/dashboard if developed
- access to legitimate research resources where appropriate
- reproducibility and evaluation infrastructure for cleaner iteration

This is framed as project support, not as a claim that the current prototype is already deployment-ready.

## Safety and Responsible Use Note

This repository is intended for defensive public-health preparedness research only. It uses synthetic or clearly public non-sensitive data and deliberately avoids operational surveillance, pathogen-specific work, laboratory assistance, exploit discovery, or other harmful capability development. Future expansion should remain within careful privacy, governance, and responsible research boundaries, with expert review where needed.

See [docs/safety_note.md](docs/safety_note.md) for the short project note.

## Limitations

- the data are synthetic, so performance numbers are only sanity checks
- the baseline is intentionally simple and should not be mistaken for a validated system
- the explanations are lightweight heuristic summaries, not full causal analysis
- this repository is aimed at research scoping, not deployment
- the current operating threshold is a hand-set demo default, not a tuned decision rule

## Potential Research Relevance

This work overlaps with broader interests in multimodal health AI methods, interpretable modelling, privacy-aware analytics, and safe deployment practices. In that sense, it is meant to be a modest but concrete starting point for a more mature research program, not a finished platform.

## Contact / Collaboration

Maintainer: R Zuberi  
Collaboration placeholder: issues and thoughtful feedback are welcome, especially on evaluation design, interpretability, privacy-preserving approaches, and responsible scoping.
