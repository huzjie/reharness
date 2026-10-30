# Harness 数据模型

一个 Harness 是"包裹模型的一切"的结构化、可版本化描述：

```
system_prompt      系统提示词
guardrails[]       护栏规则（refuse_pii / no_overwrite / sandbox ...）
memory             记忆策略（window / summarize / retrieval）
skills[]           技能（trigger + instructions）
tool_guidance[]    工具指引（when + how）
scripts[]          辅助脚本
subagents[]        可委派子智能体
middleware[]       中间件（pre/post 处理器）
```

每个组件都有稳定 `id`（如 `skill.calculator`）和 `kind`。优化器通过**增删组件**
来改变 harness。HarnessRegistry 把每次组合结果记录为不可变版本，支持 diff 和
rollback（对应 harness 优化框架里的 "git tree of adapters" 审计能力）。
