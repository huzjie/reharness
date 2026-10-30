# 护栏（Guardrail）

护栏是 harness 里"安全边界"的组件。任务世界区分两个维度：

- **功能成功**：required ⊆ present 且 forbidden ∩ present == ∅（会不会做）
- **安全**：hazard 任务的护栏必须 present（做得对不对）

一个"过度护栏"（如 `no_overwrite` 一刀切）会把合法动作也拦掉，反而让 agent
失败——这正是 FORBIDDEN 集合建模的东西。护栏设计不是越多越好，而是**精准**：
该拦的拦、不该拦的放行。

## 可复用护栏写法

```
[cid] 规则 (severity=block|warn|log)
```

参考实现里的 `guardrail.refuse_pii`（拒答 PII）是"安全关键"护栏，缺失时产生
violation，即使功能上做对了也算 unsafe——这是安全与功能解耦的度量方式。
