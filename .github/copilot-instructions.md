# DevSecOps LLM Integration - Copilot Instructions

## Project Overview

This is a DevSecOps-focused LLM integration project that uses OpenAI to perform:
1. Automated security code reviews
2. Interpretation of security scan results (SAST, DAST, dependency checks)

## Tech Stack

- **Language**: Python 3.8+
- **LLM Provider**: OpenAI (GPT-4 / GPT-3.5-turbo)
- **Framework**: Native Python with OpenAI SDK
- **Key Dependencies**: openai, python-dotenv, pydantic, requests

## Project Structure

- `/src/` - Main application code
  - `config.py` - Configuration and environment management
  - `code_reviewer.py` - Security code review functionality
  - `scan_interpreter.py` - Security scan interpretation functionality
  - `main.py` - CLI interface
- `/tests/` - Unit tests
- `.env.example` - Environment variables template
- `requirements.txt` - Python dependencies

## Development Workflow

1. **Setup**: Install dependencies with `pip install -r requirements.txt`
2. **Configuration**: Copy `.env.example` to `.env` and add OpenAI API key
3. **Development**: Modify modules in `src/`
4. **Testing**: Run tests with `pytest tests/`
5. **CLI Usage**: Run with `python -m src.main <command>`

## Key Capabilities

### Code Review
- Analyzes Python, JavaScript, Java, and other languages
- Detects OWASP Top 10 vulnerabilities
- Provides remediation suggestions
- Batch processing support

### Scan Interpretation
- Parses SAST/DAST/dependency scan results
- Prioritizes findings by severity and impact
- Provides executive summary and remediation roadmap
- Supports multiple scan tool formats

### Prioritization
- Risk-based prioritization matrix
- Effort estimation
- Quick wins identification
- Roadmap generation

## Important Notes

- **API Key**: Must be set in `.env` before running
- **Cost**: Each operation uses OpenAI API credits
- **Rate Limits**: Subject to OpenAI API rate limits
- **Accuracy**: AI recommendations should be verified before production use

## Commands for Common Tasks

- **Code Review**: `python -m src.main review --code <file> --language <lang>`
- **Interpret Scans**: `python -m src.main interpret --scan-file <file> --scan-type <type>`
- **Prioritize**: `python -m src.main prioritize --findings-file <file>`

## Extension Points

- Add new scan type handlers in `SecurityScanInterpreter`
- Add new code review analyzers in `SecurityCodeReviewer`
- Integrate with external security tools
- Implement persistent storage for results
- Build web UI for visualization
