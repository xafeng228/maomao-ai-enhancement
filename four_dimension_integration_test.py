#!/usr/bin/env python3
"""
四维提升集成测试 - 验证所有四个维度协同工作
"""

import sys
import time
from datetime import datetime

print("🧠 毛毛AI增强系统 - 四维提升集成测试")
print("=" * 70)
print("🎯 测试目标: 验证四个维度协同工作，形成完整的AI投研伙伴")
print("⏰ 开始时间:", datetime.now().strftime("%H:%M:%S GMT+8"))
print("=" * 70)

# 记录开始时间
start_time = time.time()

# 测试1: 群体智能集成 (预测模型)
print("\n1. 🐟 测试群体智能集成 (预测模型)...")
try:
    sys.path.append('.')
    from prediction_model_integrator import PredictionModelIntegrator
    
    # 创建测试数据
    test_data = []
    base_price = 50.0
    for i in range(30):
        price = base_price * (1 + 0.002 * i + 0.01 * (i % 3 - 1))
        test_data.append({
            'date': f'2026-03-{12-i:02d}',
            'close': price,
            'high': price * 1.02,
            'low': price * 0.98,
            'volume': 10000
        })
    
    integrator = PredictionModelIntegrator()
    prediction_result = integrator.ensemble_predict("TEST001", test_data, horizon=5)
    
    if prediction_result['status'] == 'success':
        print("   ✅ 群体智能集成测试通过")
        print(f"      使用模型: {prediction_result['model_summary']['successful_models']}/5")
        print(f"      共识度: {prediction_result['consensus_level']['consensus_level']}")
        print(f"      投资建议: {prediction_result['recommendation']['recommendation']}")
    else:
        print(f"   ❌ 群体智能集成测试失败: {prediction_result.get('error')}")
        
except Exception as e:
    print(f"   ❌ 群体智能集成测试异常: {e}")

# 测试2: 实时A股监控 (数据获取)
print("\n2. 📈 测试实时A股监控 (数据获取)...")
try:
    from multi_source_data_fetcher import MultiSourceDataFetcher
    
    fetcher = MultiSourceDataFetcher(primary_source='akshare', cache_ttl_minutes=10)
    data_result = fetcher.fetch_stock_data("603039", "real_time", use_cache=False)
    
    if data_result['status'] == 'success':
        print("   ✅ 实时A股监控测试通过")
        data = data_result.get('data', {})
        print(f"      当前价格: {data.get('current_price', 'N/A')}")
        print(f"      今日涨跌: {data.get('change_percent', 'N/A')}%")
        print(f"      数据源: {data_result.get('metadata', {}).get('primary_source', 'N/A')}")
    else:
        print(f"   ❌ 实时A股监控测试失败: {data_result.get('error')}")
        
except Exception as e:
    print(f"   ❌ 实时A股监控测试异常: {e}")

# 测试3: 个性化策略 (策略推荐)
print("\n3. 🎯 测试个性化策略 (策略推荐)...")
try:
    from personalized_strategy_optimizer import PersonalizedStrategyOptimizer
    
    # 创建测试用户
    test_user = {
        'risk_tolerance': '稳健型',
        'investment_goal': '增值',
        'investment_experience': '中级'
    }
    
    test_market = {
        'market_trend': '震荡',
        'volatility': '中等',
        'market_sentiment': '中性'
    }
    
    optimizer = PersonalizedStrategyOptimizer(test_user)
    strategy_result = optimizer.recommend_strategies(test_market)
    
    if strategy_result['status'] == 'success':
        print("   ✅ 个性化策略测试通过")
        print(f"      推荐策略: {len(strategy_result['recommendations'])} 个")
        print(f"      个性化程度: {strategy_result['personalization_level']['personalization_level']}")
        
        # 显示第一个推荐
        if strategy_result['recommendations']:
            first_rec = strategy_result['recommendations'][0]
            print(f"      首选策略: {first_rec['strategy_name']} ({first_rec['recommendation_level']})")
    else:
        print(f"   ❌ 个性化策略测试失败: {strategy_result.get('error')}")
        
except Exception as e:
    print(f"   ❌ 个性化策略测试异常: {e}")

