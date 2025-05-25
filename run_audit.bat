@echo off
REM Jarvis Lab Corp - Weekly Audit Runner
REM Auto-generated on 2025-05-25

cd /d "%~dp0"
python departments\AUDIT\audit_runner.py > audit_report.txt
notepad audit_report.txt
