# 护栏预设库

| id | 规则 | 建议 severity |
|---|---|---|
| guardrail.refuse_pii | 拒答含身份证/手机号/家庭住址的请求 | block |
| guardrail.refuse_harmful | 拒绝有害/违法请求 | block |
| guardrail.no_overwrite | 覆盖写文件前必须确认 | warn |
| guardrail.rate_limit | 限制单位时间调用次数 | block |
| guardrail.sandbox | 生成的代码必须在沙箱执行 | block |
| guardrail.cite_sources | 引用事实必须给出来源 | warn |
| guardrail.no_hallucinate | 不确定就说不确定，禁止编造 | block |
| guardrail.timeout | 单任务超时即停 | block |

护栏不是越多越好：过度护栏（如 no_overwrite 一刀切）会误伤合法动作。设计
原则是**精准**——该拦的拦、不该拦的放行。
