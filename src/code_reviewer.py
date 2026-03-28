"""Security code review module using OpenAI LLM."""

from openai import OpenAI
from src.config import Config


class SecurityCodeReviewer:
    """Performs automated security code reviews using LLM."""
    
    def __init__(self):
        """Initialize the code reviewer with OpenAI client."""
        Config.validate()
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.model = Config.OPENAI_MODEL
        self.max_tokens = Config.MAX_TOKENS
        self.temperature = Config.TEMPERATURE
    
    def review_code(self, code: str, language: str = "python", context: str = "") -> dict:
        """
        Perform security review on provided code.
        
        Args:
            code: The source code to review
            language: Programming language of the code
            context: Additional context about the code (e.g., file path, function purpose)
            
        Returns:
            Dictionary containing vulnerabilities, risks, and recommendations
        """
        prompt = self._build_review_prompt(code, language, context)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert security code reviewer. Analyze code for vulnerabilities, security risks, and best practices. Provide actionable recommendations."
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
                "review": response.choices[0].message.content,
                "tokens_used": response.usage.total_tokens
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "review": None
            }
    
    def _build_review_prompt(self, code: str, language: str, context: str) -> str:
        """Build the review prompt for LLM."""
        prompt = f"""
Please perform a comprehensive security code review for the following {language} code:

Context: {context if context else "N/A"}

Code:
```{language}
{code}
```

Analyze for:
1. Security vulnerabilities (OWASP Top 10, CWE)
2. Authentication/Authorization issues
3. Data exposure risks
4. Input validation problems
5. Error handling flaws
6. Best practices violations

For each issue found:
- Severity (Critical, High, Medium, Low)
- Description
- Location (line numbers if applicable)
- Recommended fix
- Example of secure code (if applicable)

Format your response as a structured security report.
"""
        return prompt
    
    def batch_review_files(self, files: list) -> list:
        """
        Review multiple files.
        
        Args:
            files: List of dicts with 'path', 'code', and 'language' keys
            
        Returns:
            List of review results
        """
        results = []
        for file_info in files:
            result = self.review_code(
                file_info["code"],
                file_info.get("language", "python"),
                file_info.get("path", "")
            )
            results.append({
                "file": file_info.get("path"),
                "result": result
            })
        return results
