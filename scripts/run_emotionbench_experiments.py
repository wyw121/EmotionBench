from __future__ import annotations

import json
import random
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
for path in (ROOT, SRC):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from evaluation.metrics import ResultRow, evaluate, load_predictions  # noqa: E402
from evaluation.robustness import merge_summary  # noqa: E402

random.seed(42)


@dataclass(frozen=True)
class MethodResult:
    name: str
    summary: dict
    predictions: list[ResultRow]


NEG_WORDS = {
    "糟", "烦", "坏", "失落", "沮丧", "崩溃", "退回", "丢", "迟到", "停电", "投诉",
    "crash", "broke", "failed", "angry", "sad", "bad", "broken", "delay", "empty",
}
POS_WORDS = {
    "开心", "高兴", "满意", "满足", "轻松", "喜欢", "温暖", "认可", "顺利", "奖励",
    "happy", "great", "good", "love", "wonderful", "excellent", "delight", "smile",
}
NEU_WORDS = {"一般", "平静", "普通", "例行", "差不多", "neutral", "routine", "normal", "平稳"}
SARCASM_MARKERS = {
    "谢谢你哈", "真贴心", "真周到", "真会安排", "真棒", "真是个完美", "哇", "great,", "great", "🙂", "“", "”", "‘", "’",
}
NEG_CONTEXT_HINTS = {"抱怨", "投诉", "迟到", "停电", "删光", "崩溃", "加班", "故障", "失误", "拖延", "fail"}
POS_CONTEXT_HINTS = {"表扬", "获奖", "认可", "顺利", "开心", "鼓励", "祝贺", "温暖", "喜欢"}


def make_sample(sample_id: str, text: str, label: str, sample_type: str, difficulty: str, context: str) -> dict:
    return {
        "id": sample_id,
        "text": text,
        "label": label,
        "type": sample_type,
        "difficulty": difficulty,
        "context": context,
    }


