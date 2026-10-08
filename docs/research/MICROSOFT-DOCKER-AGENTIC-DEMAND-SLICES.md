# Microsoft Windows + Docker SBX: agentic CPU demand, hybrid inference, and isolation

Date: 2026-10-08. Source: two uploaded transcripts (Microsoft Windows agentic platform, 1,973 lines; Docker SBX microVM, 276 lines). [Machine-readable corpus](../../data/claims/microsoft-docker-agentic-2026.json). This is source attribution, **not independent verification**. Automatic captions misrecognize product names and some numbers; broad line anchors must be tightened against video before publication of verified benchmarks.

## Joint thesis with AMD Advancing AI 2026

AMD argues CPU-only agent sandboxes become a new server demand segment. Microsoft simultaneously promotes endpoint-local models, permissioned local tools, and Windows-native agent containers; Docker promotes portable microVM isolation. This means demand is **not simply 'agents × CPU cores'**: deployment location, isolation overhead, reuse and architecture mix all matter.

### New measurable market dimensions

| Dimension | Microsoft signal | Docker signal | AMD intersection | Measure |
| --- | --- | --- | --- | --- |
| Placement | Hybrid local/cloud routing | Sandboxes across Windows/macOS/Linux | Server CPU sandbox TAM | share of agent tasks endpoint vs cloud |
| Isolation | Windows execution containers, OS agent identity | SBX microVM, isolated kernel and filesystem | incremental agent CPU rack workload | cold-start time, memory footprint, core-seconds, power |
| Inference | Windows ML CPU/GPU/NPU, llama.cpp | agent execution agnostic to model | direct x86 CPU inference vs GPU hosting | CPU inference tokens/s and CPU overhead |
| Orchestration | local subagents and persistent automation | delegated identity/policy roadmap | CPU tool orchestration | completed workflows/CPU-hour |
| Economics | demo: 1.6M local input tokens and 10,500 output tokens | low-friction 'sbx run' | forecast demand and price elasticity | local energy + amortization vs cloud API bill |
| Security | OS-enforced per-agent controls and Defender demo | egress, mounts, secret injection | enterprise adoption and cost | overhead, blocked unauthorized accesses, audit cost |

## Initial numerical slices (source claims, not representative performance)

- Microsoft's **1,600,000 input and 10,500 output tokens** imply **~152.4 input tokens per output token**, and **~1,610,500 combined tokens** for the showcased sub-session. This is a *single demo*, not average traffic. Investigate cached/repeated input, model context truncation, billing and whether 'tokens sent' means cumulative across multiple turns. Microsoft's phrase 'free' means no billed cloud tokens in the demonstration, **not zero electricity/hardware cost**.
- **256K** local model context is an advertised *context-window capacity*, not evidence that the 1.6M demo was one inference pass. Different model and cumulative accounting can explain it; do not claim a contradiction until model/session mapping is confirmed.
- Microsoft cites **3-bit quantization with nearly 80% size reduction**, and a **1.6-bit model fitting in 60GB**. Memory includes weights, KV cache, runtime and shared GPU allocations; check actual measured RAM and sustained performance.
- Microsoft's **up to 128GB** unified-memory and **up to 1 PFLOP** laptop claims imply a larger local inference tier. The TFLOPS/PFLOPS precision and model utilization are unspecified. Do not equate theoretical AI FLOPS with general x86 CPU FLOPS.
- Microsoft showcases **32 simultaneous agents** on an HP ZGX system; concurrency is not measured completed tasks/sec or per-agent CPU demand.
- Docker speaker reports **5 prompts** to reach sensitive information in a controlled demo and **7 additional keystrokes** for sandbox launch. These are anecdotes, not security failure rates or generalized deployment cost.
- Docker's **9/10** security detection score is a speaker anecdote, not an independent product safety metric.

## Model 1: endpoint displacement vs induced workload

Let `W` be annual completed workflows; `s_local` the share routed to local models; `c_local` and `c_cloud` measured CPU core-seconds per workflow, including tool and orchestration work; `i` isolation overhead fraction; `u` effective server utilization.

