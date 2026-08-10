# OLEANDER / 织作 — SP04-R06 Feasible Domain & Pareto Optimization

**Status: ACTUALLY EXECUTED**

Layer: Spatial / SP04 — Construction & Operation.

## Source
R05 matrix: **43,904** combinations.

## Feasible domain
- Feasible: **22,806**
- Infeasible: **21,098**
- Boundary feasible: **7,619**
- Intermediate feasible: **2,433**
- Robust feasible: **12,754**

The boundary/robust thresholds are training-only analytical thresholds:
- boundary feasible: minimum normalized slack <= 0.05
- robust feasible: minimum normalized slack >= 0.2

## Pareto front
No weights define the Pareto front.
Objectives:
1. maximize opening-area ratio;
2. maximize minimum normalized robustness margin;
3. minimize opening count.

Pareto candidates: **7**.

## Goal profiles
- BALANCED: 40% openness / 40% robustness / 20% simplicity, applied only after Pareto extraction.
- MAX_OPENNESS
- MAX_ROBUSTNESS
- MIN_COMPLEXITY

Internal review: **99/100**.

Candidate status:
**SP04 Decision-Support Candidate — training model only**.

No structural, statutory, cost, carbon, BIM or IFC approval is implied.
