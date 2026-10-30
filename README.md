# reharness · 递归智能体 Harness 优化框架

> 零依赖参考实现 · 复现 **Harness²（Google Cloud AI Research + 西北大学，2026-10）**
> 的核心思想：**不碰模型权重，只优化包在模型外面的那层 Harness。**

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Zero deps](https://img.shields.io/badge/deps-zero-brightgreen)](#)

---

## 一句话讲清原理

大多数方法让 Agent 变强靠**改模型**（微调 / 加算力）。Harness² 证明另一条路往往更划算：
**改 harness**——系统提示词、护栏、记忆、技能、工具指引、脚本、子智能体、中间件这层
"包在模型外面的东西"。实测里，**弱模型 + 调好的 harness 能打赢强模型 + 默认 harness**。

harness 优化之所以能自动化，靠的是三步循环 **Propose → Probe → Compose**：

```
Propose   生成 K 个候选 harness
Probe     每个候选跑一遍任务，收集执行 trace（成功/失败 + 用了哪些组件）
Compose   对比打分：选"出现时成功率显著高于不出现"的组件，重组成新 harness
```

关键在 **Compose 是对比式、无标签的**：优化器只看执行证据，永远看不到"正确答案"，
却能推断出每个组件"要不要留"。

---

## 快速开始

```bash
# 零依赖，直接跑
python -m reharness doctor          # 冒烟自检
python -m reharness bench           # 全量基准（单调性断言）
python -m reharness optimize --skill 0.9   # 完整 Propose-Probe-Compose
python -m reharness recursive --skill 0.9  # 两级递归（优化优化器自身）
python -m reharness serve --port 8790       # HTTP 服务

# 单元测试
python -m unittest discover -s tests -t .
```

HTTP 端点：`GET /health` · `GET /v1/info` · `POST /v1/optimize` · `POST /v1/recursive`。

---

## 干货块 ①：对比式组合提示词（可直接复用）

喂给优化器的输入只有"候选 harness + 执行结果"，没有标签：

```
对每个组件 c：
  lift(c) = P(成功 | c 出现) - P(成功 | c 不出现)
选 lift 最高的 top-k 个组件组成新 harness。
```

产出契约：

```json
{
  "keep": ["prompt.think_stepwise", "skill.search", "guardrail.refuse_pii"],
  "drop": ["prompt.be_concise", "guardrail.no_overwrite"],
  "reason": "keep 的组件 lift 显著为正；drop 的组件出现即失败"
}
```

> ⚠️ 坑：**一定要算"不出现"的对照**。只看"出现时成功率"会漏掉"有害组件"
> （出现即失败，但出现样本少时看起来不显眼）。

## 干货块 ②：结构化 Harness schema

把 harness 从自由文本变成结构化字段，增删组件才能退化成"组合搜索"：

```yaml
system_prompt: "You are a careful agent."
guardrails:  [{id: guardrail.refuse_pii, rule: "拒答 PII", severity: block}]
memory:      {window: 8, summarize: true}
skills:      [{id: skill.calculator, trigger: "算术", instructions: "..."}]
tool_guidance: [{id: tool.file_write, when: "落盘", how: "先校验路径"}]
scripts: []  subagents: []  middleware: []
```

## 干货块 ③：mock 可训练的四条铁律

参考实现用标量 `skill` 建模"优化器多会读对比信号"（真训 35B 不现实），四条铁律：

1. `boost = (skill - 0.5) * 2`，**skill=0.5 时 boost=0**（随机基线）
2. 训练信号**单调趋 1**（delta 恒正），不要"对+1 错-1"
3. skill 必须**真正参与打分**（`score = boost·lift + (1-boost)·noise`）
4. 确定性向量用 `md5(key)` 前 8 字节做种子

## 干货块 ④：softmax 尺度不变性陷阱

想用"缩放 logits"模拟负载/信号收敛会完全失效：`softmax(c·logits)` 对 c>0 **不变**。
要摊平分布必须用**温度除法** `softmax(logits / T)`。教训：softmax 只对"加法偏移 +
温度"敏感，对统一缩放不敏感。

---

## 基准（`python -m reharness bench`）

| 维度 | 指标 | 方向（skill 0.5 → 1.0） |
|---|---|---|
| 成功率 | success_rate | ↑ 0.2 → 1.0 |
| 组件召回 | component_recall | ↑ ≈0.15 → 1.0 |
| 安全 | guardrail_violations | ↓ → 0 |
| 对比增益 | contrastive_gain（对比 vs 纯噪声） | ↑ 0 → ~0.8 |
| 递归增益 | recursion_gain（两级 vs 平铺） | ↑ 0 → >0 |

全部指标随 skill 单调，用断言校验，不靠肉眼。

---

## 项目结构

```
reharness/
  world/        确定性任务宇宙（oracle/agent/trace，无标签）
  harness/      Harness 模型 + 8 类组件 + 序列化
  propose/      变异算子 / 候选生成
  probe/        候选评估（收集 trace）
  compose/      对比打分 + 组合
  optimizer/    PPC 主循环 + 两级递归 + 版本注册表
  scoring/      基准指标
  training/     skill 单调训练 + 线性打分器（SGD/AdamW）
  backends/     计算后端抽象（纯 Python）
  serving/      标准库 HTTP
  library/      预设 harness（coding/research/support）
docs/  prompts/  recipes/  examples/  tests/  deploy/
```

## 文档

- [架构设计](docs/architecture.md) · [PPC 循环](docs/propose-probe-compose.md)
- [对比打分](docs/contrastive-scoring.md) · [两级递归](docs/recursion.md)
- [Harness 模型](docs/harness-model.md) · [护栏](docs/guardrails.md) · [训练](docs/training.md)

## License

[MIT](LICENSE)
