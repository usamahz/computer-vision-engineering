"""Machine identification, measured rather than typed.

Every benchmark prints this banner into `results/raw.txt`, so the machine named in a README
can be checked against the machine that produced the numbers. If they disagree, the README is
wrong.

Works on Linux and on macOS, because the point of the repository is that a result says which
machine it came from: run it on an Apple M4 Pro and the banner says Apple M4 Pro.
"""

from __future__ import annotations

import os
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path


def _read(path: str) -> str:
    try:
        return Path(path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def _sysctl(key: str) -> str:
    if not shutil.which("sysctl"):
        return ""
    try:
        out = subprocess.run(["sysctl", "-n", key], capture_output=True, text=True, timeout=5)
    except (OSError, subprocess.SubprocessError):
        return ""
    return out.stdout.strip() if out.returncode == 0 else ""


def _package_version(name: str) -> str:
    try:
        module = __import__(name)
    except ImportError:
        return "not installed"
    return getattr(module, "__version__", "unknown")


def cpu_name() -> str:
    if sys.platform == "darwin":
        brand = _sysctl("machdep.cpu.brand_string")
        return brand or platform.processor() or "unknown Apple silicon"
    cpuinfo = _read("/proc/cpuinfo")
    match = re.search(r"^model name\s*:\s*(.+)$", cpuinfo, flags=re.MULTILINE)
    if match:
        return match.group(1).strip()
    match = re.search(r"^Model\s*:\s*(.+)$", cpuinfo, flags=re.MULTILINE)
    if match:
        return match.group(1).strip()
    return platform.processor() or platform.machine()


def logical_cores() -> int:
    return os.cpu_count() or 1


def physical_cores() -> int:
    if sys.platform == "darwin":
        value = _sysctl("hw.physicalcpu")
        return int(value) if value.isdigit() else logical_cores()
    cpuinfo = _read("/proc/cpuinfo")
    pairs = set(re.findall(r"physical id\s*:\s*(\d+)[\s\S]*?core id\s*:\s*(\d+)", cpuinfo))
    return len(pairs) or logical_cores()


def memory_gib() -> float:
    if sys.platform == "darwin":
        value = _sysctl("hw.memsize")
        return round(int(value) / 1024**3, 1) if value.isdigit() else 0.0
    match = re.search(r"^MemTotal:\s*(\d+) kB$", _read("/proc/meminfo"), flags=re.MULTILINE)
    return round(int(match.group(1)) / 1024**2, 1) if match else 0.0


def virtualised() -> str:
    if sys.platform == "darwin":
        return "no"
    cpuinfo = _read("/proc/cpuinfo")
    if re.search(r"^flags\s*:.*\bhypervisor\b", cpuinfo, flags=re.MULTILINE):
        return "yes, guest of a hypervisor"
    return "not detected"


def simd() -> str:
    if sys.platform == "darwin":
        return "Apple silicon NEON and AMX, not queried"
    cpuinfo = _read("/proc/cpuinfo")
    match = re.search(r"^flags\s*:\s*(.+)$", cpuinfo, flags=re.MULTILINE)
    if not match:
        return "unknown"
    flags = set(match.group(1).split())
    interesting = [f for f in ("sse4_2", "avx", "avx2", "fma", "avx512f", "avx512_vnni", "amx_int8") if f in flags]
    return ", ".join(interesting) or "none of the usual vector extensions"


def accelerators() -> str:
    """What this machine could offload to. Honest and conservative: absence is reported."""
    found = []
    if shutil.which("nvidia-smi"):
        found.append("NVIDIA GPU driver present")
    if sys.platform == "darwin":
        found.append("Apple GPU and Neural Engine present, not used by these benchmarks")
    return ", ".join(found) or "none detected"


def blas_name() -> str:
    try:
        import numpy as np
    except ImportError:
        return "numpy not installed"
    try:
        config = np.show_config(mode="dicts")  # type: ignore[call-arg]
    except (TypeError, AttributeError, ValueError):
        return "unknown"
    try:
        blas = config["Build Dependencies"]["blas"]
        return f"{blas.get('name', 'unknown')} {blas.get('version', '')}".strip()
    except (KeyError, TypeError):
        return "unknown"


def thread_env() -> dict[str, str]:
    keys = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS")
    return {key: os.environ.get(key, "unset") for key in keys}


def machine() -> dict[str, object]:
    return {
        "cpu": cpu_name(),
        "logical_cores": logical_cores(),
        "physical_cores": physical_cores(),
        "memory_gib": memory_gib(),
        "virtualised": virtualised(),
        "vector_extensions": simd(),
        "accelerators": accelerators(),
        "platform": platform.platform(),
        "python": platform.python_version(),
        "numpy": _package_version("numpy"),
        "pillow": _package_version("PIL"),
        "blas": blas_name(),
        "threads": thread_env(),
    }


def banner(extra: dict[str, object] | None = None) -> str:
    info = machine()
    lines = ["=" * 78, "machine (measured at run time, not typed into a README)", "=" * 78]
    lines.append(f"  cpu                : {info['cpu']}")
    lines.append(f"  cores              : {info['logical_cores']} logical, {info['physical_cores']} physical")
    lines.append(f"  memory             : {info['memory_gib']} GiB")
    lines.append(f"  virtual machine    : {info['virtualised']}")
    lines.append(f"  vector extensions  : {info['vector_extensions']}")
    lines.append(f"  accelerators       : {info['accelerators']}")
    lines.append(f"  platform           : {info['platform']}")
    lines.append(f"  python             : {info['python']}")
    lines.append(f"  numpy              : {info['numpy']} (blas: {info['blas']})")
    lines.append(f"  pillow             : {info['pillow']}")
    threads = info["threads"]
    assert isinstance(threads, dict)
    lines.append("  thread limits      : " + ", ".join(f"{k}={v}" for k, v in threads.items()))
    for key, value in (extra or {}).items():
        lines.append(f"  {key:<19}: {value}")
    lines.append("=" * 78)
    return "\n".join(lines)


def short_machine() -> str:
    info = machine()
    return (
        f"{info['cpu']}, {info['logical_cores']} logical cores, {info['memory_gib']} GiB, "
        f"{info['platform']}, Python {info['python']}, numpy {info['numpy']}"
    )


if __name__ == "__main__":
    print(banner())