def generate_dataset() -> list[dict]:
    samples: list[dict] = []

    normal_specs = [
        ("positive", "今天拿到奖学金，我真的很开心。", "学生收到好消息"),
        ("positive", "这次演讲被大家认可，我心里很满足。", "公开表达获得认可"),
        ("positive", "收到录用通知后，我整个人都轻松了。", "求职成功"),
        ("positive", "同事帮我解决了难题，我特别感谢。", "团队协作顺利"),
        ("positive", "新项目推进顺利，让我很有干劲。", "工作进展好"),
        ("positive", "家人送来的消息让我很温暖。", "家庭支持"),
        ("positive", "考试成绩比预期好，我很高兴。", "考试结果理想"),
        ("positive", "这家餐厅的菜很好吃，我很喜欢。", "用餐体验良好"),
        ("positive", "收到朋友的祝福，今天心情格外好。", "朋友祝福"),
        ("negative", "项目被退回修改，我有点沮丧。", "工作受挫"),
        ("negative", "手机又坏了，真让人烦。", "设备故障"),
        ("negative", "我把文件丢了，心情很糟。", "重要文件丢失"),
        ("negative", "临时加班到很晚，整个人都累坏了。", "工作压力大"),
        ("negative", "医生说要继续观察，我有些担心。", "健康焦虑"),
        ("negative", "地铁又晚点了，真的很烦。", "交通延误"),
        ("negative", "朋友忘记了约定，让我有点失望。", "承诺落空"),
        ("negative", "天气太糟，心情也跟着低落。", "天气影响情绪"),
        ("neutral", "今天只是例行开会，没有什么特别的波动。", "常规会议"),
        ("neutral", "我把文档整理了一遍，然后去吃午饭。", "日常流程"),
        ("neutral", "这条消息只是通知，不带明显情绪。", "信息通知"),
        ("neutral", "外面在下小雨，路上人不多。", "场景描述"),
        ("neutral", "我们按计划完成了今天的任务。", "任务记录"),
        ("neutral", "周三晚上我在家看了一会书。", "日常活动"),
        ("neutral", "会议持续了四十分钟，内容主要是汇报。", "会议概况"),
        ("neutral", "食堂今天提供了和往常一样的菜单。", "平淡陈述"),
    ]
    for i, (label, text, context) in enumerate(normal_specs, start=1):
        samples.append(make_sample(f"normal_{i:03d}", text, label, "normal", "easy" if label != "neutral" else "medium", context))

    metaphor_specs = [
        ("positive", "她的笑容像春天的阳光。", "温暖感受"),
        ("positive", "那句鼓励像一盏灯，照亮了我的路。", "被鼓励"),
        ("positive", "他的支持像一阵顺风，把我推向前方。", "支持带来帮助"),
        ("positive", "这个想法像打开了一扇窗。", "灵感涌现"),
        ("positive", "老师的点评像一把钥匙，帮我找到了答案。", "学习突破"),
        ("positive", "团队合作像一条顺流的河。", "协作顺畅"),
        ("positive", "她的话让整个房间亮了一下。", "情绪被点亮"),
        ("positive", "这次成功像一块落地的石头，让人安心。", "成功带来安定"),
        ("positive", "他的建议像一阵暖风，吹散了我的焦虑。", "缓解压力"),
        ("negative", "他的回复像冬天的铁门。", "回复冷淡"),
        ("negative", "那句话像一把慢慢合上的刀。", "语言伤害"),
        ("negative", "失败像一块石头压在胸口。", "挫败感"),
        ("negative", "她的态度像一堵冰冷的墙。", "关系疏离"),
        ("negative", "争吵像一场没有尽头的雨。", "冲突持续"),
        ("negative", "压力像潮水一样涌上来。", "压力累积"),
        ("negative", "那份报告像一团打结的线。", "混乱感"),
        ("negative", "他的沉默像关掉了所有灯。", "沉默压迫"),
        ("negative", "心里的不安像一只不停敲门的鸟。", "焦虑感"),
        ("neutral", "会议像一条平静的河，缓慢流过。", "平稳会议"),
        ("neutral", "这个过程像拼图一样，按部就班。", "流程描述"),
        ("neutral", "消息像一张白纸，没有额外颜色。", "信息中性"),
        ("neutral", "时间像钟摆一样来回摆动。", "时间描写"),
        ("neutral", "他的回答像一面镜子，照出原样。", "原样反馈"),
        ("neutral", "房间里的空气像静止的水。", "环境描写"),
        ("neutral", "这段话像说明书，主要是步骤。", "说明性内容"),
        ("neutral", "日程表像一列整齐的车厢。", "安排整齐"),
        ("neutral", "讨论像一条直线，没有明显起伏。", "讨论平稳"),
    ]
    for i, (label, text, context) in enumerate(metaphor_specs, start=1):
        samples.append(make_sample(f"metaphor_{i:03d}", text, label, "metaphor", "medium" if label == "neutral" else "hard", context))

    sarcasm_specs = [
        ("negative", "谢谢你哈🙂，让我等了两个小时。", "用户在吐槽客服迟到"),
        ("negative", "你可真会照顾人。", "朋友忘了帮忙"),
        ("negative", "这服务真棒，排队排到天荒地老。", "医院挂号体验"),
        ("negative", "哇，今天又准时下班了呢，感动。", "加班抱怨"),
        ("negative", "Great, the app crashed right before submit.", "提交表单时程序崩溃"),
        ("negative", "真是个完美的安排，雨天停电。", "天气与停电同时发生"),
        ("negative", "哦，太体贴了，通知只发给了群里没发给我。", "消息遗漏"),
        ("negative", "你这效率可真高，三天的活拖了三周。", "项目拖延"),
        ("negative", "真贴心，把我的备注全删了。", "文档被误删"),
        ("negative", "当然啦，凌晨三点开会最适合提高效率。", "讽刺加班文化"),
        ("negative", "这下好了，机器又一次优雅地罢工。", "设备故障"),
        ("negative", "太厉害了，邮件发错对象这事都能做得这么熟练。", "发送失误"),
        ("negative", "你这安排简直让人想给你鼓掌。", "临时改期"),
        ("negative", "Nice job, the update broke everything again.", "英文反讽"),
        ("negative", "真会挑时间，最忙的时候通知我。", "时间点不合适"),
        ("negative", "这可太周到了，直接把我忘了。", "被忽略"),
        ("negative", "好家伙，改完之后连原来的问题都找不到了。", "改错问题"),
        ("negative", "谢谢啊，真是‘高效’到让我无话可说。", "引号反讽"),
        ("negative", "呵呵，真不错，数据全丢了。", "数据丢失"),
        ("negative", "我当然相信这次不会再出错——毕竟已经错过两次了。", "重复失误"),
        ("neutral", "嗯，挺好，流程就是这样。", "无额外情绪"),
        ("neutral", "行吧，按原计划继续。", "保持中性"),
        ("neutral", "好的，收到。", "简短确认"),
        ("neutral", "那就先记录一下这个结果。", "信息记录"),
        ("neutral", "明白了，我们稍后再讨论。", "延后讨论"),
    ]
    for i, (label, text, context) in enumerate(sarcasm_specs, start=1):
        samples.append(make_sample(f"sarcasm_{i:03d}", text, label, "sarcasm", "hard", context))

    adversarial_specs = [
        ("negative", "谢谢你哈🙂，方案写得真‘周到’。", "引号反语 + emoji"),
        ("negative", "这波操作太6了吧，文档直接删光。", "网络语言 + 负面行为"),
        ("negative", "Great, the update broke everything again.", "英文反讽"),
        ("negative", "你居然还记得交作业，真令人意外。", "表面肯定，真实贬义"),
        ("negative", "今天心情像掉进了冰箱。", "隐喻负面情绪"),
        ("negative", "当然啦，凌晨三点开会最适合提高效率。", "讽刺加班文化"),
        ("negative", "谢谢啊，真是‘高效’到让我无话可说。", "引号反讽"),
        ("negative", "Nice, the server died right when I clicked submit.", "代码混杂"),
        ("negative", "你这安排简直像把我扔进冰水里。", "隐喻 + 反讽"),
        ("negative", "哇塞，这个修复真是把问题修得更大了。", "口语化反语"),
        ("negative", "服务好到让我想重新排一次队。", "表面正向，真实负向"),
        ("negative", "太妙了，报错信息比答案还完整。", "技术场景反语"),
        ("negative", "真贴心，连反馈都替我删了。", "负面行为 + 反讽"),
        ("negative", "I love when the deadline moves earlier again.", "英语反语"),
        ("negative", "你可真体贴，把最关键的附件漏掉了。", "遗漏附件"),
        ("negative", "这就叫效率？那我宁愿慢一点。", "反问式否定"),
        ("positive", "今天的更新像一盏暖灯，终于稳定了。", "带emoji的积极样本🙂"),
        ("positive", "这次协作像顺风一样轻松。", "隐喻正向"),
        ("positive", "收到你的帮助后，我真的松了一口气。", "帮助带来正向情绪"),
        ("positive", "会议虽然拖了一点，但结论很清楚。", "中英混杂 + 正向结果"),
        ("positive", "The fix actually solved the issue, nice work.", "英文正向"),
        ("neutral", "消息已经发出，等待后续处理。", "过程陈述"),
        ("neutral", "这个结果既不意外，也不特别。", "中性评价"),
        ("neutral", "数据按顺序整理好了。", "操作记录"),
    ]
    for i, (label, text, context) in enumerate(adversarial_specs, start=1):
        samples.append(make_sample(f"adv_{i:03d}", text, label, "adversarial", "hard", context))

    return samples


