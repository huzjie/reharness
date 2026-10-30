# 两级递归

Harness2 的核心创新是**递归**：不只优化 agent 的 harness，还把优化器当成一个
agent，去优化"优化器自己的 harness"（它的提议策略、打分 rubric）。

reharness 里第二级是一个小 meta 空间：

```
score.lift / score.present      打分 rubric（强 vs 弱）
op.diverse / op.narrow          提议多样性（probe_size 8 vs 3）
```

第二级用**同一个 PPC**：廉价评估 4 个候选优化器 config → 算 meta-lift →
按 skill 选 meta 组件 → 用选出的 config 跑正式 PPC。

## 收益从哪来

两级收益 = 递归成功 - 平铺（固定次优 config）成功。skill=1 时递归选出
`{lift, diverse}`，正式 PPC 恢复最优 harness（成功率 1.0）；平铺用
`{present, narrow}`，只能恢复一半 → 增益显著为正。skill=0.5 时两者都随机，
增益≈0。递归的价值正是"让优化器学会怎么优化"。
