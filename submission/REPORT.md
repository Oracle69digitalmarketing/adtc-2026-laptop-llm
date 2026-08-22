# Offline Coding Assistant for African Laptops

## ADTC 2026 Challenge Report

### 1. Abstract

This project explores a practical offline coding-assistance configuration designed for laptops with approximately 8 GB of RAM and no discrete GPU.

The system combines a compact instruction-tuned language model in GGUF Q4_K_M format with the llama.cpp inference runtime. The objective is to make useful AI-assisted development possible without requiring continuous cloud connectivity, external inference APIs, or dedicated GPU hardware.

The final configuration uses SmolLM2-135M-Instruct, a compact approximately 135-million-parameter model selected specifically for the constrained-hardware target.

Final performance figures are generated from the official ADTC participant profiler and are reported from the final reproducible run.

### 2. Problem

Modern software development increasingly relies on AI coding assistants. Many existing solutions depend on cloud inference, reliable internet connectivity, recurring API costs, or hardware substantially more powerful than the laptops available to many students and developers.

This creates a practical accessibility gap.

The project asks a simple question:

> Can useful AI coding assistance run locally on an ordinary 8 GB laptop without cloud inference?

### 3. Target Environment

The configuration is designed for:

- Approximately 8 GB system RAM
- CPU-only inference
- No discrete GPU requirement
- Linux
- Intermittent or unavailable internet connectivity
- Local/private source-code processing

The goal is not to compete directly with large cloud models on raw capability. The goal is to establish a practical local inference baseline for constrained hardware.

### 4. Solution

The solution combines:

- **Model:** SmolLM2-135M-Instruct
- **Format:** GGUF
- **Quantization:** Q4_K_M
- **Inference runtime:** llama.cpp
- **Execution:** CPU-first local inference
- **Connectivity:** No cloud inference required

The compact model substantially reduces the memory and compute requirements associated with local language-model inference.

### 5. Technical Architecture

The system consists of three primary layers:

1. **Language model**
   - SmolLM2-135M-Instruct
   - Approximately 135M parameters
   - GGUF Q4_K_M quantization

2. **Inference runtime**
   - llama.cpp
   - CPU-only execution for the benchmark configuration

3. **Benchmark environment**
   - Official ADTC participant profiler
   - Reproducible submission configuration
   - Standardized performance and resource measurements

### 6. Model Selection

The final submission uses:

| Property | Configuration |
|---|---|
| Model | SmolLM2-135M-Instruct |
| Parameters | ~135M |
| Format | GGUF |
| Quantization | Q4_K_M |
| Model file | `SmolLM2-135M-Instruct-Q4_K_M.gguf` |
| File size | ~100.6 MiB |
| Runtime | llama.cpp |
| GPU | None |

The model was selected because the challenge is specifically concerned with useful LLM inference under constrained laptop hardware.

The substantially smaller model also provides a useful test of the lower boundary at which local coding assistance becomes practical on modest hardware.

### 7. Hardware and Resource Constraints

The submission targets an approximately 8 GB RAM laptop with CPU-only inference and no discrete GPU.

The final participant benchmark was measured on the actual development environment used for the submission:

| Property | Measured Environment |
|---|---|
| CPU architecture | aarch64 |
| System RAM | 7.5 GB |
| GPU | none |
| Operating system | Ubuntu 24.04.4 LTS |
| Inference | CPU-only |
| Thermal throttling | False |

The Ubuntu 24.04.4 LTS environment is the participant benchmark environment. It should not be interpreted as a replacement for the ADTC target specification, which is based on an approximately 8 GB CPU-only laptop environment.

### 8. Benchmark Methodology

The final configuration was evaluated using the official ADTC participant profiler in participant mode.

The benchmark used the final SmolLM2-135M-Instruct-Q4_K_M submission configuration and evaluated both performance/resource behavior and ARC-Easy accuracy.

The accuracy evaluation used 50 ARC-Easy samples.

### 9. Final Benchmark Results

The final participant profiler produced the following measurements:

| Metric | Verified Value |
|---|---:|
| Model | SmolLM2-135M-Instruct-Q4_K_M |
| Parameters | 134,515,008 |
| Generation Throughput | **25.58 tok/s** |
| First-Token Latency | **8941.51 ms** |
| Prompt Tokens | 512 |
| Generated Tokens | 128 |
| Peak RSS | **175.12 MB** |
| Steady-State RSS | **110.35 MB** |
| Peak VMS | **11331.53 MB** |
| ARC-Easy Accuracy | **46%** |
| CPU p99 | 0.0% |
| Thermal Throttling | False |

The profiler reports 134,515,008 parameters, consistent with the approximately 135M parameter estimate declared in the submission metadata.

### 10. Reproducibility

The final benchmark is associated with:

- **Git commit:** `7377fb3d0804`
- **Profiler:** `adtc-profiler 0.1.0`
- **Runtime:** llama.cpp
- **Model:** `SmolLM2-135M-Instruct-Q4_K_M`
- **Quantization:** GGUF Q4_K_M
- **Model SHA-256:** `2e8040ceae7815abe0dcb3540b9995eaa1fa0d2ca9e797d0a635ae4433c68c2d`
- **Accuracy benchmark:** ARC-Easy, 50 samples
- **Random seed:** 42
- **GPU:** None

The submission includes the model configuration and a credential-free download script for obtaining the same model file.

The benchmark figures in this report are taken directly from the final participant profiler output and are not estimates.

### 11. Results Interpretation

The final interpretation is based only on measurements from the SmolLM2 configuration.

The key question is whether a compact local model can provide useful inference while remaining within the resource constraints of an ordinary 8 GB laptop.

This distinction is important: the project is evaluating practical accessibility rather than claiming that local inference matches the speed or capability of cloud-based coding assistants.

### 12. Limitations

The benchmark establishes the performance limitations of the compact model on the tested CPU.

The project also recognizes that:

- Smaller models have lower model capacity than larger coding models.
- CPU-only inference can impose significant latency.
- Quantization introduces a capability/efficiency trade-off.
- Benchmark performance does not automatically establish real-world coding-assistance quality.
- Accuracy and usefulness must be evaluated separately from raw inference performance.

### 13. Future Work

Future iterations can investigate:

- Better coding-specific prompting
- Local project-file retrieval
- Code-context management
- llama.cpp server integration
- Lightweight editor integration
- CPU-specific optimization
- Alternative compact models
- Accuracy evaluation on coding tasks
- Practical user-interface development

### 14. Conclusion

This project investigates a simple but important direction for AI accessibility: useful language-model assistance on hardware that users already have.

By combining a compact quantized model with an efficient local inference runtime, the system removes the requirement for cloud inference and creates a foundation for private, offline coding assistance on constrained laptops.

The final ADTC benchmark results establish the measured performance of this configuration on the tested hardware.

---

*This report is submitted as part of the Africa Deep Tech Challenge (ADTC) 2026.*
