#!/usr/bin/env python3
"""
用户友好界面 - 用户体验完善
"""

import sys
import time
from datetime import datetime
import json
from typing import Dict, List, Any, Optional
from enum import Enum
import threading

class Color:
    """终端颜色"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class MessageType(Enum):
    """消息类型"""
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
    PROGRESS = "progress"
    RESULT = "result"

class UserFriendlyInterface:
    """用户友好界面"""
    
    def __init__(self, show_progress=True, show_timestamps=True, interactive=True):
        """
        初始化用户友好界面
        
        Args:
            show_progress: 是否显示进度
            show_timestamps: 是否显示时间戳
            interactive: 是否交互式
        """
        self.show_progress = show_progress
        self.show_timestamps = show_timestamps
        self.interactive = interactive
        self.progress_bars = {}
        self.progress_lock = threading.Lock()
        
        print(f"{Color.BOLD}{Color.BLUE}🧠 毛毛AI增强系统 - 用户友好界面{Color.ENDC}")
        print(f"{Color.BLUE}=" * 60 + Color.ENDC)
        print(f"{Color.GREEN}📊 用户体验完善 v1.0{Color.ENDC}")
        print(f"{Color.YELLOW}🎯 目标: 完善用户界面和交互体验{Color.ENDC}")
        print(f"{Color.YELLOW}⏰ 开始时间: {datetime.now().strftime('%H:%M:%S')} GMT+8{Color.ENDC}")
        print(f"{Color.BLUE}=" * 60 + Color.ENDC)
    
    def show_message(self, message: str, msg_type: MessageType = MessageType.INFO, 
                    prefix: str = "", suffix: str = ""):
        """显示消息"""
        timestamp = f"[{datetime.now().strftime('%H:%M:%S')}] " if self.show_timestamps else ""
        
        # 根据消息类型选择颜色和图标
        if msg_type == MessageType.INFO:
            color = Color.BLUE
            icon = "ℹ️"
        elif msg_type == MessageType.SUCCESS:
            color = Color.GREEN
            icon = "✅"
        elif msg_type == MessageType.WARNING:
            color = Color.YELLOW
            icon = "⚠️"
        elif msg_type == MessageType.ERROR:
            color = Color.RED
            icon = "❌"
        elif msg_type == MessageType.PROGRESS:
            color = Color.BLUE
            icon = "⏳"
        elif msg_type == MessageType.RESULT:
            color = Color.GREEN
            icon = "📊"
        else:
            color = Color.ENDC
            icon = ""
        
        # 构建消息
        full_message = f"{timestamp}{color}{icon} {prefix}{message}{suffix}{Color.ENDC}"
        
        # 如果是进度消息，不换行
        if msg_type == MessageType.PROGRESS:
            print(f"\r{full_message}", end="", flush=True)
        else:
            print(full_message)
    
    def start_progress(self, task_id: str, task_name: str, total: int = 100):
        """开始进度条"""
        with self.progress_lock:
            self.progress_bars[task_id] = {
                'name': task_name,
                'current': 0,
                'total': total,
                'start_time': time.time()
            }
        
        if self.show_progress:
            self.show_message(f"开始: {task_name}", MessageType.INFO)
    
    def update_progress(self, task_id: str, current: int, message: str = ""):
        """更新进度条"""
        with self.progress_lock:
            if task_id not in self.progress_bars:
                return
            
            progress = self.progress_bars[task_id]
            progress['current'] = current
            
            # 计算进度百分比
            percentage = (current / progress['total']) * 100
            
            # 计算预计剩余时间
            elapsed = time.time() - progress['start_time']
            if current > 0:
                estimated_total = elapsed / (current / progress['total'])
                remaining = estimated_total - elapsed
                time_str = f"剩余: {remaining:.1f}s"
            else:
                time_str = "剩余: 计算中..."
        
        if self.show_progress:
            # 构建进度条
            bar_length = 30
            filled_length = int(bar_length * current / progress['total'])
            bar = '█' * filled_length + '░' * (bar_length - filled_length)
            
            progress_msg = f"{progress['name']}: {bar} {percentage:.1f}% ({current}/{progress['total']}) {time_str}"
            if message:
                progress_msg += f" | {message}"
            
            self.show_message(progress_msg, MessageType.PROGRESS)
    
    def complete_progress(self, task_id: str, message: str = ""):
        """完成进度条"""
        with self.progress_lock:
            if task_id not in self.progress_bars:
                return
            
            progress = self.progress_bars[task_id]
            elapsed = time.time() - progress['start_time']
            
            # 确保进度完成
            self.update_progress(task_id, progress['total'])
            
            # 显示完成消息
            if self.show_progress:
                print()  # 换行
                completion_msg = f"完成: {progress['name']} ({elapsed:.2f}秒)"
                if message:
                    completion_msg += f" - {message}"
                self.show_message(completion_msg, MessageType.SUCCESS)
            
            # 删除进度条
            del self.progress_bars[task_id]
    
    def format_stock_analysis_result(self, analysis_result: Dict[str, Any]) -> str:
        """格式化股票分析结果"""
        if not analysis_result or analysis_result.get('status') == 'error':
            return self.format_error_result(analysis_result)
        
        symbol = analysis_result.get('symbol', '未知')
        processing_time = analysis_result.get('processing_time', '未知')
        cache_hit = analysis_result.get('cache_hit', False)
        
        # 获取分析结果
        results = analysis_result.get('analysis_results', {})
        
        # 构建格式化输出
        output = []
        output.append(f"{Color.BOLD}{Color.BLUE}📈 {symbol} 分析结果{Color.ENDC}")
        output.append(f"{Color.BLUE}=" * 50 + Color.ENDC)
        
        # 实时数据
        rt_data = results.get('real_time_data', {})
        if rt_data.get('status') == 'success':
            output.append(f"{Color.GREEN}💰 实时行情: {rt_data.get('summary', 'N/A')}{Color.ENDC}")
        
        # 基本信息
        basic_info = results.get('basic_info', {})
        if basic_info.get('status') == 'success':
            output.append(f"{Color.GREEN}🏢 公司概况: {basic_info.get('summary', 'N/A')}{Color.ENDC}")
        
        # 技术分析
        tech_analysis = results.get('technical_analysis', {})
        if tech_analysis.get('status') == 'success':
            output.append(f"{Color.YELLOW}📊 技术分析: {tech_analysis.get('summary', 'N/A')}{Color.ENDC}")
        
        # 基本面分析
        fund_analysis = results.get('fundamental_analysis', {})
        if fund_analysis.get('status') == 'success':
            output.append(f"{Color.YELLOW}🧠 基本面: {fund_analysis.get('summary', 'N/A')}{Color.ENDC}")
        
        # 风险评估
        risk_assessment = results.get('risk_assessment', {})
        if risk_assessment.get('status') == 'success':
            risk_summary = risk_assessment.get('summary', '')
            if '风险等级: 高' in risk_summary:
                output.append(f"{Color.RED}⚠️ 风险评估: {risk_summary}{Color.ENDC}")
            elif '风险等级: 中' in risk_summary:
                output.append(f"{Color.YELLOW}⚠️ 风险评估: {risk_summary}{Color.ENDC}")
            else:
                output.append(f"{Color.GREEN}⚠️ 风险评估: {risk_summary}{Color.ENDC}")
        
        # 投资建议
        investment_rec = results.get('investment_recommendation', {})
        if investment_rec.get('status') == 'success':
            rec_summary = investment_rec.get('summary', '')
            if '信心度: 高' in rec_summary:
                output.append(f"{Color.GREEN}🎯 投资建议: {rec_summary}{Color.ENDC}")
            elif '信心度: 低' in rec_summary:
                output.append(f"{Color.YELLOW}🎯 投资建议: {rec_summary}{Color.ENDC}")
            else:
                output.append(f"{Color.BLUE}🎯 投资建议: {rec_summary}{Color.ENDC}")
        
        # 性能信息
        output.append(f"{Color.BLUE}=" * 50 + Color.ENDC)
        output.append(f"{Color.BOLD}⏱️ 处理时间: {processing_time}{Color.ENDC}")
        
        if cache_hit:
            output.append(f"{Color.GREEN}💾 缓存命中，节省了数据获取时间{Color.ENDC}")
        
        output.append(f"{Color.BLUE}=" * 50 + Color.ENDC)
        
        return "\n".join(output)
    
    def format_batch_analysis_result(self, batch_result: Dict[str, Any]) -> str:
        """格式化批量分析结果"""
        if not batch_result:
            return self.format_error_result({'error': '批量分析结果为空'})
        
        summary = batch_result.get('summary', {})
        performance = batch_result.get('performance', {})
        
        output = []
        output.append(f"{Color.BOLD}{Color.BLUE}🚀 批量分析结果总结{Color.ENDC}")
        output.append(f"{Color.BLUE}=" * 60 + Color.ENDC)
        
        # 基本统计
        output.append(f"{Color.GREEN}📊 分析统计:{Color.ENDC}")
        output.append(f"   股票数量: {summary.get('total_stocks', 0)}")
        output.append(f"   成功分析: {summary.get('successful', 0)}")
        output.append(f"   失败分析: {summary.get('failed', 0)}")
        output.append(f"   成功率: {summary.get('success_rate', '0%')}")
        
        # 性能统计
        output.append(f"\n{Color.YELLOW}⚡ 性能统计:{Color.ENDC}")
        output.append(f"   总耗时: {summary.get('total_time', '0秒')}")
        output.append(f"   平均每只: {summary.get('avg_time_per_stock', '0秒')}")
        output.append(f"   缓存命中率: {summary.get('cache_hit_rate', '0%')}")
        
        if 'parallel_efficiency' in summary:
            output.append(f"   并行效率: {summary.get('parallel_efficiency', 'N/A')}")
        
        # 性能指标
        if performance:
            stocks_per_second = performance.get('stocks_per_second', 0)
            output.append(f"   处理速度: {stocks_per_second:.2f} 只/秒")
        
        # 结果评估
        success_rate = float(summary.get('success_rate', '0%').replace('%', ''))
        if success_rate >= 90:
            assessment = f"{Color.GREEN}✅ 优秀 - 分析成功率很高{Color.ENDC}"
        elif success_rate >= 70:
            assessment = f"{Color.YELLOW}⚠️ 良好 - 分析成功率中等{Color.ENDC}"
        else:
            assessment = f"{Color.RED}❌ 需改进 - 分析成功率较低{Color.ENDC}"
        
        output.append(f"\n{Color.BOLD}📈 结果评估: {assessment}{Color.ENDC}")
        
        output.append(f"{Color.BLUE}=" * 60 + Color.ENDC)
        
        return "\n".join(output)
    
    def format_error_result(self, error_result: Dict[str, Any]) -> str:
        """格式化错误结果"""
        error_msg = error_result.get('error', '未知错误')
        symbol = error_result.get('symbol', '未知')
        
        output = []
        output.append(f"{Color.BOLD}{Color.RED}❌ {symbol} 分析失败{Color.ENDC}")
        output.append(f"{Color.RED}=" * 50 + Color.ENDC")
        output.append(f"{Color.RED}错误信息: {error_msg}{Color.ENDC}")
        
        # 提供解决方案建议
        solutions = self._get_error_solutions(error_msg)
        if solutions:
            output.append(f"\n{Color.YELLOW}💡 建议解决方案:{Color.ENDC}")
            for solution in solutions:
                output.append(f"   • {solution}")
        
        output.append(f"{Color.RED}=" * 50 + Color.ENDC")
        
        return "\n".join(output)
    
    def _get_error_solutions(self, error_msg: str) -> List[str]:
        """根据错误信息获取解决方案"""
        solutions = []
        
        if '网络' in error_msg or '连接' in error_msg:
            solutions.extend([
                "检查网络连接是否正常",
                "尝试稍后重试",
                "检查防火墙设置"
            ])
        
        if '数据源' in error_msg or '获取失败' in error_msg:
            solutions.extend([
                "检查数据源服务是否正常",
                "尝试使用其他数据源",
                "检查API密钥或权限"
            ])
        
        if '股票代码' in error_msg or '不存在' in error_msg:
            solutions.extend([
                "检查股票代码是否正确",
                "确认股票是否已退市",
                "尝试其他股票代码"
            ])
        
        if '缓存' in error_msg or '内存' in error_msg:
            solutions.extend([
                "尝试清除缓存后重试",
                "检查系统内存使用情况",
                "重启分析服务"
            ])
        
        if not solutions:
            solutions = [
                "尝试重新运行分析",
                "检查系统日志获取更多信息",
                "联系技术支持"
            ]
        
        return solutions
    
    def show_interactive_menu(self) -> Optional[str]:
        """显示交互式菜单"""
        if not self.interactive:
            return None
        
        print(f"\n{Color.BOLD}{Color.BLUE}📱 交互式菜单{Color.ENDC}")
        print(f"{Color.BLUE}=" * 50 + Color.ENDC)
        
        options = [
            ("1", "分析单个股票", "输入股票代码进行分析"),
            ("2", "批量分析股票", "输入多个股票代码（逗号分隔）"),
            ("3", "查看缓存统计", "显示缓存使用情况"),
            ("4", "清除缓存", "清空所有缓存数据"),
            ("5", "性能测试", "运行性能测试"),
            ("6", "帮助", "显示使用帮助"),
            ("0", "退出", "退出系统")
        ]
        
        for option in options:
            print(f"{Color.GREEN}{option[0]}. {option[1]}{Color.ENDC} - {option[2]}")
        
        print(f"{Color.BLUE}=" * 50 + Color.ENDC")
        
        while True:
            try:
                choice = input(f"{Color.YELLOW}请选择操作 (0-6): {Color.ENDC}").strip()
                
                if choice == "0":
                    self.show_message("感谢使用，再见！", MessageType.INFO)
                    return "exit"
                elif choice in ["1", "2", "3", "4", "5", "6"]:
                    return choice
                else:
                    self.show_message("无效选择，请重新输入", MessageType.WARNING)
            except KeyboardInterrupt:
                self.show_message("操作被取消", MessageType.WARNING)
                return "exit"
            except Exception as e:
                self.show_message(f"输入错误: {e}", MessageType.ERROR)
    
    def get_stock_symbol_input(self) -> List[str]:
        """获取股票代码输入"""
        while True:
            try:
                input_str = input(f"{Color.YELLOW}请输入股票代码（多个用逗号分隔）: {Color.ENDC}").strip()
                
                if not input_str:
                    self.show_message("输入不能为空", MessageType.WARNING)
                    continue
                
                # 分割股票代码
                symbols = [s.strip().upper() for s in input_str.split(',')]
                symbols = [s for s in symbols if s]  # 移除空字符串
                
                if not symbols:
                    self.show_message("未找到有效的股票代码", MessageType.WARNING)
                    continue
                
                # 验证股票代码格式（简单验证）
                valid_symbols = []
                invalid_symbols = []
                
                for symbol in symbols:
                    if len(symbol) == 6 and symbol.isdigit():
                        valid_symbols.append(symbol)
                    else:
                        invalid_symbols.append(symbol)
                
                if invalid_symbols:
                    self.show_message(f"以下股票代码格式无效: {', '.join(invalid_symbols)}", MessageType.WARNING)
                
                if valid_symbols:
                    return valid_symbols
                else:
                    self.show_message("没有有效的股票代码，请重新输入", MessageType.WARNING)
                    
            except KeyboardInterrupt:
                self.show_message("输入被取消", MessageType.WARNING)
                return []
            except Exception as e:
                self.show_message(f"输入错误: {e}", MessageType.ERROR)
                return []
    
    def show_help(self):
        """显示帮助信息"""
        help_text = f"""
{Color.BOLD}{Color.BLUE}📖 毛毛AI增强系统 - 使用帮助{Color.ENDC}
{Color.BLUE}{"=" * 60}{Color.ENDC}

