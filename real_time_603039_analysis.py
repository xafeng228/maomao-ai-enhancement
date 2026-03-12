#!/usr/bin/env python3
"""
603039实时数据分析 - 使用真实数据源
"""

import akshare as ak
import pandas as pd
from datetime import datetime
import json
import sys

def get_real_time_stock_data(symbol):
    """获取股票实时数据"""
    try:
        print(f"🔍 获取{symbol}实时数据...")
        
        # 方法1: 获取A股实时行情
        stock_zh_a_spot_df = ak.stock_zh_a_spot()
        
        if stock_zh_a_spot_df is not None and not stock_zh_a_spot_df.empty:
            # 查找目标股票
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
                    'circulating_market_cap': data['流通市值'],
                    'timestamp': datetime.now().isoformat(),
                    'data_source': 'akshare-stock_zh_a_spot'
                }
        
        # 方法2: 如果方法1失败，尝试其他接口
        print(f"⚠️ 方法1未找到{symbol}，尝试其他接口...")
        
        # 尝试获取个股实时行情
        try:
            stock_zh_a_minute_df = ak.stock_zh_a_minute(symbol=symbol, period='1', adjust="qfq")
            if stock_zh_a_minute_df is not None and not stock_zh_a_minute_df.empty:
                latest = stock_zh_a_minute_df.iloc[-1]
                return {
                    'status': 'success',
                    'symbol': symbol,
                    'current_price': float(latest['close']),
                    'volume': int(latest['volume']),
                    'timestamp': datetime.now().isoformat(),
                    'data_source': 'akshare-stock_zh_a_minute',
                    'note': '分钟级数据，非实时'
                }
        except:
            pass
        
        return {
            'status': 'error',
            'symbol': symbol,
            'error': '未找到实时数据',
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'symbol': symbol,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }

def get_stock_basic_info(symbol):
    """获取股票基本信息"""
    try:
        print(f"📋 获取{symbol}基本信息...")
        
        # 获取股票基本信息
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
                'timestamp': datetime.now().isoformat(),
                'data_source': 'akshare-stock_individual_info_em'
            }
        
        return {
            'status': 'error',
            'symbol': symbol,
            'error': '未找到基本信息',
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'symbol': symbol,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }

def get_historical_data(symbol, period="daily"):
    """获取历史数据"""
    try:
        print(f"📈 获取{symbol}历史数据...")
        
        if period == "daily":
            # 获取日线数据
            stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol=symbol, period="daily", start_date="20250101", end_date="20260312", adjust="qfq")
        elif period == "weekly":
            stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol=symbol, period="weekly", start_date="20240101", end_date="20260312", adjust="qfq")
        else:
            stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol=symbol, period="monthly", start_date="20230101", end_date="20260312", adjust="qfq")
        
        if stock_zh_a_hist_df is not None and not stock_zh_a_hist_df.empty:
            # 转换为列表格式
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
                'period': period,
                'data_points': len(history),
                'latest_date': history[0]['date'] if history else None,
                'earliest_date': history[-1]['date'] if history else None,
                'history': history[:50],  # 只返回最近50条
                'timestamp': datetime.now().isoformat(),
                'data_source': f'akshare-stock_zh_a_hist_{period}'
            }
        
        return {
            'status': 'error',
            'symbol': symbol,
            'error': '未找到历史数据',
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'symbol': symbol,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }

def analyze_stock_performance(historical_data):
    """分析股票表现"""
    try:
        if historical_data['status'] != 'success' or not historical_data.get('history'):
            return {
                'status': 'error',
                'error': '无历史数据可分析'
            }
        
        history = historical_data['history']
        
        # 计算基本统计
        closes = [h['close'] for h in history]
        volumes = [h['volume'] for h in history]
        changes = [h['change_percent'] for h in history]
        
        # 近期表现
        recent_days = min(5, len(history))
        recent_changes = changes[:recent_days]
        
        # 技术指标计算（简化版）
        if len(closes) >= 20:
            ma5 = sum(closes[:5]) / 5
            ma10 = sum(closes[:10]) / 10
            ma20 = sum(closes[:20]) / 20
        else:
            ma5 = ma10 = ma20 = None
        
        # 涨跌统计
        up_days = sum(1 for c in changes if c > 0)
        down_days = sum(1 for c in changes if c < 0)
        
        return {
            'status': 'success',
            'analysis_period': f'{len(history)}个交易日',
            'price_range': {
                'current': closes[0] if closes else None,
                'high_52w': max(closes) if closes else None,
                'low_52w': min(closes) if closes else None,
                'current_vs_high': f'{((closes[0]/max(closes)-1)*100):.2f}%' if closes else None,
                'current_vs_low': f'{((closes[0]/min(closes)-1)*100):.2f}%' if closes else None
            },
            'moving_averages': {
                'ma5': ma5,
                'ma10': ma10,
                'ma20': ma20
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
                'recent_5d_performance': f'{sum(recent_changes):.2f}%' if recent_changes else None
            },
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }

def generate_investment_analysis(real_time_data, basic_info, performance_analysis):
    """生成投资分析"""
    try:
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'data_quality': {},
            'investment_analysis': {},
            'risk_assessment': {},
            'recommendations': []
        }
        
        # 数据质量评估
        analysis['data_quality'] = {
            'real_time_data': real_time_data.get('status'),
            'basic_info': basic_info.get('status'),
            'performance_analysis': performance_analysis.get('status'),
            'overall': 'good' if all([
                real_time_data.get('status') == 'success',
                basic_info.get('status') == 'success',
                performance_analysis.get('status') == 'success'
            ]) else 'partial'
        }
        
        # 投资分析
        if real_time_data['status'] == 'success':
            rt = real_time_data
            analysis['investment_analysis']['current_situation'] = {
                'price': rt.get('current_price'),
                'change_today': f"{rt.get('change_percent', 0):.2f}%",
                'volume': rt.get('volume'),
                'turnover': rt.get('turnover'),
                'pe_ratio': rt.get('pe_ratio'),
                'pb_ratio': rt.get('pb_ratio')
            }
        
        if basic_info['status'] == 'success':
            bi = basic_info
            analysis['investment_analysis']['company_profile'] = {
                'name': bi.get('company_name'),
                'industry': bi.get('industry'),
                'listing_date': bi.get('listing_date')
            }
        
        if performance_analysis['status'] == 'success':
            pa = performance_analysis
            analysis['investment_analysis']['technical_analysis'] = {
                'price_position': pa.get('price_range', {}).get('current_vs_high'),
                'moving_averages': pa.get('moving_averages'),
                'recent_performance': pa.get('performance_stats', {}).get('recent_5d_performance')
            }
        
        # 风险评估
        risk_factors = []
        
        if real_time_data.get('change_percent', 0) > 9.5:
            risk_factors.append('今日涨幅过大，短期回调风险')
        
        if real_time_data.get('amplitude', 0) > 10:
            risk_factors.append('波动率较高，价格不稳定')
        
        if performance_analysis.get('status') == 'success':
            pa = performance_analysis
            if pa.get('performance_stats', {}).get('up_ratio', '0%') < '40%':
                risk_factors.append('近期下跌天数较多，趋势偏弱')
        
        analysis['risk_assessment'] = {
            'risk_level': 'high' if len(risk_factors) >= 2 else 'medium' if len(risk_factors) >= 1 else 'low',
            'risk_factors': risk_factors,
            'mitigation_suggestions': [
                '分批建仓，控制仓位',
                '设置止损位',
                '关注成交量变化'
            ]
        }
        
        # 投资建议
        recommendations = []
        
        # 基于PE估值
        pe = real_time_data.get('pe_ratio')
        if pe is not None:
            if pe < 15:
                recommendations.append('估值较低，具备投资价值')
            elif pe > 30:
                recommendations.append('估值较高，需谨慎投资')
            else:
                recommendations.append('估值合理，可适当关注')
        
        # 基于技术面
        if performance_analysis.get('status') == 'success':
            recent_perf = performance_analysis.get('performance_stats', {}).get('recent_5d_performance', '0%')
            if recent_perf and float(recent_perf.replace('%', '')) > 5:
                recommendations.append('近期表现强势，可考虑参与')
            elif recent_perf and float(recent_perf.replace('%', '')) < -5:
                recommendations.append('近期表现弱势，建议观望')
        
        analysis['recommendations'] = recommendations
        
        return analysis
        
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }

def main():
    """主函数"""
    print("🧠 毛毛AI增强系统 - 实时数据分析")
    print("=" * 60)
    print("📊 分析目标: 603039 (A股)")
    print("🎯 使用真实数据源，避免模拟数据误导")
    print("=" * 60)
    
    symbol = "603039"
    
    try:
        # 1. 获取实时数据
        print("\n1. 📈 获取实时行情数据...")
        real_time_data = get_real_time_stock_data(symbol)
        
        if real_time_data['status'] == 'success':
            print(f"   ✅ 实时数据获取成功")
            print(f"      名称: {real_time_data.get('name', 'N/A')}")
            print(f"      最新价: {real_time_data.get('current_price', 'N/A')}")
            print(f"      涨跌幅: {real_time_data.get('change_percent', 'N/A')}%")
            print(f"      成交量: {real_time_data.get('volume', 'N/A')}")
        else:
            print(f"   ⚠️ 实时数据获取失败: {real_time_data.get('error', '未知错误')}")
        
        # 2. 获取基本信息
        print("\n2. 📋 获取公司基本信息...")
        basic_info = get_stock_basic_info(symbol)
        
        if basic_info['status'] == 'success':
            print(f"   ✅ 基本信息获取成功")
            print(f"      公司: {basic_info.get('company_name', 'N/A')}")
            print(f"      行业: {basic_info.get('industry', 'N/A')}")
        else:
            print(f"   ⚠️ 基本信息获取失败: {basic_info.get('error', '未知错误')}")
        
        # 3. 获取历史数据
        print("\n3. 📈 获取历史表现数据...")
        historical_data = get_historical_data(symbol, "daily")
        
        if historical_data['status'] == 'success':
            print(f"   ✅ 历史数据获取成功")
            print(f"      数据点: {historical_data.get('data_points', 0)} 个")
            print(f"      最新日期: {historical_data.get('latest_date', 'N/A')}")
        else:
            print(f"   ⚠️ 历史数据获取失败: {historical_data.get('error', '未知错误')}")
        
        # 4. 分析表现
        print("\n4. 📊 分析股票表现...")
        performance_analysis = analyze_stock_performance(historical_data)
        
        if performance_analysis['status'] == 'success':
            print(f"   ✅ 表现分析完成")
            perf_stats = performance_analysis.get('performance_stats', {})
            print(f"      上涨天数比例: {perf_stats.get('up_ratio', 'N/A')}")
            print(f"      近期5日表现: {perf_stats.get('recent_5d_performance', 'N/A')}")
        else:
            print(f"   ⚠️ 表现分析失败: {performance_analysis.get('error', '未知错误')}")
        
        # 5. 生成投资分析
        print("\n5. 🎯 生成投资分析...")
        investment_analysis = generate_investment_analysis(real_time_data, basic_info, performance_analysis)
        
        # 显示分析结果
        print("\n" + "=" * 60)
        print("📋 投资分析结果")
        print("=" * 60)
        
        # 数据质量
        data_quality = investment_analysis.get('data_quality', {})
        print(f"\n📊 数据质量: {data_quality.get('overall', 'unknown').upper()}")
        print(f"   实时数据: {data_quality.get('real_time_data', 'unknown')}")
        print(f"   基本信息: {data_quality.get('basic_info', 'unknown')}")
        print(f"   表现分析: {data_quality.get('performance_analysis', 'unknown')}")
        
        # 当前情况
        current = investment_analysis.get('investment_analysis', {}).get('current_situation', {})
        if current:
            print(f"\n📈 当前情况:")
            print(f"   价格: {current.get('price', 'N/A')}")
            print(f"   今日涨跌: {current.get('change_today', 'N/A')}")
            print(f"   成交量: {current.get('volume', 'N/A')}")
            print(f"   PE比率: {current.get('pe_ratio', 'N/A')}")
            print(f"   PB比率: {current.get('pb_ratio', 'N/A')}")
        
        # 公司概况
        profile = investment_analysis.get('investment_analysis', {}).get('company_profile', {})
        if profile:
            print(f"\n🏢 公司概况:")
            print(f"   名称: {profile.get('name', 'N/A')}")
            print(f"   行业: {profile.get('industry', 'N/A')}")
            print(f"   上市日期: {profile.get('listing_date', 'N/A')}")
        
        # 技术分析
        technical = investment_analysis.get('investment_analysis', {}).get('technical_analysis', {})
        if technical:
            print(f"\n📊 技术分析:")
            print(f"   价格位置: {technical.get('price_position', 'N/A')}")
            print(f"   近期表现: {technical.get('recent_performance', 'N/A')}")
        
        # 风险评估
        risk = investment_analysis.get('risk_assessment', {})
        if risk:
            print(f"\n⚠️ 风险评估:")
            print(f"   风险等级: {risk.get('risk_level', 'N/A').upper()}")
            if risk.get('risk_factors'):
                print(f"   风险因素:")
                for factor in risk['risk_factors']:
                    print(f"     - {factor}")
        
        # 投资建议
        recommendations = investment_analysis.get('recommendations', [])
        if recommendations:
            print(f"\n🎯 投资建议:")
            for i, rec in enumerate(recommendations, 1):
                print(f"   {i}. {rec}")
        
        # 数据源说明
        print(f"\n🔍 数据源说明:")
        print(f"   实时数据: {real_time_data.get('data_source', '未知')}")
        print(f"   基本信息: {basic_info.get('data_source', '未知')}")
        print(f"   历史数据: {historical_data.get('data_source', '未知')}")
        
        print("\n" + "=" * 60)
        print("💡 重要说明:")
        print("   1. 所有数据来自公开数据源")
        print("   2. 数据可能有15分钟延迟")
        print("   3. 投资建议仅供参考")
        print("   4. 投资有风险，决策需谨慎")
        print("=" * 60)
        
        # 保存结果
        output_file = f"/root/.openclaw/workspace/maomao-enhanced-system/603039_real_time_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                'symbol': symbol,
                'analysis_time': datetime.now().isoformat(),
                'real_time_data': real_time_data,
                'basic_info': basic_info,
                'historical_data_summary': {
                    'status': historical_data['status'],
                    'data_points': historical_data.get('data_points'),
                    'period': historical_data.get('period')
                },
                'performance_analysis': performance_analysis,
                'investment_analysis': investment_analysis
            }, f, indent=2, ensure_ascii=False)
        
        print(f"\n📁 分析结果已保存: {output_file}")
        print(f"   文件大小: {len(json.dumps(investment_analysis, ensure_ascii=False))} 字符")
        
        print("\n🎉 实时数据分析完成!")
        print("   使用真实数据源，避免模拟数据误导")
        print("   提供基于实际数据的投资分析")
        
    except Exception as e:
        print(f"\n❌ 分析过程出错: {e}")
        print("\n💡 建议:")
        print("   1. 检查网络连接")
        print("   2. 确认akshare库已正确安装")
        print("   3. 尝试其他股票代码")
        print("   4. 稍后重试")

if __name__ == "__main__":
    main()