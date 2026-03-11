#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
代理基类 - 所有专业代理的基类
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@dataclass
class Task:
    """任务定义"""
    id: str
    type: str
    parameters: Dict[str, Any]
    priority: int = 1  # 1-5，5最高
    timeout: int = 30  # 秒
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

@dataclass
class TaskResult:
    """任务结果"""
    task_id: str
    success: bool
    data: Dict[str, Any]
    error: Optional[str] = None
    execution_time: float = 0.0
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

class BaseAgent(ABC):
    """代理基类"""
    
    def __init__(self, name: str, expertise: str, version: str = "1.0.0"):
        """
        初始化代理
        
        Args:
            name: 代理名称
            expertise: 专业领域描述
            version: 代理版本
        """
        self.name = name
        self.expertise = expertise
        self.version = version
        self.logger = logging.getLogger(f"agent.{name}")
        self._initialized = False
        
        # 统计信息
        self.stats = {
            'tasks_completed': 0,
            'tasks_failed': 0,
            'total_execution_time': 0.0,
            'last_execution_time': None,
        }
        
    def initialize(self) -> bool:
        """初始化代理"""
        if self._initialized:
            return True
            
        try:
            self._setup()
            self._initialized = True
            self.logger.info(f"代理 {self.name} 初始化成功")
            return True
        except Exception as e:
            self.logger.error(f"代理 {self.name} 初始化失败: {e}")
            return False
    
    @abstractmethod
    def _setup(self):
        """设置代理（子类实现）"""
        pass
    
    @abstractmethod
    def execute(self, task: Task) -> TaskResult:
        """执行任务（子类实现）"""
        pass
    
    def execute_with_retry(self, task: Task, max_retries: int = 3) -> TaskResult:
        """带重试的执行"""
        import time
        
        for attempt in range(max_retries):
            try:
                start_time = time.time()
                result = self.execute(task)
                execution_time = time.time() - start_time
                
                result.execution_time = execution_time
                
                # 更新统计
                self.stats['tasks_completed'] += 1
                self.stats['total_execution_time'] += execution_time
                self.stats['last_execution_time'] = datetime.now()
                
                if result.success:
                    self.logger.info(f"任务 {task.id} 执行成功 (尝试 {attempt+1})")
                    return result
                else:
                    self.logger.warning(f"任务 {task.id} 执行失败: {result.error} (尝试 {attempt+1})")
                    
            except Exception as e:
                self.logger.error(f"任务 {task.id} 执行异常: {e} (尝试 {attempt+1})")
                result = TaskResult(
                    task_id=task.id,
                    success=False,
                    data={},
                    error=f"执行异常: {str(e)}"
                )
            
            # 如果不是最后一次尝试，等待后重试
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # 指数退避
                self.logger.info(f"等待 {wait_time} 秒后重试...")
                time.sleep(wait_time)
        
        # 所有尝试都失败
        self.stats['tasks_failed'] += 1
        self.logger.error(f"任务 {task.id} 所有重试都失败")
        return result
    
    def get_capabilities(self) -> Dict[str, Any]:
        """获取代理能力描述"""
        return {
            'name': self.name,
            'expertise': self.expertise,
            'version': self.version,
            'initialized': self._initialized,
            'capabilities': self._get_capabilities(),
            'stats': self.stats,
        }
    
    @abstractmethod
    def _get_capabilities(self) -> List[str]:
        """获取具体能力列表（子类实现）"""
        pass
    
    def get_status(self) -> Dict[str, Any]:
        """获取代理状态"""
        return {
            'name': self.name,
            'status': 'ready' if self._initialized else 'not_initialized',
            'stats': self.stats,
            'last_update': datetime.now().isoformat(),
        }
    
    def validate_task(self, task: Task) -> bool:
        """验证任务是否适合本代理"""
        # 基础验证：检查任务类型是否在能力范围内
        capabilities = self._get_capabilities()
        return task.type in capabilities
    
    def cleanup(self):
        """清理资源"""
        self.logger.info(f"代理 {self.name} 清理资源")
        self._initialized = False
    
    def __str__(self):
        return f"{self.name} ({self.expertise}) v{self.version}"
    
    def __repr__(self):
        return f"<{self.__class__.__name__} name={self.name} expertise={self.expertise}>"
    
    def __del__(self):
        """析构函数"""
        try:
            self.cleanup()
        except:
            pass