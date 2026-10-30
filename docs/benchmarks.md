# 基准说明

`python -m reharness bench` 输出五个维度的指标，全部随 skill 单调：

| 维度 | 指标 | 方向 |
|---|---|---|
| 成功率 | success_rate | ↑（0.5 随机 → 1.0 最优） |
| 组件召回 | component_recall | ↑（≈top_k/全集 → 1.0） |
| 安全 | guardrail_violations | ↓（→ 0） |
| 对比增益 | contrastive_gain | ↑（0 → ~0.8） |
| 递归增益 | recursion_gain | ↑（0 → >0） |

`contrastive_gain = composed - random`（对比组合 vs 纯噪声选择，skill=0.5 时
两者相同故恰为 0）。`recursion_gain = recursive - flat`（两级 vs 平铺）。
