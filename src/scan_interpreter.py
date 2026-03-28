"""Security scan results interpreter using OpenAI LLM."""

from openai import OpenAI
from src.config import Config


class SecurityScanInterpreter:
    """Interprets security scan results (SAST, DAST, dependency checks)."""
    
    def __init__(self):
        """Initialize the scan interpreter with OpenAI client."""
        Config.validate()
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.model = Config.OPENAI_MODEL
        self.max_tokens = Config.MAX_TOKENS
        self.temperature = Config.TEMPERATURE
    
    def interpret_scan_results(self, scan_output: str, scan_type: str = "generic", context: str = "") -> dict:
        """
        Interpret security scan results.
        
        Args:
            scan_output: Raw output from security scanning tool
            scan_type: Type of scan (sast, dast, dependency, container, etc.)
            context: Additional context (project name, environment, etc.)
            
        Returns:
            Dictionary with interpreted findings, risk assessment, and remediation steps
        """
        prompt = self._build_interpretation_prompt(scan_output, scan_type, context)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert security analyst. Interpret security scan results, prioritize findings, assess business impact, and provide prioritized remediation guidance."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            return {
                "status": "success",
                "interpretation": response.choices[0].message.content,
                "scan_type": scan_type,
                "tokens_used": response.usage.total_tokens
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "interpretation": None
            }
    
    def _build_interpretation_prompt(self, scan_output: str, scan_type: str, context: str) -> str:
        """Build the interpretation prompt for LLM."""
        prompt = f"""
Please analyze and interpret the following {scan_type.upper()} security scan results:

Context: {context if context else "General application"}

Scan Output:
{scan_output}

Please provide:

1. **Executive Summary**: High-level overview of security posture (1-2 sentences)

2. **Risk Assessment**:
   - Overall risk level (Critical, High, Medium, Low)
   - Number of findings by severity
   - High-impact vulnerabilities

3. **Key Findings** (prioritized by severity and exploitability):
   - Vulnerability/Finding
   - Impact & Business Risk
   - Affected components
   - Remediation steps

4. **Immediate Actions** (next 24-48 hours):
   - Critical issues to address
   - Quick wins

5. **Medium-term Roadmap** (1-2 weeks):
   - Important but less critical fixes
   - Preventive measures

6. **False Positives**: Any likely false positives to investigate

7. **Metrics & Recommendations**:
   - Trend analysis if data available
   - Recommended tooling improvements
   - Process improvements

Format as a structured security report suitable for sharing with development and security teams.
"""
        return prompt
    
    def batch_interpret_scans(self, scans: list) -> list:
        """
        Interpret multiple scan results.
        
        Args:
            scans: List of dicts with 'output', 'type', and optional 'context' keys
            
        Returns:
            List of interpretation results
        """
        results = []
        for scan in scans:
            result = self.interpret_scan_results(
                scan["output"],
                scan.get("type", "generic"),
                scan.get("context", "")
            )
            results.append({
                "scan_id": scan.get("id", "unknown"),
                "result": result
            })
        return results
    
    def prioritize_findings(self, findings_text: str) -> dict:
        """
        Prioritize security findings by risk and effort.
        
        Args:
            findings_text: Formatted list of security findings
            
        Returns:
            Prioritized remediation roadmap
        """
        prompt = f"""
Based on these security findings, create a prioritization matrix and remediation roadmap:

Findings:
{findings_text}

Create a response with:
1. Quick Wins (high impact, low effort)
2. Strategic Initiatives (high impact, high effort)
3. Maintenance Tasks (low impact, low effort)
4. Future Consideration (low impact, high effort)

For each item, include:
- Finding description
- Estimated effort (hours)
- Risk reduction impact
- Owner recommendation (security/dev/devops)

Return as actionable priorities for the development team.
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a security prioritization expert. Help teams prioritize security work based on impact and effort."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            return {
                "status": "success",
                "prioritization": response.choices[0].message.content,
                "tokens_used": response.usage.total_tokens
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "prioritization": None
            }
