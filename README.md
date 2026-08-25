# Offline Coding Assistant for African Laptops

> **ADTC 2026 · Coding Assistants · Offline / Edge AI**

A reproducible local AI coding-assistant configuration designed for constrained hardware: approximately 8 GB laptops, CPU-only inference, and environments where reliable cloud connectivity cannot be assumed.

The project combines a compact instruction-tuned GGUF model with **llama.cpp** to provide local coding assistance without sending prompts or source code to a cloud inference API.

**One compact model. Multiple device classes. Local inference.**

---

## Why This Project

AI coding assistants are increasingly useful, but many students and developers work with:

- Modest laptops with limited RAM
- CPU-only hardware and no discrete GPU
- Unreliable or expensive internet connectivity
- Privacy requirements that make cloud inference undesirable
- Limited access to high-performance computing hardware

This project explores a practical alternative:

> **Put the model on the device and run the assistant locally.**

The primary target is an approximately 8 GB CPU-only laptop.

We also validated the same compact model on an **ARM64 Android phone through Termux**.

That mobile validation is supplementary to the ADTC submission, but demonstrates that the deployment can extend beyond the laptop.

---

## What We Built

We built a compact offline coding-assistant configuration around:

- **SmolLM2-135M-Instruct**
- **GGUF Q4_K_M quantization**
- **llama.cpp**
- CPU-only inference
- The official ADTC participant profiler
- Reproducible model download and benchmark tooling

The core workflow does not require a cloud inference API.

Once the model and runtime are available locally, prompts and source code can remain on the device.

---

## Final Model

| Component | Configuration |
|---|---|
| **Model** | SmolLM2-135M-Instruct |
| **Parameters** | ~135M |
| **Quantization** | GGUF Q4_K_M |
| **Model size** | ~100 MiB |
| **Runtime** | llama.cpp |
| **Primary target** | ~8 GB CPU-only laptops |
| **Additional validation** | ARM64 Android + Termux |
| **Inference** | CPU-only |

The model is deliberately small.

The objective isn't maximum model size. The objective is finding a useful operating point where AI remains deployable on hardware users may already have.

---

## ADTC Benchmark

The final participant configuration was evaluated using the official ADTC participant profiler.

### Submitted Scores

| Metric | Score |
|---|---:|
| **Self-reported Performance Score (Sperf)** | **17.60** |
| **Self-reported Efficiency Score (Seff)** | **46.82** |

### Participant Environment

| Component | Configuration |
|---|---|
| CPU | Intel Xeon CPU @ 2.20 GHz |
| RAM | 7.8 GB |
| GPU | None |
| OS | Ubuntu 24.04.4 LTS |
| Runtime | llama.cpp |
| Model | Phi-4-mini-instruct Q4_K_M |
| Model size | ~2.4 GB |
| Parameters | ~3.8B |
| Generation throughput | 2.64 tokens/s |
| First-token latency | 82.66 s |
| Generated tokens | 128 |
| Peak RSS | 3.81 GB |
| Steady-state RSS | 3.70 GB |
| CPU p99 | 68% |
| Thermal throttling | False |

Accuracy was not claimed where it was not measured.

The complete methodology and benchmark information are available in the [technical report](submission/REPORT.md).

---

## Supplementary ARM64 Mobile Validation

We additionally built an **ARM64-native llama.cpp runtime on Android using Termux** and ran the same SmolLM2-135M-Instruct Q4_K_M model.

These measurements are supplementary and are **not used as the participant-laptop benchmark**.

| Metric | Prompt 1 | Prompt 2 | Average |
|---|---:|---:|---:|
| **Generation speed** | 32.86 tok/s | 32.67 tok/s | **32.77 tok/s** |
| **Prompt evaluation** | 99.94 tok/s | 101.63 tok/s | **100.79 tok/s** |
| **Total execution time** | 1.492 s | 1.486 s | **1.489 s** |

### Mobile Environment

- **Architecture:** ARM64 / aarch64
- **Platform:** Android
- **Runtime environment:** Termux
- **Runtime:** ARM64-native llama.cpp
- **Model:** SmolLM2-135M-Instruct Q4_K_M
- **Quantization:** GGUF Q4_K_M
- **Execution:** CPU-only

The result provides a useful portability signal:

> **The same compact model can operate on a phone-class ARM64 device, not only on the target laptop environment.**

The laptop remains the primary ADTC target. The Android deployment demonstrates that the same model/runtime approach can be taken further down the hardware stack.

---

## One Model. Multiple Devices.

The Android deployment does **not** require a separate phone-specific model.

The same compact GGUF model can be used across:

| Device | Deployment |
|---|---|
| **8 GB laptop** | Primary ADTC target |
| **ARM64 Android phone** | Supplementary validation |

This keeps distribution simple and demonstrates actual model portability.

The project isn't maintaining one model for laptops and another for phones.

**One model. Different constrained devices.**

---

## Download the Model

The model binary is not committed to Git because it is a large binary artifact.

Instead, the repository provides a reproducible download script.

From the repository root:

```bash
cd submission
chmod +x download_model.sh
./download_model.sh

The script downloads:

SmolLM2-135M-Instruct-Q4_K_M.gguf

and places it at:

submission/model/SmolLM2-135M-Instruct-Q4_K_M.gguf

The download script is idempotent. If the model already exists, it skips the download.


---

Android / Termux

The same model can be downloaded and used on an Android ARM64 device.

1. Install the basic tools

pkg update
pkg install git curl

2. Clone the repository

git clone https://github.com/Oracle69digitalmarketing/adtc-2026-laptop-llm.git
cd adtc-2026-laptop-llm

3. Download the model

cd submission
chmod +x download_model.sh
./download_model.sh

The resulting GGUF model can be used with an ARM64-native llama.cpp build.


---

Run Locally

After obtaining an appropriate native llama.cpp build:

./llama-cli \
  -m submission/model/SmolLM2-135M-Instruct-Q4_K_M.gguf \
  -p "Explain the difference between a Python list and tuple." \
  -n 128

On Android/Termux, use an ARM64-native llama.cpp executable.

The model and inference runtime operate locally.

No cloud inference API is required for the core workflow.


---

Reproduce the ADTC Benchmark

Activate the project environment:

source .venv/bin/activate
export PATH=$PWD/bin:$PATH

Run the participant profiler:

adtc-profiler run \
  --submission . \
  --mode participant \
  --output submission.json

The resulting benchmark output is written to:

submission.json

The profiler implementation and tests are included under:

profiler/


---

Repository Structure

Directory / File	Purpose

app/	Application and integration code
docs/	Environment and project documentation
profiler/	Official ADTC profiler source and tests
scripts/	Utility scripts
submission/	Final competition submission package
submission/model/	Downloaded GGUF model location
submission/REPORT.md	Full technical report
submission/metadata.json	Submission metadata
submission/download_model.sh	Reproducible model download script
bin/	Runtime binaries
models/	Local benchmark models
REPORT.md	Project-level report
submission.json	Profiler output



---

Design Principles

1. Offline First

The core inference workflow runs locally.

It does not require a cloud inference API or continuous internet connectivity once the model and runtime are available on the device.

This makes the approach relevant to environments where connectivity is intermittent, expensive, or unavailable.

2. Constrained Hardware First

The model is intentionally compact and quantized.

The goal is to reduce the hardware barrier to local AI rather than assume access to:

Dedicated GPUs

Large amounts of RAM

High-end workstations

Persistent cloud connectivity


3. Reproducible Measurement

Performance claims are based on measured profiler output rather than estimates of theoretical hardware capability.

The repository contains the benchmark environment and supporting tooling required to reproduce the participant measurement.

4. Device Portability

The laptop is the primary ADTC target.

The additional Android/Termux validation demonstrates that the same model can also be deployed to smaller ARM64 devices.

8 GB Laptop
     │
     │ Same compact GGUF model
     ▼
ARM64 Android Phone

The phone result is not presented as the official laptop benchmark.

It demonstrates that the model/runtime combination can operate beyond the competition's primary target environment.


---

Why the Phone Result Matters

The project started from a laptop constraint, but the mobile validation revealed a broader deployment opportunity.

If a model designed for constrained laptop inference can also run on an ARM64 phone, the deployment boundary becomes significantly more flexible.

Potential environments include:

Student laptops

School computer laboratories

Community technology centres

Developer workstations

Low-cost PCs

Android phones

Offline field environments


This is particularly relevant in markets where users may have access to smartphones before they have access to powerful computers.

The broader principle is:

> Useful AI shouldn't always require new hardware.




---

Limitations

This is a constrained-device research and competition prototype, not a replacement for frontier cloud coding assistants.

Smaller models have lower reasoning and coding capability, while CPU-only inference introduces latency on weaker hardware.

The project does not claim that every coding workload can be handled effectively by a 135M-parameter model.

The focus is different:

> Useful local AI assistance when hardware, connectivity, privacy, or cost constraints make cloud inference impractical.




---

What's Next

The current implementation establishes the benchmarked local inference configuration.

The next stage is to improve the practical coding-assistant experience while preserving the core constraint of local execution.

Potential improvements include:

Better prompt handling

Code-context management

Retrieval of local project files

Lightweight editor integration

Improved conversation handling

Runtime optimization

Model comparison across constrained devices

More extensive coding-task accuracy evaluation

Android-focused packaging

Offline developer workflows for schools and community environments


The long-term direction is not simply to make a smaller chatbot.

It is to build practical edge AI development tools for hardware-constrained environments.


---

Full Technical Report

For the complete technical report, benchmark methodology, environment details, and supplementary mobile validation:

[Read the full technical report](submission/REPORT.md)


---

Competition

Built for:

Africa Deep Tech Challenge 2026 — Laptop LLM Challenge

Problem Domain: Coding Assistants


---

## Maintainer

**Oracle69digitalmarketing**

**Oracle69 Systems**

[GitHub Repository](https://github.com/Oracle69digitalmarketing/adtc-2026-laptop-llm)
