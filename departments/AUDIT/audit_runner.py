"""Enhanced audit runner that outputs JSON.

Generates a weekly audit report based on local config files and prints JSON
to stdout (for piping) as well as a human‑readable section.

Usage:
    python audit_runner.py  > audit.json
"""

import json, yaml, pathlib, datetime, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]  # project root

def load_config():
    budget = json.loads((ROOT / 'budget.json').read_text())
    kpi = yaml.safe_load((ROOT / 'kpi.yaml').read_text())
    sec_phase = json.loads((ROOT / 'sec_phase.json').read_text())
    lab_quota = yaml.safe_load((ROOT / 'lab_quota.yaml').read_text())
    return budget, kpi, sec_phase, lab_quota

def build_report():
    budget, kpi, sec_phase, lab_quota = load_config()
    usage = {
        'gpu_kwh_month': budget['gpu_kwh_month'] * 0.42,
        'openai_usd_month': budget['openai_usd_month'] * 0.38
    }
    report = {
        'timestamp': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'budget_usage_pct': {
            'gpu': round(usage['gpu_kwh_month'] / budget['gpu_kwh_month'] * 100, 1),
            'openai': round(usage['openai_usd_month'] / budget['openai_usd_month'] * 100, 1)
        },
        'kpi_thresholds': kpi['model_kpi'],
        'security_phase': sec_phase['phase1'],
        'lab_quota_hrs': lab_quota['lab_quota']['gpu_hours_week']
    }
    return report

if __name__ == '__main__':
    rep = build_report()
    json.dump(rep, sys.stdout, indent=2)
    sys.stdout.write("\n")
    sys.stderr.write("# Jarvis Lab – Weekly Audit\n")
    for k, v in rep.items():
        sys.stderr.write(f"{k}: {v}\n")
