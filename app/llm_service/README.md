# 基于 BiLSTM-CRF 的中文命名实体识别

## GitHub 项目地址

本项目的完整代码与实验报告已同步开源至 GitHub：[SequenceAnnotation](https://github.com/xs-william/SequenceAnnotation)

训练好的模型（利用4090训练了20轮，共40mins）位置：[best.pt](https://github.com/xs-william/SequenceAnnotation/tree/main/outputs/checkpoints)

## 一、实验目的与任务要求

本实验的目标是利用深度学习模型完成 **序列标注任务**，
要求识别出文本中的 **人名**、**地名** 和 **组织机构名**。

实验使用 1998 年《人民日报》语料中的中文数据集，格式如下：

* `train_corpus.txt`：训练文本
* `train_label.txt`：对应的标签
* `test_corpus.txt`：测试文本
* `test_label.txt`：对应的标签

评价指标要求：

> 使用 **准确率（Accuracy）**、**召回率（Recall）**、**F1 值（F1-Score）** 进行模型评估，
> 并分别计算：
> 1️⃣ 包含“O”标签的整体指标
> 2️⃣ 去除“O”标签后的实体识别指标。

---

## 二、模型结构与方法说明

### 1️⃣ 模型选择

本实验选用 **BiLSTM + CRF（双向长短时记忆网络 + 条件随机场）** 模型。

原因如下：BiLSTM 能捕捉上下文双向依赖信息，对序列任务效果显著；并且相比传统 LSTM方法，BiLSTM-CRF 更适合中文 NER 任务。

---

### 2️⃣ 模型结构

```
输入序列（字符级别）
   ↓
Embedding 层（向量化）
   ↓
双向 LSTM 层（上下文特征抽取）
   ↓
线性层（映射至标签空间）
   ↓
CRF 层（序列条件解码）
   ↓
输出预测标签序列
```

损失函数为 CRF 的负对数似然（NLL），优化器采用 Adam。

---

### 3️⃣ 模型具体参数

| 模块             | 实现方式               |
| -------------- | ------------------ |
| 嵌入层（Embedding） | 随机初始化，可学习          |
| BiLSTM 隐层维度    | 256                |
| CRF 解码         | 采用维特比算法求最优路径       |
| Dropout        | 0.3                |
| 优化器            | Adam               |
| 学习率            | 1e-3               |
| 最大轮数           | 20 轮                |
| Batch Size     | 32                 |

---

## 三、实验环境

| 环境项       | 配置                                |
| --------- | --------------------------------- |
| 操作系统      | Ubuntu 18.04                      |
| Python 版本 | 3.8                               |
| 深度学习框架    | PyTorch 2.4.1                     |
| CUDA 版本   | 11.3                              |
| GPU       | NVIDIA RTX 4090（24GB）             |
| 依赖安装      | `pip install -r requirements.txt` |

---

## 四、实验结果

### ✅ 含“O”类别（整体性能）

| 指标       | 值      |
| -------- | ------ |
| Accuracy | 0.9805 |
| Recall   | 0.9805 |
| F1       | 0.9805 |

---

### ✅ 去“O”类别（实体识别性能）

| 指标       | 值      |
| -------- | ------ |
| Accuracy | 0.9805 |
| Recall   | 0.8663 |
| F1       | 0.8883 |

所有评测结果自动保存至：

```
outputs/eval_results.txt
```

---

## 五、结果分析与思考

整体来看，**整体准确率较高（97%）**，说明模型对非实体字符预测稳定；并且**实体识别 F1 ≈ 0.88**反映了BiLSTM 能较好捕捉上下文特征。

---

## 六、运行说明

```bash
# 训练模型
python train.py

# 评估最优模型
python evaluate.py

# 预测并保存实体
python predict.py
```

预测结果保存在：

```
outputs/test_entities.tsv
```