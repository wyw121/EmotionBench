# EmotionBench

EmotionBench is a benchmark framework for evaluating large language models on complex emotion understanding tasks, including sarcasm, metaphor, implicit emotion, and adversarially perturbed text.

The repository is organized as a reproducible research artifact: it contains the benchmark data format, evaluation pipeline, visualization utilities, experiment scripts, and paper-ready figures/results.

## Paper

EmotionBench: Evaluating Large Language Models on Complex Emotion Understanding

Repository: https://github.com/wyw121/EmotionBench

Paper PDF: coming soon

## Highlights

- Unified JSON benchmark format for emotion understanding tasks
- Support for dataset building, scoring, robustness analysis, and visualization
- Rule-based baselines, prompt comparison, and real-model benchmark runs
- Paper-oriented outputs stored under `results/` and `reports/`
- Reproducible command-line entry points for evaluation and figure generation

## Repository structure

```text
EmotionBench/
├── data/                 # Small sample data demonstrating the input format
├── dataset/              # Benchmark source files used by the framework
├── dataset_expanded/     # Expanded paper-scale benchmark outputs
├── dataset_out/          # Generated combined dataset artifacts
├── evaluation/           # Metrics and scoring logic
├── prompts/              # Baseline and CoT prompt templates
├── reports/              # Paper materials, tables, and figure index
├── results/              # Summaries, predictions, charts, and run artifacts
├── scripts/              # Experiment and analysis utilities
├── src/                  # Package source code
├── visualization/        # Plotting utilities
├── main.py               # CLI entry point
├── requirements.txt      # Python dependencies
├── LICENSE               # MIT License
└── README.md
```

## Installation

```bash
pip install -r requirements.txt
```

Recommended environment:

- Python 3.10+
- pandas
- numpy
- scikit-learn
- matplotlib
- seaborn
- python-dotenv
- openai
- tqdm

## Data format

EmotionBench uses a unified JSON record format. Each sample contains an identifier, the input text, a normalized emotion label, and a task type.

```json
{
  "id": "sarcasm_001",
  "text": "谢谢你哈🙂，让我等了两个小时。",
  "label": "negative",
  "type": "sarcasm",
  "difficulty": "medium",
  "context": "用户抱怨客服响应太慢"
}
```

Prediction files are also JSON-based:

```json
[
  {
    "id": "sarcasm_001",
    "prediction": "negative",
    "raw_output": "The tone is negative because..."
  }
]
```

## Sample data

A small sample dataset is provided in `data/sample_dataset.json` so reviewers can inspect the expected input structure without downloading the full benchmark.

## Running the benchmark

Build the combined dataset artifacts:

```bash
python main.py build-dataset --output dataset_out
```

Evaluate predictions:

```bash
python main.py evaluate --dataset dataset --predictions results/demo_predictions.json --output results/summary.json
```

Generate figures:

```bash
python main.py visualize --dataset dataset --predictions results/demo_predictions.json --output results/charts
```

Generate paper-ready figures and index:

```bash
python scripts/generate_paper_figures.py --write-index
```

## Evaluation metrics

- Accuracy
- Macro-F1
- Per-type accuracy
- Robustness score
- Confusion matrix

## Key outputs

- `results/summary.json`: benchmark summary for a single run
- `results/charts/radar_chart.png`: overall comparison view
- `results/charts/confusion_matrix.png`: confusion matrix for error analysis
- `reports/figures/`: paper-ready figures for the manuscript
- `reports/error_cases.md`: representative failure analysis

## Paper figures

The following figures are tracked in the repository for paper use:

- Baseline comparison
- Prompt comparison
- Real-model overall comparison
- Type-wise accuracy heatmap
- Dataset label distribution
- Dataset type distribution

## Reproducibility notes

- The benchmark uses normalized labels: `negative`, `neutral`, and `positive`.
- Paper-scale experiments are organized under the Level 0 / Level 1 / Level 2 / Level 3 convention described in `reports/evaluation_scale_spec.md`.
- Real-model runs are stored in `results/runs/<provider>/<model>/...` with `summary.json`, `predictions.json`, `run_config.json`, `manifest.json`, and `leaderboard.csv`.

## Citation

If you use EmotionBench in your work, please cite the repository:

```bibtex
@misc{emotionbench2026,
  author = {Wang, Yirui},
  title = {EmotionBench: Evaluating Large Language Models on Complex Emotion Understanding},
  year = {2026},
  howpublished = {\url{https://github.com/wyw121/EmotionBench}}
}
```

## License

This project is released under the MIT License. See `LICENSE` for details.

## Related work

EmotionBench is inspired by benchmark-style evaluation for emotion understanding, prompting, robustness testing, and behavioral analysis in NLP. See the manuscript materials under `reports/` for the full discussion and references.
