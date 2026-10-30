# 对比式组合提示词模板（可直接复用）

这是 Harness2 风格"无标签 harness 优化"的核心提示词，把"这个组件要不要留"
交给执行证据而非人工标注。

## 输入（喂给优化器）

```
我们有 N 个候选 harness，每个由一组组件构成（组件 id 如 skill.calculator、
guardrail.refuse_pii）。每个候选在若干任务上的执行结果为 成功/失败。

任务：判断每个组件"出现 vs 不出现"时成功率差多少，选出与成功强关联的组件。
```

## 计算（对比打分）

```
对每个组件 c：
  lift(c) = P(成功 | c 出现) - P(成功 | c 不出现)
选 lift 最高的 top-k 个组件组成新 harness。
```

## 直接可用的 JSON 输出契约

```json
{
  "keep": ["prompt.think_stepwise", "skill.search", "guardrail.refuse_pii"],
  "drop": ["prompt.be_concise", "guardrail.no_overwrite"],
  "reason": "keep 的组件 lift 显著为正；drop 的组件出现即失败（lift 显著为负）"
}
```

## 复用要点

- **一定要算"不出现"的对照**：只看"出现时成功率"会漏掉有害组件。
- 候选集要够多样，否则 lift 被共线性污染。
- 中性组件 lift≈0，别被有限样本噪声骗进 keep 列表。
