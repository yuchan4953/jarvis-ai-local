# Jarvis Lab – Auto Audit Pipeline

**Generated**: 2025-05-23

This package adds full automation so that weekly audit reports generated
locally are posted to both the 05‑AUDIT and 01‑HUB chat threads
via the OpenAI Assistants API.

## Files

* `departments/AUDIT/audit_runner.py`  
  Generates a JSON report from local config (`budget.json`, `kpi.yaml`, etc.).

* `departments/ENG-INFRA/audit_auto_send.py`  
  Runs the audit, then publishes:
    1. Full `[report]` message to AUDIT thread  
    2. Concise summary to HUB thread

## Setup

```powershell
cd "C:\Users\MSI\Desktop\jarvis company lab"
python -m venv .venv
.venv\Scripts\activate
pip install openai pyyaml
```

Set required environment variables (PowerShell):

```powershell
$env:OPENAI_API_KEY   = "<your OpenAI API key>"
$env:ASSISTANT_ID     = "<assistant id of Jarvis Assistant>"
$env:AUDIT_THREAD_ID  = "<thread id for 05-AUDIT chat>"
$env:HUB_THREAD_ID    = "<thread id for 01-HUB chat>"
```

## Run

```powershell
python departments\ENG-INFRA\audit_auto_send.py
```

Automate by adding a Windows Task Scheduler job (weekly, Mon 09:25) or a cron job on Linux.

## Note
* The script assumes you are using the OpenAI **Assistants API** and already have threads set up for each chat tab.  
* If you're using a different chat platform, modify `post_message` accordingly.