{Color.GREEN}🎯 系统功能:{Color.ENDC}
   • 实时股票数据分析
   • 技术面和基本面分析
   • 风险评估和投资建议
   • 批量股票分析
   • 智能缓存机制

{Color.YELLOW}📊 股票代码格式:{Color.ENDC}
   • A股: 6位数字代码 (如: 603039, 000001, 600036)
   • 多个股票: 用逗号分隔 (如: 603039,000001,600036)

{Color.BLUE}⚡ 性能特性:{Color.ENDC}
   • 智能缓存: 减少重复数据请求
   • 并发处理: 支持批量快速分析
   • 实时进度: 显示分析进度和状态
   • 错误恢复: 自动重试和降级处理

{Color.PURPLE}📈 分析维度:{Color.ENDC}
   • 实时行情: 价格、涨跌、成交量等
   • 技术分析: 趋势、移动平均线、近期表现
   • 基本面: 估值、行业分析、公司概况
   • 风险评估: 风险等级、风险因素、缓解建议
   • 投资建议: 具体建议、信心度、时间范围

{Color.CYAN}💡 使用技巧:{Color.ENDC}
   • 首次分析后，后续分析会使用缓存加速
   • 批量分析时，系统会自动并行处理
   • 遇到错误时，系统会提供解决方案建议
   • 可以随时清除缓存以获取最新数据

