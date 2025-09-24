#!/usr/bin/env python3
"""
测试LLM调用记录功能
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 加载.env文件
try:
    from dotenv import load_dotenv
    env_file = project_root / ".env"
    if env_file.exists():
        load_dotenv(env_file)
        print(f"✅ 已加载环境变量文件: {env_file}")
    else:
        print(f"⚠️ 未找到.env文件: {env_file}")
        print("请确保在项目根目录创建.env文件并配置API密钥")
except ImportError:
    print("⚠️ 未安装python-dotenv，尝试从系统环境变量读取")
except Exception as e:
    print(f"⚠️ 加载.env文件失败: {e}")

def check_api_keys():
    """检查API密钥配置"""
    print("\n🔑 检查API密钥配置:")
    
    api_keys = {
        'DEEPSEEK_API_KEY': os.getenv('DEEPSEEK_API_KEY'),
        'DASHSCOPE_API_KEY': os.getenv('DASHSCOPE_API_KEY'),
        'GOOGLE_API_KEY': os.getenv('GOOGLE_API_KEY'),
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY')
    }
    
    available_keys = []
    for key_name, key_value in api_keys.items():
        if key_value:
            print(f"   ✅ {key_name}: {key_value[:8]}...")
            available_keys.append(key_name)
        else:
            print(f"   ❌ {key_name}: 未设置")
    
    if not available_keys:
        print("\n⚠️ 未找到任何API密钥，请在.env文件中配置至少一个API密钥")
        print("示例配置:")
        print("   DEEPSEEK_API_KEY=sk-your-deepseek-key")
        print("   DASHSCOPE_API_KEY=sk-your-dashscope-key")
        return False
    
    print(f"\n✅ 找到 {len(available_keys)} 个可用的API密钥")
    return True

def test_llm_recorder():
    """测试LLM记录功能"""
    
    print("🧪 测试LLM调用记录功能")
    print("=" * 50)
    
    # 检查API密钥
    if not check_api_keys():
        return
    
    # 启用LLM记录
    os.environ['LLM_RECORD_ENABLED'] = 'true'
    
    # 测试不同的适配器
    adapters_to_test = [
        {
            'name': 'ChatDeepSeek',
            'module': 'tradingagents.llm_adapters.deepseek_adapter',
            'class': 'ChatDeepSeek',
            'api_key_env': 'DEEPSEEK_API_KEY',
            'model': 'deepseek-chat'
        },
        {
            'name': 'DeepSeekDirectAdapter',
            'module': 'tradingagents.llm_adapters.deepseek_direct_adapter',
            'class': 'DeepSeekDirectAdapter',
            'api_key_env': 'DEEPSEEK_API_KEY',
            'model': 'deepseek-chat'
        },
        {
            'name': 'ChatDashScopeOpenAI',
            'module': 'tradingagents.llm_adapters.dashscope_openai_adapter',
            'class': 'ChatDashScopeOpenAI',
            'api_key_env': 'DASHSCOPE_API_KEY',
            'model': 'qwen-turbo'
        }
    ]
    
    successful_tests = 0
    
    for adapter_config in adapters_to_test:
        print(f"\n🔧 测试 {adapter_config['name']}...")
        
        # 检查API密钥
        api_key = os.getenv(adapter_config['api_key_env'])
        if not api_key:
            print(f"⚠️ {adapter_config['api_key_env']}未设置，跳过测试")
            continue
        
        try:
            # 动态导入适配器
            module = __import__(adapter_config['module'], fromlist=[adapter_config['class']])
            adapter_class = getattr(module, adapter_config['class'])
            
            # 创建LLM实例
            if adapter_config['name'] == 'DeepSeekDirectAdapter':
                llm = adapter_class(
                    model=adapter_config['model'],
                    temperature=0.1,
                    max_tokens=100
                )
            else:
                llm = adapter_class(
                    model=adapter_config['model'],
                    temperature=0.1,
                    max_tokens=100
                )
            
            # 测试调用
            test_messages = [
                ("system", "你是一个有用的助手。"),
                ("human", "请简单介绍一下股票投资的基本概念。")
            ]
            
            if adapter_config['name'] == 'DeepSeekDirectAdapter':
                # 直接适配器使用不同的消息格式
                test_messages = [
                    {"role": "system", "content": "你是一个有用的助手。"},
                    {"role": "user", "content": "请简单介绍一下股票投资的基本概念。"}
                ]
                response = llm.invoke(test_messages, session_id=f"test_{adapter_config['name']}", analysis_type="test")
                response_content = response
            else:
                response = llm.invoke(test_messages, session_id=f"test_{adapter_config['name']}", analysis_type="test")
                response_content = response.content
            
            print(f"✅ {adapter_config['name']} 调用成功")
            print(f"   响应长度: {len(response_content)} 字符")
            print(f"   响应预览: {response_content[:100]}...")
            
            successful_tests += 1
            
        except Exception as e:
            print(f"❌ {adapter_config['name']} 测试失败: {e}")
            import traceback
            traceback.print_exc()
    
    # 检查记录
    print(f"\n📝 检查调用记录... (成功测试: {successful_tests})")
    try:
        from tradingagents.utils.llm_call_recorder import get_llm_recorder
        
        recorder = get_llm_recorder()
        recent_records = recorder.get_recent_records(limit=successful_tests)
        
        if recent_records:
            print(f"✅ 找到 {len(recent_records)} 条最新记录:")
            
            for i, record in enumerate(recent_records):
                print(f"\n📋 记录 {i+1}:")
                print(f"   记录ID: {record['id']}")
                print(f"   提供商: {record['provider']}")
                print(f"   模型: {record['model']}")
                print(f"   会话ID: {record['session_id']}")
                print(f"   执行时间: {record['duration']:.2f}秒")
                print(f"   输入tokens: {record['input_tokens']}")
                print(f"   输出tokens: {record['output_tokens']}")
                print(f"   成本: ¥{record['cost']:.6f}")
                print(f"   文件: data/llm_records/{record['id']}.json")
            
        else:
            print("❌ 未找到调用记录")
        
    except Exception as e:
        print(f"❌ 检查记录失败: {e}")
        import traceback
        traceback.print_exc()

def show_usage():
    """显示使用说明"""
    print("\n" + "=" * 60)
    print("📖 LLM调用记录功能使用说明")
    print("=" * 60)
    print()
    print("1. 启用记录功能:")
    print("   export LLM_RECORD_ENABLED=true")
    print()
    print("2. 运行分析:")
    print("   python your_analysis_script.py")
    print()
    print("3. 查看记录文件:")
    print("   ls data/llm_records/")
    print("   cat data/llm_records/deepseek_*.json")
    print()
    print("4. 记录文件包含:")
    print("   - 完整的输入消息（system + human）")
    print("   - 完整的输出响应")
    print("   - Token使用量和成本")
    print("   - 执行时间和上下文信息")
    print()
    print("5. 支持的适配器:")
    print("   ✅ ChatDeepSeek")
    print("   ✅ ChatDashScopeOpenAI")
    print("   🔄 其他适配器可按需添加")

if __name__ == "__main__":
    test_llm_recorder()
    show_usage()
