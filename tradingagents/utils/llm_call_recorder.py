#!/usr/bin/env python3
"""
LLM调用记录器
用于记录大模型的输入和输出内容
"""

import json
import os
import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from pathlib import Path

from tradingagents.utils.logging_manager import get_logger
logger = get_logger('llm_recorder')


class LLMCallRecorder:
    """LLM调用记录器"""
    
    def __init__(self, record_dir: str = "data/llm_records"):
        self.record_dir = Path(record_dir)
        self.record_dir.mkdir(parents=True, exist_ok=True)
        self.enabled = self._check_enabled()
        
        if self.enabled:
            logger.info(f"📝 LLM调用记录器已启用，记录目录: {self.record_dir}")
        else:
            logger.debug(f"📝 LLM调用记录器未启用")
    
    def _check_enabled(self) -> bool:
        """检查是否启用记录"""
        return os.getenv('LLM_RECORD_ENABLED', 'false').lower() == 'true'
    
    def is_enabled(self) -> bool:
        """检查记录器是否启用"""
        return self.enabled
    
    def record_call(
        self, 
        provider: str, 
        model: str, 
        messages: Any, 
        response: Any, 
        duration: float, 
        session_id: str = None, 
        context: Dict = None,
        input_tokens: int = 0,
        output_tokens: int = 0,
        cost: float = 0.0
    ):
        """记录LLM调用"""
        
        if not self.enabled:
            return
        
        try:
            # 生成记录ID
            timestamp = datetime.now()
            record_id = f"{provider}_{model}_{timestamp.strftime('%Y%m%d_%H%M%S_%f')}"
            
            # 准备记录数据
            record = {
                "id": record_id,
                "timestamp": timestamp.isoformat(),
                "provider": provider,
                "model": model,
                "session_id": session_id or "unknown",
                "duration": round(duration, 3),
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "cost": cost,
                "context": context or {},
                "request": self._serialize_messages(messages),
                "response": self._serialize_response(response),
            }
            
            # 保存到文件
            record_file = self.record_dir / f"{record_id}.json"
            with open(record_file, 'w', encoding='utf-8') as f:
                json.dump(record, f, ensure_ascii=False, indent=2)
            
            logger.debug(f"📝 LLM调用记录已保存: {record_file.name}")
            
        except Exception as e:
            logger.error(f"❌ 保存LLM调用记录失败: {e}")
    
    def _serialize_messages(self, messages):
        """序列化输入消息"""
        try:
            if isinstance(messages, str):
                return {
                    "type": "string",
                    "content": messages
                }
            elif isinstance(messages, list):
                serialized = []
                for msg in messages:
                    if hasattr(msg, 'content'):
                        # LangChain消息对象
                        serialized.append({
                            "type": msg.__class__.__name__,
                            "content": msg.content
                        })
                    elif isinstance(msg, tuple) and len(msg) == 2:
                        # 元组格式 (role, content)
                        serialized.append({
                            "role": msg[0],
                            "content": msg[1]
                        })
                    elif isinstance(msg, dict):
                        # 字典格式
                        serialized.append(msg)
                    else:
                        serialized.append(str(msg))
                return {
                    "type": "list",
                    "messages": serialized
                }
            else:
                return {
                    "type": "unknown",
                    "content": str(messages)
                }
        except Exception as e:
            return {
                "type": "error",
                "error": str(e)
            }
    
    def _serialize_response(self, response):
        """序列化输出响应"""
        try:
            if hasattr(response, 'generations') and response.generations:
                # ChatResult对象
                generations = []
                for gen in response.generations:
                    if hasattr(gen, 'message') and hasattr(gen.message, 'content'):
                        generations.append({
                            "type": gen.message.__class__.__name__,
                            "content": gen.message.content
                        })
                return {
                    "type": "ChatResult",
                    "generations": generations
                }
            elif hasattr(response, 'content'):
                # AIMessage对象
                return {
                    "type": response.__class__.__name__,
                    "content": response.content
                }
            elif isinstance(response, str):
                return {
                    "type": "string",
                    "content": response
                }
            else:
                return {
                    "type": "unknown",
                    "content": str(response)
                }
        except Exception as e:
            return {
                "type": "error",
                "error": str(e)
            }
    
    def get_recent_records(self, limit: int = 10) -> List[Dict]:
        """获取最近的记录"""
        try:
            record_files = sorted(
                self.record_dir.glob("*.json"),
                key=lambda x: x.stat().st_mtime,
                reverse=True
            )
            
            records = []
            for record_file in record_files[:limit]:
                try:
                    with open(record_file, 'r', encoding='utf-8') as f:
                        record = json.load(f)
                        records.append(record)
                except Exception as e:
                    logger.warning(f"读取记录文件失败 {record_file}: {e}")
            
            return records
        except Exception as e:
            logger.error(f"获取记录失败: {e}")
            return []


# 全局记录器实例
_llm_recorder = None


def get_llm_recorder() -> LLMCallRecorder:
    """获取全局LLM记录器实例"""
    global _llm_recorder
    if _llm_recorder is None:
        _llm_recorder = LLMCallRecorder()
    return _llm_recorder
