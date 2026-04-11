# Action Engine

The Action Engine is the orchestration and decision layer of the Autonomous Operations Intelligence System.

It takes structured incident inputs such as likely cause, risk score, confidence level, and recommended action, then generates a human-readable and machine-structured Action Memo for frontline response.

## Purpose

The goal of this project is to reduce cognitive load during equipment incidents by turning raw diagnostic and prioritization signals into clear next-step recommendations.

Instead of requiring an operator or technician to interpret multiple data points manually, the Action Engine produces a grounded response that includes:

- incident summary
- likely cause
- recommended action
- required parts
- estimated time to fix
- status classification
- escalation guidance
- evidence trail

## Question this project answers

**“Given the diagnosis and priority, what should the system recommend, trigger, or escalate next?”**

This makes the Action Engine the final decision layer in the broader system.

## Status logic

The engine classifies each incident into one of three modes:

- **ACT**  
  High-confidence match. A clear SOP-aligned action can be taken.

- **INSPECT**  
  Moderate-confidence match. A technician should verify the condition before replacing parts or taking further action.

- **ESCALATE**  
  Low-confidence match. The pattern does not strongly align to known SOPs and should be escalated to a maintenance lead or SME.

## Key design choices

### 1. Explainable outputs
The project does not produce an open-ended chatbot response. It generates a structured action memo with clearly defined fields.

### 2. Externalized configuration
Thresholds such as `ACT`, `INSPECT`, and `ESCALATE` are stored in `config/settings.json` so the system can be tuned without changing source code.

### 3. Guardrailed reasoning
The Action Engine is designed to support constrained reasoning. In a fuller production version, recommendations would be restricted to verified SOP-aligned actions and known repair patterns.

### 4. Feedback loop support
Operators can submit feedback on whether a recommendation was helpful. This allows the system to capture real-world correction signals for future refinement.

## How this fits into the full system

This module is Project 3 of the Autonomous Operations Intelligence System:

- **Project 1 — Root Cause Agent**  
  Identifies likely causes of downtime events.

- **Project 2 — Risk Engine**  
  Determines which issues should be addressed first.

- **Project 3 — Action Engine**  
  Converts those structured signals into a clear action memo for response, inspection, or escalation.

The overall flow is:

**incident signal → likely cause → risk priority → action recommendation**

## Folder structure

```text
action_engine/
├── README.md
├── main.py
├── config/
│   ├── settings.json
│   └── prompt_templates.json
├── data/
│   └── sample_incidents.json
├── outputs/
│   ├── operator_feedback.json
│   └── sample_action_memos.json
└── src/
    └── action_engine.py

Input

The engine reads from:

data/sample_incidents.json

Each incident contains fields such as:

incident_id
machine_id
summary
risk_score
likely_cause
recommended_action
required_parts
estimated_time_to_fix_minutes
confidence
evidence
Output
Action memos

Generated memos are written to:

outputs/sample_action_memos.json

Each memo includes fields such as:

incident_id
machine_id
summary
risk_score
likely_cause
recommended_action
required_parts
estimated_time_to_fix_minutes
status
mode_reason
escalation_target
confidence
evidence
generated_at
Operator feedback

Feedback records are written to:

outputs/operator_feedback.json

This supports future analysis of whether recommendations were useful, partially helpful, or incorrect.

How to run

From inside the action_engine folder:

python main.py

If needed, use:

py main.py
Example workflow
The engine reads a batch of sample incidents.
It determines whether each incident should be classified as ACT, INSPECT, or ESCALATE.
It generates a structured action memo for each incident.
It writes those memos to the outputs folder.
It saves a sample operator feedback record to demonstrate the feedback loop.
Why this matters

Many operational teams rely on fragmented spreadsheets, tribal knowledge, and reactive troubleshooting. This project shows how a constrained reasoning layer can convert incident data into actionable, explainable next steps while preserving safety and escalation discipline.
