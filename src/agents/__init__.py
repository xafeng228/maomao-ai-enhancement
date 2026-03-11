"""
多代理系统 - 专业投资代理协作框架

包含6个专业投资代理：
1. TechnicalAgent - 技术分析代理
2. FundamentalAgent - 基本面分析代理
3. RiskManagementAgent - 风险管理代理
4. SentimentAnalysisAgent - 情绪分析代理
5. MacroAnalysisAgent - 宏观分析代理
6. LearningAgent - 学习优化代理
"""

from .base_agent import BaseAgent
from .technical_agent import TechnicalAgent
from .fundamental_agent import FundamentalAgent
from .risk_management_agent import RiskManagementAgent
from .sentiment_analysis_agent import SentimentAnalysisAgent
from .macro_analysis_agent import MacroAnalysisAgent
from .learning_agent import LearningAgent

__all__ = [
    'BaseAgent',
    'TechnicalAgent',
    'FundamentalAgent',
    'RiskManagementAgent',
    'SentimentAnalysisAgent',
    'MacroAnalysisAgent',
    'LearningAgent',
]

__version__ = '1.0.0'