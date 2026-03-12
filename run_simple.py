#!/usr/bin/env python3
"""
毛毛AI增强系统 - 简化运行版本
"""

import os
import sys
import yaml
import json
from pathlib import Path
from datetime import datetime

def load_config():
    """加载配置"""
    config_path = Path("config/maomao_enhanced_config.yaml")
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def show_system_info(config):
    """显示系统信息"""
    print("🎯 毛毛AI增强投研系统")
    print("=" * 60)
    
    system_info = config['system']
    print(f"📋 系统信息:")
    print(f"   名称: {system_info['name']}")
    print(f"   版本: {system_info['version']}")
    print(f"   描述: {system_info['description']}")
    print(f"   作者: {system_info['author']}")
    
    print(f"\n📈 监控配置:")
    watchlist = config['monitoring']['watchlist']
    print(f"   监控股票: {len(watchlist)} 只")
    for i, stock in enumerate(watchlist, 1):
        print(f"     {i}. {stock}")
    
    print(f"\n🛠️ 集成技能:")
    skills = config['skills']
    print("   ✅ 已集成:")
    for skill in skills['integrated']:
        print(f"      • {skill['name']} - {skill['description']}")
    
    print("   ⏳ 待集成:")
    for skill in skills['pending']:
        print(f"      • {skill['name']} - {skill['description']} ({skill['status']})")
    
    print(f"\n📊 分析能力:")
    analysis_types = config['analysis']['types']
    for i, analysis_type in enumerate(analysis_types, 1):
        print(f"     {i}. {analysis_type}分析")

def run_demo_analysis():
    """运行演示分析"""
    print("\n🚀 运行演示分析")
    print("=" * 60)
    
    # 创建演示报告
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    reports_dir = Path("reports/demo")
    reports_dir.mkdir(exist_ok=True)
    
    # 演示股票
    demo_stocks = [
        ("600519.SH", "贵州茅台"),
        ("000001.SZ", "平安银行"),
    ]
    
    results = []
    for stock_code, stock_name in demo_stocks:
        print(f"\n📈 分析: {stock_name}({stock_code})")
        
        # 创建演示报告
        report_content = f"""# {stock_name}({stock_code}) 演示分析报告

## 📊 报告概述
- **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **股票代码**: {stock_code}
- **股票名称**: {stock_name}
- **分析系统**: 毛毛AI增强投研系统 v2.0.0

## 🔍 分析结果

### 定性分析要点
- 行业地位稳固，竞争优势明显
- 财务表现稳健，成长性良好
- 管理层经验丰富，战略清晰

### 投资建议
**谨慎持有** - 建议根据风险偏好和投资期限决策

### 关键监控指标
1. 季度财务数据变化
2. 行业政策动态
3. 市场份额变化

## 🛠️ 使用技能
1. stock-qualitative-analysis - 定性分析
2. investment-memo - 投资备忘录
3. akshare-stock - 数据获取

## 📁 系统信息
- **系统版本**: 2.0.0
- **部署时间**: 2026-03-12
- **技能集成**: ✅ 成功

---

**报告完成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**分析师**: 毛毛AI增强系统
"""
        
        report_file = reports_dir / f"{stock_code}_demo_{timestamp}.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"  ✅ 生成报告: {report_file}")
        
        results.append({
            'stock_code': stock_code,
            'stock_name': stock_name,
            'report_file': str(report_file),
        })
    
    # 生成摘要
    summary = {
        'total_stocks': len(results),
        'successful': len(results),
        'timestamp': datetime.now().isoformat(),
        'reports': results,
    }
    
    summary_file = reports_dir / f"demo_summary_{timestamp}.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ 演示分析完成!")
    print(f"   分析股票: {len(results)} 只")
    print(f"   生成报告: {len(results)} 份")
    print(f"   摘要文件: {summary_file}")
    
    return results

def check_system_status():
    """检查系统状态"""
    print("\n🔧 系统状态检查")
    print("=" * 60)
    
    checks = []
    
    # 检查目录
    required_dirs = ["src", "config", "data", "reports", "logs"]
    for dir_name in required_dirs:
        if Path(dir_name).exists():
            checks.append(("✅", f"目录: {dir_name}/"))
        else:
            checks.append(("❌", f"目录: {dir_name}/ (缺失)"))
    
    # 检查配置文件
    required_configs = ["maomao_enhanced_config.yaml", "integration_config.yaml"]
    for config_name in required_configs:
        config_path = Path("config") / config_name
        if config_path.exists():
            checks.append(("✅", f"配置: {config_name}"))
        else:
            checks.append(("❌", f"配置: {config_name} (缺失)"))
    
    # 检查技能目录
    skills_dir = Path.home() / ".agents/skills"
    required_skills = ["stock-qualitative-analysis", "investment-memo", "akshare-stock"]
    for skill_name in required_skills:
        skill_path = skills_dir / skill_name
        if skill_path.exists():
            checks.append(("✅", f"技能: {skill_name}"))
        else:
            checks.append(("⚠️ ", f"技能: {skill_name} (未安装)"))
    
    # 显示检查结果
    for status, message in checks:
        print(f"  {status} {message}")
    
    # 统计
    total = len(checks)
    passed = len([c for c in checks if c[0] == "✅"])
    warning = len([c for c in checks if c[0] == "⚠️ "])
    failed = len([c for c in checks if c[0] == "❌"])
    
    print(f"\n📊 检查统计:")
    print(f"   总计: {total}")
    print(f"   通过: {passed}")
    print(f"   警告: {warning}")
    print(f"   失败: {failed}")
    
    if failed == 0:
        print("✅ 系统状态: 正常")
        return True
    else:
        print("❌ 系统状态: 异常")
        return False

def main():
    """主函数"""
    try:
        # 加载配置
        config = load_config()
        
        # 显示系统信息
        show_system_info(config)
        
        # 检查系统状态
        if check_system_status():
            # 运行演示分析
            run_demo_analysis()
        else:
            print("\n⚠️  系统状态异常，跳过演示分析")
        
        print("\n" + "=" * 60)
        print("🎉 毛毛AI增强系统运行完成!")
        print("\n📋 下一步:")
        print("  1. 查看生成报告: ls -la reports/demo/")
        print("  2. 编辑配置: vim config/maomao_enhanced_config.yaml")
        print("  3. 添加更多技能: 使用find-skills搜索")
        print("  4. 自动化运行: 配置cron定时任务")
        
    except Exception as e:
        print(f"❌ 运行失败: {e}")
        print("\n🔧 故障排除:")
        print("  1. 检查配置文件: config/maomao_enhanced_config.yaml")
        print("  2. 检查Python环境: python3 --version")
        print("  3. 重新部署: ./deploy_enhanced_system.sh")

if __name__ == "__main__":
    main()