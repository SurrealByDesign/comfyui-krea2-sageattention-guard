#!/usr/bin/env python3
"""Check that this repo's patches apply cleanly to a KJNodes checkout."""

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def run(cmd, cwd):
    result = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if result.returncode != 0:
        sys.stderr.write(result.stdout)
        sys.stderr.write(result.stderr)
        raise SystemExit(result.returncode)
    return result


def main():
    repo_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(
        description="Verify that the Krea 2 SageAttention patches apply to a KJNodes checkout."
    )
    parser.add_argument(
        "kjnodes",
        type=Path,
        help="Path to a ComfyUI-KJNodes checkout.",
    )
    args = parser.parse_args()

    source = args.kjnodes.resolve()
    target_file = source / "nodes" / "model_optimization_nodes.py"
    if not target_file.exists():
        raise SystemExit(f"Not a KJNodes checkout, missing: {target_file}")

    patches = [
        repo_root / "patches" / "0001-krea2-guarded-sageattention.patch",
        repo_root / "patches" / "0002-krea2-output-shape-validation.patch",
    ]
    for patch in patches:
        if not patch.exists():
            raise SystemExit(f"Missing patch file: {patch}")

    with tempfile.TemporaryDirectory(prefix="krea2_sage_patch_check_") as tmp:
        worktree = Path(tmp) / "ComfyUI-KJNodes"
        ignore = shutil.ignore_patterns(".git", "__pycache__", "*.pyc")
        shutil.copytree(source, worktree, ignore=ignore)

        for patch in patches:
            run(["git", "apply", "--check", str(patch)], worktree)
            run(["git", "apply", str(patch)], worktree)
            print(f"OK: {patch.name}")

    print("All patches apply cleanly in sequence.")


if __name__ == "__main__":
    main()
