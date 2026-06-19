# Experimentation Lab

## Problem

Product teams run A/B tests and make ship/no-ship decisions without checking whether the data is trustworthy. Sample ratio mismatch, underpowered samples, and wrong test choice lead to false positives and missed wins.

## Approach

End-to-end experimentation workflow: create experiments, simulate traffic, analyze results.

- **Assignment:** SHA-256 hash of `user_id + experiment_id` maps users to control/variant deterministically (no server-side state per user).
- **Metrics:** Conversion rate and revenue per user, with absolute and relative lift.
- **Stats:** Two-proportion z-test for conversion; Welch t-test for revenue.
- **Guardrails:** Chi-square sample ratio mismatch check (critical value 3.84); sample-size adequacy check against a 10% MDE at 80% power.

## Impact / Metric

Primary metric is selectable at experiment creation: conversion rate or revenue per user. The analyze view reports lift, p-values, and 95% confidence intervals.

**Result:** TODO - demo uses synthetic simulation, not production experiment outcomes.

## Tech Stack

Streamlit, Pandas, NumPy, SciPy, Plotly, SQLite

## How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
pytest tests/ -v
```

## Live Demo

https://x-lab-argon.streamlit.app/

## Design Decisions

- **SHA-256 assignment:** Same user always lands in the same variant for a given experiment, without storing per-user assignment records.
- **SRM before lift:** If traffic split is broken, lift numbers are meaningless; flag it first.
- **Separate tests for conversion vs revenue:** Binary outcome needs a proportion test; continuous revenue needs a t-test.
