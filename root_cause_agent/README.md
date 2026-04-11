# Root Cause Agent

The Root Cause Agent is the diagnostic layer of the Autonomous Operations Intelligence System.

It ingests downtime event data, detects recurring operational patterns, and generates structured root-cause hypotheses with action-oriented diagnostic outputs.

---

## Project Overview

Manual downtime analysis is often reactive, fragmented, and time-consuming. This project explores how operational data can be transformed into a structured diagnostic system that assists in identifying recurring issues and guiding decision-making.

The Root Cause Agent simulates how production events can be interpreted through system logic to provide clarity on what is happening, why it is happening, and what should be done next.

---

## Role in System Architecture

This project represents the **Diagnostic Layer** in the overall Autonomous Operations Intelligence System:

Incident Data  
↓  
Root Cause Agent (Project 1)  
↓  
Risk & Prioritization Layer (Project 2)  
↓  
Action & Execution Layer (Project 3)  

The Root Cause Agent focuses on interpreting operational events, identifying recurring patterns, and generating structured diagnostic insights. It provides the foundational understanding required for downstream systems to prioritize and act effectively.

## What the Agent Does

The pipeline:

1. Loads downtime event data from CSV  
2. Cleans and enriches the data using:
   - machine context  
   - reason classification logic  
   - derived time-based features  
3. Detects patterns such as:
   - recurring issues  
   - top downtime loss drivers  
   - short-stop clusters  
   - symptom-source relationships  
4. Assigns:
   - priority score  
   - priority classification  
   - suggested owner  
   - urgency level  
   - recommended action type  
5. Generates:
   - diagnostic brief (`.txt`)  
   - pattern table (`.csv`)  
   - run log (`.json`)  

---

## Example Business Value

This system helps answer key operational questions:

- What issue is recurring most frequently?  
- Which issues are driving the most downtime loss?  
- Is this a true root cause or a downstream symptom?  
- Who should own the issue?  
- How urgent is the response?  
- What type of action should be taken next?  

---

## Inputs

Located in `data/raw/`:

- `downtime_events.csv`  
- `machine_context.csv`  
- `reason_dictionary.csv`  

---

## Outputs

Located in `data/outputs/`:

- `diagnostic_brief.txt`  
- `pattern_table.csv`  
- `run_log.json`  

---

## Project Structure

```text
root_cause_agent/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── outputs/
│
├── src/
│   ├── config.py
│   ├── data_loader.py
│   ├── preprocess.py
│   ├── pattern_detector.py
│   ├── triage_engine.py
│   ├── report_generator.py
│   └── utils.py
│
├── requirements.txt
├── main.py
└── README.md

Core Capabilities
Recurring issue detection
Downtime loss ranking
Short-stop clustering
Symptom-source linkage
Rule-based root-cause hypothesis generation
Owner and urgency classification
Action-type recommendation
Structured output generation for both humans and downstream systems
Example Logic

Examples of reasoning used in the system:

Infeed Starved is treated as a downstream symptom rather than a root cause
Bearing Seizure is classified as a high-severity mechanical failure requiring immediate maintenance attention
Minor Stop patterns are identified as chronic nuisance losses
Operator Adjustments may indicate underlying issues being temporarily managed
Belt Slip suggests developing conveyor or drive-related degradation
Mechanical Failure triggers immediate escalation and ownership assignment
Tech Stack
Python
pandas
pathlib
JSON / CSV / TXT outputs
How to Run
1. Install dependencies
pip install -r requirements.txt
2. Run the project
python main.py
Example Output

The system generates a diagnostic brief containing:

run metadata
executive summary
top priority issue
top recurring issues
symptom-source relationships
likely root-cause hypotheses
recommended actions
Why This Project Matters

This project demonstrates how operational event data can be transformed into a structured diagnostic system rather than a static reporting layer.

It highlights how real-world production data can support faster diagnosis, clearer ownership, and more consistent, action-oriented decision-making.

Future Improvements

Potential enhancements include:

Streamlit interface for interactive exploration
SQL or SharePoint integration
LLM-based reasoning layer
visualization of trends and patterns
integration with maintenance history
spare parts and inventory linkage
closed-loop tracking of issue resolution
Author

Built by Nisha Puri