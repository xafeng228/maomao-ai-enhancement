#!/usr/bin/env python3
"""
简化版用户界面测试
"""

import time
from datetime import datetime

class Color:
    """终端颜色"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

class SimpleUI:
    """简化版用户界面"""
    
    def __init__(self):
        print(f"{Color.BOLD}{Color.BLUE}🧠 毛毛AI增强系统 - 简化界面测试{Color.ENDC}")
        print(f"{Color.BLUE}=" * 60 + Color.ENDC)
    
    def show_progress_bar(self, task_name, current, total, message=""):
        """显示进度条"""
        percentage = (current / total) * 100
        bar_length = 30
        filled_length = int(bar_length * current / total)
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        
        progress_msg = f"{task_name}: {bar} {percentage:.1f}% ({current}/{total})"
        if message:
            progress_msg += f" | {message}"
        
        print(f"\r{Color.BLUE}⏳ {progress_msg}{Color.ENDC}", end="", flush=True)
        
        if current == total:
            print(f" {Color.GREEN}✅{Color.ENDC}")
    
    def show_result(self, symbol, price, change, trend, risk, recommendation):
        """显示分析结果"""
        print(f"\n{Color.BOLD}{Color.BLUE}📈 {symbol} 分析结果{Color.ENDC}")
        print(f"{Color.BLUE}=" * 50 + Color.ENDC)
        
        # 价格信息
        if change >= 0:
            price_color = Color.GREEN
        else:
            price_color = Color.RED
        
        print(f"{price_color}💰 当前价格: {price} ({change:+.2f}%){Color.ENDC}")
        
        # 趋势信息
        if trend == "上涨":
            trend_color = Color.GREEN
        elif trend == "下跌":
            trend_color = Color.RED
        else:
            trend_color = Color.YELLOW
        
        print(f"{trend_color}📊 技术趋势: {trend}{Color.ENDC}")
        
        # 风险信息
        if risk == "高":
            risk_color = Color.RED
        elif risk == "中":
            risk_color = Color.YELLOW
        else:
            risk_color = Color.GREEN
        
        print(f"{risk_color}⚠️ 风险等级: {risk}{Color.ENDC}")
        
        # 建议信息
        if "建议观望" in recommendation:
            rec_color = Color.YELLOW
        elif "可考虑参与" in recommendation:
            rec_color = Color.GREEN
        else:
            rec_color = Color.BLUE
        
        print(f"{rec_color}🎯 投资建议: {recommendation}{Color.ENDC}")
        
        print(f"{Color.BLUE}=" * 50 + Color.ENDC)
    
    def show_batch_summary(self, total, successful, total_time, avg_time):
        """显示批量分析总结"""
        success_rate = (successful / total) * 100
        
        print(f"\n{Color.BOLD}{Color.BLUE}🚀 批量分析结果总结{Color.ENDC}")
        print(f"{Color.BLUE}=" * 60 + Color.ENDC)
        
        print(f"{Color.GREEN}📊 分析统计:{Color.ENDC}")
        print(f"   股票数量: {total}")
        print(f"   成功分析: {successful}")
        print(f"   成功率: {success_rate:.1f}%")
        
        print(f"\n{Color.YELLOW}⚡ 性能统计:{Color.ENDC}")
        print(f"   总耗时: {total_time:.2f}秒")
        print(f"   平均每只: {avg_time:.2f}秒")
        
        # 结果评估
        if success_rate >= 90:
            assessment = f"{Color.GREEN}✅ 优秀 - 分析成功率很高{Color.ENDC}"
        elif success_rate >= 70:
            assessment = f"{Color.YELLOW}⚠️ 良好 - 分析成功率中等{Color.ENDC}"
        else:
            assessment = f"{Color.RED}❌ 需改进 - 分析成功率较低{Color.ENDC}"
        
        print(f"\n{Color.BOLD}📈 结果评估: {assessment}{Color.ENDC}")
        print(f"{Color.BLUE}=" * 60 + Color.ENDC)

def main():
    """主函数"""
    ui = SimpleUI()
    
    # 演示进度条
    print("\n🔍 演示进度条:")
    total_steps = 50
    for i in range(total_steps + 1):
        ui.show_progress_bar("数据获取", i, total_steps, f"处理中...")
        time.sleep(0.05)
    
    # 演示单个股票结果
    print("\n🔍 演示单个股票分析结果:")
    ui.show_result(
        symbol="603039",
        price=57.20,
        change=6.84,
        trend="下跌",
        risk="中",
        recommendation="技术面弱势，建议观望"
    )
    
    # 演示批量分析结果
    print("\n🔍 演示批量分析结果:")
    ui.show_batch_summary(
        total=3,
        successful=3,
        total_time=7.41,
        avg_time=2.47
    )
    
    print(f"\n{Color.BOLD}{Color.GREEN}🎉 用户体验完善演示完成!{Color.ENDC}")
    print(f"{Color.YELLOW}   界面更友好，操作更简单，结果更易懂{Color.ENDC}")

if __name__ == "__main__":
    main()