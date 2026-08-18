# Environment Documentation

## Hardware
- **CPU**: Intel(R) Xeon(R) CPU @ 2.20GHz (2 vCPUs)
- **RAM**: 7.8 GiB
- **Storage**: ~4.0 GiB available in `/home` (Google Cloud Shell)
- **OS**: Ubuntu 24.04.4 LTS (Noble Numbat)

## Software
- **Python**: 3.12.3
- **GCC/G++**: 13.3.0
- **CMake**: 3.28.3
- **ADTC Profiler**: 0.1.0
- **llama.cpp**: b10175 (Commit: 60bccc3763395e01b039aa1ddeacc8cc0ea69f70)
- **llama-cpp-python**: 0.3.35
- **lm-eval**: 0.4.12
- **llama-bench**: Built from llama.cpp b10175

## Installation Steps
1. Create virtual environment: `python3 -m venv .venv`
2. Install profiler: `pip install -e ./profiler`
3. Build llama.cpp:
   ```bash
   cmake -B build -DBUILD_SHARED_LIBS=OFF
   cmake --build build --config Release --target llama-bench llama-cli llama-server
   ```
4. Copy binaries to `bin/` and add to `PATH`.

## Verification
Verified via:
- `python -c "import adtc_profiler"`
- `python -c "import lm_eval"`
- `llama-bench --help`
