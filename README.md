# 应急场景下基于多智能体的意图理解和协同决策

## 部署方法

准备一个 NUWA 平台的 API key，用于大模型接口

```shell
python ./interface/gradio_app.py
```

## 模块

由 app/pipeline.py 执行整个核心逻辑，依次调用模块

- 规划器 planner
- 调用器 executor
- 总结器 aggregator

## 注意事项

- 寻路图片格式要求见测试样例
- 音频请使用 flac
