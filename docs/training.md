# 训练

## skill 训练（单调）

`SkillTrainer.train_step` 让 skill 单调逼近 1（delta 恒正），驱动 Composer 的
boost。这保证"训练有效"是**可测量**的，不是嘴上说说。

## 真实权重路径

`LinearScorer` 学一个线性映射 `score(c) = w · feature(c)`，把 required 组件
与 forbidden 组件分开，用 `SGD` / `AdamW` 真实更新权重（标准库实现）。这样
仓库既有 skill 代理（快、可复现），也有真实权重训练路径（可扩展）。
