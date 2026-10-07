#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/src"
for f in 01_kpi_review 02_rwa_verification 03_omicron_impact 04_limits_monitoring; do echo "== $f"; python $f.py; done
