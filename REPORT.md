# Offline Coding Assistant for African Laptops
## ADTC 2026 Challenge Report

### 1. Abstract
This project presents a reproducible, local-first environment for running large language models (LLMs) on commodity hardware, specifically targeting the constraints of laptops in the African context. By utilizing highly quantized models and efficient C++ runtimes, we provide a foundation for offline coding assistance where internet connectivity is intermittent or costly. Our results demonstrate that a 3.8B parameter model can run within an 8 GB RAM footprint on a standard CPU, establishing a baseline for privacy-first, offline development tools.

### 2. Problem
Modern software development increasingly relies on Large Language Model (LLM) coding assistants. However, these tools are predominantly cloud-based, creating two significant barriers:
*   **Cost**: Sustained API usage fees are prohibitively expensive for many independent developers and students in emerging markets.
*   **Connectivity**: High-quality internet access is often intermittent or unavailable in many parts of the African continent, rendering cloud-dependent tools unreliable for daily professional work.

### 3. African and Local-Computing Context
In the African computing context, the "standard" developer machine is frequently a mid-range laptop with 8 GB of RAM and integrated graphics. To foster local innovation, AI tools must be adapted to these hardware constraints. A local-first assistant ensures that developers can remain productive regardless of infrastructure stability, while also keeping proprietary source code and intellectual property on the device.

### 4. Solution
Our solution integrates a highly efficient C++ inference engine with a compact, high-quality instructor-tuned model. We focus on maximizing CPU-bound throughput by using advanced quantization techniques that reduce the memory footprint enough to allow the model to reside comfortably in RAM alongside other development tools (IDEs, compilers, etc.).

### 5. Technical Architecture
The system is built upon the following components:
*   **Inference Engine**: `llama.cpp` (b10175), chosen for its minimal dependencies and exceptional optimization for CPU architectures.
*   **Environment**: A reproducible Linux-based stack managed via virtual environments (`.venv`).
*   **Profiler**: The official ADTC Profiler (v0.1.0) for standardized measurement and telemetry collection.

### 6. Model and Q4_K_M Quantization
We selected **microsoft/Phi-4-mini-instruct** due to its state-of-the-art performance in the < 4B parameter class.
*   **Architecture**: `phi3`
*   **Parameter Count**: 3.8B (3,836,021,856)
*   **Quantization**: `Q4_K_M` (4-bit GGUF)
*   **Reasoning**: This quantization level provides a ~4x reduction in model size while maintaining significant reasoning capability. The resulting ~2.4 GB model file fits easily into the target memory profile.

### 7. Hardware and Resource Constraints
The project targets laptops with:
*   **RAM**: 8 GB total (approx. 7.8 GB available).
*   **CPU**: Commodity 2-core or 4-core mobile processors (tested on Intel Xeon 2.20GHz baseline).
*   **GPU**: None (CPU-only inference).

### 8. Benchmark Methodology
Benchmarks were conducted using the official **ADTC Profiler** in `participant` mode. We utilized the `-ngl 0` flag to ensure a fair CPU-only baseline, disabling GPU offloading. The benchmark evaluated throughput on a 512-token prompt with 128-token generation. In accordance with the permitted submission guidelines, accuracy was skipped (`--skip-accuracy`) to focus on the performance and efficiency baseline.

### 9. Benchmark Results

| Metric | Verified Value |
| :--- | :--- |
| **Model** | Phi-4-mini-instruct-Q4_K_M |
| **Quantization** | GGUF Q4_K_M |
| **Generation Throughput** | 2.64 tokens/second |
| **First-Token Latency** | 82,664.44 ms |
| **Peak Memory (RSS)** | 3,812.03 MB |
| **Steady-State RSS** | 3,698.99 MB |
| **Peak VMS** | 4,361.71 MB |
| **CPU Utilization (p99)** | 68.0% |
| **Thermal Throttling** | False |
| **Prompt Tokens** | 512 |
| **Generated Tokens** | 128 |
| **Random Seed** | 42 |

### 10. Exact Sperf Calculation
The Performance Score (Sperf) is normalized against a reference target of 15.0 tokens/second.
*   **Formula**: `min(TPS / 15.0, 1.0) * 100`
*   **Calculation**: `(2.64 / 15.0) * 100 = 17.60`
*   **Sperf = 17.60**

### 11. Exact Seff Calculation
The Efficiency Score (Seff) is normalized against a 7.0 GB RAM budget.
*   **Peak RSS (GB)**: `3812.03 MB / 1024 = 3.7227 GB`
*   **Formula**: `max(0, (7.0 - peak_rss_gb) / 7.0) * 100`
*   **Calculation**: `((7.0 - 3.7227) / 7.0) * 100 = 46.82`
*   **Seff = 46.82**

### 12. Reproducibility
The results documented in this report are reproducible within the provided repository environment:
*   **Git Commit SHA**: `af0edb6cd564`
*   **Model MD5**: Verified against the microsoft/Phi-4-mini GGUF release.
*   **Command**: `adtc-profiler run --submission . --mode participant --output submission.json --skip-accuracy`

### 13. Results Interpretation
The benchmark confirms the feasibility of running a high-quality coding assistant on a CPU-only 8 GB laptop. While a generation speed of 2.64 tokens/sec is modest, it is sufficient for "background" tasks such as generating boilerplate, refactoring assistance, or documentation generation where real-time typing speed is not the primary constraint. The memory efficiency is excellent, consuming less than 50% of the target system's RAM.

### 14. Limitations
*   **Throughput**: The measured speed is significantly lower than cloud-based alternatives, reflecting the heavy compute load of the Phi-4 model on standard CPUs.
*   **Latency**: The first-token latency of ~82 seconds is high, indicating a significant initialization cost on the tested environment.
*   **Accuracy**: As the accuracy pipeline was skipped for this baseline run, the reasoning quality of the 4-bit quantization remains to be empirically verified in this specific context.

### 15. Lessons Learned
Quantization is the single most critical lever for accessibility. The transition from FP16 to Q4_K_M is what makes this project possible on 8 GB hardware. Furthermore, pinning to CPU (`-ngl 0`) provides a more honest representation of the hardware actually available to the average developer in target regions.

### 16. Future Work
*   **Inference Optimization**: Investigating AVX/AVX2/AVX-512 instruction utilization to improve CPU-bound throughput.
*   **Model Compression**: Testing 3-bit (IQ3_S) quantization to further reduce memory pressure.
*   **User Interface**: Developing a lightweight VS Code extension that interacts with the `llama-server` binary for an integrated offline experience.
*   **Accuracy Auditing**: Running the full `lm-eval` suite to ensure no significant degradation in coding logic occurred during quantization.

### 17. Conclusion
This project demonstrates that local, private, and offline LLM assistance is a viable path for the African developer ecosystem. By optimizing for the hardware already in users' hands, we reduce the barriers to entry for advanced AI-assisted software engineering.

---
*This report is submitted as part of the Africa Deep Tech Challenge (ADTC) 2026.*
