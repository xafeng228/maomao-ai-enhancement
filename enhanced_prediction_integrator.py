#!/usr/bin/env python3
"""
增强版预测模型集成器 - 集成涨停板模式识别
在现有四维架构基础上，增加A股实战能力
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')
import json

class LimitUpPatternModel:
    """涨停板模式识别模型 - 新增A股实战模块"""
    
    def __init__(self):
        self.model_name = "涨停板模式识别模型"
        self.feature_importance = [
            {'feature': 'seal_funds', 'importance': 0.2384, 'description': '封板资金'},
            {'feature': 'industry_encoded', 'importance': 0.1599, 'description': '行业编码'},
            {'feature': 'break_times', 'importance': 0.1335, 'description': '炸板次数'},
            {'feature': 'turnover_rate', 'importance': 0.0798, 'description': '换手率'},
            {'feature': 'increase_pct', 'importance': 0.0773, 'description': '涨跌幅'}
        ]
        print(f"✅ {self.model_name} 初始化完成")
    
    def analyze_limit_up_stock(self, stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """分析涨停板股票"""
        analysis = {
            'is_limit_up': False,
            'continuation_probability': 0.5,
            'risk_level': 'medium',
            'recommendation': 'hold',
            'confidence': 0.7,
            'key_factors': []
        }
        
        # 检查是否为涨停板
        if 'increase_pct' in stock_data and stock_data['increase_pct'] >= 9.5:
            analysis['is_limit_up'] = True
            
            # 计算继续上涨概率
            probability = 0.5
            
            # 基于特征计算
            if 'seal_funds' in stock_data and stock_data['seal_funds'] > 0.5:  # 封板资金大于5000万
                probability += 0.2
                analysis['key_factors'].append('封板资金充足')
            
            if 'turnover_rate' in stock_data and 10 <= stock_data['turnover_rate'] <= 30:
                probability += 0.15
                analysis['key_factors'].append('换手率适中')
            
            if 'continuous_days' in stock_data and 1 <= stock_data['continuous_days'] <= 3:
                probability += 0.1
                analysis['key_factors'].append('连板数适中')
            
            if 'break_times' in stock_data and stock_data['break_times'] == 0:
                probability += 0.05
                analysis['key_factors'].append('无炸板')
            
            # 限制概率范围
            probability = max(0.1, min(0.9, probability))
            analysis['continuation_probability'] = probability
            
            # 确定风险等级和推荐
            if probability > 0.7:
                analysis['risk_level'] = 'low'
                analysis['recommendation'] = 'buy'
                analysis['confidence'] = 0.8
            elif probability > 0.5:
                analysis['risk_level'] = 'medium'
                analysis['recommendation'] = 'hold'
                analysis['confidence'] = 0.7
            else:
                analysis['risk_level'] = 'high'
                analysis['recommendation'] = 'sell'
                analysis['confidence'] = 0.6
        
        return analysis
    
    def get_model_info(self) -> Dict[str, Any]:
        """获取模型信息"""
        return {
            'model_name': self.model_name,
            'description': 'A股涨停板模式识别模型，分析涨停后继续上涨概率',
            'feature_count': len(self.feature_importance),
            'trained_at': datetime.now().isoformat(),
            'applicable_markets': ['A股'],
            'specialization': '涨停板分析'
        }

class EnhancedPredictionModelIntegrator:
    """增强版预测模型集成器 - 集成涨停板分析"""
    
    def __init__(self):
        print("🚀 增强版预测模型集成器初始化...")
        
        # 原有模型
        self.base_models = [
            {'name': '简单移动平均', 'weight': 0.15, 'confidence': 0.6},
            {'name': '指数平滑', 'weight': 0.15, 'confidence': 0.65},
            {'name': '线性回归', 'weight': 0.15, 'confidence': 0.7},
            {'name': '时间序列分解', 'weight': 0.15, 'confidence': 0.6},
            {'name': '季节性模型', 'weight': 0.15, 'confidence': 0.55}
        ]
        
        # 新增涨停板模型
        self.limit_up_model = LimitUpPatternModel()
        self.limit_up_weight = 0.25  # 涨停板模型权重
        
        print(f"✅ 集成 {len(self.base_models)} 个基础模型 + 1 个涨停板模型")
    
    def integrate_predictions(self, stock_data: Dict[str, Any], 
                             base_predictions: List[float]) -> Dict[str, Any]:
        """集成预测结果"""
        print(f"🔗 集成预测结果...")
        
        # 基础模型集成
        base_prediction = np.average(
            base_predictions,
            weights=[m['weight'] for m in self.base_models]
        )
        
        # 涨停板分析
        limit_up_analysis = self.limit_up_model.analyze_limit_up_stock(stock_data)
        
        # 综合集成
        if limit_up_analysis['is_limit_up']:
            # 如果是涨停板，给予涨停板模型更高权重
            limit_up_weight = self.limit_up_weight
            base_weight = 1 - limit_up_weight
            
            # 涨停板模型的预测基于继续上涨概率
            limit_up_prediction = limit_up_analysis['continuation_probability'] * 0.2  # 转换为涨跌幅预测
            
            final_prediction = (
                base_prediction * base_weight + 
                limit_up_prediction * limit_up_weight
            )
            
            print(f"📈 涨停板股票特殊处理:")
            print(f"   基础预测: {base_prediction:.2%}")
            print(f"   涨停板分析: {limit_up_analysis['continuation_probability']:.1%} 继续上涨概率")
            print(f"   综合预测: {final_prediction:.2%}")
            
        else:
            # 非涨停板，使用基础模型
            final_prediction = base_prediction
            print(f"📊 非涨停板股票:")
            print(f"   基础预测: {final_prediction:.2%}")
        
        # 计算共识度
        consensus = self.calculate_consensus(base_predictions, limit_up_analysis)
        
        # 生成投资建议
        recommendation = self.generate_recommendation(final_prediction, limit_up_analysis, consensus)
        
        return {
            'final_prediction': final_prediction,
            'base_prediction': base_prediction,
            'limit_up_analysis': limit_up_analysis,
            'consensus': consensus,
            'recommendation': recommendation,
            'model_count': len(self.base_models) + 1,
            'integration_method': 'weighted_average_with_limit_up_adjustment',
            'timestamp': datetime.now().isoformat()
        }
    
    def calculate_consensus(self, base_predictions: List[float], 
                           limit_up_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """计算共识度"""
        # 基础模型共识
        base_std = np.std(base_predictions)
        base_consensus = 1.0 / (1.0 + base_std)  # 标准差越小，共识度越高
        
        # 涨停板分析共识
        limit_up_consensus = limit_up_analysis.get('confidence', 0.5)
        
        # 综合共识
        total_consensus = (base_consensus * 0.7 + limit_up_consensus * 0.3)
        
        return {
            'base_consensus': base_consensus,
            'limit_up_consensus': limit_up_consensus,
            'total_consensus': total_consensus,
            'interpretation': self.interpret_consensus(total_consensus)
        }
    
    def interpret_consensus(self, consensus: float) -> str:
        """解释共识度"""
        if consensus >= 0.8:
            return "高度共识，预测可靠性高"
        elif consensus >= 0.6:
            return "中度共识，预测有一定可靠性"
        elif consensus >= 0.4:
            return "低度共识，预测需谨慎"
        else:
            return "分歧较大，预测不确定性高"
    
    def generate_recommendation(self, prediction: float,
                               limit_up_analysis: Dict[str, Any],
                               consensus: Dict[str, Any]) -> Dict[str, Any]:
        """生成投资建议"""
        
        # 基础建议
        if prediction > 0.05:  # 预测上涨5%以上
            base_action = 'buy'
            confidence = 'high' if prediction > 0.1 else 'medium'
        elif prediction < -0.03:  # 预测下跌3%以上
            base_action = 'sell'
            confidence = 'high' if prediction < -0.06 else 'medium'
        else:
            base_action = 'hold'
            confidence = 'medium'
        
        # 考虑涨停板分析
        if limit_up_analysis['is_limit_up']:
            if limit_up_analysis['recommendation'] == 'buy':
                action = 'buy'
                reason = '涨停板模式识别显示继续上涨概率高'
            elif limit_up_analysis['recommendation'] == 'sell':
                action = 'sell'
                reason = '涨停板模式识别显示风险较高'
            else:
                action = base_action
                reason = '涨停板分析建议持有'
        else:
            action = base_action
            reason = '基于技术分析预测'
        
        # 考虑共识度
        if consensus['total_consensus'] < 0.4:
            action = 'hold'  # 共识度低时建议持有
            reason = '模型共识度低，建议观望'
            confidence = 'low'
        
        return {
            'action': action,
            'confidence': confidence,
            'reason': reason,
            'predicted_return': f"{prediction:.2%}",
            'consensus_level': consensus['interpretation'],
            'limit_up_specific': limit_up_analysis['is_limit_up'],
            'risk_level': limit_up_analysis.get('risk_level', 'medium'),
            'key_factors': limit_up_analysis.get('key_factors', [])
        }
    
    def get_system_info(self) -> Dict[str, Any]:
        """获取系统信息"""
        return {
            'system_name': '增强版预测模型集成器',
            'version': '3.0.0-alpha',
            'description': '在四维架构基础上集成涨停板模式识别',
            'model_count': len(self.base_models) + 1,
            'special_features': ['涨停板分析', 'A股特性集成', '动态权重调整'],
            'integration_method': '加权平均 + 涨停板调整',
            'applicable_scenarios': ['常规分析', '涨停板分析', '短线交易'],
            'created_at': datetime.now().isoformat()
        }

# 使用示例
def main():
    """主函数 - 演示集成效果"""
    print("="*60)
    print("🧠 增强版预测模型集成器 - 演示")
    print("="*60)
    
    # 创建集成器
    integrator = EnhancedPredictionModelIntegrator()
    
    # 示例1：涨停板股票
    print("\n📈 示例1：涨停板股票分析")
    limit_up_stock = {
        'code': '603039',
        'name': '示例涨停股',
        'increase_pct': 10.0,
        'seal_funds': 0.8,  # 8000万封板资金
        'turnover_rate': 15.5,
        'continuous_days': 2,
        'break_times': 0,
        'close': 25.5
    }
    
    # 模拟基础模型预测
    base_predictions = [0.08, 0.12, 0.05, 0.10, 0.07]  # 5个基础模型的预测
    
    result = integrator.integrate_predictions(limit_up_stock, base_predictions)
    
    print(f"\n✅ 集成结果:")
    print(f"   最终预测: {result['final_prediction']:.2%}")
    print(f"   共识度: {result['consensus']['total_consensus']:.2%}")
    print(f"   投资建议: {result['recommendation']['action']}")
    print(f"   建议理由: {result['recommendation']['reason']}")
    
    # 示例2：非涨停板股票
    print("\n📊 示例2：非涨停板股票分析")
    normal_stock = {
        'code': '000001',
        'name': '示例普通股',
        'increase_pct': 2.5,
        'close': 15.3
    }
    
    base_predictions2 = [0.03, -0.01, 0.02, 0.01, 0.00]
    result2 = integrator.integrate_predictions(normal_stock, base_predictions2)
    
    print(f"\n✅ 集成结果:")
    print(f"   最终预测: {result2['final_prediction']:.2%}")
    print(f"   共识度: {result2['consensus']['total_consensus']:.2%}")
    print(f"   投资建议: {result2['recommendation']['action']}")
    
    # 系统信息
    print("\n" + "="*60)
    print("📋 系统信息:")
    system_info = integrator.get_system_info()
    for key, value in system_info.items():
        print(f"   {key}: {value}")
    
    print("\n" + "="*60)
    print("🎉 增强版集成器演示完成!")
    print("✅ 成功集成涨停板模式识别到四维架构")
    print("="*60)

if __name__ == "__main__":
    main()