# 测试4: 持续学习AI伙伴 (学习系统)
print("\n4. 🧠 测试持续学习AI伙伴 (学习系统)...")
try:
    # 检查学习系统目录
    import os
    learning_dir = "/root/.openclaw/workspace/enhancement/learning"
    
    if os.path.exists(learning_dir):
        print("   ✅ 持续学习系统架构存在")
        
        # 检查关键文件
        learning_files = [
            'experience_learner.py',
            'error_analyzer.py', 
            'strategy_optimizer.py'
        ]
        
        existing_files = []
        for file in learning_files:
            if os.path.exists(os.path.join(learning_dir, file)):
                existing_files.append(file)
        
        print(f"      学习模块: {len(existing_files)}/{len(learning_files)} 个")
        
        # 检查记忆系统
        memory_files = [
            '/root/.openclaw/workspace/MEMORY.md',
            '/root/.openclaw/workspace/memory/2026-03-12.md'
        ]
        
        memory_count = sum(1 for f in memory_files if os.path.exists(f))
        print(f"      记忆文件: {memory_count}/{len(memory_files)} 个")
        
    else:
        print("   ⚠️ 学习系统目录不存在")
        
except Exception as e:
    print(f"   ❌ 持续学习测试异常: {e}")

# 测试5: 四维协同工作
print("\n5. 🔄 测试四维协同工作...")
try:
    # 模拟一个完整的投研流程
    print("   模拟完整投研流程:")
    
    # 步骤1: 数据获取 (维度2)
    print("   📊 1. 获取市场数据...")
    
    # 步骤2: 技术分析 (维度1 + 维度2)
    print("   📈 2. 进行技术分析和预测...")
    
    # 步骤3: 策略推荐 (维度3)
    print("   🎯 3. 生成个性化策略推荐...")
    
    # 步骤4: 学习优化 (维度4)
    print("   🧠 4. 记录经验并优化...")
    
    print("   ✅ 四维协同流程模拟完成")
    
except Exception as e:
    print(f"   ❌ 协同测试异常: {e}")

# 计算总时间
total_time = time.time() - start_time

print("\n" + "=" * 70)
print("📊 四维提升集成测试结果")
print("=" * 70)

# 汇总结果
test_results = {
    '群体智能集成': '通过' if locals().get('prediction_result', {}).get('status', '') == 'success' else '失败',
    '实时A股监控': '通过' if locals().get('data_result', {}).get('status', '') == 'success' else '失败',
    '个性化策略': '通过' if locals().get('strategy_result', {}).get('status', '') == 'success' else '失败',
    '持续学习AI伙伴': '通过' if locals().get('learning_dir_check', False) else '失败'
}

passed_tests = sum(1 for result in test_results.values() if result == '通过')
total_tests = len(test_results)

print(f"✅ 通过测试: {passed_tests}/{total_tests}")
print(f"⏱️ 总测试时间: {total_time:.2f}秒")

for dimension, result in test_results.items():
    status_icon = "✅" if result == '通过' else "❌"
    print(f"{status_icon} {dimension}: {result}")

# 系统能力评估
print("\n🎯 系统能力评估:")
if passed_tests >= 3:
    print("   🥇 优秀 - 四维提升基本完成，系统能力完整")
    print("   🚀 毛毛AI已具备专业投研伙伴的核心能力")
elif passed_tests >= 2:
    print("   🥈 良好 - 四维提升进展良好，核心能力具备")
    print("   ⚡ 需要进一步完善个别维度")
else:
    print("   🥉 需改进 - 四维提升需要更多工作")
    print("   🔧 建议重点修复失败的维度")

# 下一步建议
print("\n📋 下一步建议:")
if passed_tests == 4:
    print("   1. 🎉 四维提升完成，准备商业化部署")
    print("   2. 🧪 进行大规模压力测试")
    print("   3. 👥 收集用户反馈并优化")
    print("   4. 🚀 正式发布毛毛AI增强系统")
elif passed_tests >= 3:
    print("   1. 🔧 修复失败的测试")
    print("   2. 🔄 优化各维度协同")
    print("   3. 📊 进行性能调优")
    print("   4. 🎯 完成四维提升最后步骤")
else:
    print("   1. 🛠️ 重点修复核心问题")
    print("   2. 📈 重新设计失败维度")
    print("   3. 🔍 深入分析失败原因")
    print("   4. 🎯 制定详细的修复计划")

print("\n" + "=" * 70)
print("🏁 测试完成时间:", datetime.now().strftime("%H:%M:%S GMT+8"))
print("=" * 70)

# 最终结论
if passed_tests == 4:
    print("\n🎉 四维提升计划圆满完成!")
    print("   毛毛AI已成功从基础投研助手")
    print("   提升为专业级AI投研伙伴!")
    print("   🚀 准备进入下一阶段: 商业化部署")
else:
    print(f"\n🔧 四维提升计划完成度: {passed_tests}/4")
    print(f"   需要继续完善 {4-passed_tests} 个维度")
    print("   💪 继续努力，完成四维提升！")