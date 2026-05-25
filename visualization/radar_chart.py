from __future__ import annotations

from math import pi
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def plot_radar_chart(scores: dict[str, float], output_path: str | Path) -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    labels = list(scores.keys())
    values = [float(scores[k]) for k in labels]
    values += values[:1]
    angles = np.linspace(0, 2 * pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
    ax.plot(angles, values, linewidth=2, color="#4C78A8")
    ax.fill(angles, values, color="#4C78A8", alpha=0.25)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_yticklabels([])
    ax.set_title("EmotionBench Capability Radar")
    ax.set_ylim(0, 1)
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close(fig)
    return output_path
