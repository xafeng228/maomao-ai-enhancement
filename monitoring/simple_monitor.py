#!/usr/bin/env python3
"""
简单性能监控器
"""

import json
from datetime import datetime
from pathlib import Path

def collect_metrics():
    """收集性能指标"""
    try:
        import psutil
        
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'system': '毛毛AI增强系统 v2.1.0',
            
            'cpu': {
                'percent': psutil.cpu_percent(interval=1),
                'count': psutil.cpu_count(),
            },
            
            'memory': {
                'percent': psutil.virtual_memory().percent,
                'used_gb': round(psutil.virtual_memory().used / (1024**3), 2),
                'available_gb': round(psutil.virtual_memory().available / (1024**3), 2),
            },
            
            'disk': {
                'percent': psutil.disk_usage('/').percent,
                'used_gb': round(psutil.disk_usage('/').used / (1024**3), 2),
                'free_gb': round(psutil.disk_usage('/').free / (1024**3), 2),
            },
            
            'status': 'normal',
        }
        
        # 检查阈值
        thresholds = {'cpu': 80, 'memory': 85, 'disk': 90}
        if metrics['cpu']['percent'] > thresholds['cpu']:
            metrics['status'] = 'warning'
        elif metrics['memory']['percent'] > thresholds['memory']:
            metrics['status'] = 'warning'
        elif metrics['disk']['percent'] > thresholds['disk']:
            metrics['status'] = 'warning'
        
        return metrics
        
    except ImportError:
        # 模拟数据
        return {
            'timestamp': datetime.now().isoformat(),
            'system': '毛毛AI增强系统 v2.1.0',
            'cpu': {'percent': 25.5, 'count': 4},
            'memory': {'percent': 45.2, 'used_gb': 2.1, 'available_gb': 8.5},
            'disk': {'percent': 65.8, 'used_gb': 32.5, 'free_gb': 45.2},
            'status': 'normal',
            'note': '模拟数据',
        }

def save_metrics(metrics):
    """保存指标"""
    metrics_dir = Path("metrics")
    metrics_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    metrics_file = metrics_dir / f"performance_{timestamp}.json"
    
    with open(metrics_file, 'w', encoding='utf-8') as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)
    
    return metrics_file

def generate_report():
    """生成报告"""
    metrics = collect_metrics()
    
    report = f"""# 性能监控报告

## 📊 系统状态
- **监控时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **系统版本**: {metrics['system']}
- **总体状态**: {metrics['status']}

## 📈 CPU状态
- **使用率**: {metrics['cpu']['percent']}%
- **核心数**: {metrics['cpu']['count']}
- **状态**: {'正常' if metrics['cpu']['percent'] < 70 else '注意' if metrics['cpu']['percent'] < 85 else '警告'}

## 💾 内存状态
- **使用率**: {metrics['memory']['percent']}%
- **已使用**: {metrics['memory']['used_gb']} GB
- **可用**: {metrics['memory']['available_gb']} GB
- **状态**: {'正常' if metrics['memory']['percent'] < 70 else '注意' if metrics['memory']['percent'] < 85 else '警告'}

## 💿 磁盘状态
- **使用率**: {metrics['disk']['percent']}%
- **已使用**: {metrics['disk']['used_gb']} GB
- **可用**: {metrics['disk']['free_gb']} GB
- **状态**: {'正常' if metrics['disk']['percent'] < 70 else '注意' if metrics['disk']['percent'] < 85 else '警告'}

## 🎯 建议

"""
    
    # 生成建议
    if metrics['cpu']['percent'] > 70:
        report += "1. CPU使用率较高，建议优化计算任务\n"
    else:
        report += "1. CPU使用率正常\n"
    
    if metrics['memory']['percent'] > 70:
        report += "2. 内存使用率较高，建议优化内存使用\n"
    else:
        report += "2. 内存使用率正常\n"
    
    if metrics['disk']['percent'] > 70:
        report += "3. 磁盘使用率较高，建议定期清理\n"
    else:
        report += "3. 磁盘使用率正常\n"
    
    if metrics['status'] == 'warning':
        report += "4. ⚠️ 系统需要重点关注\n"
    else:
        report += "4. ✅ 系统运行正常\n"
    
    report += f"""
## 📝 详细信息
```json
{json.dumps(metrics, indent=2, ensure_ascii=False)}
```

---
**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**监控系统**: 毛毛AI增强系统性能监控器
"""
    
    # 保存报告
    report_dir = Path("reports")
    report_dir.mkdir(exist_ok=True)
    
    report_file = report_dir / f"performance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    return report_file, metrics

def main():
    """主函数"""
    print("🔧 毛毛AI增强系统 - 性能监控")
    print("=" * 50)
    
    # 收集指标
    print("📊 收集性能指标...")
    metrics = collect_metrics()
    
    # 保存指标
    metrics_file = save_metrics(metrics)
    print(f"✅ 指标保存: {metrics_file}")
    
    # 生成报告
    print("📄 生成性能报告...")
    report_file, metrics = generate_report()
    print(f"✅ 报告生成: {report_file}")
    
    # 显示摘要
    print("\n📋 性能摘要:")
    print(f"   系统状态: {metrics['status']}")
    print(f"   CPU使用率: {metrics['cpu']['percent']}%")
    print(f"   内存使用率: {metrics['memory']['percent']}%")
    print(f"   磁盘使用率: {metrics['disk']['percent']}%")
    
    print("\n🎯 建议:")
    if metrics['status'] == 'warning':
        print("   ⚠️ 系统需要优化")
    else:
        print("   ✅ 系统运行正常")

if __name__ == "__main__":
    main()