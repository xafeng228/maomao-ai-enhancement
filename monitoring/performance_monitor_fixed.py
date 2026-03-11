#!/usr/bin/env python3
"""
性能监控和优化系统 - 简化版本
"""

import time
import json
from datetime import datetime, timedelta
from pathlib import Path
import logging

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('performance_monitor.log')
    ]
)
logger = logging.getLogger(__name__)

class SimplePerformanceMonitor:
    """简化性能监控器"""
    
    def __init__(self):
        self.metrics_dir = Path("metrics")
        self.metrics_dir.mkdir(exist_ok=True)
        
        # 性能阈值
        self.thresholds = {
            'cpu': 80.0,
            'memory': 85.0,
            'disk': 90.0,
        }
        
        logger.info("简化性能监控器初始化完成")
    
    def collect_metrics(self):
        """收集性能指标"""
        try:
            import psutil
            
            metrics = {
                'timestamp': datetime.now().isoformat(),
                'system': {
                    'name': '毛毛AI增强系统',
                    'version': '2.1.0',
                },
                
                # CPU指标
                'cpu': {
                    'percent': psutil.cpu_percent(interval=1),
                    'count': psutil.cpu_count(),
                },
                
                # 内存指标
                'memory': {
                    'percent': psutil.virtual_memory().percent,
                    'used_gb': round(psutil.virtual_memory().used / (1024**3), 2),
                    'available_gb': round(psutil.virtual_memory().available / (1024**3), 2),
                },
                
                # 磁盘指标
                'disk': {
                    'percent': psutil.disk_usage('/').percent,
                    'used_gb': round(psutil.disk_usage('/').used / (1024**3), 2),
                    'free_gb': round(psutil.disk_usage('/').free / (1024**3), 2),
                },
                
                # 状态
                'status': 'normal',
            }
            
            # 检查阈值
            if metrics['cpu']['percent'] > self.thresholds['cpu']:
                metrics['status'] = 'warning'
                logger.warning(f"CPU使用率过高: {metrics['cpu']['percent']}%")
            elif metrics['memory']['percent'] > self.thresholds['memory']:
                metrics['status'] = 'warning'
                logger.warning(f"内存使用率过高: {metrics['memory']['percent']}%")
            elif metrics['disk']['percent'] > self.thresholds['disk']:
                metrics['status'] = 'warning'
                logger.warning(f"磁盘使用率过高: {metrics['disk']['percent']}%")
            
            return metrics
            
        except ImportError:
            # 如果没有psutil，返回模拟数据
            logger.warning("psutil未安装，使用模拟数据")
            return {
                'timestamp': datetime.now().isoformat(),
                'system': {'name': '毛毛AI增强系统', 'version': '2.1.0'},
                'cpu': {'percent': 25.5, 'count': 4},
                'memory': {'percent': 45.2, 'used_gb': 2.1, 'available_gb': 8.5},
                'disk': {'percent': 65.8, 'used_gb': 32.5, 'free_gb': 45.2},
                'status': 'normal',
                'note': '模拟数据',
            }
    
    def save_metrics(self, metrics):
        """保存性能指标"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        metrics_file = self.metrics_dir / f"performance_metrics_{timestamp}.json"
        
        with open(metrics_file, 'w', encoding='utf-8') as f:
            json.dump(metrics, f, indent=2, ensure_ascii=False)
        
        logger.info(f"性能指标保存完成: {metrics_file}")
        
        return metrics_file
    
    def generate_report(self):
        """生成简单报告"""
        # 收集最近的文件
        metrics_files = list(self.metrics_dir.glob("performance_metrics_*.json"))
        if not metrics_files:
            logger.warning("无性能指标数据")
            return None
        
        # 读取最新文件
        latest_file = max(metrics_files, key=lambda p: p.stat().st_mtime)
        with open(latest_file, 'r', encoding='utf-8') as f:
            metrics = json.load(f)
        
        # 生成报告
        report = {
            'report_time': datetime.now().isoformat(),
            'latest_metrics': metrics,
            'summary': {
                'cpu_status': '正常' if metrics['cpu']['percent'] < 70 else '注意' if metrics['cpu']['percent'] < 85 else '警告',
                'memory_status': '正常' if metrics['memory']['percent'] < 70 else '注意' if metrics['memory']['percent'] < 85 else '警告',
                'disk_status': '正常' if metrics['disk']['percent'] < 70 else '注意' if metrics['disk']['percent'] < 85 else '警告',
                'overall_status': metrics['status'],
            },
            'recommendations': self._generate_recommendations(metrics),
        }
        
        # 保存报告
        report_file = self.metrics_dir / f"performance_report_{datetime.now().strftime('%Y%m%d_%H