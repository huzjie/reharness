# 架构设计

reharness 是一个**零依赖**的递归智能体 Harness 优化框架，复现 Harness2 的核心
思想：**不碰模型权重，只优化包在模型外面的那层 Harness**（系统提示词、护栏、
记忆、技能、工具指引、脚本、子智能体、中间件）。

## 分层结构

```
world         确定性任务宇宙（oracle / agent / trace），只从 trace 学，不泄露标签
harness       Harness 数据模型 + 8 类组件 + 序列化
propose       变异算子：随机子集 / 增删 / 开关
probe         在候选 harness 下跑 agent，收集执行 trace
compose       对比打分（success-lift）+ 按 skill 选择 + 重组成新 harness
optimizer     PPC 主循环 + 两级递归（优化优化器自身的 config）
scoring       指标：成功率 / 组件召回 / 护栏违规 / 对比增益
training      skill 单调训练 + 线性打分器（真实权重 SGD/AdamW）
serving       标准库 HTTP（/v1/optimize /v1/recursive）
```

## 核心设计取舍

1. **只优化 harness，不优化权重**：权重是"谁在思考"，harness 是"它怎么思考"。
   改 harness 便宜、可审计、可回滚，而且实证上（Harness2 的结论）调好 harness
   的弱模型能打赢用默认 harness 的强模型。
2. **无标签学习**：优化器只看到执行 trace（成功/失败 + 用了哪些组件），永远
   看不到 oracle 的"正确答案"。这是"对比式 Propose-Probe-Compose"的根基。
3. **可证伪的单调性**：所有基准指标（成功率、组件召回、护栏违规、对比增益、
   递归增益）都随 skill 单调，用断言而非肉眼判断。
