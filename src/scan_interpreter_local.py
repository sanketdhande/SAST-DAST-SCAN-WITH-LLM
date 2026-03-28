"""Security scan interpretation module using local heuristics (no LLM)."""

import re


class LocalSecurityScanInterpreter:
    """Interprets security scan results using local rule-based heuristics."""

    def interpret_scan_results(self, scan_output: str, scan_type: str = "generic", context: str = "") -> dict:
        """Interpret scan output and produce a basic prioritized report."""
        if not scan_output or not scan_output.strip():
            return {
                "status": "error",
                "error": "Scan output is empty",
                "interpretation": None,
                "mode": "local"
            }

        lines = [line.strip() for line in scan_output.splitlines() if line.strip()]

        counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
        findings = []

        for line in lines:
            low = line.lower()
            if 'critical' in low or 'rce' in low or 'sql injection' in low:
                counts['critical'] += 1
                findings.append({"severity": "Critical", "detail": line})
            elif 'high' in low or 'xss' in low or 'auth bypass' in low:
                counts['high'] += 1
                findings.append({"severity": "High", "detail": line})
            elif 'medium' in low or 'sensitive' in low or 'info leak' in low:
                counts['medium'] += 1
                findings.append({"severity": "Medium", "detail": line})
            else:
                counts['low'] += 1
                findings.append({"severity": "Low", "detail": line})

        overall = "Low"
        if counts['critical'] > 0 or counts['high'] > 3:
            overall = "Critical"
        elif counts['high'] > 0 or counts['medium'] > 2:
            overall = "High"
        elif counts['medium'] > 0:
            overall = "Medium"

        quick_wins = [f"{f['severity']}: {f['detail']}" for f in findings if f['severity'] in ('High','Medium')][:5]

        interpretation = {
            "mode": "local",
            "context": context or "N/A",
            "scan_type": scan_type,
            "overall_risk": overall,
            "counts": counts,
            "top_findings": quick_wins or ['No immediate issues identified by heuristics'],
            "recommendations": [
                "Validate the scanner findings with tool-specific documentation.",
                "Address critical and high issues first.",
                "Regularly rerun scans after fixes.",
                "Consider integrating a full SAST/DAST toolchain.",
            ]
        }

        return {
            "status": "success",
            "interpretation": interpretation,
            "mode": "local"
        }

    def prioritize_findings(self, findings_text: str) -> dict:
        """Simple priority selection without LLM."""
        if not findings_text or not findings_text.strip():
            return {
                "status": "error",
                "error": "No findings provided",
                "prioritization": None,
                "mode": "local"
            }

        lines = [line.strip() for line in findings_text.splitlines() if line.strip()]
        priorities = []

        for line in lines:
            low = line.lower()
            if any(k in low for k in ['critical', 'rce', 'sql injection', 'auth bypass']):
                priorities.append((line, 'Critical', '8-16h'))
            elif any(k in low for k in ['high', 'xss', 'privilege escalation']):
                priorities.append((line, 'High', '4-8h'))
            elif any(k in low for k in ['medium', 'sensitive', 'info leak']):
                priorities.append((line, 'Medium', '2-4h'))
            else:
                priorities.append((line, 'Low', '1-2h'))

        result_text = "\n".join([f"{sev}: {item} (est {effort})" for item, sev, effort in priorities])
        return {
            "status": "success",
            "prioritization": result_text,
            "mode": "local"
        }
