# Krea 2 SageAttention Guard for ComfyUI-KJNodes

This repo contains a small compatibility patch and a known-good workflow for using the `Patch Sage Attention KJ` node with local Krea 2 / Krea 2 Turbo workflows in [ComfyUI](https://github.com/comfyanonymous/ComfyUI).

This is not an installable ComfyUI custom node. Do not clone this repository into `custom_nodes`. Apply the patch files to an existing [ComfyUI-KJNodes](https://github.com/kijai/ComfyUI-KJNodes) checkout instead.

The patch is for [ComfyUI-KJNodes](https://github.com/kijai/ComfyUI-KJNodes). It keeps KJNodes' existing [SageAttention](https://github.com/thu-ml/SageAttention) behavior for non-Krea models, while adding a guarded Krea 2 path that only accelerates allowlisted diffusion attention calls and falls back to ComfyUI's original attention for unsupported calls.

## What It Fixes

Krea 2 has attention paths that should not be patched blindly. In particular, its text-fusion path can use different head counts/shapes than the main diffusion attention. A global SageAttention override can hit those unsupported paths and fail with Triton/compiler errors, invalid tensor shapes, NaNs, or black images.

This patch adds:

- Krea 2 model detection.
- A guarded SageAttention override for Krea 2.
- Skip/fallback behavior for unsupported dtype, mask, device, shape, head count, and fp8 Sage modes.
- Logging for patched and skipped attention paths.
- Optional `dry_run` validation on the `Patch Sage Attention KJ` node.
- Output-shape validation for ComfyUI's `skip_reshape=True` attention path.

## Contents

```text
patches/
  0001-krea2-guarded-sageattention.patch
  0002-krea2-output-shape-validation.patch
workflows/
  Krea2 RAW SageAttention - Test Baseline.json
  Krea2 RAW SageAttention 2.2 - Verified Baseline.json
  Krea2 Turbo SageAttention - Working Baseline.json
  Krea2 Turbo SageAttention 2.2 - Verified Baseline.json
PATCH_NOTES.md
THIRD_PARTY_NOTICES.md
requirements.txt
```

## Requirements

- ComfyUI with local Krea 2 support.
- ComfyUI-KJNodes installed.
- CUDA-capable NVIDIA GPU.
- A working SageAttention install.
- Krea 2 model files.

Tested against:

```text
ComfyUI-KJNodes: kijai/ComfyUI-KJNodes @ 50a0837f9aea602b184bbf6dbabf66ed2c7a1d22
SageAttention: sageattention==1.0.6
SageAttention: sageattention==2.2.0 from upstream source tag v2.2.0
```

KJNodes moves quickly and does not always have tagged releases. If your local KJNodes copy is much newer than the tested commit, `git apply` may fail or require manual conflict resolution.

Known-good model files:

```text
Turbo diffusion model: krea2_turbo_fp8_scaled.safetensors
RAW diffusion model: raw.safetensors local test name; public filename may vary, for example krea2_raw_bf16.safetensors
text encoder: qwen3vl_4b_fp8_scaled.safetensors
CLIPLoader type: krea2
VAE: qwen_image_vae.safetensors
```

The RAW workflow was smoke-tested with a locally named `raw.safetensors` file. Public Krea 2 RAW downloads may use a more specific filename such as `krea2_raw_bf16.safetensors`; if your file has a different name, select it in the `Load Diffusion Model` node after loading the workflow.

## Installation

From your KJNodes folder, apply the patches in order. Depending on your operating system and install method, the folder may be named `ComfyUI-KJNodes` or `comfyui-kjnodes`.

```powershell
git apply "path/to/patches/0001-krea2-guarded-sageattention.patch"
git apply "path/to/patches/0002-krea2-output-shape-validation.patch"
```

If `Patch Sage Attention KJ` already has a `dry_run` option, this patch may already be installed in that KJNodes copy.

Install SageAttention separately rather than vendoring it into this repo:

```powershell
python -m pip install sageattention==1.0.6
```

The `sageattention==1.0.6` wheel is the easiest known working install path. SageAttention `2.2.0` was also validated with this patch on Windows, but it may need to be built from the upstream source tag because PyPI may not provide a `2.2.0` wheel for your setup.

For a source build, follow the SageAttention project instructions and install tag `v2.2.0` into the same Python environment used by ComfyUI. On Windows, this typically requires CUDA Toolkit, Visual Studio 2022 Build Tools with x64 C++ tools, and an x64 developer command prompt.

On Windows, Triton support may require a Windows-compatible Triton package:

```powershell
python -m pip install triton-windows
```

Restart ComfyUI after patching or installing packages.

## Reverting

From the same KJNodes folder, reverse the patches in the opposite order:

```powershell
git apply -R "path/to/patches/0002-krea2-output-shape-validation.patch"
git apply -R "path/to/patches/0001-krea2-guarded-sageattention.patch"
```

If your KJNodes folder is a git checkout and you only want to discard local patch changes, you can also restore the touched file from upstream:

```powershell
git restore nodes/model_optimization_nodes.py
```

## Workflow

Load one of:

```text
workflows/Krea2 RAW SageAttention - Test Baseline.json
workflows/Krea2 RAW SageAttention 2.2 - Verified Baseline.json
workflows/Krea2 Turbo SageAttention - Working Baseline.json
workflows/Krea2 Turbo SageAttention 2.2 - Verified Baseline.json
```

The included sample workflows are blank-prompt baselines with no generated images embedded.

Krea 2 Turbo was tested as the initial known-good path. Krea 2 RAW was also smoke-tested with `raw.safetensors` and the `qwen3vl_4b_fp8_scaled.safetensors` text encoder. RAW output quality is more sensitive to sampler settings than Turbo, so the RAW workflow uses a slower quality baseline instead of Turbo's fast 8-step settings.

Shared SageAttention settings:

```text
Patch Sage Attention KJ:
  sage_attention: auto
  allow_compile: false
  dry_run: true
```

The `2.2 - Verified Baseline` workflows use the same KJNodes patch node. The workflow cannot pin the installed SageAttention Python package; it will use whichever SageAttention version is active in your ComfyUI Python environment.

## SageAttention 2.2 Verification

SageAttention `2.2.0` was built locally from upstream tag `v2.2.0` and tested through the ComfyUI Desktop API with this guarded Krea patch. The test machine used ComfyUI `0.26.2`, PyTorch `2.8.0+cu129`, CUDA `12.9`, and an NVIDIA RTX 5080.

Both Krea 2 Turbo and Krea 2 RAW completed successfully with SageAttention `2.2.0` enabled.

Observed local benchmark timings:

```text
512x512
Turbo no Sage:   15.844s
Turbo Sage 2.2:   5.573s
RAW no Sage:     66.693s
RAW Sage 2.2:    45.964s

1024x1024
Turbo no Sage:   16.796s
Turbo Sage 2.2:  10.718s
RAW no Sage:    111.669s
RAW Sage 2.2:   104.812s
```

On this setup, Turbo showed a clear speedup with SageAttention `2.2.0`. RAW also worked, but the 1024x1024 RAW speedup was small.

Turbo KSampler baseline:

```text
KSampler:
  steps: 8
  cfg: 1.0
  sampler: euler
  scheduler: simple
```

RAW KSampler baseline:

```text
KSampler:
  size: 1024x1024
  steps: 40
  cfg: 4.0
  sampler: dpmpp_2m
  scheduler: beta
```

If the RAW workflow runs out of VRAM, lower only the latent size to `768x768` first and keep the sampler settings unchanged.

## Troubleshooting

If you see:

```text
Krea2 expects conditioning with 12x2560=30720 features but got 4096
```

Set `CLIPLoader` type to `krea2` and use the Krea-compatible Qwen3-VL 4B text encoder. Do not use `qwen_image`, `flux2`, or `stable_diffusion` as the CLIP type for Krea 2.

If you see:

```text
Failed to find C compiler. Please specify via CC environment variable.
```

First confirm the patched KJNodes node is active. The `Patch Sage Attention KJ` node should show a `dry_run` option. If it does not, the patch is not installed in the ComfyUI instance you are running.

If the patched node is active and the compiler error remains, install a Windows-compatible Triton package or a C compiler usable by Triton.

If output is black or unstable, set `sage_attention` to `disabled` to confirm the base Krea workflow is healthy, then re-enable `auto` with `dry_run` on.

If `git apply` fails, your KJNodes copy probably differs from the tested commit. Check whether the patch is already present by looking for `dry_run` on the `Patch Sage Attention KJ` node. If it is not present, update or reset KJNodes to a known state and try again, or apply the changes manually from the patch files.

## License And Attribution

This patch modifies behavior in ComfyUI-KJNodes, which is distributed under GPL-3.0. This repository includes the GPL v3 license text and uses GPL-3.0-or-later wording for compatibility with the standard GPL v3 boilerplate.

SageAttention is not distributed with this repository. Users install it separately and are responsible for complying with its license. The tested package versions were `sageattention==1.0.6` and `sageattention==2.2.0`; installed package metadata for the tested 1.0.6 wheel declared BSD 3-Clause.

See `PATCH_NOTES.md` for the project copyright and modification notice, and `THIRD_PARTY_NOTICES.md` for project credits and dependency notes. The placeholder example near the end of the GPL license text is part of the standard GPL appendix, not a missing repository field.

Krea 2 model weights, Qwen text encoders, VAE files, generated images, package caches, and Triton caches are not included. This repository is not affiliated with ComfyUI, KJNodes, SageAttention, Krea, Qwen, or their maintainers.

This repository is not legal advice.
