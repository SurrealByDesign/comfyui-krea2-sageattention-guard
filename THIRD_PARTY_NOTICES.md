# Third-Party Notices

This repository is a small compatibility patch and workflow package.

It does not vendor:

- ComfyUI
- ComfyUI-KJNodes
- SageAttention
- Triton
- model weights
- text encoders
- VAEs
- generated images

## ComfyUI

- Project: ComfyUI
- URL: https://github.com/comfyanonymous/ComfyUI
- Role: Host application and local model runtime.

## ComfyUI-KJNodes

- Project: ComfyUI-KJNodes
- URL: https://github.com/kijai/ComfyUI-KJNodes
- Role: Upstream custom node package that provides `Patch Sage Attention KJ`.
- Tested commit: `50a0837f9aea602b184bbf6dbabf66ed2c7a1d22`
- License note: The patch files in this repository are derived from KJNodes source context and include the GPL v3 license text for compatibility with upstream KJNodes.

## SageAttention

- Project: SageAttention
- URL: https://github.com/thu-ml/SageAttention
- Role: Optional external attention backend used by KJNodes.
- Tested package: `sageattention==1.0.6`
- License note: The locally tested `sageattention==1.0.6` wheel metadata declares BSD 3-Clause. SageAttention is not distributed with this repository; users install it separately and are responsible for complying with its license.

If you use SageAttention in published work, consider citing the papers listed by the SageAttention project:

- "SageAttention: Accurate 8-Bit Attention for Plug-and-play Inference Acceleration"
- "SageAttention2 Technical Report: Accurate 4-Bit Attention for Plug-and-play Inference Acceleration"

## Triton / Triton Windows

- Project: Triton
- URL: https://github.com/triton-lang/triton
- Role: Runtime/compiler dependency used by SageAttention.
- Windows note: Some Windows setups may use a Windows-compatible Triton package such as `triton-windows`.

## Krea 2, Qwen, And Model Files

- Role: Model weights, text encoders, and VAE files referenced by the workflow.
- Included here: No.
- Users must obtain model files separately and follow the licenses or usage terms for those files.

The workflow references filenames that were useful for local testing:

```text
krea2_turbo_fp8_scaled.safetensors
raw.safetensors
qwen3vl_4b_fp8_scaled.safetensors
qwen_image_vae.safetensors
```

The RAW checkpoint was locally named `raw.safetensors` during smoke testing. Public downloads may use a more specific filename such as `krea2_raw_bf16.safetensors`.

These filenames are references only. They are not included in this repository.
