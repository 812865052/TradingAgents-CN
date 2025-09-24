# LLM调用记录功能

## 📋 概述

LLM调用记录功能允许您详细记录所有大模型的输入和输出内容，用于调试、分析和优化模型使用。

## 🚀 快速开始

### 1. 启用记录功能

```bash
# 设置环境变量启用记录
export LLM_RECORD_ENABLED=true

# 或者在.env文件中添加
echo "LLM_RECORD_ENABLED=true" >> .env
```

### 2. 运行分析

```bash
# 运行任何使用LLM的分析
python examples/simple_analysis_demo.py

# 或者通过Web界面进行分析
python start_web.py
```

### 3. 查看记录

```bash
# 查看记录文件
ls data/llm_records/

# 查看具体记录
cat data/llm_records/deepseek_deepseek-chat_20250923_225500_123456.json
```

## 📊 记录内容

每次LLM调用都会生成一个JSON记录文件，包含以下信息：

### 基本信息
- `id`: 唯一记录ID
- `timestamp`: 调用时间戳
- `provider`: 模型提供商（如：deepseek、dashscope）
- `model`: 具体模型名称
- `session_id`: 会话ID
- `duration`: 执行时间（秒）

### Token和成本信息
- `input_tokens`: 输入token数量
- `output_tokens`: 输出token数量
- `cost`: 调用成本（人民币）

### 调用详情
- `request`: 完整的输入消息
- `response`: 完整的输出响应
- `context`: 上下文信息（分析类型、参数等）

## 📝 记录文件示例

```json
{
  "id": "deepseek_deepseek-chat_20250923_225500_123456",
  "timestamp": "2025-09-23T22:55:00.123456",
  "provider": "deepseek",
  "model": "deepseek-chat",
  "session_id": "analysis_9813c258_20250923_224032",
  "duration": 2.45,
  "input_tokens": 1165,
  "output_tokens": 82,
  "cost": 0.001861,
  "context": {
    "analysis_type": "stock_analysis",
    "stop_sequences": null,
    "kwargs": {}
  },
  "request": {
    "type": "list",
    "messages": [
      {
        "role": "system",
        "content": "您是一位专业的金融分析助手，负责从交易员的分析报告中提取结构化的投资决策信息..."
      },
      {
        "role": "human",
        "content": "# TEM 综合分析报告\n\n## 📊 实时行情\n- 股票名称: Tempus AI Inc..."
      }
    ]
  },
  "response": {
    "type": "ChatResult",
    "generations": [
      {
        "type": "AIMessage",
        "content": "{\"action\": \"卖出\", \"target_price\": 0.0, \"confidence\": 0.9, \"risk_score\": 0.9, \"reasoning\": \"标的股票TEM基本身份信息无法验证...\"}"
      }
    ]
  }
}
```

## 🔧 支持的适配器

### ✅ 已支持
- `ChatDeepSeek` - DeepSeek模型适配器
- `ChatDashScopeOpenAI` - 阿里百炼模型适配器

### 🔄 待支持
- `ChatGoogleOpenAI` - Google Gemini适配器
- `ChatOpenAI` - OpenAI模型适配器

## 📁 文件结构

```
data/llm_records/
├── deepseek_deepseek-chat_20250923_225500_123456.json
├── dashscope_qwen-turbo_20250923_225501_234567.json
└── ...
```

## 🛠️ 高级用法

### 编程方式访问记录

```python
from tradingagents.utils.llm_call_recorder import get_llm_recorder

# 获取记录器
recorder = get_llm_recorder()

# 检查是否启用
if recorder.is_enabled():
    print("记录功能已启用")

# 获取最近的记录
recent_records = recorder.get_recent_records(limit=10)
for record in recent_records:
    print(f"调用: {record['provider']}/{record['model']}")
    print(f"成本: ¥{record['cost']:.6f}")
    print(f"时长: {record['duration']:.2f}s")
```

### 自定义记录目录

```python
from tradingagents.utils.llm_call_recorder import LLMCallRecorder

# 自定义记录目录
recorder = LLMCallRecorder(record_dir="my_custom_records")
```

## 📊 分析记录数据

### 成本分析脚本

```python
import json
import glob
from pathlib import Path

def analyze_costs():
    """分析LLM调用成本"""
    records_dir = Path("data/llm_records")
    total_cost = 0
    provider_costs = {}
    
    for record_file in records_dir.glob("*.json"):
        with open(record_file, 'r', encoding='utf-8') as f:
            record = json.load(f)
            
        cost = record.get('cost', 0)
        provider = record.get('provider', 'unknown')
        
        total_cost += cost
        provider_costs[provider] = provider_costs.get(provider, 0) + cost
    
    print(f"总成本: ¥{total_cost:.6f}")
    for provider, cost in provider_costs.items():
        print(f"{provider}: ¥{cost:.6f}")

analyze_costs()
```

### Token使用分析

```python
def analyze_tokens():
    """分析Token使用情况"""
    records_dir = Path("data/llm_records")
    total_input = 0
    total_output = 0
    
    for record_file in records_dir.glob("*.json"):
        with open(record_file, 'r', encoding='utf-8') as f:
            record = json.load(f)
            
        total_input += record.get('input_tokens', 0)
        total_output += record.get('output_tokens', 0)
    
    print(f"总输入tokens: {total_input:,}")
    print(f"总输出tokens: {total_output:,}")
    print(f"总tokens: {total_input + total_output:,}")

analyze_tokens()
```

## ⚠️ 注意事项

### 隐私和安全
- 记录文件包含完整的输入输出内容，可能包含敏感信息
- 请妥善保管记录文件，避免泄露
- 生产环境中请谨慎启用此功能

### 存储空间
- 每次调用都会生成一个JSON文件
- 长时间运行可能产生大量记录文件
- 建议定期清理旧记录文件

### 性能影响
- 记录功能对性能影响很小
- 文件写入是异步的，不会阻塞LLM调用
- 如果遇到性能问题，可以禁用记录功能

## 🔧 故障排除

### 记录文件未生成
1. 检查环境变量：`echo $LLM_RECORD_ENABLED`
2. 检查目录权限：`ls -la data/`
3. 检查日志：查看是否有记录相关的错误信息

### 记录内容不完整
1. 确保使用支持的LLM适配器
2. 检查是否有异常被捕获但未报告

### 禁用记录功能
```bash
# 临时禁用
unset LLM_RECORD_ENABLED

# 或设置为false
export LLM_RECORD_ENABLED=false
```

## 📞 支持

如果您在使用过程中遇到问题，请：
1. 检查上述故障排除步骤
2. 查看项目日志文件
3. 提交Issue到项目仓库
