#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技术分析代理 - 负责股票技术分析
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
import logging

from .base_agent import BaseAgent, Task, TaskResult

logger = logging.getLogger(__name__)

class TechnicalAgent(BaseAgent):
    """技术分析代理"""
    
    def __init__(self):
        super().__init__(
            name="TechnicalAgent",
            expertise="股票技术分析，包括K线、均线、指标、趋势分析",
            version="1.0.0"
        )
        
        # 技术指标配置
        self.indicators_config = {
            'moving_averages': [5, 10, 20, 60],  # 移动平均线周期
            'rsi_period': 14,                    # RSI周期
            'macd_fast': 12,                     # MACD快线
            'macd_slow': 26,                     # MACD慢线
            'macd_signal': 9,                    # MACD信号线
            'bollinger_period': 20,              # 布林带周期
            'bollinger_std': 2,                  # 布林带标准差
            'kdj_period': 9,                     # KDJ周期
        }
        
        # 缓存最近分析结果
        self.analysis_cache = {}
        self.cache_ttl = 300  # 5分钟缓存
        
    def _setup(self):
        """设置技术分析代理"""
        logger.info("设置技术分析代理...")
        
        # 这里可以加载预训练模型或配置文件
        # 目前主要是初始化配置
        
        logger.info("技术分析代理设置完成")
    
    def execute(self, task: Task) -> TaskResult:
        """执行技术分析任务"""
        try:
            task_type = task.type
            params = task.parameters
            
            if task_type == 'analyze_stock':
                result = self._analyze_stock(params)
            elif task_type == 'calculate_indicators':
                result = self._calculate_indicators(params)
            elif task_type == 'identify_signals':
                result = self._identify_signals(params)
            elif task_type == 'assess_trend':
                result = self._assess_trend(params)
            elif task_type == 'generate_technical_report':
                result = self._generate_technical_report(params)
            else:
                raise ValueError(f"不支持的任务类型: {task_type}")
            
            return TaskResult(
                task_id=task.id,
                success=True,
                data=result
            )
            
        except Exception as e:
            logger.error(f"技术分析任务执行失败: {e}")
            return TaskResult(
                task_id=task.id,
                success=False,
                data={},
                error=str(e)
            )
    
    def _analyze_stock(self, params: Dict) -> Dict:
        """分析单只股票"""
        symbol = params.get('symbol')
        period = params.get('period', 'daily')
        days = params.get('days', 60)
        
        logger.info(f"分析股票 {symbol}，周期 {period}，天数 {days}")
        
        # 获取股票数据（这里需要数据服务层）
        price_data = self._get_price_data(symbol, period, days)
        
        if price_data.empty:
            return {'error': '无法获取价格数据'}
        
        # 计算技术指标
        indicators = self._calculate_all_indicators(price_data)
        
        # 识别技术信号
        signals = self._identify_technical_signals(price_data, indicators)
        
        # 评估趋势
        trend_assessment = self._assess_stock_trend(price_data, indicators)
        
        # 生成分析总结
        summary = self._generate_technical_summary(symbol, indicators, signals, trend_assessment)
        
        return {
            'symbol': symbol,
            'period': period,
            'analysis_date': datetime.now().isoformat(),
            'price_data_summary': {
                'start_date': price_data.index[0].strftime('%Y-%m-%d'),
                'end_date': price_data.index[-1].strftime('%Y-%m-%d'),
                'records': len(price_data),
                'current_price': price_data['close'].iloc[-1],
                'price_change': self._calculate_price_change(price_data),
            },
            'indicators': indicators,
            'signals': signals,
            'trend_assessment': trend_assessment,
            'summary': summary,
            'recommendation': self._generate_recommendation(signals, trend_assessment),
        }
    
    def _calculate_all_indicators(self, df: pd.DataFrame) -> Dict:
        """计算所有技术指标"""
        indicators = {}
        
        # 移动平均线
        for period in self.indicators_config['moving_averages']:
            key = f'ma{period}'
            indicators[key] = self._calculate_moving_average(df['close'], period)
        
        # RSI
        indicators['rsi'] = self._calculate_rsi(df['close'], self.indicators_config['rsi_period'])
        
        # MACD
        macd, signal, hist = self._calculate_macd(
            df['close'],
            self.indicators_config['macd_fast'],
            self.indicators_config['macd_slow'],
            self.indicators_config['macd_signal']
        )
        indicators['macd'] = macd
        indicators['macd_signal'] = signal
        indicators['macd_histogram'] = hist
        
        # 布林带
        upper, middle, lower = self._calculate_bollinger_bands(
            df['close'],
            self.indicators_config['bollinger_period'],
            self.indicators_config['bollinger_std']
        )
        indicators['bollinger_upper'] = upper
        indicators['bollinger_middle'] = middle
        indicators['bollinger_lower'] = lower
        
        # KDJ
        k, d, j = self._calculate_kdj(
            df['high'], df['low'], df['close'],
            self.indicators_config['kdj_period']
        )
        indicators['kdj_k'] = k
        indicators['kdj_d'] = d
        indicators['kdj_j'] = j
        
        # 成交量指标
        indicators['volume_ma5'] = self._calculate_moving_average(df['volume'], 5)
        indicators['volume_ratio'] = df['volume'] / indicators['volume_ma5']
        
        return indicators
    
    def _calculate_moving_average(self, series: pd.Series, period: int) -> pd.Series:
        """计算移动平均线"""
        return series.rolling(window=period).mean()
    
    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """计算RSI指标"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def _calculate_macd(self, prices: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> Tuple:
        """计算MACD指标"""
        exp1 = prices.ewm(span=fast, adjust=False).mean()
        exp2 = prices.ewm(span=slow, adjust=False).mean()
        macd = exp1 - exp2
        signal_line = macd.ewm(span=signal, adjust=False).mean()
        histogram = macd - signal_line
        return macd, signal_line, histogram
    
    def _calculate_bollinger_bands(self, prices: pd.Series, period: int = 20, std: int = 2) -> Tuple:
        """计算布林带"""
        middle = prices.rolling(window=period).mean()
        std_dev = prices.rolling(window=period).std()
        upper = middle + (std_dev * std)
        lower = middle - (std_dev * std)
        return upper, middle, lower
    
    def _calculate_kdj(self, high: pd.Series, low: pd.Series, close: pd.Series, period: int = 9) -> Tuple:
        """计算KDJ指标"""
        low_min = low.rolling(window=period).min()
        high_max = high.rolling(window=period).max()
        
        rsv = 100 * ((close - low_min) / (high_max - low_min))
        k = rsv.ewm(com=2).mean()
        d = k.ewm(com=2).mean()
        j = 3 * k - 2 * d
        
        return k, d, j
    
    def _identify_technical_signals(self, df: pd.DataFrame, indicators: Dict) -> Dict:
        """识别技术信号"""
        signals = {
            'buy_signals': [],
            'sell_signals': [],
            'neutral_signals': [],
            'warning_signals': [],
        }
        
        # 获取最新值
        latest_close = df['close'].iloc[-1]
        latest_rsi = indicators['rsi'].iloc[-1] if not indicators['rsi'].empty else 50
        latest_macd = indicators['macd'].iloc[-1] if not indicators['macd'].empty else 0
        latest_macd_signal = indicators['macd_signal'].iloc[-1] if not indicators['macd_signal'].empty else 0
        
        # RSI信号
        if latest_rsi < 30:
            signals['buy_signals'].append({
                'type': 'rsi_oversold',
                'description': 'RSI超卖 (<30)',
                'strength': 'strong',
                'value': latest_rsi
            })
        elif latest_rsi > 70:
            signals['sell_signals'].append({
                'type': 'rsi_overbought',
                'description': 'RSI超买 (>70)',
                'strength': 'strong',
                'value': latest_rsi
            })
        
        # MACD信号
        if latest_macd > latest_macd_signal:
            signals['buy_signals'].append({
                'type': 'macd_bullish',
                'description': 'MACD金叉',
                'strength': 'medium',
                'value': f"MACD={latest_macd:.2f}, Signal={latest_macd_signal:.2f}"
            })
        elif latest_macd < latest_macd_signal:
            signals['sell_signals'].append({
                'type': 'macd_bearish',
                'description': 'MACD死叉',
                'strength': 'medium',
                'value': f"MACD={latest_macd:.2f}, Signal={latest_macd_signal:.2f}"
            })
        
        # 价格与移动平均线关系
        for period in self.indicators_config['moving_averages']:
            ma_key = f'ma{period}'
            if ma_key in indicators and not indicators[ma_key].empty:
                latest_ma = indicators[ma_key].iloc[-1]
                
                if latest_close > latest_ma * 1.05:  # 价格高于均线5%
                    signals['buy_signals'].append({
                        'type': f'price_above_ma{period}',
                        'description': f'价格在MA{period}之上',
                        'strength': 'weak',
                        'value': f"价格={latest_close:.2f}, MA{period}={latest_ma:.2f}"
                    })
                elif latest_close < latest_ma * 0.95:  # 价格低于均线5%
                    signals['sell_signals'].append({
                        'type': f'price_below_ma{period}',
                        'description': f'价格在MA{period}之下',
                        'strength': 'weak',
                        'value': f"价格={latest_close:.2f}, MA{period}={latest_ma:.2f}"
                    })
        
        # 布林带信号
        if 'bollinger_upper' in indicators and 'bollinger_lower' in indicators:
            upper = indicators['bollinger_upper'].iloc[-1] if not indicators['bollinger_upper'].empty else 0
            lower = indicators['bollinger_lower'].iloc[-1] if not indicators['bollinger_lower'].empty else 0
            
            if latest_close > upper:
                signals['sell_signals'].append({
                    'type': 'bollinger_upper_break',
                    'description': '突破布林带上轨',
                    'strength': 'medium',
                    'value': f"价格={latest_close:.2f}, 上轨={upper:.2f}"
                })
            elif latest_close < lower:
                signals['buy_signals'].append({
                    'type': 'bollinger_lower_break',
                    'description': '跌破布林带下轨',
                    'strength': 'medium',
                    'value': f"价格={latest_close:.2f}, 下轨={lower:.2f}"
                })
        
        return signals
    
    def _assess_stock_trend(self, df: pd.DataFrame, indicators: Dict) -> Dict:
        """评估股票趋势"""
        # 简单趋势判断
        prices = df['close']
        
        # 短期趋势（5日）
        if len(prices) >= 5:
            short_trend = '上涨' if prices.iloc[-1] > prices.iloc[-5] else '下跌'
            short_strength = abs(prices.iloc[-1] - prices.iloc[-5]) / prices.iloc[-5]
        else:
            short_trend = '未知'
            short_strength = 0
        
        # 中期趋势（20日）
        if len(prices) >= 20:
            medium_trend = '上涨' if prices.iloc[-1] > prices.iloc[-20] else '下跌'
            medium_strength = abs(prices.iloc[-1] - prices.iloc[-20]) / prices.iloc[-20]
        else:
            medium_trend = '未知'
            medium_strength = 0
        
        # 移动平均线排列
        ma_alignment = '未知'
        if all(key in indicators for key in ['ma5', 'ma10', 'ma20']):
            ma5 = indicators['ma5'].iloc[-1] if not indicators['ma5'].empty else 0
            ma10 = indicators['ma10'].iloc[-1] if not indicators['ma10'].empty else 0
            ma20 = indicators['ma20'].iloc[-1] if not indicators['ma20'].empty else 0
            
            if ma5 > ma10 > ma20:
                ma_alignment = '多头排列'
            elif ma5 < ma10 < ma20:
                ma_alignment = '空头排列'
            else:
                ma_alignment = '纠结排列'
        
        return {
            'short_term': {
                'trend': short_trend,
                'strength': short_strength,
                'description': f'短期({short_trend})，强度{short_strength:.2%}'
            },
            'medium_term': {
                'trend': medium_trend,
                'strength': medium_strength,
                'description': f'中期({medium_trend})，强度{medium_strength:.2%}'
            },
            'ma_alignment': ma_alignment,
            'overall_trend': self._determine_overall_trend(short_trend, medium_trend, ma_alignment),
            'confidence': self._calculate_trend_confidence(short_strength, medium_strength),
        }
    
    def _determine_overall_trend(self, short_trend: str, medium_trend: str, ma_alignment: str) -> str:
        """确定整体趋势"""
        if short_trend == '上涨' and medium_trend == '上涨' and ma_alignment == '多头排列':
            return '强势上涨'
        elif short_trend == '上涨' and medium_trend == '上涨':
            return '上涨'
        elif short_trend == '下跌' and medium_trend == '下跌' and ma_alignment == '空头排列':
            return '强势下跌'
        elif short_trend == '下跌' and medium_trend == '下跌':
            return '下跌'
        else:
            return '震荡'
    
    def _calculate_trend_confidence(self, short_strength: float, medium_strength: float) -> float:
        """计算趋势置信度"""
        # 基于趋势强度的简单置信度计算
        avg_strength = (short_strength + medium_strength) / 2
        confidence = min(avg_strength * 10, 1.0)  # 转换到0-1范围
        return round(confidence, 2)
    
    def _generate_technical_summary(self, symbol: str, indicators: Dict, signals: Dict, trend: Dict) -> str:
        """生成技术分析总结"""
        summary_parts = []
        
        # 趋势总结
        summary_parts.append(f"📈 **趋势分析**: {trend['overall_trend']} (置信度: {trend['confidence']})")
        
        # 信号总结
        buy_count = len(signals['buy_signals'])
        sell_count = len(signals['sell_signals'])
        
        if buy_count > sell_count:
            signal_summary = f"买入信号较多 ({buy_count}个买入 vs {sell_count}个卖出)"
        elif sell_count > buy_count:
            signal_summary = f"卖出信号较多 ({sell_count}个卖出 vs {buy_count}个买入)"
        else:
            signal_summary = "买卖信号平衡"
        
        summary_parts.append(f"📊 **技术信号**: {signal_summary}")
        
        # 关键指标
        if 'rsi' in indicators and not indicators['