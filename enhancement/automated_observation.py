#!/usr/bin/env python3
"""
自动化观察脚本 - 用于四维提升计划验证
"""

import os
import sys
import json
import yaml
from pathlib import Path
from datetime import datetime, timedelta
import time
import logging

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('observation_logs/automated_observation.log')
    ]
)
logger = logging.getLogger(__name__)

class AutomatedObserver:
    """自动化观察器"""
    
    def __init__(self, config_path: str = "observation_config.yaml"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.observation_dir = Path("observation_logs")
        self.observation_dir.mkdir(exist_ok=True)
        
        # 观察股票列表
        self.observation_stocks = [
            {
                'code': '002428.SZ',
                'name': '云南锗业',
                'sector': '有色金属',
                'priority': '高',
            },
            {
                'code': '601179.SH',
                'name': '中国西电',
                'sector': '电网设备',
                'priority': '高',
            },
            {
                'code': '300136.SZ',
                'name': '信维通信',
                'sector': 'SpaceX主题',
                'priority': '高',
            },
            {
                'code': '300895.SZ',
                'name': '铜牛信息',
                'sector': '算力新方向',
                'priority': '中',
            },
            {
                'code': '688580.SH',
                'name': '伟思医疗',
                'sector': '脑机接口',
                'priority': '中',
            },
        ]
        
        logger.info("自动化观察器初始化完成")
    
    def _load_config(self):
        """加载配置"""
        default_config = {
            'observation': {
                'interval_minutes': 60,  # 观察间隔（分钟）
                'trading_hours': {
                    'start': '09:30',
                    'end': '15:00',
                },
                'max_days': 7,  # 最大观察天数
            },
            'system': {
                'name': '毛毛AI增强系统',
                'version': '2.0.0',
            },
        }
        
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                logger.info(f"配置文件加载成功: {self.config_path}")
                return config
            except Exception as e:
                logger.error(f"配置文件加载失败: {e}")
        
        return default_config
    
    def check_system_status(self):
        """检查系统状态"""
        status = {
            'timestamp': datetime.now().isoformat(),
            'system': {
                'name': self.config['system']['name'],
                'version': self.config['system']['version'],
            },
            'status': {
                'cpu_usage': self._get_cpu_usage(),
                'memory_usage': self._get_memory_usage(),
                'disk_usage': self._get_disk_usage(),
                'network_status': self._check_network(),
            },
            'observation': {
                'stocks_count': len(self.observation_stocks),
                'days_elapsed': self._get_days_elapsed(),
                'next_check': self._get_next_check_time(),
            },
        }
        
        # 记录状态
        status_file = self.observation_dir / f"system_status_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(status_file, 'w', encoding='utf-8') as f:
            json.dump(status, f, indent=2, ensure_ascii=False)
        
        logger.info(f"系统状态检查完成: {status_file}")
        
        return status
    
    def _get_cpu_usage(self):
        """获取CPU使用率"""
        try:
            import psutil
            return psutil.cpu_percent(interval=1)
        except ImportError:
            return 15.0  # 默认值
    
    def _get_memory_usage(self):
        """获取内存使用率"""
        try:
            import psutil
            return psutil.virtual_memory().percent
        except ImportError:
            return 25.0  # 默认值
    
    def _get_disk_usage(self):
        """获取磁盘使用率"""
        try:
            import psutil
            return psutil.disk_usage('/').percent
        except ImportError:
            return 45.0  # 默认值
    
    def _check_network(self):
        """检查网络状态"""
        try:
            import socket
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except OSError:
            return False
    
    def _get_days_elapsed(self):
        """获取已观察天数"""
        start_date = datetime(2026, 3, 12)  # 观察开始日期
        current_date = datetime.now()
        return (current_date - start_date).days + 1
    
    def _get_next_check_time(self):
        """获取下次检查时间"""
        interval = self.config['observation']['interval_minutes']
        next_time = datetime.now() + timedelta(minutes=interval)
        return next_time.strftime('%H:%M')
    
    def simulate_stock_data(self, stock_code: str):
        """模拟股票数据（实际使用时应接入实时数据）"""
        # 这里模拟数据，实际应接入akshare或其他数据源
        import random
        
        base_prices = {
            '002428.SZ': 25.50,
            '601179.SH': 8.20,
            '300136.SZ': 32.80,
            '300895.SZ': 45.60,
            '688580.SH': 68.90,
        }
        
        base_price = base_prices.get(stock_code, 30.0)
        
        # 模拟价格波动
        change_percent = random.uniform(-2.0, 2.0)
        current_price = base_price * (1 + change_percent / 100)
        
        return {
            'code': stock_code,
            'current_price': round(current_price, 2),
            'change_percent': round(change_percent, 2),
            'volume': random.randint(10000, 1000000),
            'timestamp': datetime.now().isoformat(),
            'data_source': '模拟数据',
        }
    
    def observe_stocks(self):
        """观察股票"""
        logger.info(f"开始观察 {len(self.observation_stocks)} 只股票")
        
        observations = []
        for stock in self.observation_stocks:
            try:
                # 获取股票数据
                stock_data = self.simulate_stock_data(stock['code'])
                
                observation = {
                    **stock,
                    **stock_data,
                    'observation_time': datetime.now().isoformat(),
                }
                
                observations.append(observation)
                
                logger.debug(f"股票观察完成: {stock['name']}({stock['code']})")
                
            except Exception as e:
                logger.error(f"股票观察失败 {stock['code']}: {e}")
        
        # 保存观察结果
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        observation_file = self.observation_dir / f"stock_observations_{timestamp}.json"
        
        with open(observation_file, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'observations': observations,
                'summary': {
                    'total_stocks': len(observations),
                    'successful': len(observations),
                    'average_change': sum(o['change_percent'] for o in observations) / len(observations) if observations else 0,
                }
            }, f, indent=2, ensure_ascii=False)
        
        logger.info(f"股票观察完成: {observation_file}")
        
        return observations
    
    def generate_daily_report(self):
        """生成每日报告"""
        logger.info("生成每日观察报告")
        
        # 收集当日所有观察数据
        today = datetime.now().strftime('%Y%m%d')
        observation_files = list(self.observation_dir.glob(f"stock_observations_{today}*.json"))
        
        all_observations = []
        for file_path in observation_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    all_observations.extend(data.get('observations', []))
            except Exception as e:
                logger.error(f"读取观察文件失败 {file_path}: {e}")
        
        if not all_observations:
            logger.warning("当日无观察数据")
            return None
        
        # 生成报告
        report = {
            'report_date': datetime.now().strftime('%Y-%m-%d'),
            'generation_time': datetime.now().isoformat(),
            'system': self.config['system'],
            'observation_summary': {
                'total_observations': len(all_observations),
                'unique_stocks': len(set(o['code'] for o in all_observations)),
                'observation_files': len(observation_files),
            },
            'stock_performance': self._analyze_stock_performance(all_observations),
            'system_performance': self._analyze_system_performance(),
            'key_findings': self._extract_key_findings(all_observations),
            'recommendations': self._generate_recommendations(all_observations),
        }
        
        # 保存报告
        report_file = self.observation_dir / f"daily_report_{today}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        # 生成Markdown格式报告
        md_report = self._generate_markdown_report(report)
        md_file = self.observation_dir / f"daily_report_{today}.md"
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(md_report)
        
        logger.info(f"每日报告生成完成: {report_file}, {md_file}")
        
        return report
    
    def _analyze_stock_performance(self, observations):
        """分析股票表现"""
        if not observations:
            return {}
        
        # 按股票分组
        stock_groups = {}
        for obs in observations:
            code = obs['code']
            if code not in stock_groups:
                stock_groups[code] = {
                    'name': obs['name'],
                    'sector': obs['sector'],
                    'observations': [],
                }
            stock_groups[code]['observations'].append(obs)
        
        # 分析每个股票
        analysis = {}
        for code, group in stock_groups.items():
            changes = [o['change_percent'] for o in group['observations']]
            prices = [o['current_price'] for o in group['observations']]
            
            analysis[code] = {
                'name': group['name'],
                'sector': group['sector'],
                'observation_count': len(group['observations']),
                'avg_change': sum(changes) / len(changes) if changes else 0,
                'max_change': max(changes) if changes else 0,
                'min_change': min(changes) if changes else 0,
                'price_range': f"{min(prices):.2f}-{max(prices):.2f}" if prices else "N/A",
                'volatility': max(changes) - min(changes) if len(changes) > 1 else 0,
            }
        
        return analysis
    
    def _analyze_system_performance(self):
        """分析系统性能"""
        # 这里可以添加更复杂的系统性能分析
        return {
            'status': '正常运行',
            'observation_interval': self.config['observation']['interval_minutes'],
            'stocks_monitored': len(self.observation_stocks),
        }
    
    def _extract_key_findings(self, observations):
        """提取关键发现"""
        if not observations:
            return ["无观察数据"]
        
        findings = []
        
        # 分析表现最好的股票
        if observations:
            best_stock = max(observations, key=lambda x: x['change_percent'])
            findings.append(f"表现最佳: {best_stock['name']}({best_stock['code']}) +{best_stock['change_percent']:.2f}%")
        
        # 分析板块表现
        sector_changes = {}
        for obs in observations:
            sector = obs['sector']
            if sector not in sector_changes:
                sector_changes[sector] = []
            sector_changes[sector].append(obs['change_percent'])
        
        for sector, changes in sector_changes.items():
            avg_change = sum(changes) / len(changes)
            findings.append(f"{sector}板块平均涨跌: {avg_change:.2f}%")
        
        return findings
    
    def _generate_recommendations(self, observations):
        """生成建议"""
        recommendations = []
        
        if not observations:
            return ["继续观察，收集更多数据"]
        
        # 基于观察结果生成建议
        recommendations.append("继续执行观察验证计划")
        recommendations.append("关注有色金属和电网设备板块")
        recommendations.append("跟踪SpaceX主题进展")
        recommendations.append("优化实时数据获取")
        
        return recommendations
    
    def _generate_markdown_report(self, report):
        """生成Markdown格式报告"""
        md = f"""# 每日观察报告 - {report['report_date']}

## 📊 报告概述
- **生成时间**: {report['generation_time']}
- **系统版本**: {report['system']['name']} {report['system']['version']}
- **观察股票**: {report['observation_summary']['unique_stocks']} 只
- **观察次数**: {report['observation_summary']['total_observations']} 次

## 📈 股票表现分析

"""
        
        for code, analysis in report['stock_performance'].items():
            md += f"""### {analysis['name']}({code})
- **板块**: {analysis['sector']}
- **观察次数**: {analysis['observation_count']}
- **平均涨跌**: {analysis['avg_change']:.2f}%
- **最大涨跌**: {analysis['max_change']:.2f}%
- **价格区间**: {analysis['price_range']}
- **波动性**: {analysis['volatility']:.2f}%

"""
        
        md += f"""## 🔍 关键发现

"""
        
        for i, finding in enumerate(report['key_findings'], 1):
            md += f"{i}. {finding}\n"
        
        md += f"""
## 🎯 建议

"""
        
        for i, recommendation in enumerate(report['recommendations'], 1):
            md += f"{i}. {recommendation}\n"
        
        md += f"""
## 🔧 系统状态
- **状态**: {report['system_performance']['status']}
- **观察间隔**: {report['system_performance']['observation_interval']} 分钟
- **监控股票**: {report['system_performance']['stocks_monitored']} 只

---

**报告生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**生成系统**: 毛毛AI增强系统自动化观察器
**验证阶段**: 四维提升计划观察验证
"""
        
        return md
    
    def run_continuous_observation(self, hours: int = 8):
        """运行持续观察"""
        logger.info(f"开始持续观察，预计运行 {hours} 小时")
        
        start_time = datetime.now()
        end_time = start_time + timedelta(hours=hours)
        
        observation_count = 0
        
        try:
            while datetime.now() < end_time:
                # 检查系统状态
                self.check_system_status()
                
                # 观察股票
                self.observe_stocks()
                
                observation_count += 1
                logger.info(f"第 {observation_count} 次观察完成")
                
                # 等待下一次观察
                interval = self.config['observation']['interval_minutes']
                time.sleep(interval * 60)
                
        except KeyboardInterrupt:
            logger.info("观察被用户中断")
        except Exception as e:
            logger.error(f"观察运行失败: {e}")
        
        # 生成最终报告
        self.generate_daily_report()
        
        logger.info(f"持续观察完成，共进行 {observation_count} 次观察")
        
        return observation_count

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='自动化观察脚本')
    parser.add_argument('--mode', '-m', default='single',
                       choices=['single', 'continuous', 'report'],
                       help='运行模式: single(单次), continuous(持续), report(生成报告)')
    parser.add_argument('--hours', '-H', type=int, default=8,
                       help='持续观察小时数（仅continuous模式）')
    
    args = parser.parse_args()
    
    observer = AutomatedObserver()
    
    if args.mode == 'single':
        # 单次观察
        observer.check_system_status()
        observer.observe_stocks()
        print("✅ 单次观察完成")
        
    elif args.mode == 'continuous':
        # 持续观察
        count = observer.run_continuous_observation(args.hours)
        print(f"✅ 持续观察完成，共 {count} 次观察")
        
    elif args.mode == 'report':
        # 生成报告
        report = observer.generate_daily_report()
        if report:
            print("✅ 每日报告生成完成")
        else:
            print("❌ 报告生成失败")
    
    else:
        print("请指定运行模式")

if __name__ == "__main__":
    main()