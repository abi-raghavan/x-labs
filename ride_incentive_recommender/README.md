# Ride Incentive Recommender

## Problem

Ride platforms often send the same discount to every rider. Per-rider incentive selection can raise booking probability without giving away margin on riders who would book anyway.

## Approach

Train a logistic regression model on synthetic rider history (rides, recency, trip value, promo acceptance). For a new rider profile, score four incentive options by adding fixed conversion lifts to the model's baseline booking probability, then pick the highest.

Incentive options: No Incentive, 10% Discount, 15% Discount, $5 Ride Credit.

## Impact / Metric

Expected conversion rate for the recommended incentive vs the no-incentive baseline.

**Result:** TODO - trained on synthetic data; no live A/B validation.

## Tech Stack

Streamlit, Pandas, NumPy, scikit-learn

## How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
pytest tests/ -v
```

## Live Demo

https://ride-signal-argon.streamlit.app/

## Design Decisions

- **Logistic regression over a deep model:** Small feature set, interpretable coefficients, fast to train at demo scale.
- **Fixed incentive lifts in the scoring loop:** Separates "will this rider book?" from "how much does this incentive help?" so the demo stays explainable without real uplift labels per incentive.