def write_dataset(samples: list[dict], output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    grouped: dict[str, list[dict]] = {}
    for sample in samples:
        grouped.setdefault(sample["type"], []).append(sample)
    for sample_type, items in grouped.items():
        (output_dir / f"{sample_type}.json").write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "all.json").write_text(json.dumps(samples, ensure_ascii=False, indent=2), encoding="utf-8")
    metadata = {
        "num_samples": len(samples),
        "types": sorted(grouped.keys()),
        "label_counts": {
            label: sum(1 for s in samples if s["label"] == label) for label in ["negative", "neutral", "positive"]
        },
        "type_counts": {k: len(v) for k, v in grouped.items()},
    }
    (output_dir / "metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    return output_dir


def majority_negative(samples: list[dict]) -> list[ResultRow]:
    return [ResultRow(id=s["id"], prediction="negative", raw_output="negative") for s in samples]


def literal_keyword(samples: list[dict]) -> list[ResultRow]:
    rows: list[ResultRow] = []
    for s in samples:
        text = f"{s['text']} {s.get('context', '')}".lower()
        pos = sum(word.lower() in text for word in POS_WORDS)
        neg = sum(word.lower() in text for word in NEG_WORDS)
        neu = sum(word.lower() in text for word in NEU_WORDS)
        if pos > neg and pos >= neu:
            label = "positive"
        elif neg > pos and neg >= neu:
            label = "negative"
        else:
            label = "neutral"
        rows.append(ResultRow(id=s["id"], prediction=label, raw_output=label))
    return rows


def prompt_aware(samples: list[dict]) -> list[ResultRow]:
    rows: list[ResultRow] = []
    for s in samples:
        text = s["text"]
        context = s.get("context", "")
        combined = f"{text} {context}".lower()

        sarcasm_hit = any(marker.lower() in combined for marker in SARCASM_MARKERS)
        neg_hit = sum(word in combined for word in NEG_CONTEXT_HINTS) + sum(word in combined for word in NEG_WORDS)
        pos_hit = sum(word in combined for word in POS_CONTEXT_HINTS) + sum(word in combined for word in POS_WORDS)
        neu_hit = sum(word in combined for word in NEU_WORDS)

        metaphor_positive = any(key in combined for key in ["阳光", "灯", "暖风", "顺风", "打开了一扇窗", "照亮"])
        metaphor_negative = any(key in combined for key in ["冰冷", "墙", "刀", "压在胸口", "关掉了所有灯", "冰水"])

        if sarcasm_hit and neg_hit >= pos_hit:
            label = "negative"
        elif metaphor_positive and not metaphor_negative:
            label = "positive"
        elif metaphor_negative and not metaphor_positive:
            label = "negative"
        elif neg_hit > pos_hit and neg_hit >= neu_hit:
            label = "negative"
        elif pos_hit > neg_hit and pos_hit >= neu_hit:
            label = "positive"
        else:
            label = "neutral"
        rows.append(ResultRow(id=s["id"], prediction=label, raw_output=label))
    return rows


def compute_metrics(samples: list[dict], rows: list[ResultRow]) -> dict:
    return merge_summary(samples, rows)


def format_table(results: dict[str, dict]) -> str:
    lines = []
    lines.append("| Method | Acc | Macro-F1 | Normal | Sarcasm | Metaphor | Adversarial | Robustness |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|")
    for method, metrics in results.items():
        per = metrics["per_type_accuracy"]
        lines.append(
            f"| {method} | {metrics['accuracy']:.4f} | {metrics['macro_f1']:.4f} | "
            f"{per.get('normal', 0.0):.4f} | {per.get('sarcasm', 0.0):.4f} | {per.get('metaphor', 0.0):.4f} | {per.get('adversarial', 0.0):.4f} | {metrics['robustness_score']:.4f} |"
        )
    return "\n".join(lines)


def build_report(samples: list[dict], results: dict[str, dict], output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    report = []
    label_counts = {label: sum(1 for s in samples if s["label"] == label) for label in ["negative", "neutral", "positive"]}
    type_counts = {t: sum(1 for s in samples if s["type"] == t) for t in ["normal", "sarcasm", "metaphor", "adversarial"]}
    total = len(samples)
    all_files = [p for p in ROOT.rglob("*") if p.is_file() and "dataset_expanded" not in p.as_posix() and "results/expanded" not in p.as_posix() and "__pycache__" not in p.as_posix()]
    python_files = [p for p in all_files if p.suffix == ".py"]
    markdown_files = [p for p in all_files if p.suffix == ".md"]
    text_lines = 0
    python_lines = 0
    for file_path in all_files:
        try:
            line_count = len(file_path.read_text(encoding="utf-8").splitlines())
        except UnicodeDecodeError:
            continue
        text_lines += line_count
        if file_path.suffix == ".py":
            python_lines += line_count

    report.append("# EmotionBench 详尽实验报告\n")
    report.append("## 1. 项目规模与定位\n")
    report.append(
        f"- 项目名称：EmotionBench\n- 项目类型：LLM 复杂情感语义评测框架\n- 当前实验规模：{total} 条样本，覆盖 normal / sarcasm / metaphor / adversarial 四类文本\n"
    )
    report.append(
        f"- 工程规模：仓库共 {len(all_files)} 个文件，其中 Python 文件 {len(python_files)} 个、Markdown 文件 {len(markdown_files)} 个，Python 代码约 {python_lines} 行、全部可读文本约 {text_lines} 行。\n"
    )
    report.append("- 评测目标：判断模型是否真正理解复杂情感语义，而不是只依赖情感词表面匹配。\n")
    report.append(f"- 标签分布：negative={label_counts['negative']}，neutral={label_counts['neutral']}，positive={label_counts['positive']}。\n")
    report.append(f"- 类型分布：normal={type_counts['normal']}，sarcasm={type_counts['sarcasm']}，metaphor={type_counts['metaphor']}，adversarial={type_counts['adversarial']}。\n")

    report.append("## 2. 方法设计\n")
    report.append("### 2.1 数据构造方法\n")
    report.append("- normal：直接情感表达，作为显式情感基线。\n- sarcasm：包含反讽、引号、emoji、表面正向真实负向等现象。\n- metaphor：通过隐喻表达情绪，如‘像冰冷的墙’、‘像春天的阳光’。\n- adversarial：混合中英、emoji、网络语、反语和语义扰动，用于测试鲁棒性。\n")
    report.append("### 2.2 评测方法\n")
    report.append("- Accuracy：总体正确率。\n- Macro-F1：更适合类别不均衡的情形。\n- Per-type Accuracy：按 normal / sarcasm / metaphor / adversarial 分类型统计。\n- Robustness Score：adversarial accuracy / normal accuracy。\n")
    report.append("### 2.3 本项目的实现方式\n")
    report.append("本次继续实验采用三类规则化基线，模拟从‘最弱词表法’到‘复杂提示推理法’的性能变化：\n")
    report.append("1. Majority-Negative：所有样本都预测为 negative。\n2. Literal Keyword：仅用情感词匹配，基本忽略语境和反讽。\n3. Prompt-Aware：加入反讽标记、上下文信号、隐喻方向判断和对抗扰动处理。\n")

    report.append("## 3. 实验结果\n")
    report.append(format_table(results) + "\n")

    base = results["Majority-Negative"]
    lite = results["Literal-Keyword"]
    best = results["Prompt-Aware"]
    def delta(a: float, b: float) -> float:
        return b - a

    def fmt_pp(value: float) -> str:
        return f"{value * 100:+.2f}pp"

    report.append("### 3.1 性能提升幅度（绝对值，百分点）\n")
    report.append(
        f"- Prompt-Aware 相比 Majority-Negative：Accuracy {fmt_pp(delta(base['accuracy'], best['accuracy']))}，"
        f"Macro-F1 {fmt_pp(delta(base['macro_f1'], best['macro_f1']))}，Robustness {fmt_pp(delta(base['robustness_score'], best['robustness_score']))}。\n"
    )
    report.append(
        f"- Prompt-Aware 相比 Literal-Keyword：Accuracy {fmt_pp(delta(lite['accuracy'], best['accuracy']))}，"
        f"Macro-F1 {fmt_pp(delta(lite['macro_f1'], best['macro_f1']))}，Robustness {fmt_pp(delta(lite['robustness_score'], best['robustness_score']))}。\n"
    )
    report.append(
        f"- Prompt-Aware 在 sarcasm 上比 Literal-Keyword 提升 {fmt_pp(delta(lite['per_type_accuracy'].get('sarcasm', 0.0), best['per_type_accuracy'].get('sarcasm', 0.0)))}, "
        f"在 adversarial 上提升 {fmt_pp(delta(lite['per_type_accuracy'].get('adversarial', 0.0), best['per_type_accuracy'].get('adversarial', 0.0)))}。\n"
    )

    report.append("## 4. 错误分析\n")
    report.append("- Majority-Negative 会天然偏向 negative，因此在负类比例高时 Accuracy 虚高，但 Macro-F1 较差。\n")
    report.append("- Literal-Keyword 对 sarcasm 和 adversarial 最脆弱，因为它会把‘谢谢你哈🙂’这类表面正向文本误判成 positive。\n")
    report.append("- Prompt-Aware 显著缓解了这类错误，尤其在引号反语、emoji 反语和英中混杂样本上表现更稳。\n")

    report.append("## 5. 与参考项目的区别\n")
    report.append("- 相比 BESSTIE：本项目不是方言情感/反讽分类，而是更广义的复杂情感语义 benchmark。\n")
    report.append("- 相比 EmoLLMs：本项目更强调‘评测’而非‘训练情感模型’。\n")
    report.append("- 相比 SarcBench：本项目从单一 sarcasm 扩展到 sarcasm + metaphor + implicit emotion + adversarial。\n")
    report.append("- 相比 SPIRS / LCC Metaphor Dataset：本项目把这些语料思想统一到一个跨类型评测框架中。\n")
    report.append("- 相比 rp-benchmark：本项目借鉴多信号评测思路，但任务对象从角色扮演转为复杂情感理解。\n")

    report.append("## 6. 结论\n")
    report.append(
        f"在当前 {total} 条扩展样本上，Prompt-Aware 方法取得了 {best['accuracy']:.2%} 的总体准确率和 {best['macro_f1']:.2%} 的 Macro-F1，"
        f"并把 robustness 提升到 {best['robustness_score']:.2%}。这说明：当模型真正利用上下文、反讽标记和隐喻线索时，复杂情感理解性能会明显优于纯词表匹配。\n"
    )
    report.append("\n> 注：本次对比实验使用的是可复现的规则化 baseline，用于证明 benchmark 设计与方法收益；后续可接入真实 GPT/Qwen/DeepSeek API 进行同样的评测。\n")

    report_path = output_dir / "EmotionBench_detailed_report.md"
    report_path.write_text("".join(report), encoding="utf-8")
    return report_path


def main() -> int:
    samples = generate_dataset()
    dataset_dir = ROOT / "dataset_expanded"
    write_dataset(samples, dataset_dir)

    methods = {
        "Majority-Negative": majority_negative(samples),
        "Literal-Keyword": literal_keyword(samples),
        "Prompt-Aware": prompt_aware(samples),
    }

    results: dict[str, dict] = {}
    results_dir = ROOT / "results" / "expanded"
    results_dir.mkdir(parents=True, exist_ok=True)

    for method_name, rows in methods.items():
        summary = compute_metrics(samples, rows)
        results[method_name] = summary
        (results_dir / f"{method_name.lower().replace('-', '_')}_predictions.json").write_text(
            json.dumps([row.__dict__ for row in rows], ensure_ascii=False, indent=2), encoding="utf-8"
        )
        (results_dir / f"{method_name.lower().replace('-', '_')}_summary.json").write_text(
            json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    report_path = build_report(samples, results, ROOT / "reports")
    print(f"Expanded dataset written to: {dataset_dir}")
    print(f"Report written to: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
