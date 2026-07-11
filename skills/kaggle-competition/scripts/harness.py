"""Shared Kaggle pipeline: download -> (model builds submission.csv) -> submit -> log score.

A thin, auditable wrapper over the `kaggle` CLI (invoked as `python -m kaggle`
so it works even when `kaggle.exe` is not on PATH). Each competition folder has
its own model script that writes a `submission.csv`; this harness handles the
identical download/submit/score plumbing so the per-competition code stays
focused on the modelling.

Layout it expects (harness.py + registry.py sit at the project root):

    <root>/
      registry.py            # your competitions: key -> {slug, title, rules_url, ...}
      harness.py             # this file
      competitions/
        <key>/
          data/              # downloaded + unzipped (git-ignore this)
          model.py           # writes submission.csv (CSV path)
          submission.csv
          kernel/            # code-competitions only (kernel path)

Two submission paths:
  * CSV path (getting-started / Playground): a local model writes submission.csv
    and we push it with `competitions submit`.
  * Kernel path (code-competitions): the scoring code must *run on Kaggle's own
    infra* (GPU, no local file upload). We scaffold a kernel-metadata.json,
    push+run the notebook/script on Kaggle, poll its status, and pull the output
    back. The final code-competition submit is a website click (accept-the-rules
    style human action), not an API call.

Usage:
    python harness.py download      <key>
    python harness.py submit        <key> [--file submission.csv] [--message "..."]
    python harness.py score         <key>          # latest submission score off the API
    python harness.py kernel-init   <key> [--gpu] [--script] [--code-file notebook.ipynb]
    python harness.py kernel-push   <key>          # push + run the kernel on Kaggle
    python harness.py kernel-status <key>          # poll the run status
    python harness.py kernel-output <key>          # pull run outputs (e.g. submission.csv) locally

Auth: set up a Kaggle API token first — either the classic
`~/.kaggle/kaggle.json` (username+key) or the newer `~/.kaggle/access_token`.
Both are resolved automatically.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from registry import COMPETITIONS

ROOT = Path(__file__).resolve().parent
COMP_DIR = ROOT / "competitions"
KAGGLE_JSON = Path.home() / ".kaggle" / "kaggle.json"


def _kaggle(*args: str) -> subprocess.CompletedProcess:
    """Run the kaggle CLI, returning the completed process (never raises)."""
    return subprocess.run(
        [sys.executable, "-m", "kaggle", *args],
        capture_output=True,
        text=True,
    )


def _resolve(key: str) -> dict:
    if key not in COMPETITIONS:
        raise SystemExit(f"unknown competition key '{key}'. Known: {', '.join(COMPETITIONS)}")
    return COMPETITIONS[key]


def download(key: str) -> Path:
    comp = _resolve(key)
    dest = COMP_DIR / key / "data"
    dest.mkdir(parents=True, exist_ok=True)
    proc = _kaggle("competitions", "download", "-c", comp["slug"], "-p", str(dest), "--force")
    print(proc.stdout or proc.stderr)
    if proc.returncode != 0:
        raise SystemExit(f"download failed for {comp['slug']} — accept the rules at {comp['rules_url']}")
    # unzip everything the CLI dropped
    import zipfile
    for zf in dest.glob("*.zip"):
        with zipfile.ZipFile(zf) as z:
            z.extractall(dest)
    print(f"[ok] data ready in {dest}")
    return dest


def submit(key: str, file: str = "submission.csv", message: str = "") -> None:
    comp = _resolve(key)
    path = COMP_DIR / key / file
    if not path.exists():
        raise SystemExit(f"no submission file at {path} — run the model script first")
    msg = message or f"{comp['title']} — harness submit"
    proc = _kaggle("competitions", "submit", "-c", comp["slug"], "-f", str(path), "-m", msg)
    print(proc.stdout or proc.stderr)
    if proc.returncode != 0:
        raise SystemExit("submit failed — is the rules-acceptance done on the website?")


def score(key: str) -> None:
    comp = _resolve(key)
    proc = _kaggle("competitions", "submissions", "-c", comp["slug"], "--csv")
    print(proc.stdout or proc.stderr)


# ---------------------------------------------------------------------------
# Kernel path — for code-competitions whose scoring code must run on Kaggle's
# own infra (often GPU). Mirrors the CSV path but wraps `kaggle kernels *`.
# ---------------------------------------------------------------------------

def _kaggle_username() -> str:
    """Resolve the Kaggle username — needed for the kernel `id`.

    Handles both auth styles: the KAGGLE_USERNAME env var, the newer
    ~/.kaggle/access_token (ask the SDK, which resolves the username for it),
    and the classic ~/.kaggle/kaggle.json.
    """
    import os
    if os.environ.get("KAGGLE_USERNAME"):
        return os.environ["KAGGLE_USERNAME"]
    try:
        from kaggle import KaggleApi
        api = KaggleApi()
        api.authenticate()
        user = api.get_config_value("username")
        if user:
            return user
    except Exception:
        pass
    if KAGGLE_JSON.exists():
        return json.loads(KAGGLE_JSON.read_text())["username"]
    raise SystemExit("could not resolve Kaggle username — set up the API token first")


def _kernel_dir(key: str) -> Path:
    return COMP_DIR / key / "kernel"


def kernel_init(key: str, gpu: bool = False, script: bool = False,
                code_file: str = "", force: bool = False) -> Path:
    """Scaffold competitions/<key>/kernel/ with a kernel-metadata.json + code stub.

    Wires the competition as a source so the notebook can read /kaggle/input/*
    and its output is eligible for a code-competition submission on the website.
    Refuses to overwrite an existing kernel-metadata.json unless force=True.
    """
    comp = _resolve(key)
    kdir = _kernel_dir(key)
    kdir.mkdir(parents=True, exist_ok=True)
    if (kdir / "kernel-metadata.json").exists() and not force:
        raise SystemExit(
            f"{kdir / 'kernel-metadata.json'} already exists — pass --force to overwrite"
        )
    user = _kaggle_username()
    kernel_type = "script" if script else "notebook"
    default_code = "main.py" if script else "notebook.ipynb"
    code_file = code_file or default_code
    slug = f"{key}-submission"

    meta = {
        "id": f"{user}/{slug}",
        "title": f"{comp['title']} — submission",
        "code_file": code_file,
        "language": "python",
        "kernel_type": kernel_type,
        "is_private": "true",
        "enable_gpu": "true" if gpu else "false",
        "enable_tpu": "false",
        "enable_internet": "false",  # code-competitions forbid internet at scoring
        "dataset_sources": [],
        "competition_sources": [comp["slug"]],
        "kernel_sources": [],
        "model_sources": [],
    }
    meta_path = kdir / "kernel-metadata.json"
    meta_path.write_text(json.dumps(meta, indent=2))

    code_path = kdir / code_file
    if not code_path.exists():
        if script:
            code_path.write_text(
                "# runs on Kaggle infra; reads /kaggle/input/<comp>/, writes submission.csv\n"
            )
        else:
            stub = {
                "cells": [{
                    "cell_type": "code", "execution_count": None, "metadata": {},
                    "outputs": [],
                    "source": ["# runs on Kaggle infra; write submission.csv to /kaggle/working/\n"],
                }],
                "metadata": {}, "nbformat": 4, "nbformat_minor": 5,
            }
            code_path.write_text(json.dumps(stub, indent=1))

    print(f"[ok] scaffolded {meta_path}")
    print(f"     gpu={'on' if gpu else 'off'}  type={kernel_type}  code={code_file}")
    print(f"     edit {code_path} then: python harness.py kernel-push {key}")
    return kdir


def kernel_push(key: str) -> None:
    kdir = _kernel_dir(key)
    if not (kdir / "kernel-metadata.json").exists():
        raise SystemExit(f"no kernel at {kdir} — run: python harness.py kernel-init {key}")
    proc = _kaggle("kernels", "push", "-p", str(kdir))
    print(proc.stdout or proc.stderr)
    if proc.returncode != 0:
        raise SystemExit("kernel push failed — check the metadata and rules acceptance")
    print(f"[ok] pushed + running on Kaggle — poll with: python harness.py kernel-status {key}")


def kernel_status(key: str) -> None:
    kdir = _kernel_dir(key)
    meta = kdir / "kernel-metadata.json"
    if not meta.exists():
        raise SystemExit(f"no kernel at {kdir} — run: python harness.py kernel-init {key}")
    kid = json.loads(meta.read_text())["id"]
    proc = _kaggle("kernels", "status", kid)
    print(proc.stdout or proc.stderr)


def kernel_output(key: str) -> None:
    kdir = _kernel_dir(key)
    meta = kdir / "kernel-metadata.json"
    if not meta.exists():
        raise SystemExit(f"no kernel at {kdir} — run: python harness.py kernel-init {key}")
    kid = json.loads(meta.read_text())["id"]
    dest = kdir / "output"
    dest.mkdir(exist_ok=True)
    proc = _kaggle("kernels", "output", kid, "-p", str(dest))
    print(proc.stdout or proc.stderr)
    if proc.returncode == 0:
        print(f"[ok] outputs in {dest}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("action", choices=[
        "download", "submit", "score",
        "kernel-init", "kernel-push", "kernel-status", "kernel-output",
    ])
    ap.add_argument("key")
    ap.add_argument("--file", default="submission.csv")
    ap.add_argument("--message", default="")
    ap.add_argument("--gpu", action="store_true", help="kernel-init: enable GPU")
    ap.add_argument("--script", action="store_true", help="kernel-init: .py script instead of notebook")
    ap.add_argument("--code-file", default="", help="kernel-init: code filename")
    ap.add_argument("--force", action="store_true", help="kernel-init: overwrite existing metadata")
    a = ap.parse_args()
    if a.action == "download":
        download(a.key)
    elif a.action == "submit":
        submit(a.key, a.file, a.message)
    elif a.action == "score":
        score(a.key)
    elif a.action == "kernel-init":
        kernel_init(a.key, gpu=a.gpu, script=a.script, code_file=a.code_file, force=a.force)
    elif a.action == "kernel-push":
        kernel_push(a.key)
    elif a.action == "kernel-status":
        kernel_status(a.key)
    elif a.action == "kernel-output":
        kernel_output(a.key)


if __name__ == "__main__":
    main()
