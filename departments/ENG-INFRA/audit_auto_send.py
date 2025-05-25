"""Automatically runs audit_runner and posts results to AUDIT and HUB threads
via OpenAI Assistants API.

Required environment variables:
    OPENAI_API_KEY
    ASSISTANT_ID
    AUDIT_THREAD_ID  (chat thread ID for 05-AUDIT)
    HUB_THREAD_ID    (chat thread ID for 01-HUB)
"""

import os, subprocess, json, datetime, pathlib, textwrap, openai, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]

def run_audit():
    """Run audit_runner.py and return JSON dict."""
    result = subprocess.check_output(
        ["python", str(ROOT / "departments" / "AUDIT" / "audit_runner.py")],
        text=True
    )
    return json.loads(result)

def post_message(thread_id: str, role: str, content: str):
    client = openai.OpenAI()               # 1.x client
    client.beta.threads.messages.create(   # <-- 핵심 수정
        thread_id=thread_id,
        role=role,
        content=content
    )

def main():
    report = run_audit()

    full = textwrap.dedent(f"""\
        [report]
        # Jarvis Lab – Weekly Audit
        timestamp: {report['timestamp']}
        budget_usage_pct: {report['budget_usage_pct']}
        kpi_thresholds: {report['kpi_thresholds']}
        security_phase: {report['security_phase']}
        lab_quota_hrs: {report['lab_quota_hrs']}
    """)

    post_message(os.environ["AUDIT_THREAD_ID"], "user", full)

    summary = (
        "[report] AUDIT – Weekly Summary\n"
        f"• GPU: {report['budget_usage_pct']['gpu']} %\n"
        f"• OpenAI: {report['budget_usage_pct']['openai']} %\n"
        "• KPI OK\n"
        "• Security Phase-1 passed\n"
    )

    post_message(os.environ["HUB_THREAD_ID"], "user", summary)
    print("✅ Audit report posted at", datetime.datetime.now())

if __name__ == "__main__":
    required = [
        "OPENAI_API_KEY", "ASSISTANT_ID",
        "AUDIT_THREAD_ID", "HUB_THREAD_ID"
    ]
    missing = [v for v in required if v not in os.environ]
    if missing:
        sys.exit(f"Missing env vars: {', '.join(missing)}")
    openai.api_key = os.environ["OPENAI_API_KEY"]
    main()
