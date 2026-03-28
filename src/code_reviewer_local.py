"""Security code review module using local heuristic checks (no LLM)."""

import re


class LocalSecurityCodeReviewer:
    """Performs security code review using local heuristics."""

    def review_code(self, code: str, language: str = "python", context: str = "") -> dict:
        """Analyze code for common security patterns and return structured findings."""
        findings = []

        # Insecure patterns and practices
        if re.search(r"\b(eval|exec)\b", code):
            findings.append({
                "severity": "Critical",
                "issue": "Dynamic code execution (eval/exec)",
                "recommendation": "Avoid eval/exec; use safe parsers or built-in behavior."
            })

        if re.search(r"(SELECT|UPDATE|DELETE|INSERT).*\+.*", code, re.IGNORECASE):
            findings.append({
                "severity": "High",
                "issue": "Possible SQL concatenation",
                "recommendation": "Use parameterized queries or ORM with escaping."
            })

        if re.search(r"password\s*=\s*['\"][^'\"]+['\"]", code, re.IGNORECASE):
            findings.append({
                "severity": "High",
                "issue": "Hardcoded credentials",
                "recommendation": "Use environment variables or secret store."
            })

        if re.search(r"api[_-]?key\s*=\s*['\"][^'\"]+['\"]", code, re.IGNORECASE):
            findings.append({
                "severity": "High",
                "issue": "Hardcoded API key",
                "recommendation": "Use secure configuration management for secrets."
            })

        if re.search(r"request\.GET\(|request\.POST\(|axios\.get\(|fetch\(", code):
            findings.append({
                "severity": "Medium",
                "issue": "HTTP API call without explicit timeout or error handling",
                "recommendation": "Add timeout and retries."
            })

        if re.search(r"crypto\.random|Random\(|secret", code, re.IGNORECASE):
            findings.append({
                "severity": "Medium",
                "issue": "Potential weak random or secret handling",
                "recommendation": "Use cryptographic libraries and secure storage."
            })

        if not findings:
            findings.append({
                "severity": "Low",
                "issue": "No suspicious patterns detected by local analyzer",
                "recommendation": "Perform in-depth static analysis with SAST tools for better coverage."
            })

        return {
            "status": "success",
            "mode": "local",
            "context": context or "N/A",
            "language": language,
            "findings": findings,
            "summary": f"{len(findings)} issues found"
        }

    def batch_review_files(self, files: list) -> list:
        """Review multiple files with local heuristic scanner."""
        results = []
        for file_info in files:
            out = self.review_code(
                file_info.get("code", ""),
                file_info.get("language", "python"),
                file_info.get("path", "")
            )
            results.append({
                "file": file_info.get("path"),
                "result": out
            })
        return results
