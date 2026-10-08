# Research dossier: ROCm → x86 CPU execution (2026–2031)

**As-of:** 2026-10-08  
**Scope:** Public information only. This dossier assesses whether AMD is likely to support *execution of AI/HIP kernels on general-purpose x86 CPU cores*, not merely install ROCm on an x86 machine to drive an AMD GPU.  
**Status:** Active hypothesis; **no publicly confirmed AMD first-class x86 HIP/ROCm device roadmap** identified.  
**Related themes:** Server CPU demand, x86 Ecosystem Advisory Group, AVX10/ACE, AI inference economics, AMD EPYC software differentiation.

## Executive answer

**Short answer:** This is technically achievable and there is direct historical precedent *inside AMD's ROCm GitHub organization*, but the principal AMD-hosted CPU HIP runtime repository was **archived on 2026-07-07**. AMD's current ROCm and HIP hardware documentation remains GPU-centric. The stronger public forward signals are (a) widening the open and cross-platform GPU programming stack, (b) LLVM x86 code generation, (c) x86 AI instruction standardization via ACE, and (d) independent cross-device frameworks such as AdaptiveCpp. These do not amount to an AMD commitment to native HIP kernels as CPU compute devices.

**Critical distinction:** ROCm *on an x86 CPU host* is already routine; ROCm/HIP *executing GPU kernel code on x86 CPU cores* is a different and much less mature capability. A Ryzen APU running ROCm on its Radeon GPU is not evidence of the latter.

### What 'support x86' could mean

