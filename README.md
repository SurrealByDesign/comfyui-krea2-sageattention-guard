# Krea 2 SageAttention Guard for ComfyUI-KJNodes

This repo contains a small compatibility patch and a known-good workflow for using the `Patch Sage Attention KJ` node with local Krea 2 / Krea 2 Turbo workflows in [ComfyUI](https://github.com/comfyanonymous/ComfyUI).

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
  Krea2 Turbo SageAttention - Working Baseline.json
THIRD_PARTY_NOTICES.md
requirements.txt
```

## Requirements

- ComfyUI with local Krea 2 support.
- ComfyUI-KJNodes installed.
- CUDA-capable NVIDIA GPU.
- A working SageAttention install.
- Krea 2 model files.

Known-good workflow files:

```text
diffusion model: krea2_turbo_fp8_scaled.safetensors
text encoder: qwen3vl_4b_fp8_scaled.safetensors
CLIPLoader type: krea2
VAE: qwen_image_vae.safetensors
```

## Installation

From your `ComfyUI/custom_nodes/comfyui-kjnodes` folder, apply the patches in order:

```powershell
git apply "path\to\patches\0001-krea2-guarded-sageattention.patch"
git apply "path\to\patches\0002-krea2-output-shape-validation.patch"
```

Install SageAttention separately rather than vendoring it into this repo:

```powershell
python -m pip install sageattention==1.0.6
```

On Windows, Triton support may require a Windows-compatible Triton package:

```powershell
python -m pip install triton-windows
```

Restart ComfyUI after patching or installing packages.

## Workflow

Load:

```text
workflows/Krea2 Turbo SageAttention - Working Baseline.json
```

This included sample workflow is the known-good Krea 2 Turbo + SageAttention baseline tested for this patch. It intentionally has blank prompt fields and no generated image embedded.

Important settings:

```text
Patch Sage Attention KJ:
  sage_attention: auto
  allow_compile: false
  dry_run: true

KSampler:
  steps: 8
  cfg: 1.0
  sampler: euler
  scheduler: simple
```

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

## License And Attribution

This patch modifies behavior in ComfyUI-KJNodes, which is distributed under GPL-3.0. This repository is distributed under GPL-3.0-only for compatibility with that upstream project.

SageAttention is not vendored here. It is used as an external dependency. The tested package was `sageattention==1.0.6`, whose installed package metadata declares BSD 3-Clause.

See `THIRD_PARTY_NOTICES.md` for project credits and dependency notes.

Krea 2 model weights, Qwen text encoders, VAE files, generated images, package caches, and Triton caches are not included. This repository is not affiliated with ComfyUI, KJNodes, SageAttention, Krea, Qwen, or their maintainers.