{Color.BLUE}{"=" * 60}{Color.ENDC}
{Color.BOLD}📞 技术支持:{Color.ENDC}
   如有问题，请联系毛毛AI技术支持
"""
        print(help_text)
    
    def show_welcome_message(self):
        """显示欢迎消息"""
        welcome_text = f"""
{Color.BOLD}{Color.BLUE}✨ 欢迎使用毛毛AI增强系统! ✨{Color.ENDC}

{Color.GREEN}🧠 您的专属投研助手已就绪{Color.ENDC}
{Color.YELLOW}🎯 为您提供专业的股票投资分析{Color.ENDC}

{Color.BLUE}📊 系统特性:{Color.ENDC}
   ✅ 真实数据源，避免模拟数据误导
   ✅ 多维度分析，提供全面投资视角
   ✅ 智能缓存机制，分析速度大幅提升
   ✅ 用户友好界面，操作简单直观
   ✅ 专业风险评估，投资决策更可靠

{Color.PURPLE}🚀 立即开始:{Color.ENDC}
   1. 选择"分析单个股票"或"批量分析股票"
   2. 输入股票代码（如: 603039）
   3. 查看详细分析结果
   4. 根据建议制定投资策略

{Color.CYAN}💡 提示:{Color.ENDC}
   • 首次使用建议先分析1-2只股票熟悉流程
   • 批量分析适合跟踪多个股票
   • 系统会记住您的分析历史
   • 所有分析基于公开数据，投资需谨慎

