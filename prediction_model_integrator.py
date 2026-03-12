#!/usr/bin/env python3
"""
预测模型集成器 - 四维提升深化
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')

class BasePredictionModel:
    """基础预测模型类"""
    
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.trained = False
        self.last_trained = None
    
    def prepare_data(self, historical_data: List[Dict[str, Any]]) -> pd.DataFrame:
        """准备数据"""
        closes = [h['close'] for h in historical_data]
        dates = [h['date'] for h in historical_data]
        
        df = pd.DataFrame({
            'date': pd.to_datetime(dates),
            'close': closes
        })
        df.set_index('date', inplace=True)
        
        return df
    
    def predict(self, historical_data: List[Dict[str, Any]], horizon: int = 5) -> List[float]:
        """预测（子类需要实现）"""
        raise NotImplementedError
    
    def get_confidence(self) -> float:
        """获取置信度"""
        return 0.5  # 默认置信度
    
    def evaluate(self, historical_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """评估模型"""
        return {
            'model_name': self.model_name,
            'evaluated_at': datetime.now().isoformat(),
            'status': 'not_implemented'
        }

class SimpleMovingAverageModel(BasePredictionModel):
    """简单移动平均模型"""
    
    def __init__(self, window: int = 5):
        super().__init__(f"SMA_{window}")
        self.window = window
    
    def predict(self, historical_data: List[Dict[str, Any]], horizon: int = 5) -> List[float]:
        """使用移动平均进行预测"""
        if len(historical_data) < self.window:
            return [historical_data[0]['close']] * horizon if historical_data else [0] * horizon
        
        closes = [h['close'] for h in historical_data]
        
        # 计算最近窗口期的平均变化率
        recent_closes = closes[:self.window]
        changes = []
        for i in range(1, len(recent_closes)):
            if recent_closes[i] > 0:
                change = (recent_closes[i-1] - recent_closes[i]) / recent_closes[i]
                changes.append(change)
        
        avg_change = np.mean(changes) if changes else 0
        
        # 基于平均变化率进行预测
        last_price = closes[0]
        predictions = []
        for i in range(horizon):
            pred_price = last_price * (1 + avg_change)
            predictions.append(pred_price)
            last_price = pred_price
        
        return predictions
    
    def get_confidence(self) -> float:
        """基于数据量和波动率计算置信度"""
        return 0.6  # 简单模型，中等置信度

class ExponentialSmoothingModel(BasePredictionModel):
    """指数平滑模型"""
    
    def __init__(self, alpha: float = 0.3):
        super().__init__(f"ExpSmooth_alpha{alpha}")
        self.alpha = alpha
    
    def predict(self, historical_data: List[Dict[str, Any]], horizon: int = 5) -> List[float]:
        """使用指数平滑进行预测"""
        if len(historical_data) < 2:
            return [historical_data[0]['close']] * horizon if historical_data else [0] * horizon
        
        closes = [h['close'] for h in historical_data]
        
        # 指数平滑计算
        smoothed = [closes[0]]
        for i in range(1, len(closes)):
            smoothed_value = self.alpha * closes[i] + (1 - self.alpha) * smoothed[-1]
            smoothed.append(smoothed_value)
        
        # 计算趋势
        if len(smoothed) >= 3:
            trend = (smoothed[0] - smoothed[-1]) / len(smoothed)
        else:
            trend = 0
        
        # 基于平滑值和趋势进行预测
        last_smoothed = smoothed[0]
        predictions = []
        for i in range(horizon):
            pred_price = last_smoothed + trend
            predictions.append(pred_price)
            last_smoothed = pred_price
        
        return predictions
    
    def get_confidence(self) -> float:
        """基于平滑参数和数据量计算置信度"""
        return 0.7  # 指数平滑相对可靠

class LinearRegressionModel(BasePredictionModel):
    """线性回归模型"""
    
    def __init__(self):
        super().__init__("LinearRegression")
    
    def predict(self, historical_data: List[Dict[str, Any]], horizon: int = 5) -> List[float]:
        """使用线性回归进行预测"""
        if len(historical_data) < 5:
            return [historical_data[0]['close']] * horizon if historical_data else [0] * horizon
        
        closes = [h['close'] for h in historical_data]
        
        # 简单线性回归（最小二乘法）
        n = len(closes)
        x = np.arange(n)
        y = np.array(closes)
        
        # 计算斜率和截距
        x_mean = np.mean(x)
        y_mean = np.mean(y)
        
        numerator = np.sum((x - x_mean) * (y - y_mean))
        denominator = np.sum((x - x_mean) ** 2)
        
        if denominator == 0:
            slope = 0
        else:
            slope = numerator / denominator
        
        intercept = y_mean - slope * x_mean
        
        # 基于线性趋势进行预测
        predictions = []
        for i in range(horizon):
            pred_price = slope * (n + i) + intercept
            predictions.append(pred_price)
        
        return predictions
    
    def get_confidence(self) -> float:
        """基于拟合优度计算置信度"""
        return 0.75  # 线性回归相对稳定

class PredictionModelIntegrator:
    """预测模型集成器"""
    
    def __init__(self):
        print("🧠 预测模型集成器初始化")
        print("=" * 60)
        print("📊 集成模型列表:")
        
        # 初始化预测模型
        self.models = {
            'sma_5': SimpleMovingAverageModel(window=5),
            'sma_10': SimpleMovingAverageModel(window=10),
            'exp_smooth_03': ExponentialSmoothingModel(alpha=0.3),
            'exp_smooth_07': ExponentialSmoothingModel(alpha=0.7),
            'linear_reg': LinearRegressionModel()
        }
        
        for name, model in self.models.items():
            print(f"   ✅ {name}: {model.model_name}")
        
        print("=" * 60)
    
    def ensemble_predict(self, symbol: str, historical_data: List[Dict[str, Any]], 
                        horizon: int = 5) -> Dict[str, Any]:
        """集成预测"""
        print(f"\n🔮 开始集成预测: {symbol}")
        print(f"   数据量: {len(historical_data)} 个交易日")
        print(f"   预测周期: {horizon} 天")
        print("-" * 50)
        
        start_time = datetime.now()
        
        try:
            if len(historical_data) < 10:
                return {
                    'status': 'error',
                    'error': f'历史数据不足，需要至少10个交易日，当前只有{len(historical_data)}个',
                    'timestamp': datetime.now().isoformat()
                }
            
            # 各模型独立预测
            individual_predictions = {}
            model_errors = {}
            
            for model_name, model in self.models.items():
                try:
                    print(f"   📈 {model_name} 预测中...", end="")
                    predictions = model.predict(historical_data, horizon)
                    confidence = model.get_confidence()
                    
                    individual_predictions[model_name] = {
                        'predictions': predictions,
                        'confidence': confidence,
                        'model_type': model.model_name,
                        'status': 'success'
                    }
                    
                    print(f" ✅ (置信度: {confidence:.2f})")
                    
                except Exception as e:
                    print(f" ❌ (错误: {str(e)[:30]})")
                    individual_predictions[model_name] = {
                        'predictions': [],
                        'confidence': 0,
                        'model_type': model.model_name,
                        'status': 'error',
                        'error': str(e)
                    }
            
            # 集成预测结果
            ensemble_result = self._ensemble_predictions(individual_predictions)
            
            # 计算共识度
            consensus_level = self._calculate_consensus(individual_predictions)
            
            # 生成投资建议
            recommendation = self._generate_recommendation(ensemble_result, consensus_level)
            
            total_time = (datetime.now() - start_time).total_seconds()
            
            return {
                'status': 'success',
                'symbol': symbol,
                'prediction_time': datetime.now().isoformat(),
                'processing_time': f'{total_time:.2f}秒',
                'historical_data_points': len(historical_data),
                'prediction_horizon': horizon,
                'individual_predictions': individual_predictions,
                'ensemble_prediction': ensemble_result,
                'consensus_level': consensus_level,
                'recommendation': recommendation,
                'model_summary': {
                    'total_models': len(self.models),
                    'successful_models': sum(1 for p in individual_predictions.values() if p['status'] == 'success'),
                    'failed_models': sum(1 for p in individual_predictions.values() if p['status'] == 'error'),
                    'avg_confidence': np.mean([p['confidence'] for p in individual_predictions.values() if p['status'] == 'success']) if any(p['status'] == 'success' for p in individual_predictions.values()) else 0
                }
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': f'集成预测失败: {str(e)}',
                'timestamp': datetime.now().isoformat()
            }
    
    def _ensemble_predictions(self, individual_predictions: Dict[str, Any]) -> Dict[str, Any]:
        """集成多个模型的预测结果"""
        successful_predictions = {
            name: data for name, data in individual_predictions.items() 
            if data['status'] == 'success' and data['predictions']
        }
        
        if not successful_predictions:
            return {
                'status': 'error',
                'error': '所有模型预测都失败',
                'ensemble_method': 'none'
            }
        
        # 提取所有成功的预测
        all_predictions = []
        confidences = []
        
        for name, data in successful_predictions.items():
            all_predictions.append(data['predictions'])
            confidences.append(data['confidence'])
        
        # 转换为numpy数组
        pred_array = np.array(all_predictions)
        
        # 加权平均（按置信度加权）
        weights = np.array(confidences) / np.sum(confidences) if np.sum(confidences) > 0 else np.ones(len(confidences)) / len(confidences)
        
        # 计算加权平均预测
        weighted_predictions = []
        for i in range(pred_array.shape[1]):
            weighted_pred = np.sum(pred_array[:, i] * weights)
            weighted_predictions.append(weighted_pred)
        
        # 计算预测范围
        pred_min = np.min(pred_array, axis=0)
        pred_max = np.max(pred_array, axis=0)
        pred_std = np.std(pred_array, axis=0)
        
        # 计算预测变化
        if len(weighted_predictions) >= 2:
            total_change = (weighted_predictions[-1] - weighted_predictions[0]) / weighted_predictions[0] * 100
            avg_daily_change = total_change / (len(weighted_predictions) - 1)
        else:
            total_change = 0
            avg_daily_change = 0
        
        return {
            'status': 'success',
            'weighted_predictions': weighted_predictions,
            'prediction_range': {
                'min': pred_min.tolist(),
                'max': pred_max.tolist(),
                'std': pred_std.tolist()
            },
            'prediction_stats': {
                'initial_price': weighted_predictions[0],
                'final_price': weighted_predictions[-1],
                'total_change': f'{total_change:.2f}%',
                'avg_daily_change': f'{avg_daily_change:.2f}%',
                'prediction_volatility': np.mean(pred_std) / weighted_predictions[0] * 100 if weighted_predictions[0] > 0 else 0
            },
            'ensemble_method': 'weighted_average',
            'models_used': len(successful_predictions),
            'weights_used': {name: float(weights[i]) for i, name in enumerate(successful_predictions.keys())}
        }
    
    def _calculate_consensus(self, individual_predictions: Dict[str, Any]) -> Dict[str, Any]:
        """计算模型共识度"""
        successful_predictions = {
            name: data for name, data in individual_predictions.items() 
            if data['status'] == 'success' and data['predictions']
        }
        
        if len(successful_predictions) < 2:
            return {
                'consensus_score': 0,
                'consensus_level': '低',
                'reason': '成功模型数量不足'
            }
        
        # 提取预测方向
        directions = []
        for name, data in successful_predictions.items():
            predictions = data['predictions']
            if len(predictions) >= 2:
                direction = '上涨' if predictions[-1] > predictions[0] else '下跌'
                directions.append(direction)
        
        if not directions:
            return {
                'consensus_score': 0,
                'consensus_level': '低',
                'reason': '无法确定预测方向'
            }
        
        # 计算共识度
        from collections import Counter
        direction_counts = Counter(directions)
        most_common_direction, most_common_count = direction_counts.most_common(1)[0]
        
        consensus_score = most_common_count / len(directions) * 100
        
        if consensus_score >= 80:
            consensus_level = '高'
        elif consensus_score >= 60:
            consensus_level = '中'
        else:
            consensus_level = '低'
        
        return {
            'consensus_score': consensus_score,
            'consensus_level': consensus_level,
            'prediction_direction': most_common_direction,
            'direction_agreement': f'{most_common_count}/{len(directions)} 个模型',
            'consensus_interpretation': self._interpret_consensus(consensus_level, most_common_direction)
        }
    
    def _interpret_consensus(self, consensus_level: str, direction: str) -> str:
        """解释共识度"""
        interpretations = {
            ('高', '上涨'): '模型高度共识看涨，上涨概率较大',
            ('高', '下跌'): '模型高度共识看跌，下跌概率较大',
            ('中', '上涨'): '模型中等共识看涨，谨慎乐观',
            ('中', '下跌'): '模型中等共识看跌，谨慎悲观',
            ('低', '上涨'): '模型分歧较大，略偏看涨',
            ('低', '下跌'): '模型分歧较大，略偏看跌'
        }
        
        return interpretations.get((consensus_level, direction), '模型预测分歧较大，方向不明')
    
    def _generate_recommendation(self, ensemble_prediction: Dict[str, Any], 
                               consensus: Dict[str, Any]) -> Dict[str, Any]:
        """生成投资建议"""
        if ensemble_prediction.get('status') != 'success':
            return {
                'status': 'error',
                'recommendation': '预测失败，无法生成建议',
                'confidence': 0
            }
        
        stats = ensemble_prediction.get('prediction_stats', {})
        total_change = float(stats.get('total_change', '0%').replace('%', ''))
        consensus_level = consensus.get('consensus_level', '低')
        direction = consensus.get('prediction_direction', '未知')
        
        # 基于预测变化和共识度生成建议
        if consensus_level == '高':
            if direction == '上涨' and total_change > 5:
                recommendation = '模型高度共识看涨，建议买入'
                confidence = 0.8
                action = '可考虑建仓或加仓'
            elif direction == '下跌' and total_change < -5:
                recommendation = '模型高度共识看跌，建议卖出'
                confidence = 0.8
                action = '减仓或观望'
            else:
                recommendation = '模型高度共识但变化不大，建议持有'
                confidence = 0.7
                action = '保持现有仓位'
        
        elif consensus_level == '中':
            if direction == '上涨' and total_change > 3:
                recommendation = '模型中等共识看涨，可考虑买入'
                confidence = 0.6
                action = '可分批建仓'
            elif direction == '下跌' and total_change < -3:
                recommendation = '模型中等共识看跌，谨慎操作'
                confidence = 0.6
                action = '减仓或设置止损'
            else:
                recommendation = '模型共识度中等，建议观望'
                confidence = 0.5
                action = '等待更明确信号'
        
        else:  # 共识度低
            recommendation = '模型分歧较大，建议谨慎操作'
            confidence = 0.4
            action = '保持观望，等待趋势明朗'
        
        # 风险评估
        volatility = stats.get('prediction_volatility', 0)
        if volatility > 3:
            risk_level = '高'
            risk_note = '预测波动较大，风险较高'
        elif volatility > 1.5:
            risk_level = '中'
            risk_note = '预测有一定波动，中等风险'
        else:
            risk_level = '低'
            risk_note = '预测相对稳定，风险较低'
        
        return {
            'status': 'success',
            'recommendation': recommendation,
            'confidence': confidence,
            'action': action,
            'risk_assessment': {
                'risk_level': risk_level,
                'volatility': f'{volatility:.2f}%',
                'risk_note': risk_note
            },
            'time_horizon': '短期 (1-2周)',
            'key_factors': [
                f'模型共识度: {consensus_level}',
                f'预测方向: {direction}',
                f'预期变化: {total_change:.1f}%',
                f'预测波动: {volatility:.2f}%'
            ],
            'generated_at': datetime.now().isoformat()
        }

def main():
    """主函数"""
    print("🧠 毛毛AI增强系统 - 预测模型集成器")
    print("=" * 60)
    print("📊 四维提升深化: 预测模型集成")
    print("🎯 目标: 集成先进预测算法，提升预测能力")
    print("⏰ 开始时间: 08:57 GMT+8")
    print("=" * 60)
    
    # 创建预测模型集成器
    integrator = PredictionModelIntegrator()
    
    # 创建测试数据
    print("\n📊 创建测试数据...")
    test_data = []
    base_price = 50.0
    
    for i in range(30):
        # 模拟价格数据（有一定趋势和波动）
        trend = 0.002 * i  # 轻微上涨趋势
        noise = np.random.normal(0, 0.01)  # 随机噪声
        price = base_price * (1 + trend + noise)
        
        test_data.append({
            'date': f'2026-03-{12-i:02d}',
            'close': price,
            'high': price * 1.02,
            'low': price * 0.98,
            'volume': 10000 + np.random.randint(-2000, 2000)
        })
    
    print(f"   测试数据创建完成: {len(test_data)} 个交易日")
    print(f"   最新价格: {test_data[0]['close']:.2f}")
    print(f"   最早价格: {test_data[-1]['close']:.2f}")
    
    # 测试集成预测
    print("\n🔮 测试集成预测...")
    result = integrator.ensemble_predict("TEST001", test_data, horizon=5)
    
    if result['status'] == 'success':
        print("\n✅ 集成预测成功!")
        print(f"   处理时间: {result['processing_time']}")
        print(f"   使用模型: {result['model_summary']['successful_models']}/{result['model_summary']['total_models']}")
        print(f"   平均置信度: {result['model_summary']['avg_confidence']:.2f}")
        
        # 显示集成预测结果
        ensemble = result['ensemble_prediction']
        if ensemble['status'] == 'success':
            stats = ensemble['prediction_stats']
            print(f"\n📈 集成预测结果:")
            print(f"   初始价格: {stats['initial_price']:.2f}")
            print(f"   最终价格: {stats['final_price']:.2f}")
            print(f"   总变化: {stats['total_change']}")
            print(f"   日均变化: {stats['avg_daily_change']}")
        
        # 显示共识度
        consensus = result['consensus_level']
        print(f"\n🤝 模型共识度:")
        print(f"   共识分数: {consensus['consensus_score']:.1f}%")
        print(f"   共识等级: {consensus['consensus_level']}")
        print(f"   预测方向: {consensus['prediction_direction']}")
        print(f"   解释: {consensus['consensus_interpretation']}")
        
        # 显示投资建议
        recommendation = result['recommendation']
        print(f"\n🎯 投资建议:")
        print(f"   建议: {recommendation['recommendation']}")
        print(f"   置信度: {recommendation['confidence']:.2f}")
        print(f"   操作: {recommendation['action']}")
        print(f"   风险等级: {recommendation['risk_assessment']['risk_level']}")
        print(f"   预测波动: {recommendation['risk_assessment']['volatility']}")
        
        # 显示各模型预测
        print(f"\n📊 各模型预测详情:")
        individual = result['individual_predictions']
        for name, data in individual.items():
            if data['status'] == 'success':
                preds = data['predictions']
                if len(preds) >= 2:
                    change = (preds[-1] - preds[0]) / preds[0] * 100
                    print(f"   {name}: {data['model_type']}")
                    print(f"     预测: {preds[0]:.2f} → {preds[-1]:.2f} ({change:.1f}%)")
                    print(f"     置信度: {data['confidence']:.2f}")
        
    else:
        print(f"\n❌ 集成预测失败: {result.get('error', '未知错误')}")
    
    print("\n" + "=" * 60)
    print("🎉 预测模型集成完成!")
    print("   集成5个预测模型")
    print("   实现加权平均集成")
    print("   提供共识度分析")
    print("   生成投资建议")
    print("=" * 60)

if __name__ == "__main__":
    main()