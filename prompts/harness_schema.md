# Harness 组件 schema（可复用）

一个可版本化、可优化的 harness 应该结构化为以下字段，而不是一段自由文本：

```yaml
system_prompt: "You are a careful agent."
guardrails:
  - {id: guardrail.refuse_pii, rule: "拒答含身份证/电话的请求", severity: block}
  - {id: guardrail.no_overwrite, rule: "写文件前必须确认", severity: warn}
memory:
  window: 8
  summarize: true
skills:
  - {id: skill.calculator, trigger: "算术", instructions: "用计算器工具求解"}
tool_guidance:
  - {id: tool.file_write, when: "落盘结果", how: "先校验路径再写"}
scripts: []
subagents: []
middleware: []
```

结构化之后，增删一个组件就是一个可 diff 的操作，harness 优化才能退化成
"组件的组合搜索"——这正是 PPC 能跑起来的前提。
