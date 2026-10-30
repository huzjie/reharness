# 对比打分细节

## skill 的作用

参考实现用标量 `skill` 建模"优化器多会读对比信号"（真训 35B MoE 不现实）：

```
boost = (skill - 0.5) * 2
score(c) = boost * lift(c) + (1 - boost) * noise(c)
```

- skill=0.5 → boost=0 → 纯噪声选择（随机基线，组件召回 ≈ top_k / 全集）
- skill=1.0 → boost=1 → 纯 lift 选择（精确恢复最优集合）

训练信号单调趋 1，skill=0.5 时 boost=0（随机基线），这是 mock 可训练的铁律。

## 为什么用 lift 而不是 presence-rate

presence-rate（"出现时的成功率"）不看"不出现"的对照，信号弱很多。递归
（两级）演示里专门用 presence-rate 当"弱 rubric"，与 lift 形成对照：同一份
trace，用 lift 能恢复最优 harness，用 presence-rate 只能恢复一半——这正说明
"对比"这个动作本身是价值的来源。

## 坑

- `softmax(c·logits)` 对 c>0 不变（尺度不变性），要摊平分布必须用温度除法。
- `argmax` 全等并列恒取 index 0，统计负载/门控时要用软统计而非硬 argmax。
