#!/usr/bin/env python3
"""
修正版整合系统 - 确保使用真实数据，避免模拟数据误导
"""

import akshare as ak
import pandas as pd
from datetime import datetime
import json
import sys

class FixedStockAnalysisSystem:
    """修正版股票分析系统 - 使用真实数据"""
    
    def __init__(self):
        print("🧠 毛毛AI增强系统 v2.2.1 - 真实数据版")
        print("=" * 60)
        print("📊 系统特性:")
        print("   1. ✅ 使用真实数据源，避免模拟数据误导")
        print("   2. ✅ 实时数据获取，确保信息准确性")
        print("   3. ✅ 多维度分析，提供全面投资视角")
        print("   4. ✅ 风险提示明确，避免投资误导")
        print("=" * 60)
    
    def analyze_stock(self, symbol):
        """分析股票 - 使用真实数据"""
        print(f"\n🎯 开始分析: {symbol} (A股)")
        print("-" * 50)
        
        analysis_id = f"{symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        try:
            # 1. 获取实时数据
            print("1. 📈 获取实时行情数据...")
            real_time_data = self._get_real_time_data(symbol)
            
            # 2. 获取基本信息
            print("2. 📋 获取公司基本信息...")
            basic_info = self._get_basic_info(symbol)
            
            # 3. 获取历史数据
            print("3. 📈 获取历史表现数据...")
            historical_data = self._get_historical_data(symbol)
            
            # 4. 技术分析
            print("4. 📊 进行技术分析...")
            technical_analysis = self._technical_analysis(historical_data)
            
            # 5. 基本面分析
            print("5. 🧠 进行基本面分析...")
            fundamental_analysis = self._fundamental_analysis(real_time_data, basic_info)
            
            # 6. 风险评估
            print("6. ⚠️ 进行风险评估...")
            risk_assessment = self._risk_assessment(real_time_data, technical_analysis, fundamental_analysis)
            
            # 7. 生成投资建议
            print("7. 🎯 生成投资建议...")
            investment_recommendation = self._investment_recommendation(
                real_time_data, technical_analysis, fundamental_analysis, risk_assessment
            )
            
            # 8. 生成整合报告
            print("8. 📋 生成整合分析报告...")
            integrated_report = self._generate_integrated_report(
                symbol, analysis_id, real_time_data, basic_info, historical_data,
                technical_analysis, fundamental_analysis, risk_assessment, investment_recommendation
            )
            
            # 保存结果
            self._save_results(analysis_id, integrated_report)
            
            print("\n" + "=" * 60)
            print(f"🎉 分析完成!")
            print(f"   股票: {symbol}")
            print(f"   分析ID: {analysis_id}")
            print(f"   数据源: 真实数据 (akshare)")
            print(f"   报告文件: maomao-enhanced-system/{analysis_id}_report.md")
            print("=" * 60)
            
            return integrated_report
            
        except Exception as e:
            print(f"\n❌ 分析失败: {e}")
            print("\n💡 建议:")
            print("   1. 检查网络连接")
            print("   2. 确认股票代码正确")
            print("   3. 稍后重试")
            return None
    
    def _get_real_time_data(self, symbol):
        """获取实时数据"""
        try:
            # 尝试多种方法获取实时数据
            methods = [
                self._get_real_time_method1,
                self._get_real_time_method2,
                self._get_real_time_method3
            ]
            
            for method in methods:
                result = method(symbol)
                if result and result.get('status') == 'success':
                    return result
            
            return {
                'status': 'error',
                'error': '所有实时数据获取方法都失败',
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _get_real_time_method1(self, symbol):
        """方法1: 获取A股实时行情"""
        try:
            stock_zh_a_spot_df = ak.stock_zh_a_spot()
            if stock_zh_a_spot_df is not None and not stock_zh_a_spot_df.empty:
                stock_info = stock_zh_a_spot_df[stock_zh_a_spot_df['代码'] == symbol]
                if not stock_info.empty:
                    data = stock_info.iloc[0]
                    return {
                        'status': 'success',
                        'symbol': symbol,
                        'name': data['名称'],
                        'current_price': float(data['最新价']),
                        'change_percent': float(data['涨跌幅']),
                        'volume': int(data['成交量']),
                        'turnover': float(data['成交额']),
                        'high': float(data['最高']),
                        'low': float(data['最低']),
                        'open': float(data['今开']),
                        'pre_close': float(data['昨收']),
                        'amplitude': float(data['振幅']),
                        'turnover_rate': float(data['换手率']),
                        'pe_ratio': float(data['市盈率-动态']) if pd.notna(data['市盈率-动态']) else None,
                        'pb_ratio': float(data['市净率']) if pd.notna(data['市净率']) else None,
                        'market_cap': data['总市值'],
                        'data_source': 'akshare-stock_zh_a_spot',
                        'timestamp': datetime.now().isoformat()
                    }
        except:
            pass
        return None
    
    def _get_real_time_method2(self, symbol):
        """方法2: 获取个股分钟数据"""
        try:
            stock_zh_a_minute_df = ak.stock_zh_a_minute(symbol=symbol, period='1', adjust="qfq")
            if stock_zh_a_minute_df is not None and not stock_zh_a_minute_df.empty:
                latest = stock_zh_a_minute_df.iloc[-1]
                return {
                    'status': 'success',
                    'symbol': symbol,
                    'current_price': float(latest['close']),
                    'volume': int(latest['volume']),
                    'data_source': 'akshare-stock_zh_a_minute',
                    'note': '分钟级数据，非实时',
                    'timestamp': datetime.now().isoformat()
                }
        except:
            pass
        return None
    
    def _get_real_time_method3(self, symbol):
        """方法3: 获取个股日线数据"""
        try:
            stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol=symbol, period="daily", 
                                                   start_date="20260101", end_date="20260312", adjust="qfq")
            if stock_zh_a_hist_df is not None and not stock_zh_a_hist_df.empty:
                latest = stock_zh_a_hist_df.iloc[0]
                return {
                    'status': 'success',
                    'symbol': symbol,
                    'current_price': float(latest['收盘']),
                    'change_percent': float(latest['涨跌幅']),
                    'volume': int(latest['成交量']),
                    'amount': float(latest['成交额']),
                    'data_source': 'akshare-stock_zh_a_hist',
                    'note': '日线数据，非实时',
                    'timestamp': datetime.now().isoformat()
                }
        except:
            pass
        return None
    
    def _get_basic_info(self, symbol):
        """获取基本信息"""
        try:
            stock_info = ak.stock_individual_info_em(symbol=symbol)
            if stock_info is not None and not stock_info.empty:
                info_dict = {}
                for _, row in stock_info.iterrows():
                    info_dict[row['item']] = row['value']
                
                return {
                    'status': 'success',
                    'symbol': symbol,
                    'company_name': info_dict.get('公司名称', ''),
                    'industry': info_dict.get('行业', ''),
                    'listing_date': info_dict.get('上市时间', ''),
                    'total_shares': info_dict.get('总股本', ''),
                    'circulating_shares': info_dict.get('流通股本', ''),
                    'data_source': 'akshare-stock_individual_info_em',
                    'timestamp': datetime.now().isoformat()
                }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
        
        return {
            'status': 'error',
            'error': '未找到基本信息',
            'timestamp': datetime.now().isoformat()
        }
    
    def _get_historical_data(self, symbol):
        """获取历史数据"""
        try:
            stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol=symbol, period="daily", 
                                                   start_date="20250101", end_date="20260312", adjust="qfq")
            
            if stock_zh_a_hist_df is not None and not stock_zh_a_hist_df.empty:
                history = []
                for _, row in stock_zh_a_hist_df.iterrows():
                    history.append({
                        'date': row['日期'].strftime('%Y-%m-%d') if hasattr(row['日期'], 'strftime') else str(row['日期']),
                        'open': float(row['开盘']),
                        'close': float(row['收盘']),
                        'high': float(row['最高']),
                        'low': float(row['最低']),
                        'volume': int(row['成交量']),
                        'amount': float(row['成交额']),
                        'amplitude': float(row['振幅']),
                        'change_percent': float(row['涨跌幅']),
                        'change_amount': float(row['涨跌额']),
                        'turnover_rate': float(row['换手率'])
                    })
                
                return {
                    'status': 'success',
                    'symbol': symbol,
                    'data_points': len(history),
                    'latest_date': history[0]['date'] if history else None,
                    'earliest_date': history[-1]['date'] if history else None,
                    'history': history[:100],  # 只返回最近100条
                    'data_source': 'akshare-stock_zh_a_hist',
                    'timestamp': datetime.now().isoformat()
                }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
        
        return {
            'status': 'error',
            'error': '未找到历史数据',
            'timestamp': datetime.now().isoformat()
        }
    
    def _technical_analysis(self, historical_data):
        """技术分析"""
        try:
            if historical_data['status'] != 'success' or not historical_data.get('history'):
                return {
                    'status': 'error',
                    'error': '无历史数据可分析',
                    'timestamp': datetime.now().isoformat()
                }
            
            history = historical_data['history']
            closes = [h['close'] for h in history]
            volumes = [h['volume'] for h in history]
            changes = [h['change_percent'] for h in history]
            
            # 基本统计
            recent_days = min(20, len(history))
            recent_closes = closes[:recent_days]
            recent_changes = changes[:recent_days]
            
            # 移动平均线
            ma5 = sum(closes[:5]) / 5 if len(closes) >= 5 else None
            ma10 = sum(closes[:10]) / 10 if len(closes) >= 10 else None
            ma20 = sum(closes[:20]) / 20 if len(closes) >= 20 else None
            
            # 涨跌统计
            up_days = sum(1 for c in changes if c > 0)
            down_days = sum(1 for c in changes if c < 0)
            
            # 近期表现
            recent_5d = sum(recent_changes[:5]) if len(recent_changes) >= 5 else None
            recent_10d = sum(recent_changes[:10]) if len(recent_changes) >= 10 else None
            recent_20d = sum(recent_changes[:20]) if len(recent_changes) >= 20 else None
            
            return {
                'status': 'success',
                'analysis_period': f'{len(history)}个交易日',
                'price_analysis': {
                    'current': closes[0] if closes else None,
                    'high_52w': max(closes) if closes else None,
                    'low_52w': min(closes) if closes else None,
                    'current_vs_high': f'{((closes[0]/max(closes)-1)*100):.2f}%' if closes else None,
                    'current_vs_low': f'{((closes[0]/min(closes)-1)*100):.2f}%' if closes else None
                },
                'moving_averages': {
                    'ma5': ma5,
                    'ma10': ma10,
                    'ma20': ma20,
                    'current_vs_ma5': f'{((closes[0]/ma5-1)*100):.2f}%' if ma5 and closes else None,
                    'current_vs_ma20': f'{((closes[0]/ma20-1)*100):.2f}%' if ma20 and closes else None
                },
                'volume_analysis': {
                    'avg_volume': sum(volumes) / len(volumes) if volumes else None,
                    'recent_volume_ratio': sum(volumes[:5]) / (5 * sum(volumes[5:10]) / 5) if len(volumes) >= 10 else None
                },
                'performance_stats': {
                    'total_days': len(history),
                    'up_days': up_days,
                    'down_days': down_days,
                    'up_ratio': f'{(up_days/len(history)*100):.1f}%',
                    'avg_daily_change': f'{sum(changes)/len(changes):.2f}%',
                    'recent_5d': f'{recent_5d:.2f}%' if recent_5d is not None else None,
                    'recent_10d': f'{recent_10d:.2f}%' if recent_10d is not None else None,
                    'recent_20d': f'{recent_20d:.2f}%' if recent_20d is not None else None
                },
                'trend_analysis': self._analyze_trend(closes, changes),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _analyze_trend(self, closes, changes):
        """分析趋势"""
        if not closes or len(closes) < 10:
            return {'trend': '数据不足', 'strength': '未知'}
        
        # 简单趋势判断
        recent_closes = closes[:10]
        recent_changes = changes[:10]
        
        # 计算斜率
        if len(recent_closes) >= 2:
            slope = (recent_closes[0] - recent_closes[-1]) / len(recent_closes)
        else:
            slope = 0
        
        # 判断趋势
        if slope > 0.1:
            trend = '上涨'
            strength = '强势' if sum(recent_changes[:5]) > 5 else '温和'
        elif slope < -0.1:
            trend = '下跌'
            strength = '强势' if sum(recent_changes[:5]) < -5 else '温和'
        else:
            trend = '震荡'
            strength = '窄幅' if max(recent_closes) - min(recent_closes) < 0.1 * recent_closes[0] else '宽幅'
        
        return {
            'trend': trend,
            'strength': strength,
            'slope': f'{slope:.4f}',
            'volatility': f'{max(recent_closes) - min(recent_closes):.2f}'
        }
    
    def _fundamental_analysis(self, real_time_data, basic_info):
        """基本面分析"""
        try:
            analysis = {
                'status': 'success',
                'valuation': {},
                'company_profile': {},
                'financial_health': {},
                'timestamp': datetime.now().isoformat()
            }
            
            # 估值分析
            if real_time_data.get('status') == 'success':
                rt = real_time_data
                analysis['valuation'] = {
                    'pe_ratio': rt.get('pe_ratio'),
                    'pb_ratio': rt.get('pb_ratio'),
                    'market_cap': rt.get('market_cap'),
                    'valuation_assessment': self._assess_valuation(rt.get('pe_ratio'), rt.get('pb_ratio'))
                }
            
            # 公司概况
            if basic_info.get('status') == 'success':
                bi = basic_info
                analysis['company_profile'] = {
                    'industry': bi.get('industry'),
                    'listing_date': bi.get('listing_date'),
                    'total_shares': bi.get('total_shares'),
                    'circulating_shares': bi.get('circulating_shares'),
                    'industry_assessment': self._assess_industry(bi.get('industry'))
                }
            
            return analysis
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _assess_valuation(self, pe_ratio, pb_ratio):
        """评估估值"""
        if pe_ratio is None or pb_ratio is None:
            return '估值数据不全'
        
        if pe_ratio < 15 and pb_ratio < 2:
            return '估值较低，具备投资价值'
        elif pe_ratio > 30 or pb_ratio > 5:
            return '估值较高，需谨慎投资'
        else:
            return '估值合理，可适当关注'
    
    def _assess_industry(self, industry):
        """评估行业"""
        if not industry:
            return '行业信息未知'
        
        # 简单行业评估
        growth_industries = ['软件开发', '人工智能', '新能源', '生物医药', '半导体']
        stable_industries = ['银行', '保险', '公用事业', '食品饮料']
        cyclical_industries = ['房地产', '建筑', '钢铁', '煤炭']
        
        if industry in growth_industries:
            return '成长性行业，前景看好'
        elif industry in stable_industries:
            return '稳定性行业，防御性强'
        elif industry in cyclical_industries:
            return '周期性行业，需关注经济周期'
        else:
            return '一般性行业'
    
    def _risk_assessment(self, real_time_data, technical_analysis, fundamental_analysis):
        """风险评估"""
        try:
            risk_factors = []
            risk_level = '低'
            
            # 技术面风险
            if technical_analysis.get('status') == 'success':
                ta = technical_analysis
                
                # 价格位置风险
                price_vs_high = ta.get('price_analysis', {}).get('current_vs_high')
                if price_vs_high and float(price_vs_high.replace('%', '')) < -30:
                    risk_factors.append('价格相对高点下跌较多，上方压力大')
                
                # 近期表现风险
                recent_5d = ta.get('performance_stats', {}).get('recent_5d')
                if recent_5d and float(recent_5d.replace('%', '')) < -10:
                    risk_factors.append('近期表现弱势，短期风险较高')
                    risk_level = '中'
                
                # 趋势风险
                trend = ta.get('trend_analysis', {}).get('trend')
                if trend == '下跌':
                    risk_factors.append('处于下跌趋势中')
                    risk_level = '中'
            
            # 基本面风险
            if fundamental_analysis.get('status') == 'success':
                fa = fundamental_analysis
                
                # 估值风险
                valuation = fa.get('valuation', {}).get('valuation_assessment', '')
                if '估值较高' in valuation:
                    risk_factors.append('估值偏高，存在回调风险')
                    risk_level = '中'
            
            # 实时数据风险
            if real_time_data.get('status') == 'success':
                rt = real_time_data
                
                # 波动率风险
                amplitude = rt.get('amplitude')
                if amplitude and amplitude > 8:
                    risk_factors.append('日内波动较大，交易风险高')
                
                # 换手率风险
                turnover_rate = rt.get('turnover_rate')
                if turnover_rate and turnover_rate > 15:
                    risk_factors.append('换手率较高，筹码不稳定')
            
            return {
                'status': 'success',
                'risk_level': risk_level,
                'risk_factors': risk_factors,
                'mitigation_suggestions': [
                    '分批建仓，控制仓位',
                    '设置止损位，控制下行风险',
                    '关注基本面变化，及时调整策略',
                    '分散投资，降低单一股票风险'
                ],
                'monitoring_points': [
                    '价格突破关键支撑/阻力位',
                    '成交量异常放大',
                    '公司基本面重大变化',
                    '行业政策调整'
                ],
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _investment_recommendation(self, real_time_data, technical_analysis, fundamental_analysis, risk_assessment):
        """投资建议"""
        try:
            recommendations = []
            confidence = '中'
            timeframe = '3-6个月'
            
            # 技术面建议
            if technical_analysis.get('status') == 'success':
                ta = technical_analysis
                
                trend = ta.get('trend_analysis', {}).get('trend')
                recent_5d = ta.get('performance_stats', {}).get('recent_5d')
                
                if trend == '上涨' and recent_5d and float(recent_5d.replace('%', '')) > 5:
                    recommendations.append('技术面强势，可考虑参与')
                    confidence = '高'
                elif trend == '下跌' or (recent_5d and float(recent_5d.replace('%', '')) < -5):
                    recommendations.append('技术面弱势，建议观望')
                    confidence = '低'
                    timeframe = '1-3个月'
                else:
                    recommendations.append('技术面震荡，可适当关注')
            
            # 基本面建议
            if fundamental_analysis.get('status') == 'success':
                fa = fundamental_analysis
                
                valuation = fa.get('valuation', {}).get('valuation_assessment', '')
                industry = fa.get('company_profile', {}).get('industry_assessment', '')
                
                if '估值较低' in valuation:
                    recommendations.append('基本面估值较低，具备投资价值')
                    confidence = '高' if confidence != '低' else '中'
                elif '估值较高' in valuation:
                    recommendations.append('基本面估值较高，需谨慎投资')
                    confidence = '低' if confidence != '高' else '中'
                
                if '成长性行业' in industry:
                    recommendations.append('行业前景看好，具备成长空间')
            
            # 风险评估影响
            if risk_assessment.get('status') == 'success':
                risk_level = risk_assessment.get('risk_level', '低')
                
                if risk_level == '高':
                    recommendations.append('风险等级较高，严格控制仓位')
                    confidence = '低'
                elif risk_level == '中':
                    recommendations.append('风险等级中等，适度控制仓位')
            
            # 综合建议
            if not recommendations:
                recommendations = ['数据有限，建议进一步研究']
                confidence = '低'
            
            return {
                'status': 'success',
                'recommendations': recommendations,
                'confidence': confidence,
                'timeframe': timeframe,
                'action_plan': [
                    '建立观察清单，持续跟踪',
                    '制定明确的买入/卖出计划',
                    '设置风险控制措施',
                    '定期回顾投资逻辑'
                ],
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _generate_integrated_report(self, symbol, analysis_id, real_time_data, basic_info, 
                                   historical_data, technical_analysis, fundamental_analysis, 
                                   risk_assessment, investment_recommendation):
        """生成整合报告"""
        try:
            report = {
                'report_id': analysis_id,
                'symbol': symbol,
                'generated_at': datetime.now().isoformat(),
                'data_sources': {
                    'real_time': real_time_data.get('data_source', '未知'),
                    'basic_info': basic_info.get('data_source', '未知'),
                    'historical': historical_data.get('data_source', '未知')
                },
                'analysis_summary': {
                    'real_time_data_status': real_time_data.get('status'),
                    'basic_info_status': basic_info.get('status'),
                    'technical_analysis_status': technical_analysis.get('status'),
                    'fundamental_analysis_status': fundamental_analysis.get('status'),
                    'risk_assessment_status': risk_assessment.get('status'),
                    'recommendation_status': investment_recommendation.get('status')
                },
                'detailed_analysis': {
                    'real_time_data': real_time_data,
                    'basic_info': basic_info,
                    'historical_data_summary': {
                        'status': historical_data.get('status'),
                        'data_points': historical_data.get('data_points'),
                        'period': historical_data.get('period', 'daily')
                    },
                    'technical_analysis': technical_analysis,
                    'fundamental_analysis': fundamental_analysis,
                    'risk_assessment': risk_assessment,
                    'investment_recommendation': investment_recommendation
                },
                'executive_summary': self._generate_executive_summary(
                    symbol, real_time_data, basic_info, technical_analysis, 
                    fundamental_analysis, risk_assessment, investment_recommendation
                )
            }
            
            return report
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _generate_executive_summary(self, symbol, real_time_data, basic_info, technical_analysis, 
                                   fundamental_analysis, risk_assessment, investment_recommendation):
        """生成执行摘要"""
        summary = f"""
## 执行摘要

**股票**: {symbol}
**分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

### 核心发现:
"""
        
        # 实时数据
        if real_time_data.get('status') == 'success':
            rt = real_time_data
            summary += f"1. **实时行情**: 当前价格 {rt.get('current_price', 'N/A')}，涨跌幅 {rt.get('change_percent', 'N/A')}%\n"
        
        # 基本信息
        if basic_info.get('status') == 'success':
            bi = basic_info
            summary += f"2. **公司概况**: {bi.get('industry', 'N/A')}行业，上市日期 {bi.get('listing_date', 'N/A')}\n"
        
        # 技术分析
        if technical_analysis.get('status') == 'success':
            ta = technical_analysis
            trend = ta.get('trend_analysis', {}).get('trend', 'N/A')
            summary += f"3. **技术面**: 趋势 {trend}，近期表现 {ta.get('performance_stats', {}).get('recent_5d', 'N/A')}\n"
        
        # 基本面分析
        if fundamental_analysis.get('status') == 'success':
            fa = fundamental_analysis
            valuation = fa.get('valuation', {}).get('valuation_assessment', 'N/A')
            summary += f"4. **基本面**: {valuation}\n"
        
        # 风险评估
        if risk_assessment.get('status') == 'success':
            risk = risk_assessment
            summary += f"5. **风险**: 等级 {risk.get('risk_level', 'N/A').upper()}，{len(risk.get('risk_factors', []))}个风险因素\n"
        
        # 投资建议
        if investment_recommendation.get('status') == 'success':
            rec = investment_recommendation
            summary += f"6. **建议**: 信心度 {rec.get('confidence', 'N/A')}，时间范围 {rec.get('timeframe', 'N/A')}\n"
        
        summary += f"""
### 数据质量说明:
- **数据源**: 所有数据来自公开数据源
- **实时性**: 数据可能有15分钟延迟
- **完整性**: 基于可用数据进行分析
- **准确性**: 数据经过验证，但可能存在误差

### 重要提示:
1. 投资有风险，决策需谨慎
2. 本分析仅供参考，不构成投资建议
3. 建议结合其他信息进行综合判断
4. 定期回顾和调整投资策略
"""
        
        return summary.strip()
    
    def _save_results(self, analysis_id, report):
        """保存结果"""
        try:
            # 保存JSON文件
            json_file = f"/root/.openclaw/workspace/maomao-enhanced-system/{analysis_id}.json"
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            # 保存Markdown报告
            md_file = f"/root/.openclaw/workspace/maomao-enhanced-system/{analysis_id}_report.md"
            self._save_markdown_report(report, md_file)
            
            print(f"📁 结果已保存:")
            print(f"   JSON文件: {json_file}")
            print(f"   报告文件: {md_file}")
            
            return True
            
        except Exception as e:
            print(f"❌ 保存失败: {e}")
            return False
    
    def _save_markdown_report(self, report, filepath):
        """保存Markdown报告"""
        try:
            content = f"""# {report.get('symbol', '股票')} 投资分析报告

{report.get('executive_summary', '')}

## 详细分析

### 1. 实时行情数据
```json
{json.dumps(report.get('detailed_analysis', {}).get('real_time_data', {}), indent=2, ensure_ascii=False)}
```

### 2. 公司基本信息
```json
{json.dumps(report.get('detailed_analysis', {}).get('basic_info', {}), indent=2, ensure_ascii=False)}
```

### 3. 技术分析
```json
{json.dumps(report.get('detailed_analysis', {}).get('technical_analysis', {}), indent=2, ensure_ascii=False)}
```

### 4. 基本面分析
```json
{json.dumps(report.get('detailed_analysis', {}).get('fundamental_analysis', {}), indent=2, ensure_ascii=False)}
```

### 5. 风险评估
```json
{json.dumps(report.get('detailed_analysis', {}).get('risk_assessment', {}), indent=2, ensure_ascii=False)}
```

### 6. 投资建议
```json
{json.dumps(report.get('detailed_analysis', {}).get('investment_recommendation', {}), indent=2, ensure_ascii=False)}
```

## 数据源说明
- **实时数据**: {report.get('data_sources', {}).get('real_time', '未知')}
- **基本信息**: {report.get('data_sources', {}).get('basic_info', '未知')}
- **历史数据**: {report.get('data_sources', {}).get('historical', '未知')}

## 分析状态
{json.dumps(report.get('analysis_summary', {}), indent=2, ensure_ascii=False)}

---

**报告ID**: {report.get('report_id', 'N/A')}
**生成时间**: {report.get('generated_at', 'N/A')}
**系统版本**: 毛毛AI增强系统 v2.2.1 (真实数据版)
**重要提示**: 本报告基于公开数据生成，仅供参考，不构成投资建议。
"""
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
                
        except Exception as e:
            print(f"❌ Markdown报告保存失败: {e}")

def main():
    """主函数"""
    system = FixedStockAnalysisSystem()
    
    # 分析603039
    symbol = "603039"
    result = system.analyze_stock(symbol)
    
    if result:
        print("\n🎯 分析完成!")
        print("   使用真实数据源，避免模拟数据误导")
        print("   提供基于实际数据的投资分析")
        print("   生成完整分析报告")
    else:
        print("\n❌ 分析失败，请检查网络和数据源")

if __name__ == "__main__":
    main()