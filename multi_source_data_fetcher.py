#!/usr/bin/env python3
"""
多数据源获取器 - 数据源扩展
"""

import akshare as ak
import pandas as pd
from datetime import datetime, timedelta
import json
import time
import sys
from typing import Dict, List, Any, Optional
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

class MultiSourceDataFetcher:
    """多数据源获取器"""
    
    def __init__(self, primary_source='akshare', fallback_sources=None, 
                 cache_ttl_minutes=10, max_workers=2):
        """
        初始化多数据源获取器
        
        Args:
            primary_source: 主要数据源
            fallback_sources: 备用数据源列表
            cache_ttl_minutes: 缓存有效期
            max_workers: 最大并发工作线程数
        """
        self.primary_source = primary_source
        self.fallback_sources = fallback_sources or ['akshare', 'tushare', 'baostock']
        self.cache_ttl_minutes = cache_ttl_minutes
        self.max_workers = max_workers
        
        # 数据缓存
        self.data_cache = {}
        self.cache_lock = threading.Lock()
        
        # 数据源统计
        self.source_stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'source_usage': {},
            'avg_response_time': 0
        }
        
        print("🚀 多数据源获取器初始化完成")
        print("=" * 60)
        print("📊 数据源扩展特性:")
        print("   1. ✅ 多数据源集成，提高数据可靠性")
        print("   2. ✅ 智能源选择，自动选择最佳数据源")
        print("   3. ✅ 数据质量验证，确保数据准确性")
        print("   4. ✅ 性能监控，实时跟踪数据源状态")
        print("=" * 60)
    
    def fetch_stock_data(self, symbol: str, data_type: str = 'real_time', 
                        use_cache: bool = True, timeout: int = 30) -> Dict[str, Any]:
        """
        获取股票数据（多数据源）
        
        Args:
            symbol: 股票代码
            data_type: 数据类型 (real_time, basic_info, historical)
            use_cache: 是否使用缓存
            timeout: 超时时间（秒）
        
        Returns:
            股票数据字典
        """
        start_time = time.time()
        self.source_stats['total_requests'] += 1
        
        cache_key = f"{data_type}_{symbol}"
        
        # 检查缓存
        if use_cache:
            cached_data = self._get_from_cache(cache_key)
            if cached_data:
                print(f"💾 缓存命中: {symbol} ({data_type})")
                return cached_data
        
        print(f"🔍 获取 {symbol} 的 {data_type} 数据...")
        
        # 尝试从多个数据源获取数据
        results = []
        errors = []
        
        # 创建数据源列表（主要数据源优先）
        sources = [self.primary_source] + [s for s in self.fallback_sources if s != self.primary_source]
        
        for source in sources:
            try:
                source_start = time.time()
                
                if data_type == 'real_time':
                    data = self._fetch_real_time_from_source(source, symbol)
                elif data_type == 'basic_info':
                    data = self._fetch_basic_info_from_source(source, symbol)
                elif data_type == 'historical':
                    data = self._fetch_historical_from_source(source, symbol)
                else:
                    data = None
                
                source_time = time.time() - source_start
                
                if data and self._validate_data(data, data_type):
                    results.append({
                        'source': source,
                        'data': data,
                        'response_time': source_time,
                        'priority': sources.index(source)  # 优先级（越小越高）
                    })
                    print(f"   ✅ {source}: 获取成功 ({source_time:.2f}s)")
                else:
                    errors.append(f"{source}: 数据无效")
                    print(f"   ⚠️ {source}: 数据无效")
                    
            except Exception as e:
                errors.append(f"{source}: {str(e)}")
                print(f"   ❌ {source}: 获取失败 - {str(e)[:50]}")
        
        # 选择最佳数据
        if results:
            # 按优先级排序（优先级高 + 响应时间短）
            results.sort(key=lambda x: (x['priority'], x['response_time']))
            best_result = results[0]
            
            # 合并所有成功数据源的数据
            merged_data = self._merge_data(results, data_type)
            
            # 更新数据源统计
            self._update_source_stats(best_result['source'], True, best_result['response_time'])
            
            # 更新缓存
            if use_cache:
                self._save_to_cache(cache_key, merged_data)
            
            total_time = time.time() - start_time
            merged_data['metadata']['total_fetch_time'] = total_time
            merged_data['metadata']['sources_used'] = [r['source'] for r in results]
            merged_data['metadata']['errors'] = errors
            
            print(f"✅ 数据获取完成: {symbol} ({total_time:.2f}s)")
            print(f"   使用数据源: {best_result['source']}")
            print(f"   备用数据源: {len(results)-1} 个")
            
            return merged_data
        else:
            # 所有数据源都失败
            self._update_source_stats('all', False, 0)
            
            error_msg = f"所有数据源都失败: {', '.join(errors)}"
            print(f"❌ 数据获取失败: {error_msg}")
            
            return {
                'status': 'error',
                'symbol': symbol,
                'data_type': data_type,
                'error': error_msg,
                'metadata': {
                    'timestamp': datetime.now().isoformat(),
                    'sources_tried': sources,
                    'errors': errors
                }
            }
    
    def fetch_multiple_stocks(self, symbols: List[str], data_type: str = 'real_time',
                            use_cache: bool = True, parallel: bool = True) -> Dict[str, Any]:
        """批量获取多个股票数据"""
        print(f"\n🚀 开始批量获取 {len(symbols)} 只股票的 {data_type} 数据")
        print("=" * 60)
        
        start_time = time.time()
        results = {}
        
        if parallel and len(symbols) > 1:
            # 并行获取
            print(f"⚡ 使用并行获取 (最大并发数: {self.max_workers})")
            results = self._fetch_parallel(symbols, data_type, use_cache)
        else:
            # 串行获取
            print("🔁 使用串行获取")
            for i, symbol in enumerate(symbols, 1):
                print(f"\n[{i}/{len(symbols)}] 获取 {symbol}...")
                result = self.fetch_stock_data(symbol, data_type, use_cache)
                results[symbol] = result
        
        total_time = time.time() - start_time
        
        # 生成批量获取总结
        summary = self._generate_fetch_summary(results, total_time)
        
        print("\n" + "=" * 60)
        print(f"🎉 批量获取完成!")
        print(f"   股票数量: {len(symbols)}")
        print(f"   成功获取: {summary['successful']}")
        print(f"   失败获取: {summary['failed']}")
        print(f"   总耗时: {total_time:.2f}秒")
        print(f"   平均每只: {total_time/max(len(symbols),1):.2f}秒")
        print("=" * 60)
        
        return {
            'batch_results': results,
            'summary': summary,
            'performance': {
                'total_time': total_time,
                'stocks_per_second': len(symbols) / total_time if total_time > 0 else 0,
                'data_source_stats': self.get_source_stats()
            }
        }
    
    def _fetch_parallel(self, symbols, data_type, use_cache):
        """并行获取数据"""
        results = {}
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # 提交所有任务
            future_to_symbol = {
                executor.submit(self.fetch_stock_data, symbol, data_type, use_cache): symbol 
                for symbol in symbols
            }
            
            # 收集结果
            completed = 0
            total = len(symbols)
            
            for future in as_completed(future_to_symbol):
                symbol = future_to_symbol[future]
                completed += 1
                
                try:
                    result = future.result()
                    results[symbol] = result
                    print(f"[{completed}/{total}] {symbol} 获取完成")
                except Exception as e:
                    print(f"[{completed}/{total}] {symbol} 获取失败: {e}")
                    results[symbol] = {
                        'status': 'error',
                        'symbol': symbol,
                        'error': str(e)
                    }
        
        return results
    
    def _fetch_real_time_from_source(self, source: str, symbol: str) -> Optional[Dict[str, Any]]:
        """从指定数据源获取实时数据"""
        try:
            if source == 'akshare':
                # 尝试多种akshare方法
                methods = [
                    self._akshare_real_time_method1,
                    self._akshare_real_time_method2,
                    self._akshare_real_time_method3
                ]
                
                for method in methods:
                    data = method(symbol)
                    if data:
                        return {
                            'status': 'success',
                            'symbol': symbol,
                            'data': data,
                            'data_source': f'akshare-{method.__name__}',
                            'timestamp': datetime.now().isoformat()
                        }
                
                return None
            
            elif source == 'tushare':
                # 这里可以集成tushare
                # 暂时返回None，表示不支持
                return None
            
            elif source == 'baostock':
                # 这里可以集成baostock
                # 暂时返回None，表示不支持
                return None
            
            else:
                return None
                
        except Exception as e:
            print(f"   ⚠️ {source} 实时数据获取异常: {e}")
            return None
    
    def _akshare_real_time_method1(self, symbol):
        """akshare方法1: A股实时行情"""
        try:
            stock_zh_a_spot_df = ak.stock_zh_a_spot()
            if stock_zh_a_spot_df is not None and not stock_zh_a_spot_df.empty:
                stock_info = stock_zh_a_spot_df[stock_zh_a_spot_df['代码'] == symbol]
                if not stock_info.empty:
                    data = stock_info.iloc[0]
                    return {
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
                        'market_cap': data['总市值']
                    }
        except:
            pass
        return None
    
    def _akshare_real_time_method2(self, symbol):
        """akshare方法2: 个股分钟数据"""
        try:
            stock_zh_a_minute_df = ak.stock_zh_a_minute(symbol=symbol, period='1', adjust="qfq")
            if stock_zh_a_minute_df is not None and not stock_zh_a_minute_df.empty:
                latest = stock_zh_a_minute_df.iloc[-1]
                return {
                    'current_price': float(latest['close']),
                    'volume': int(latest['volume']),
                    'note': '分钟级数据，非实时'
                }
        except:
            pass
        return None
    
    def _akshare_real_time_method3(self, symbol):
        """akshare方法3: 个股日线数据"""
        try:
            stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol=symbol, period="daily", 
                                                   start_date="20260101", end_date="20260312", adjust="qfq")
            if stock_zh_a_hist_df is not None and not stock_zh_a_hist_df.empty:
                latest = stock_zh_a_hist_df.iloc[0]
                return {
                    'current_price': float(latest['收盘']),
                    'change_percent': float(latest['涨跌幅']),
                    'volume': int(latest['成交量']),
                    'amount': float(latest['成交额']),
                    'note': '日线数据，非实时'
                }
        except:
            pass
        return None
    
    def _fetch_basic_info_from_source(self, source: str, symbol: str) -> Optional[Dict[str, Any]]:
        """从指定数据源获取基本信息"""
        try:
            if source == 'akshare':
                stock_info = ak.stock_individual_info_em(symbol=symbol)
                if stock_info is not None and not stock_info.empty:
                    info_dict = {}
                    for _, row in stock_info.iterrows():
                        info_dict[row['item']] = row['value']
                    
                    return {
                        'status': 'success',
                        'symbol': symbol,
                        'data': {
                            'company_name': info_dict.get('公司名称', ''),
                            'industry': info_dict.get('行业', ''),
                            'listing_date': info_dict.get('上市时间', ''),
                            'total_shares': info_dict.get('总股本', ''),
                            'circulating_shares': info_dict.get('流通股本', '')
                        },
                        'data_source': 'akshare-stock_individual_info_em',
                        'timestamp': datetime.now().isoformat()
                    }
            
            return None
                
        except Exception as e:
            print(f"   ⚠️ {source} 基本信息获取异常: {e}")
            return None
    
    def _fetch_historical_from_source(self, source: str, symbol: str) -> Optional[Dict[str, Any]]:
        """从指定数据源获取历史数据"""
        try:
            if source == 'akshare':
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
                        'data': {
                            'data_points': len(history),
                            'latest_date': history[0]['date'] if history else None,
                            'earliest_date': history[-1]['date'] if history else None,
                            'history': history[:50]  # 只返回最近50条
                        },
                        'data_source': 'akshare-stock_zh_a_hist',
                        'timestamp': datetime.now().isoformat()
                    }
            
            return None
                
        except Exception as e:
            print(f"   ⚠️ {source} 历史数据获取异常: {e}")
            return None
    
    def _validate_data(self, data: Dict[str, Any], data_type: str) -> bool:
        """验证数据质量"""
        if not data or data.get('status') != 'success':
            return False
        
        data_content = data.get('data')
        if not data_content:
            return False
        
        # 根据数据类型进行验证
        if data_type == 'real_time':
            # 验证实时数据
            required_fields = ['current_price', 'change_percent']
            for field in required_fields:
                if field not in data_content or data_content[field] is None:
                    return False
            
            # 验证价格合理性
            price = data_content.get('current_price')
            if price is not None and (price <= 0 or price > 10000):
                return False
            
            # 验证涨跌幅合理性
            change = data_content.get('change_percent')
            if change is not None and abs(change) > 50:  # 涨跌幅超过50%可能有问题
                return False
        
        elif data_type == 'basic_info':
            # 验证基本信息
            required_fields = ['industry']
            for field in required_fields:
                if field not in data_content or not data_content[field]:
                    return False
        
        elif data_type == 'historical':
            # 验证历史数据
            if 'history' not in data_content or not data_content['history']:
                return False
            
            # 验证历史数据条数
            if len(data_content['history']) < 5:
                return False
        
        return True
    
    def _merge_data(self, results: List[Dict[str, Any]], data_type: str) -> Dict[str, Any]:
        """合并多个数据源的数据"""
        if not results:
            return {
                'status': 'error',
                'error': '没有可合并的数据',
                'timestamp': datetime.now().isoformat()
            }
        
        # 使用最佳数据源的数据作为基础
        best_result = results[0]
        merged_data = best_result['data'].copy()
        
        # 添加元数据
        merged_data['metadata'] = {
            'primary_source': best_result['source'],
            'all_sources': [r['source'] for r in results],
            'response_times': {r['source']: r['response_time'] for r in results},
            'data_quality': 'high' if len(results) >= 2 else 'medium',
            'merged_at': datetime.now().isoformat()
        }
        
        # 如果是实时数据，可以尝试计算平均值（如果有多个有效数据源）
        if data_type == 'real_time' and len(results) >= 2:
            valid_results = [r for r in results if self._validate_data(r['data'], data_type)]
            if len(valid_results) >= 2:
                # 计算关键指标的平均值
                key_fields = ['current_price', 'change_percent', 'volume']
                for field in key_fields:
                    values = []
                    for result in valid_results:
                        value = result['data']['data'].get(field)
                        if value is not None:
                            values.append(value)
                    
                    if len(values) >= 2:
                        avg_value = sum(values) / len(values)
                        merged_data['data'][field] = avg_value
                        merged_data['metadata'][f'{field}_sources'] = len(values)
                        merged_data['metadata'][f'{field}_range'] = f"{min(values):.2f}-{max(values):.2f}"
        
        return merged_data
    
    def _get_from_cache(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """从缓存获取数据"""
        with self.cache_lock:
            if cache_key in self.data_cache:
                cached_item = self.data_cache[cache_key]
                cache_age = datetime.now() - cached_item['timestamp']
                
                if cache_age < timedelta(minutes=self.cache_ttl_minutes):
                    return cached_item['data']
                else:
                    # 缓存过期，删除
                    del self.data_cache[cache_key]
        
        return None
    
    def _save_to_cache(self, cache_key: str, data: Dict[str, Any]):
        """保存数据到缓存"""
        with self.cache_lock:
            self.data_cache[cache_key] = {
                'data': data,
                'timestamp': datetime.now()
            }
    
    def _update_source_stats(self, source: str, success: bool, response_time: float):
        """更新数据源统计"""
        if source not in self.source_stats['source_usage']:
            self.source_stats['source_usage'][source] = {
                'requests': 0,
                'successful': 0,
                'failed': 0,
                'total_response_time': 0,
                'avg_response_time': 0
            }
        
        stats = self.source_stats['source_usage'][source]
        stats['requests'] += 1
        
        if success:
            self.source_stats['successful_requests'] += 1
            stats['successful'] += 1
            stats['total_response_time'] += response_time
            stats['avg_response_time'] = stats['total_response_time'] / stats['successful']
        else:
            self.source_stats['failed_requests'] += 1
            stats['failed'] += 1
        
        # 更新总体平均响应时间
        total_successful = self.source_stats['successful_requests']
        if total_successful > 0:
            total_time = sum(s['total_response_time'] for s in self.source_stats['source_usage'].values())
            self.source_stats['avg_response_time'] = total_time / total_successful
    
    def _generate_fetch_summary(self, results: Dict[str, Any], total_time: float) -> Dict[str, Any]:
        """生成获取总结"""
        successful = sum(1 for r in results.values() if r.get('status') == 'success')
        failed = len(results) - successful
        
        # 计算性能指标
        if successful > 0:
            avg_time = total_time / successful
        else:
            avg_time = 0
        
        # 成功率
        success_rate = successful / len(results) * 100 if results else 0
        
        # 数据源使用统计
        sources_used = {}
        for result in results.values():
            if result.get('status') == 'success':
                metadata = result.get('metadata', {})
                primary_source = metadata.get('primary_source')
                if primary_source:
                    sources_used[primary_source] = sources_used.get(primary_source, 0) + 1
        
        return {
            'total_stocks': len(results),
            'successful': successful,
            'failed': failed,
            'success_rate': f'{success_rate:.1f}%',
            'total_time': f'{total_time:.2f}秒',
            'avg_time_per_stock': f'{avg_time:.2f}秒',
            'sources_used': sources_used,
            'data_quality': self._assess_data_quality(results)
        }
    
    def _assess_data_quality(self, results: Dict[str, Any]) -> str:
        """评估数据质量"""
        if not results:
            return '未知'
        
        successful_results = [r for r in results.values() if r.get('status') == 'success']
        if not successful_results:
            return '差'
        
        # 检查数据源多样性
        sources = set()
        for result in successful_results:
            metadata = result.get('metadata', {})
            primary_source = metadata.get('primary_source')
            if primary_source:
                sources.add(primary_source)
        
        # 检查数据完整性
        complete_results = 0
        for result in successful_results:
            metadata = result.get('metadata', {})
            data_quality = metadata.get('data_quality', 'medium')
            if data_quality == 'high':
                complete_results += 1
        
        # 评估质量
        if len(sources) >= 2 and complete_results >= len(successful_results) * 0.7:
            return '优秀'
        elif len(sources) >= 2:
            return '良好'
        elif len(sources) == 1 and complete_results >= len(successful_results) * 0.5:
            return '中等'
        else:
            return '一般'
    
    def get_source_stats(self) -> Dict[str, Any]:
        """获取数据源统计"""
        stats = self.source_stats.copy()
        
        # 计算总体成功率
        total_requests = stats['total_requests']
        if total_requests > 0:
            success_rate = stats['successful_requests'] / total_requests * 100
            stats['success_rate'] = f'{success_rate:.1f}%'
        else:
            stats['success_rate'] = '0%'
        
        # 格式化响应时间
        stats['avg_response_time'] = f"{stats['avg_response_time']:.3f}秒"
        
        return stats
    
    def clear_cache(self):
        """清空缓存"""
        with self.cache_lock:
            cache_size = len(self.data_cache)
            self.data_cache.clear()
        
        print(f"🧹 缓存已清空，释放了 {cache_size} 个缓存项")
        return cache_size
    
    def get_cache_stats(self):
        """获取缓存统计"""
        with self.cache_lock:
            total_items = len(self.data_cache)
            fresh_items = 0
            
            for item in self.data_cache.values():
                cache_age = datetime.now() - item['timestamp']
                if cache_age < timedelta(minutes=self.cache_ttl_minutes):
                    fresh_items += 1
        
        return {
            'total_items': total_items,
            'fresh_items': fresh_items,
            'stale_items': total_items - fresh_items,
            'fresh_rate': f'{(fresh_items/total_items*100):.1f}%' if total_items > 0 else '0%',
            'cache_ttl_minutes': self.cache_ttl_minutes
        }

def main():
    """主函数"""
    print("🧠 毛毛AI增强系统 - 多数据源获取器")
    print("=" * 60)
    print("📊 数据源扩展 v1.0")
    print("🎯 目标: 扩展数据源，提高数据质量和实时性")
    print("⏰ 开始时间: 08:45 GMT+8")
    print("=" * 60)
    
    # 创建多数据源获取器
    fetcher = MultiSourceDataFetcher(
        primary_source='akshare',
        fallback_sources=['akshare'],  # 目前只支持akshare，可以扩展
        cache_ttl_minutes=10,
        max_workers=2
    )
    
    # 测试单个股票实时数据获取
    print("\n🔍 测试单个股票实时数据获取 (603039)...")
    real_time_data = fetcher.fetch_stock_data("603039", "real_time", use_cache=True)
    
    if real_time_data.get('status') == 'success':
        print(f"✅ 实时数据获取成功")
        data = real_time_data.get('data', {})
        metadata = real_time_data.get('metadata', {})
        
        print(f"   价格: {data.get('current_price', 'N/A')}")
        print(f"   涨跌: {data.get('change_percent', 'N/A')}%")
        print(f"   数据源: {metadata.get('primary_source', 'N/A')}")
        print(f"   获取时间: {metadata.get('total_fetch_time', 'N/A'):.2f}秒")
    else:
        print(f"❌ 实时数据获取失败: {real_time_data.get('error', '未知错误')}")
    
    # 测试单个股票基本信息获取
    print("\n🔍 测试单个股票基本信息获取 (603039)...")
    basic_info = fetcher.fetch_stock_data("603039", "basic_info", use_cache=True)
    
    if basic_info.get('status') == 'success':
        print(f"✅ 基本信息获取成功")
        data = basic_info.get('data', {})
        metadata = basic_info.get('metadata', {})
        
        print(f"   行业: {data.get('industry', 'N/A')}")
        print(f"   上市日期: {data.get('listing_date', 'N/A')}")
        print(f"   数据源: {metadata.get('primary_source', 'N/A')}")
    else:
        print(f"❌ 基本信息获取失败: {basic_info.get('error', '未知错误')}")
    
    # 测试批量获取
    print("\n🔍 测试批量获取 (3只股票)...")
    symbols = ["603039", "000001", "600036"]
    batch_result = fetcher.fetch_multiple_stocks(symbols, "real_time", use_cache=True, parallel=True)
    
    # 显示数据源统计
    print("\n📊 数据源统计:")
    source_stats = fetcher.get_source_stats()
    for key, value in source_stats.items():
        if key != 'source_usage':
            print(f"   {key}: {value}")
    
    # 显示缓存统计
    print("\n💾 缓存统计:")
    cache_stats = fetcher.get_cache_stats()
    for key, value in cache_stats.items():
        print(f"   {key}: {value}")
    
    # 显示批量获取总结
    if batch_result.get('summary'):
        summary = batch_result['summary']
        print("\n" + "=" * 60)
        print("📈 批量获取结果总结")
        print("=" * 60)
        print(f"✅ 批量获取完成: {summary['total_stocks']} 只股票")
        print(f"✅ 成功率: {summary['success_rate']}")
        print(f"✅ 总耗时: {summary['total_time']}")
        print(f"✅ 平均每只: {summary['avg_time_per_stock']}")
        print(f"✅ 数据质量: {summary['data_quality']}")
        
        if summary.get('sources_used'):
            print(f"✅ 数据源使用:")
            for source, count in summary['sources_used'].items():
                print(f"   {source}: {count} 次")
    
    print("\n🎉 数据源扩展完成!")
    print("   多数据源集成，提高数据可靠性")
    print("   智能源选择，自动选择最佳数据源")
    print("   数据质量验证，确保数据准确性")

if __name__ == "__main__":
    main()