| Meaning | Current evidence | Assessment |
| --- | --- | --- |
| x86 CPU hosts AMD ROCm GPU workload | Official ROCm system requirements and HIP host/device programming architecture | **Established**, routine |
| AMD Ryzen AI APU has ROCm support | AMD Radeon/Ryzen GPU support lists | **Established for supported integrated GPU hardware**, not x86 CPU core acceleration |
| ROCm LLVM compiler generates native x86 code | Official ROCm compiler reference builds x86 and AMDGPU targets | **Established host-code capability**, not a default HIP CPU device |
| HIP GPU kernels run on generic x86 CPU cores | AMD-org [HIP-CPU](https://github.com/ROCm/HIP-CPU) project | **Prototype/experimental precedent**; repository archived July 7, 2026 |
| Portable CUDA/HIP-style code can run on x86 CPUs using another project | [AdaptiveCpp PCUDA](https://github.com/AdaptiveCpp/AdaptiveCpp) | **Experimental independent route**, not an AMD product promise |
| First-class ROCm CPU device (rocBLAS/hipBLAS/PyTorch HIP stack on pure CPU) | No verified official roadmap or public compatibility/support commitment | **Not established** |
| AMD x86 CPU-specific AI acceleration ISA | x86 EAG [ACE specification v1.16.2](https://x86ecosystem.org/resource/ai-compute-extensions-ace-specification/) (July 2026) | **Published architectural standard**; hardware, compiler and framework rollout must be tracked separately |
| x86 ISA becoming an open, royalty-free architecture | Not established by either ROCm open-sourcing or x86 EAG | **Do not infer**. Open software, public extension specs and open ISA rights are different claims. |

## High-signal evidence ledger

| ID | As of / period | Evidence | Interpretation | Strength |
| --- | --- | --- | --- | --- |
| R1 | 2026-08 | [Official ROCm 10.1 overview](https://rocm.docs.amd.com/en/docs-10.1.0/) and [What is ROCm](https://rocm.docs.amd.com/en/docs-10.1.0/about/what-is-rocm.html) explicitly define a GPU-compute platform | Primary commercial focus is GPUs, including GPU components in Ryzen APUs | Primary / direct |
| R2 | Current | [HIP official FAQ](https://rocmdocs.amd.com/projects/HIP/en/latest/faq.html): HIP supports AMD GPUs | No current official first-class CPU kernel device listed | Primary / direct, absence is not categorical prohibition |
| R3 | Current | [ROCm compiler reference](https://rocm.docs.amd.com/projects/llvm-project/en/latest/reference/rocmcc.html): LLVM toolchain builds x86 and AMDGPU targets | Supports x86 compilation already, but alone says nothing about launching HIP GPU kernels on CPUs | Primary / direct |
| R4 | Archived 2026-07-07 | [ROCm/HIP-CPU](https://github.com/ROCm/HIP-CPU) is a header-only CPU runtime able to execute mostly unmodified HIP code; [issue tracker](https://github.com/ROCm/HIP-CPU/issues) confirms project archived | Strong evidence the *idea* was implemented in AMD's ecosystem; **negative signal for current maintenance** | Primary / direct |
| R5 | 2026-07-28 | [x86 EAG ACE v1.16.2](https://x86ecosystem.org/resource/ai-compute-extensions-ace-specification/) describes matrix multiplication, tile state, reduced-precision formats and AVX10 integration | CPU execution of selected AI kernels could become more attractive, regardless of whether ROCm becomes the software interface | Primary / direct |
| R6 | 2026 | [AdaptiveCpp project](https://github.com/AdaptiveCpp/AdaptiveCpp): experimental PCUDA can compile CUDA/HIP-like kernels for CPUs, AMD, NVIDIA and Intel GPUs. [Compilation documentation](https://github.com/AdaptiveCpp/AdaptiveCpp/blob/develop/doc/compilation.md) clarifies separate CPU and HIP backends | Cross-hardware source portability is feasible without an official ROCm CPU backend | Primary / direct, separate organization |
| R7 | 2026 | [TheRock ROCm build system](https://rocm.docs.amd.com/en/docs-10.1.0/about/what-is-rocm.html) and [Windows source support status](https://github.com/ROCm/TheRock/blob/main/docs/development/windows_support.md) | Modular, open source, multi-OS GPU software is advancing; Windows component support still uneven; does not imply x86 compute device support | Primary / direct |
| R8 | 2026 | [ROCm licensing](https://rocm.docs.amd.com/en/docs-10.1.0/about/license.html) lists component-specific terms and proprietary packages | Do not claim all ROCm components are open, or equate ROCm openness with opening the x86 ISA | Primary / direct |

### One misleading phrase to avoid

AMD documentation says HIP supports heterogeneous systems "using CPUs and GPUs from a single source code base." **That does not mean the same HIP GPU device kernel automatically runs on CPU cores.** The HIP model ordinarily combines CPU *host* code with GPU *device* code. This is the most important methodological issue in this investigation.

### Strong counter-signal: HIP-CPU archived

The [ROCm/HIP-CPU](https://github.com/ROCm/HIP-CPU) README describes a generic CPU runtime but also discloses incomplete features. Its [issue tracker](https://github.com/ROCm/HIP-CPU/issues) was archived on 2026-07-07 with unresolved issues, including synchronization and API coverage. This is evidence against a *currently maintained official CPU backend*, not proof that AMD has permanently abandoned all CPU work. Determine whether the work was merged, replaced, forked or simply retired before deriving long-term intentions.

## Why x86 CPU kernels could matter economically

A universal CPU/GPU execution model could support:
1. Portable development and debugging: use a CPU as a fallback/execution target for GPU-style kernels.
2. Small-batch and low-latency inference: select CPU when GPU scheduling/transfer overhead dominates.
3. CPU-heavy agentic orchestration, data transformation, retrieval and postprocessing around GPU inference.
4. Vector/tile acceleration with AVX10/ACE, if silicon and compilers eventually implement it.
5. Better portability and potentially lower software switching costs across mixed compute fleets.

**Limits:** GPUs retain substantial throughput and memory-bandwidth advantages for many matrix-heavy models; CPU memory capacity, latency and energy efficiency are workload-specific. No claim of a general GPU replacement. Also, a single source language does not ensure feature-complete libraries, performance portability or numerical reproducibility.

### Vendor economics test

- If AMD makes CPU and GPU programming more unified, it could increase platform attractiveness, developer adoption, mixed CPU/GPU deployments and EPYC pull-through.
- Conversely, an open CPU backend might commoditize part of software differentiation and could benefit Intel CPUs too.
- Workload demand and vendor monetization must be measured separately: GPU inference growth does not automatically imply proportionate x86 CPU units or ASP uplift.

## Distinguish three possible five-year paths (analyst scenarios, **not** AMD announcements)

| Scenario | 2026–2031 direction | Supporting indicators | Disconfirming indicators |
| --- | --- | --- | --- |
| A — GPU-first ROCm + separate CPU AI paths | ROCm remains mainly for GPU devices; CPUs use optimized runtimes and standard framework CPU backends | Present official GPU-specific docs; archived HIP-CPU; ACE growth as separate ISA | Official HIP CPU device/runtime release and production libraries |
| B — Unified *framework-level* CPU/GPU experience | PyTorch/ONNX/MLIR/other orchestration dispatches intelligently to ROCm GPU kernels or CPU libraries behind common frontend APIs | TheRock modularization; ACE; demand for heterogeneous AI systems | Frameworks and toolchains stay sharply vendor-siloed |
| C — First-class x86 HIP compute backend | AMD or consortium maintains CPU HIP device runtime, compiler lowering, libraries, CI and supported SKU matrix | CPU runtime appears in supported HIP hardware list; GPU kernel execution on CPU; tests + performance | Persistent lack of CPU-device support; project retirement without replacement |

**Directional assessment:** A is the observed default; B is plausible; C is technically feasible but presently speculative and unsupported by a public AMD commitment. Avoid assigning numeric probabilities until there is a documented scoring rubric and repeatable evidence cadence.

## x86 EAG / ACE relationship to ROCm

The [ACE specification v1.16.2](https://x86ecosystem.org/resource/ai-compute-extensions-ace-specification/) was published July 28, 2026. It defines AVX/tile integrated matrix multiplication and reduced-precision support on x86. ACE should be treated as a **CPU ISA initiative** independently of any AMD GPU software roadmap.

Build a traceable chain:
`published spec → AMD/Intel CPU silicon support → LLVM/GCC/oneDNN/BLAS kernel support → PyTorch/ONNX deployment → credible workload benchmark → commercial impact`.

**Do not mark any intermediate step as delivered simply because a specification was published.** Also, the x86 advisory group's public coordination on extensions does not by itself open the underlying x86 ISA or intellectual-property rights.

## Follow-up primary research required

- Inspect archived HIP-CPU commit history, contributors and forks; look for successor work integrated into `ROCm/TheRock`, `rocm-systems`, `ROCm/llvm-project` or outside AMD.
- Search ROCm and HIP issues/discussions for terms `HIP CPU device`, `CPU backend`, `hip-cpu`, `host fallback`, `ACE`, `x86` and `PCUDA`; cite *current engineering decisions*, not just suggestions.
- Check ROCm 10.x release notes every release for CPU kernels, new HIP backends, CPU-supported library builds or genuine runtime registration.
- Compare AdaptiveCpp PCUDA's current compatibility/tests/performance with archived HIP-CPU.
- Track ACE specification revisions and actual EPYC and Xeon support announcements; record ISA features and CPU SKU availability independently.
- Track oneDNN, PyTorch CPU, OpenMP, LLVM MLIR and inference engine CPU paths and decide whether those are a more likely direction than HIP-on-CPU.
- Interview AMD ROCm developers or review public presentations **only using releasable information**.

## Dashboard/UI implementation proposal

Add an **Architecture & Software → ROCm / x86 Futures** panel, connected to the existing x86 roadmap and AI demand sections:

- **Support matrix** with distinct axes for `host x86`, `integrated Radeon GPU`, `discrete GPU`, `HIP kernel on CPU`, `CPU-specific AI ISA`. Show chips and operating systems separately.
- **Evidence vs inference rail:** confirmed / experimental / archived / proposed / not established.
- **Five-year scenario cards:** A (GPU-first), B (framework convergence), C (HIP CPU backend). Never present a forecast as AMD guidance.
- **Signal timeline** with an irreversible citation link on each event, e.g. July 2026 HIP-CPU archive / July 2026 ACE spec / August 2026 ROCm 10.1 documentation.
- **Impact graph:** `developer portability → workload placement → x86 CPU capacity → EPYC vs Xeon adoption → CPU ASP/mix`; visualize alternate paths and uncertainties.
- **Milestone tracker** supporting `published / implemented / tested / shipping / commercially material`, and a field for independent benchmark method.
- **Key open question:** Would making ROCm CPU-capable increase AMD's value capture, or mainly enable portability benefiting competitors?

No private GLG material, client identity or screenshots in public repo.

## Suggested research metadata

Use records with fields `signal_id`, `published_at`, `observed_at`, `subject`, `execution_target`, `claim`, `evidence_type`, `maturity`, `source_url`, `counter_evidence_url`, `implication`, `confidence`, `as_of`. Require explicit `official_AMD_commitment: false` unless backed by an attributable AMD source. Avoid assuming the x86 ISA is open.

## Sources (primary unless noted)

1. https://rocm.docs.amd.com/en/docs-10.1.0/
2. https://rocm.docs.amd.com/en/docs-10.1.0/about/what-is-rocm.html
3. https://rocmdocs.amd.com/projects/HIP/en/latest/faq.html
4. https://rocm.docs.amd.com/projects/llvm-project/en/latest/reference/rocmcc.html
5. https://github.com/ROCm/HIP-CPU
6. https://github.com/ROCm/HIP-CPU/issues
7. https://github.com/ROCm/HIP-CPU/blob/master/docs/overview.md
8. https://github.com/AdaptiveCpp/AdaptiveCpp
9. https://github.com/AdaptiveCpp/AdaptiveCpp/blob/develop/doc/compilation.md
10. https://x86ecosystem.org/resource/ai-compute-extensions-ace-specification/
11. https://github.com/ROCm/TheRock/blob/main/docs/development/windows_support.md
12. https://rocm.docs.amd.com/en/docs-10.1.0/about/license.html

_Research-only analysis, based on sources available as of date above. Forecast scenarios are interpretations, not AMD statements._
