# 快速开始

```bash
# 零依赖，直接跑
python -m reharness doctor          # 冒烟自检
python -m reharness bench           # 全量基准（单调性断言）
python -m reharness compose --skill 0.8   # 单次对比组合
python -m reharness optimize --skill 0.9  # 完整 PPC
python -m reharness recursive --skill 0.9 # 两级递归
python -m reharness train --epochs 12     # skill 训练
python -m reharness serve --port 8790     # HTTP 服务
```

HTTP 端点：`/health`、`/v1/info`、`POST /v1/optimize`、`POST /v1/recursive`。

## 单元测试

```bash
python -m unittest discover -s tests -t .
```
