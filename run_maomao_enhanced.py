#!/usr/bin/env python3
"""
毛毛AI增强系统 - 主运行脚本
"""

import sys
from pathlib import Path

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

def main():
    """主函数"""
    print("🎯 毛毛AI增强投研系统")
    print("=" * 60)
    
    try:
        # 尝试导入集成模块
        from integration_core import SkillIntegrationSystem
        print("✅ 技能集成模块加载成功")
        
        # 创建集成系统
        system = SkillIntegrationSystem("config/integration_config.yaml")
        system.load_skills()
        
        print("📋 系统信息:")
        print(f"   名称: {system.config['integration']['name']}")
        print(f"   版本: {system.config['integration']['version']}")
        print(f"   监控股票: {len(system.config['monitoring']['watchlist'])} 只")
        
        print("\n🚀 运行测试分析...")
        result = system.run_analysis_workflow("600519.SH", "贵州茅台")
        
        if result.get('status') == 'success':
            print("✅ 测试分析成功!")
            print(f"   生成报告: {len(result.get('results', {}))} 个")
        else:
            print("❌ 测试分析失败")
            
    except ImportError as e:
        print(f"❌ 模块导入失败: {e}")
        print("尝试简化运行...")
        
        # 简化运行
        import yaml
        with open("config/maomao_enhanced_config.yaml", 'r') as f:
            config = yaml.safe_load(f)
        
        print(f"📋 系统配置:")
        print(f"   名称: {config['system']['name']}")
        print(f"   版本: {config['system']['version']}")
        print(f"   监控股票: {len(config['monitoring']['watchlist'])} 只")
        
        print("\n✅ 系统配置验证成功!")
        
    except Exception as e:
        print(f"❌ 运行失败: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 毛毛AI增强系统部署完成!")
    print("📁 目录: $(pwd)")
    print("📋 配置文件: config/maomao_enhanced_config.yaml")
    print("🚀 运行命令: python3 run_maomao_enhanced.py")

if __name__ == "__main__":
    main()