{Color.BOLD}{Color.GREEN}开始您的专业投研之旅吧! 🚀{Color.ENDC}
"""
        print(welcome_text)

def main():
    """主函数"""
    # 创建用户友好界面
    ui = UserFriendlyInterface(show_progress=True, show_timestamps=True, interactive=True)
    
    # 显示欢迎消息
    ui.show_welcome_message()
    
    # 演示进度条
    ui.start_progress("demo", "演示进度条", 100)
    for i in range(101):
        ui.update_progress("demo", i, f"处理中...")
        time.sleep(0.02)
    ui.complete_progress("demo", "演示完成")
    
    # 演示消息类型
    ui.show_message("这是一条信息消息", MessageType.INFO)
    ui.show_message("这是一条成功消息", MessageType.SUCCESS)
    ui.show_message("这是一条警告消息", MessageType.WARNING)
    ui.show_message("这是一条错误消息", MessageType.ERROR)
    
    # 演示格式化结果
    demo_result = {
        'symbol': '603039',
        'processing_time': '3.45秒',
        'cache_hit': True,
        'analysis_results': {
            'real_time_data': {
                'status': 'success',
                'summary': '价格: 57.20, 涨跌: +6.84%',
                'data_source': 'akshare'
            },
            'basic_info': {
                'status': 'success',
                'summary': '行业: 软件开发, 上市: 20170113',
                'data_source': 'akshare'
            },
            'technical_analysis': {
                'status': 'success',
                'summary': '趋势: 下跌, 近期5日: -15.06%',
                'analysis_period': '100个交易日'
            },
            'fundamental_analysis': {
                'status': 'success',
                'summary': '估值: 估值数据不全, 行业: 成长性行业，前景看好'
            },
            'risk_assessment': {
                'status': 'success',
                'summary': '风险等级: 中, 风险因素: 3个'
            },
            'investment_recommendation': {
                'status': 'success',
                'summary': '建议: 技术面弱势，建议观望 (信心度: 低)'
            }
        }
    }
    
    print("\n" + "=" * 60)
    print("📊 演示格式化结果:")
    print("=" * 60)
    print(ui.format_stock_analysis_result(demo_result))
    
    # 演示批量结果
    demo_batch_result = {
        'summary': {
            'total_stocks': 3,
            'successful': 3,
            'failed': 0,
            'success_rate': '100.0%',
            'total_time': '8.23秒',
            'avg_time_per_stock': '2.74秒',
            'cache_hit_rate': '66.7%',
            'parallel_efficiency': '95.2%'
        },
        'performance': {
            'stocks_per_second': 0.36
        }
    }
    
    print("\n" + "=" * 60)
    print("🚀 演示批量分析结果:")
    print("=" * 60)
    print(ui.format_batch_analysis_result(demo_batch_result))
    
    # 演示错误结果
    demo_error_result = {
        'symbol': '999999',
        'error': '股票代码不存在或已退市',
        'status': 'error'
    }
    
    print("\n" + "=" * 60)
    print("❌ 演示错误结果:")
    print("=" * 60)
    print(ui.format_error_result(demo_error_result))
    
    print(f"\n{Color.BOLD}{Color.GREEN}🎉 用户体验完善演示完成!{Color.ENDC}")
    print(f"{Color.YELLOW}   界面更友好，操作更简单，结果更易懂{Color.ENDC}")

if __name__ == "__main__":
    main()