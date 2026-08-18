# ADTC 2026 Laptop LLM Challenge

This repository contains the development environment and submission artifacts for the Africa Deep Tech Challenge 2026.

## Workspace Structure

- `app/`: Final application code.
- `benchmarks/`: Local benchmark results.
- `docs/`: Project documentation.
- `models/`: GGUF model files (Gitignored).
- `scripts/`: Utility scripts.
- `submission/`: Final submission artifacts.
- `tools/`: Build tools (llama.cpp).
- `profiler/`: Official ADTC profiler repository.

## Getting Started

1. Activate the virtual environment:
   ```bash
   source .venv/bin/activate
   ```
2. Ensure `bin/` is on your `PATH`:
   ```bash
   export PATH=$PWD/bin:$PATH
   ```
3. Run the profiler:
   ```bash
   adtc-profiler run --submission . --mode participant --output submission.json
   ```

For detailed environment information, see [docs/environment.md](docs/environment.md).
