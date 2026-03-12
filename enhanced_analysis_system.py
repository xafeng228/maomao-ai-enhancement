#!/usr/bin/env python3
"""
增强版分析系统 - 功能增强
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import math
from typing import Dict, List, Any, Optional, Tuple

class EnhancedAnalysisSystem:
    """增强版分析系统"""
    
    def __init__(self):
        print("🧠 毛毛AI增强系统 - 增强版分析系统")
        print("=" * 60)
        print("📊 功能增强 v1.0")
        print("🎯 目标: 增强系统功能和分析能力")
        print("⏰ 开始时间: 08:46 GMT+8")
        print("=" * 60)
    
    def enhanced_technical_analysis(self, historical_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """增强技术分析"""
        print("📊 进行增强技术分析...")
        
        if not historical_data or len(historical_data) < 20:
            return {
                'status': 'error',
                'error': '历史数据不足，至少需要20个交易日数据',
                'timestamp': datetime.now().isoformat()
            }
        
        try:
            # 准备数据
            closes = [h['close'] for h in historical_data]
            highs = [h['high'] for h in historical_data]
            lows = [h['low'] for h in historical_data]
            volumes = [h['volume'] for h in historical_data]
            dates = [h['date'] for h in historical_data]
            
            # 1. 基础技术指标
            print("   1. 📈 计算基础技术指标...")
            basic_indicators = self._calculate_basic_indicators(closes, volumes)
            
            # 2. 趋势分析
            print("   2. 📊 进行趋势分析...")
            trend_analysis = self._analyze_trend_enhanced(closes, highs, lows)
            
            # 3. 动量指标
            print("   3. ⚡ 计算动量指标...")
            momentum_indicators = self._calculate_momentum_indicators(closes)
            
            # 4. 波动率分析
            print("   4. 📉 分析波动率...")
            volatility_analysis = self._analyze_volatility(closes)
            
            # 5. 成交量分析
            print("   5. 📊 分析成交量...")
            volume_analysis = self._analyze_volume_enhanced(volumes, closes)
            
            # 6. 支撑阻力分析
            print("   6. 🎯 分析支撑阻力位...")
            support_resistance = self._analyze_support_resistance(closes, highs, lows)
            
            # 7. 技术信号生成
            print("   7. 🔔 生成技术信号...")
            technical_signals = self._generate_technical_signals(
                basic_indicators, trend_analysis, momentum_indicators,
                volatility_analysis, volume_analysis, support_resistance
            )
            
            # 8. 技术评分
            print("   8. 📋 计算技术评分...")
            technical_score = self._calculate_technical_score(technical_signals)
            
            return {
                'status': 'success',
                'analysis_date': datetime.now().isoformat(),
                'data_period': f"{len(historical_data)}个交易日 ({dates[-1]} 至 {dates[0]})",
                'basic_indicators': basic_indicators,
                'trend_analysis': trend_analysis,
                'momentum_indicators': momentum_indicators,
                'volatility_analysis': volatility_analysis,
                'volume_analysis': volume_analysis,
                'support_resistance': support_resistance,
                'technical_signals': technical_signals,
                'technical_score': technical_score,
                'investment_recommendation': self._generate_technical_recommendation(technical_score, technical_signals)
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': f"技术分析失败: {str(e)}",
                'timestamp': datetime.now().isoformat()
            }
    
    def _calculate_basic_indicators(self, closes: List[float], volumes: List[int]) -> Dict[str, Any]:
        """计算基础技术指标"""
        indicators = {}
        
        # 移动平均线
        if len(closes) >= 5:
            indicators['ma5'] = sum(closes[:5]) / 5
        if len(closes) >= 10:
            indicators['ma10'] = sum(closes[:10]) / 10
        if len(closes) >= 20:
            indicators['ma20'] = sum(closes[:20]) / 20
        if len(closes) >= 60:
            indicators['ma60'] = sum(closes[:60]) / 60
        
        # 指数移动平均线
        if len(closes) >= 12:
            indicators['ema12'] = self._calculate_ema(closes, 12)
        if len(closes) >= 26:
            indicators['ema26'] = self._calculate_ema(closes, 26)
        
        # MACD
        if 'ema12' in indicators and 'ema26' in indicators:
            macd_line = indicators['ema12'] - indicators['ema26']
            signal_line = self._calculate_ema([macd_line] * 9, 9) if len(closes) >= 26 else None
            macd_histogram = macd_line - signal_line if signal_line else None
            
            indicators['macd'] = {
                'macd_line': macd_line,
                'signal_line': signal_line,
                'histogram': macd_histogram,
                'signal': '金叉' if macd_line > signal_line else '死叉' if signal_line else None
            }
        
        # 布林带
        if len(closes) >= 20:
            middle_band = indicators.get('ma20', sum(closes[:20]) / 20)
            std_dev = np.std(closes[:20]) if len(closes) >= 20 else 0
            indicators['bollinger_bands'] = {
                'upper': middle_band + 2 * std_dev,
                'middle': middle_band,
                'lower': middle_band - 2 * std_dev,
                'bandwidth': (middle_band + 2 * std_dev - (middle_band - 2 * std_dev)) / middle_band * 100,
                'position': (closes[0] - (middle_band - 2 * std_dev)) / (4 * std_dev) * 100 if std_dev > 0 else None
            }
        
        # RSI
        if len(closes) >= 14:
            rsi = self._calculate_rsi(closes, 14)
            indicators['rsi'] = {
                'value': rsi,
                'level': '超买' if rsi > 70 else '超卖' if rsi < 30 else '正常',
                'signal': '卖出' if rsi > 70 else '买入' if rsi < 30 else '持有'
            }
        
        # KDJ
        if len(closes) >= 9:
            kdj = self._calculate_kdj(closes, highs=None, lows=None)  # 简化计算
            indicators['kdj'] = kdj
        
        return indicators
    
    def _calculate_ema(self, prices: List[float], period: int) -> float:
        """计算指数移动平均线"""
        if len(prices) < period:
            return sum(prices) / len(prices)
        
        multiplier = 2 / (period + 1)
        ema = sum(prices[:period]) / period
        
        for price in prices[period:]:
            ema = (price - ema) * multiplier + ema
        
        return ema
    
    def _calculate_rsi(self, prices: List[float], period: int = 14) -> float:
        """计算RSI"""
        if len(prices) < period + 1:
            return 50  # 默认值
        
        gains = []
        losses = []
        
        for i in range(1, period + 1):
            change = prices[i-1] - prices[i]
            if change > 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(change))
        
        avg_gain = sum(gains) / period
        avg_loss = sum(losses) / period
        
        if avg_loss == 0:
            return 100
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    def _calculate_kdj(self, closes: List[float], highs: Optional[List[float]] = None, 
                      lows: Optional[List[float]] = None) -> Dict[str, Any]:
        """计算KDJ指标（简化版）"""
        if len(closes) < 9:
            return {'k': 50, 'd': 50, 'j': 50, 'signal': '中性'}
        
        # 简化计算
        recent_closes = closes[:9]
        highest = max(recent_closes)
        lowest = min(recent_closes)
        
        if highest == lowest:
            rsv = 50
        else:
            rsv = (closes[0] - lowest) / (highest - lowest) * 100
        
        # 简化K、D、J计算
        k = 2/3 * 50 + 1/3 * rsv  # 假设前一日K=50
        d = 2/3 * 50 + 1/3 * k    # 假设前一日D=50
        j = 3 * k - 2 * d
        
        # 判断信号
        if k > 80 and d > 80:
            signal = '超买'
        elif k < 20 and d < 20:
            signal = '超卖'
        elif k > d:
            signal = '金叉'
        elif k < d:
            signal = '死叉'
        else:
            signal = '中性'
        
        return {
            'k': k,
            'd': d,
            'j': j,
            'signal': signal
        }
    
    def _analyze_trend_enhanced(self, closes: List[float], highs: List[float], lows: List[float]) -> Dict[str, Any]:
        """增强趋势分析"""
        if len(closes) < 20:
            return {'trend': '数据不足', 'strength': '未知', 'confidence': 0}
        
        # 多时间框架趋势分析
        short_term = closes[:10]
        medium_term = closes[:30] if len(closes) >= 30 else closes
        long_term = closes[:60] if len(closes) >= 60 else closes
        
        # 计算各时间框架趋势
        short_trend = self._calculate_simple_trend(short_term)
        medium_trend = self._calculate_simple_trend(medium_term)
        long_trend = self._calculate_simple_trend(long_term)
        
        # 趋势一致性
        trends = [short_trend['direction'], medium_trend['direction'], long_trend['direction']]
        trend_consistency = trends.count(trends[0]) / len(trends) * 100
        
        # 综合趋势判断
        if trend_consistency >= 66.7:
            main_trend = trends[0]
            confidence = '高'
        elif short_trend['direction'] == medium_trend['direction']:
            main_trend = short_trend['direction']
            confidence = '中'
        else:
            main_trend = '震荡'
            confidence = '低'
        
        # 趋势强度
        strength_scores = {
            '上涨': short_trend['strength_score'] * 0.4 + medium_trend['strength_score'] * 0.4 + long_trend['strength_score'] * 0.2,
            '下跌': short_trend['strength_score'] * 0.4 + medium_trend['strength_score'] * 0.4 + long_trend['strength_score'] * 0.2,
            '震荡': 50  # 默认值
        }
        
        strength = '强势' if strength_scores.get(main_trend, 50) > 70 else '温和' if strength_scores.get(main_trend, 50) > 40 else '弱势'
        
        return {
            'short_term': short_trend,
            'medium_term': medium_trend,
            'long_term': long_trend,
            'main_trend': main_trend,
            'trend_consistency': f'{trend_consistency:.1f}%',
            'confidence': confidence,
            'strength': strength,
            'strength_score': strength_scores.get(main_trend, 50)
        }
    
    def _calculate_simple_trend(self, prices: List[float]) -> Dict[str, Any]:
        """计算简单趋势"""
        if len(prices) < 2:
            return {'direction': '未知', 'slope': 0, 'strength': '未知', 'strength_score': 50}
        
        # 线性回归计算斜率
        x = list(range(len(prices)))
        y = prices
        
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(x[i] * y[i] for i in range(n))
        sum_x2 = sum(x[i] ** 2 for i in range(n))
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2) if (n * sum_x2 - sum_x ** 2) != 0 else 0
        
        # 判断趋势方向
        if slope > 0.01:
            direction = '上涨'
        elif slope < -0.01:
            direction = '下跌'
        else:
            direction = '震荡'
        
        # 计算趋势强度分数（0-100）
        price_range = max(prices) - min(prices)
        avg_price = sum(prices) / len(prices)
        
        if price_range > 0:
            volatility = price_range / avg_price * 100
            trend_strength = min(abs(slope) * 1000, 100)  # 斜率越大趋势越强
            strength_score = min(trend_strength * (1 + volatility/100), 100)
        else:
            strength_score = 50
        
        strength = '强势' if strength_score > 70 else '温和' if strength_score > 40 else '弱势'
        
        return {
            'direction': direction,
            'slope': slope,
            'strength': strength,
            'strength_score': strength_score,
            'period': f'{len(prices)}个数据点'
        }
    
    def _calculate_momentum_indicators(self, closes: List[float]) -> Dict[str, Any]:
        """计算动量指标"""
        indicators = {}
        
        # 近期动量
        if len(closes) >= 5:
            momentum_5d = (closes[0] / closes[4] - 1) * 100
            indicators['momentum_5d'] = {
                'value': momentum_5d,
                'signal': '强势' if momentum_5d > 5 else '弱势' if momentum_5d < -5 else '中性'
            }
        
        if len(closes) >= 10:
            momentum_10d = (closes[0] / closes[9] - 1) * 100
            indicators['momentum_10d'] = {
                'value': momentum_10d,
                'signal': '强势' if momentum_10d > 8 else '弱势' if momentum_10d < -8 else '中性'
            }
        
        if len(closes) >= 20:
            momentum_20d = (closes[0] / closes[19] - 1) * 100
            indicators['momentum_20d'] = {
                'value': momentum_20d,
                'signal': '强势' if momentum_20d > 12 else '弱势' if momentum_20d < -12 else '中性'
            }
        
        # 动量一致性
        momentum_values = [ind.get('value', 0) for ind in indicators.values() if 'value' in ind]
        if momentum_values:
            positive_momentum = sum(1 for v in momentum_values if v > 0)
            momentum_consistency = positive_momentum / len(momentum_values) * 100
            indicators['momentum_consistency'] = f'{momentum_consistency:.1f}%'
        
        return indicators
    
    def _analyze_volatility(self, closes: List[float]) -> Dict[str, Any]:
        """分析波动率"""
        if len(closes) < 2:
            return {'volatility': '数据不足', 'level': '未知', 'score': 50}
        
        # 计算日收益率
        returns = []
        for i in range(1, min(20, len(closes))):
            if closes[i] > 0:
                daily_return = (closes[i-1] - closes[i]) / closes[i] * 100
                returns.append(daily_return)
        
        if not returns:
            return {'volatility': '数据不足', 'level': '未知', 'score': 50}
        
        # 计算波动率（年化）
        daily_std = np.std(returns)
        annualized_volatility = daily_std * math.sqrt(252)  # 假设252个交易日
        
        # 波动率水平
        if annualized_volatility > 40:
            level = '极高'
            score = 90
        elif annualized_volatility > 30:
            level = '高'
            score = 70
        elif annualized_volatility > 20:
            level = '中等'
            score = 50
        elif annualized_volatility > 10:
            level = '低'
            score = 30
        else:
