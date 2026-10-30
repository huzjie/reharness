# HTTP API

## GET /health
`{"status": "ok", "name": "reharness"}`

## GET /v1/info
返回名称、版本与可用端点。

## POST /v1/optimize
```json
{"skill": 0.9, "top_k": 6, "scoring": "lift", "probe_size": 8}
```
返回完整 PPC 结果：`success_rate / component_recall / guardrail_violations / contrastive_gain / selected`。

## POST /v1/recursive
```json
{"skill": 0.9}
```
返回 `recursive / flat / gain / meta_selected`。
