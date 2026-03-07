from __future__ import annotations
import argparse
import sys
from pathlib import Path
import yaml
from src.config.manager import load_config, load_project_version, merge_with_cli
from src.graph.pipeline import PipelineStatus, run_pipeline
from src.llm.client import create_chat_model
from src.report.generator import generate_report

def _load_prompt(name: str) -> str:
    return (Path(__file__).resolve().parent / "prompts" / f"{name}.md").read_text(encoding="utf-8")

def build_parser(version: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="agentic-converter-lc",
        description="Convert Jenkinsfiles to GitHub Actions YAML via a LangChain agentic loop.",
        epilog=(
            "Examples:\n"
            "  uv run python -m src.main .data/input/1/Jenkinsfile\n"
            "  uv run python -m src.main .data/input/ -n 3 -v\n"
            "  uv run python -m src.main --version"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("path", nargs="?", help="Jenkinsfile or directory containing Jenkinsfiles")
    parser.add_argument("-V", "--version", action="version", version=f"%(prog)s {version}")
    parser.add_argument("-o", "--output-dir", metavar="DIR", default=None, help="Output directory")
    parser.add_argument("-n", "--max-iterations", metavar="N", type=int, default=None,
                        help="Maximum converter-reviewer iterations")
    parser.add_argument("-v", "--verbose", action="store_true", default=None, help="Verbose output")
    return parser

def main() -> None:
    try:
        version = load_project_version()
        parser = build_parser(version)
        args = parser.parse_args()
    except Exception as exc:
        print(f"Error: failed to initialize CLI: {exc}", file=sys.stderr)
        sys.exit(1)
    if not args.path:
        parser.error("path is required unless using --help or --version")
    try:
        config = merge_with_cli(load_config(), vars(args))
    except Exception as exc:
        print(f"Error: failed to load configuration: {exc}", file=sys.stderr)
        sys.exit(1)
    input_path = Path(args.path)
    if not input_path.exists():
        print(f"Error: path does not exist: {input_path}", file=sys.stderr)
        sys.exit(1)
    try:
        converter_prompt = _load_prompt("converter")
        reviewer_prompt = _load_prompt("reviewer")
    except Exception as exc:
        print(f"Error: failed to load prompts: {exc}", file=sys.stderr)
        sys.exit(1)
    converter_model = create_chat_model(config, config.llm.converter)
    reviewer_model = create_chat_model(config, config.llm.reviewer)
    jenkinsfiles = [input_path] if input_path.is_file() else sorted(input_path.rglob("Jenkinsfile"))
    if not jenkinsfiles:
        print(f"Error: no Jenkinsfiles found in {input_path}", file=sys.stderr)
        sys.exit(1)
    if config.verbose:
        print(f"Found {len(jenkinsfiles)} Jenkinsfile(s)")
    results: list[PipelineStatus] = []
    output_base = Path(config.output_dir)
    for jf_path in jenkinsfiles:
        if config.verbose:
            print(f"\nProcessing: {jf_path}")
        jenkinsfile_content = jf_path.read_text(encoding="utf-8")
        try:
            state = run_pipeline(
                jenkinsfile=jenkinsfile_content,
                converter_model=converter_model,
                reviewer_model=reviewer_model,
                converter_prompt=converter_prompt,
                reviewer_prompt=reviewer_prompt,
                max_iterations=config.max_iterations,
                progress_callback=print if config.verbose else None,
            )
        except Exception as exc:
            print(f"Error: conversion failed for {jf_path}. Is LM Studio running at "
                  f"{config.llm.base_url}? Details: {exc}", file=sys.stderr)
            results.append(PipelineStatus.ERROR)
            continue
        if not state.workflow_yaml:
            print(f"Warning: empty workflow generated for {jf_path}", file=sys.stderr)
            results.append(PipelineStatus.ERROR)
            continue
        try:
            yaml.safe_load(state.workflow_yaml)
        except yaml.YAMLError as exc:
            print(f"Warning: generated YAML is invalid for {jf_path}: {exc}", file=sys.stderr)
        relative = jf_path.parent.relative_to(jf_path.parent.parent) if input_path.is_file() else jf_path.parent.relative_to(input_path)
        output_dir = output_base / relative
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / "ci.yml"
        output_file.write_text(state.workflow_yaml, encoding="utf-8")

        report_file = output_dir / "report.md"
        report_file.write_text(
            generate_report(
                state=state,
                source_path=str(jf_path),
                output_path=str(output_file),
                max_iterations=config.max_iterations,
            ),
            encoding="utf-8",
        )

        print(f"{output_file} ({state.status.value}, iteration={state.iteration})")
        results.append(state.status)

    approved = sum(1 for r in results if r == PipelineStatus.APPROVED)
    max_iterations_reached = sum(1 for r in results if r == PipelineStatus.MAX_ITERATIONS)
    errors = sum(1 for r in results if r == PipelineStatus.ERROR)

    print("\n" + "=" * 50)
    print(f"Processed {len(results)} file(s)")
    if approved == len(results) and results:
        print(f"✅ {len(results)} file(s) converted successfully")
        sys.exit(0)
    if errors == len(results):
        print("❌ All conversions failed")
        sys.exit(1)
    print(f"⚠️  {approved} approved, {max_iterations_reached} max-iterations, {errors} failed")
    sys.exit(2)

if __name__ == "__main__":
    main()
