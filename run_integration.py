#!/usr/bin/env python3
"""
毛毛AI技能集成系统 - 运行脚本
"""

import sys
from pathlib import Path

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from integration_core import SkillIntegrationSystem

def test_single_stock():
    """测试单只股票分析"""
    print("🚀 测试单只股票分析")
    print("=" * 60)
    
    system = SkillIntegrationSystem()
    system.load_skills()
    
    # 测试贵州茅台
    result = system.run_analysis_workflow("600519.SH", "贵州茅台")
    
    print(f"✅ 分析完成: 贵州茅台(600519.SH)")
    print(f"   状态: {result.get('status', 'unknown')}")
    print(f"   步骤数: {len(result.get('steps', []))}")
    
    if result.get('status') == 'success':
        print("📁 生成文件:")
        for key, value in result.get('results', {}).items():
            if isinstance(value, dict) and 'report_file' in value:
                print(f"   📄 {key}: {value['report_file']}")
    
    return result

def test_batch_analysis():
    """测试批量分析"""
    print("\n🚀 测试批量分析")
    print("=" * 60)
    
    system = SkillIntegrationSystem()
    system.load_skills()
    
    # 测试3只股票
    test_stocks = ["600519.SH", "000001.SZ", "300750.SZ"]
    
    result = system.run_batch_analysis(test_stocks)
    summary = result['summary']
    
    print(f"✅ 批量分析完成!")
    print(f"   总股票数: {summary['total_stocks']}")
    print(f"   成功: {summary['successful']}")
    print(f"   失败: {summary['failed']}")
    print(f"   成功率: {summary['success_rate']:.1%}")
    
    print("\n📊 成功股票:")
    for stock in summary['details']['successful_stocks']:
        print(f"   ✅ {stock}")
    
    if summary['details']['failed_stocks']:
        print("\n❌ 失败股票:")
        for stock in summary['details']['failed_stocks']:
            print(f"   ❌ {stock}")
    
    return result

def show_system_info():
    """显示系统信息"""
    print("🔧 毛毛AI技能集成系统")
    print("=" * 60)
    
    system = SkillIntegrationSystem()
    config = system.config
    
    print(f"📋 系统信息:")
    print(f"   名称: {config['integration']['name']}")
    print(f"   版本: {config['integration']['version']}")
    print(f"   描述: {config['integration']['description']}")
    
    print(f"\n🎯 监控股票: {len(config['monitoring']['watchlist'])} 只")
    for stock in config['monitoring']['watchlist']:
        print(f"   📈 {stock}")
    
    print(f"\n🛠️ 集成技能:")
    skills = config['skills']
    for skill_name, skill_config in skills.items():
        status = "✅ 已启用" if skill_config.get('enabled') else "⏳ 待安装"
        print(f"   {status} {skill_name}: {skill_config.get('description', 'N/A')}")
    
    print(f"\n📁 输出目录:")
    print(f"   报告目录: {config['output']['reports_dir']}")
    print(f"   数据目录: {config['output']['data_dir']}")
    print(f"   日志目录: {config['output']['logs_dir']}")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='毛毛AI技能集成系统')
    parser.add_argument('--test', '-t', action='store_true', help='运行测试')
    parser.add_argument('--single', '-s', help='分析单只股票')
    parser.add_argument('--batch', '-b', action='store_true', help='批量分析')
    parser.add_argument('--info', '-i', action='store_true', help='显示系统信息')
    
    args = parser.parse_args()
    
    if args.test:
        # 运行完整测试
        test_single_stock()
        test_batch_analysis()
        
    elif args.single:
        # 分析单只股票
        system = SkillIntegrationSystem()
        system.load_skills()
        result = system.run_analysis_workflow(args.single)
        print(f"✅ 分析完成: {args.single}")
        
    elif args.batch:
        # 批量分析
        test_batch_analysis()
        
    elif args.info:
        # 显示系统信息
        show_system_info()
        
    else:
        # 默认运行测试
        print("毛毛AI技能集成系统")
        print("使用 --help 查看选项")
        show_system_info()

if __name__ == "__main__":
    main()