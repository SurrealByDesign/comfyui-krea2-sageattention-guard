# Patch Notes And Modification Notice

This repository contains patch files that modify this ComfyUI-KJNodes source file:

```text
nodes/model_optimization_nodes.py
```

Project copyright notice:

```text
Copyright (C) 2026 SurrealByDesign
```

Original project:

```text
https://github.com/kijai/ComfyUI-KJNodes
```

Upstream license:

```text
GPL-3.0
```

Tested upstream commit:

```text
50a0837f9aea602b184bbf6dbabf66ed2c7a1d22
```

Modified by:

```text
SurrealByDesign, 2026
```

Purpose:

```text
Adds guarded Krea 2 / Krea 2 Turbo SageAttention fallback behavior.
```

Summary of modifications:

- Detect Krea 2 model patchers before installing the SageAttention override.
- Allowlist the main Krea 2 diffusion attention path.
- Skip likely text-fusion attention paths by head count and tensor shape.
- Fall back to ComfyUI's original attention for unsupported masks, devices, dtypes, shapes, or SageAttention failures.
- Add `dry_run` validation to the `Patch Sage Attention KJ` node.
- Validate expected output shape for `skip_reshape=True` attention calls.

The included workflow is a sample workflow only. It does not include model weights, text encoders, VAEs, generated images, or SageAttention/Triton packages.
