# DevSecOps LLM Integration

An intelligent DevSecOps tool powered by OpenAI's LLM that performs automated security code reviews and interprets security scan results.

## Features

- **Automated Security Code Review**: Analyze code for vulnerabilities, security risks, and OWASP Top 10 issues
- **Security Scan Interpretation**: Parse and interpret SAST, DAST, and dependency check results
- **Finding Prioritization**: Prioritize security findings by risk and remediation effort
- **Multi-language Support**: Review code in multiple programming languages
- **Actionable Recommendations**: Get remediation guidance and best practices suggestions

## Project Structure

```
LLM Proj/
├── src/
│   ├── __init__.py
│   ├── config.py              # Configuration management
│   ├── code_reviewer.py       # Security code review module
│   ├── scan_interpreter.py    # Security scan interpretation module
│   └── main.py                # CLI entry point
├── tests/                      # Unit tests
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
└── README.md                  # This file
```

## Installation

### Prerequisites
- Python 3.8+
- OpenAI API key

### Setup

1. **Clone or navigate to the project**
   ```bash
   cd "/home/xyz/main/LLM Proj"
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

## Usage

### Security Code Review

The project supports both LLM mode (`--mode llm`) and local heuristic mode (`--mode local`).

**Review a file (LLM mode):**
```bash
python -m src.main review --code path/to/file.py --language python --mode llm
```

**Review a file (local mode):**
```bash
python -m src.main review --code path/to/file.py --language python --mode local
```

**Review code from stdin:**
```bash
python -m src.main review --code "def login(user, pwd): db.execute(f'SELECT * FROM users WHERE username={user}')" --language python --context "Login function"
```

**Save output to file:**
```bash
python -m src.main review --code path/to/file.py --language python --output review_result.json
```

### Interpret Security Scan Results

**Interpret SAST scan results (LLM):**
```bash
python -m src.main interpret --scan-file sast_output.txt --scan-type sast --mode llm
```

**Interpret SAST scan results (local):**
```bash
python -m src.main interpret --scan-file sast_output.txt --scan-type sast --mode local
```

**Interpret dependency check (local):**
```bash
python -m src.main interpret --scan-file dependencies.json --scan-type dependency --context "Production environment" --mode local
```

### Prioritize Security Findings

**Prioritize findings (LLM):**
```bash
python -m src.main prioritize --findings-file findings.txt --output priorities.json --mode llm
```

**Prioritize findings (local):**
```bash
python -m src.main prioritize --findings-file findings.txt --output priorities.json --mode local
```

## Environment Variables

Create a `.env` file based on `.env.example`:

```
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4                        # or gpt-3.5-turbo
LOG_LEVEL=INFO
MAX_TOKENS=2000
TEMPERATURE=0.7
```

## API Usage

### Code Review Example

```python
from src.code_reviewer import SecurityCodeReviewer

reviewer = SecurityCodeReviewer()
result = reviewer.review_code(
    code="SELECT * FROM users WHERE id = " + user_input,
    language="python",
    context="Database query handler"
)

print(result["review"])
```

### Scan Interpretation Example

```python
from src.scan_interpreter import SecurityScanInterpreter

interpreter = SecurityScanInterpreter()

# Read scan output
with open("scan_results.txt") as f:
    scan_output = f.read()

result = interpreter.interpret_scan_results(
    scan_output,
    scan_type="sast",
    context="API microservice"
)

print(result["interpretation"])
```

### Batch Operations

```python
# Review multiple files
files = [
    {"path": "app.py", "code": code1, "language": "python"},
    {"path": "main.js", "code": code2, "language": "javascript"}
]
results = reviewer.batch_review_files(files)
```

## Configuration

### OpenAI Models

- `gpt-4`: Most capable, recommended for comprehensive analysis
- `gpt-3.5-turbo`: Faster, more cost-effective

### Temperature Settings

- `0.0-0.3`: Deterministic, consistent results (recommended for security reviews)
- `0.7-1.0`: More creative, varied responses

## Security Considerations

- Store your OpenAI API key securely in `.env` file (never commit to version control)
- Add `.env` to `.gitignore`
- Review AI-generated recommendations before applying to production
- Use for supplementary analysis alongside established security tools

## Supported Scan Types

- `sast`: Static Application Security Testing
- `dast`: Dynamic Application Security Testing
- `dependency`: Dependency vulnerability scanning
- `container`: Container/image scanning
- `generic`: Generic security findings

## Limitations

- Requires valid OpenAI API key with appropriate quota
- Rate limited by OpenAI API
- LLM models may have hallucinations; recommendations should be verified
- Large code files may require multiple API calls

## Future Enhancements

- [ ] Integration with popular SAST/DAST tools (SonarQube, Snyk, etc.)
- [ ] Custom security policies and rules
- [ ] Remediation automation workflows
- [ ] Security metrics dashboard
- [ ] Collaboration features for security teams
- [ ] Fine-tuned models for specific security domains

## License

MIT

## Support

For issues and questions, please reference the project documentation.
