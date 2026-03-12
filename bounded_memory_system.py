    def create_memory_monitor(self):
        """创建记忆监控器"""
        print("\n📈 创建记忆监控器...")
        
        monitor_script = """#!/usr/bin/env python3
"""
        # 这里可以添加定期监控脚本
        
        monitor_file = self.workspace / "memory_monitor.py"
        with open(monitor_file, 'w', encoding='utf-8') as f:
            f.write(monitor_script)
        
        print(f"   监控器创建: {monitor_file}")
    
    def run_demo(self):
        """运行演示"""
        print("=" * 60)
        print("🧠 有界记忆系统演示")
        print("=" * 60)
        
        # 1. 分析当前状态
        stats = self.analyze_current_state()
        if not stats:
            return
        
        print("\n" + "=" * 60)
        print("📋 章节详情:")
        print("=" * 60)
        for i, section in enumerate(stats['section_details'], 1):
            print(f"{i:2d}. {section['title'][:40]:40} {section['size']:5d}字符 {section['lines']:3d}行")
        
        print("\n" + "=" * 60)
        print("🎯 优化建议:")
        print("=" * 60)
        
        if stats['needs_optimization']:
            print(f"1. 需要减少 {stats['reduction_needed']} 字符 ({stats['reduction_percent']:.1f}%)")
            print("2. 建议优化策略:")
            print("   a) 自动优化 - 压缩内容，保留关键信息")
            print("   b) 摘要优化 - 创建摘要，详细内容移到扩展记忆")
            print("   c) 移动到扩展记忆 - 主文件只保留摘要")
            
            # 询问用户选择
            print("\n请选择优化策略:")
            print("1. 自动优化")
            print("2. 摘要优化") 
            print("3. 移动到扩展记忆")
            print("4. 暂不优化")
            
            # 这里可以添加用户输入，现在先演示自动优化
            choice = "1"
            
            if choice == "1":
                self.optimize_memory("auto")
            elif choice == "2":
                self.optimize_memory("summary")
            elif choice == "3":
                self.optimize_memory("move_extended")
            else:
                print("   跳过优化")
        else:
            print("✅ 记忆大小正常，无需优化")
        
        print("\n" + "=" * 60)
        print("🔧 工具建议:")
        print("=" * 60)
        print("1. 定期运行记忆监控")
        print("2. 设置自动优化计划")
        print("3. 使用扩展记忆存储详细内容")
        print("4. 建立记忆维护流程")
        
        print("\n" + "=" * 60)
        print("✅ 演示完成!")
        print("=" * 60)

def main():
    """主函数"""
    print("🚀 启动有界记忆系统...")
    
    # 初始化系统
    memory_system = BoundedMemorySystem()
    
    # 运行演示
    memory_system.run_demo()
    
    # 创建监控器
    memory_system.create_memory_monitor()
    
    print("\n🎯 下一步:")
    print("1. 定期检查记忆大小")
    print("2. 设置自动优化")
    print("3. 使用扩展记忆存储详细内容")
    print("4. 建立记忆维护工作流")

if __name__ == "__main__":
    main()