`Server CPU core-hours = W × (1 - s_local) × c_cloud × (1 + i) / 3600`.

**Caution:** This is a simplified scenario. Local inference can still use cloud tools; a local model may spawn remote agents; some server-side non-inference compute persists. Extend to an activity transition matrix `endpoint → cloud → endpoint` with per-step telemetry. Do not treat the equation as observed demand.

Scenario experiment, with explicit illustrative assumptions only: 1M workflows/day, 10 CPU core-seconds/workflow, isolation overhead 20%, and endpoint shares 0%, 25%, 50%, 75%. Server core-hours/day = 3,333; 2,500; 1,667; 833 respectively. These values are **model outputs**, not market data. At a 60% CPU utilization target, the corresponding average provisioned server cores are approximately 231, 174, 116, 58.

### Immediate follow-up research

1. Verify exact Microsoft event date, product spellings and GA versus preview for MXC/MEXC, Windows ML and HydraFusion; verify Windows and Linux isolation boundary and whether announced capabilities are shipping. Separate announcements, demos and independently usable features.
2. Verify Docker SBX installation, supported hypervisors and Windows requirements; measure true VM memory overhead, CPU utilization, launch latency, I/O and networking penalties. Differentiate existing allow/deny/mount/MCP policies from promised Cedar identity delegation and L7 policy.
3. Reproduce the same agent workflow in **native host**, **Windows execution container**, **Docker SBX microVM**, **WSL/Hyper-V VM**, and **cloud VM**, holding task success and model constant.
4. Compare Windows x86 vs Windows ARM endpoint deployment and EPYC/Xeon vs ARM server execution. Track host ISA, accelerator architecture and binary translation separately.
5. Compare cost per **successful workflow**, not billed tokens alone: energy, amortization, software licenses, operator time, latency, idle and security risk.
6. Build a local/cloud transition matrix by step (inference, retrieval, tool execution, testing, browser automation, storage), measuring where data and CPU work actually occur.
7. Extend AMD TAM bridge to `cloud sandbox CPU`, `endpoint sandbox CPU`, `GPU-host CPU`, and `traditional server CPU`. Prevent double counting endpoint CPU purchases as server CPU revenue.
8. Test elasticity: cheaper local inference can increase workflow volume enough to **increase** total cloud CPU demand despite shifting some steps locally.

## Required dashboard slices

**Hybrid placement slider:** local share 0–100%, induced demand multiplier, per-step CPU time, isolation overhead, utilization, x86 share. Plot cloud cores, local cores, cloud x86 socket demand and successful workflows. Show sensitivity to local model hardware capacity.

**Isolation comparison:** native process vs Windows MXC vs Docker SBX vs generic VM, with measured startup ms, resident RAM, CPU-seconds/task, storage/network throughput, identity isolation, policy controls and OS support. Missing values should remain blank.

**Security-to-economics:** chart agent adoption uplift from stronger containment as a *scenario parameter* and offset CPU/memory overhead as separately measured costs. Do not claim secure containment automatically creates CPU TAM.

**Three-source contradiction/confirmation matrix:** AMD's agent sandbox growth hypothesis; Microsoft's local compute shift; Docker's microVM isolation. Record which claims reinforce or compete, and what empirical observation would falsify each.

## Data acquisition and validation gate

Capture machine SKU, architecture, hypervisor, host OS, sandbox version, model location and version, prompt/workload hash, number of successful tasks, CPU process/core-seconds, memory peak, energy, wall time, input/output/cache tokens, I/O, network, billing, isolation violations and confidence intervals. Run at least 20 repeated trials per representative workload before asserting performance differences. Archive reproducible harness config and logs without secrets or private user data.

**First concrete deliverable:** an interactive sensitivity analysis using clearly hypothetical inputs and a benchmark schema; do not wait for broad market datasets to start quantifying mechanisms. All vendor announcements and anecdotes remain attributed until verified.
