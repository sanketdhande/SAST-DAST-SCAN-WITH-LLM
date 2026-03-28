"""Main entry point for DevSecOps LLM integration application."""

import argparse
import sys
import json
from pathlib import Path

from src.code_reviewer import SecurityCodeReviewer
from src.scan_interpreter import SecurityScanInterpreter
from src.code_reviewer_local import LocalSecurityCodeReviewer
from src.scan_interpreter_local import LocalSecurityScanInterpreter


def main():
    """Main application entry point."""
    parser = argparse.ArgumentParser(
        description="DevSecOps LLM Integration - Security analysis and interpretation tool"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Code Review Command
    review_parser = subparsers.add_parser("review", help="Perform security code review")
    review_parser.add_argument("--code", required=True, help="Path to code file or code string")
    review_parser.add_argument("--language", default="python", help="Programming language")
    review_parser.add_argument("--context", default="", help="Additional context")
    review_parser.add_argument("--output", help="Output file path (JSON)")
    review_parser.add_argument("--mode", default="llm", choices=["llm", "local"], help="Review mode: llm or local")
    
    # Scan Interpretation Command
    scan_parser = subparsers.add_parser("interpret", help="Interpret security scan results")
    scan_parser.add_argument("--scan-file", required=True, help="Path to scan output file")
    scan_parser.add_argument("--scan-type", default="generic", 
                            choices=["sast", "dast", "dependency", "container", "generic"],
                            help="Type of security scan")
    scan_parser.add_argument("--context", default="", help="Additional context")
    scan_parser.add_argument("--output", help="Output file path (JSON)")
    scan_parser.add_argument("--mode", default="llm", choices=["llm", "local"], help="Interpretation mode: llm or local")
    
    # Prioritize Command
    prioritize_parser = subparsers.add_parser("prioritize", help="Prioritize security findings")
    prioritize_parser.add_argument("--findings-file", required=True, help="Path to findings file")
    prioritize_parser.add_argument("--output", help="Output file path (JSON)")
    prioritize_parser.add_argument("--mode", default="llm", choices=["llm", "local"], help="Prioritization mode: llm or local")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == "review":
        handle_review(args)
    elif args.command == "interpret":
        handle_interpret(args)
    elif args.command == "prioritize":
        handle_prioritize(args)


def handle_review(args):
    """Handle security code review command."""
    try:
        # Read code from file or use as string
        if Path(args.code).exists():
            with open(args.code, 'r') as f:
                code = f.read()
        else:
            code = args.code
        
        if args.mode == "local":
            reviewer = LocalSecurityCodeReviewer()
        else:
            reviewer = SecurityCodeReviewer()
        result = reviewer.review_code(code, args.language, args.context)
        
        output = {
            "command": "review",
            "language": args.language,
            "mode": args.mode,
            "status": result.get("status"),
            "review": result.get("review"),
            "findings": result.get("findings"),
            "error": result.get("error"),
            "tokens_used": result.get("tokens_used")
        }
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(output, f, indent=2)
            print(f"Review saved to {args.output}")
        else:
            print(json.dumps(output, indent=2))
            
    except Exception as e:
        print(f"Error during code review: {e}", file=sys.stderr)
        sys.exit(1)


def handle_interpret(args):
    """Handle scan interpretation command."""
    try:
        # Read scan output
        with open(args.scan_file, 'r') as f:
            scan_output = f.read()
        
        if args.mode == "local":
            interpreter = LocalSecurityScanInterpreter()
        else:
            interpreter = SecurityScanInterpreter()

        result = interpreter.interpret_scan_results(
            scan_output,
            args.scan_type,
            args.context
        )
        
        output = {
            "command": "interpret",
            "scan_type": args.scan_type,
            "mode": args.mode,
            "status": result.get("status"),
            "interpretation": result.get("interpretation"),
            "error": result.get("error"),
            "tokens_used": result.get("tokens_used")
        }
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(output, f, indent=2)
            print(f"Interpretation saved to {args.output}")
        else:
            print(json.dumps(output, indent=2))
            
    except Exception as e:
        print(f"Error during scan interpretation: {e}", file=sys.stderr)
        sys.exit(1)


def handle_prioritize(args):
    """Handle findings prioritization command."""
    try:
        # Read findings
        with open(args.findings_file, 'r') as f:
            findings = f.read()
        
        if args.mode == "local":
            interpreter = LocalSecurityScanInterpreter()
        else:
            interpreter = SecurityScanInterpreter()

        result = interpreter.prioritize_findings(findings)
        
        output = {
            "command": "prioritize",
            "mode": args.mode,
            "status": result.get("status"),
            "prioritization": result.get("prioritization"),
            "error": result.get("error"),
            "tokens_used": result.get("tokens_used")
        }
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(output, f, indent=2)
            print(f"Prioritization saved to {args.output}")
        else:
            print(json.dumps(output, indent=2))
            
    except Exception as e:
        print(f"Error during prioritization: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
