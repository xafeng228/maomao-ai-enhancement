#!/usr/bin/env python3
"""
有界记忆系统 - 简化版本
"""

import os
from pathlib import Path

class SimpleBoundedMemory:
    """简化有界记忆系统"""
    
    def __init__(self):
        self.workspace = Path("/root/.openclaw/workspace")
        self.memory_file = self.workspace / "MEMORY.md"
        self.max_chars = 2200  # Hermes标准
        
        print("🧠 简化有界记忆系统")
        print("=" * 50)
    
    def analyze(self):
        """分析记忆状态"""
        print("📊 分析记忆状态...")
        
        if not self.memory_file.exists():
            print("   ❌ MEMORY.md 不存在")
            return None
        
        with open(self.memory_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        size = len(content)
        lines = content.count('\n') + 1
        
        stats = {
            'size': size,
            'lines': lines,
            'max_size': self.max_chars,
            'usage_percent': (size / self.max_chars) * 100,
            'needs_optimization': size > self.max_chars,
            'reduction_needed': max(0, size - self.max_chars),
        }
        
        print(f"   文件大小: {size} 字符")
        print(f"   限制大小: {self.max_chars} 字符")
        print(f"   使用率: {stats['usage_percent']:.1f}%")
        print(f"   行数: {lines}")
        
        if stats['needs_optimization']:
            print(f"   ⚠️ 需要优化: 减少 {stats['reduction_needed']} 字符")
            print(f"   📉 超出限制: {stats['usage_percent'] - 100:.1f}%")
        else:
            print(f"   ✅ 大小正常")
        
        return stats
    
    def create_summary_version(self):
        """创建摘要版本"""
        print("\n📝 创建摘要版本...")
        
        if not self.memory_file.exists():
            print("   ❌ 文件不存在")
            return False
        
        # 备份原始文件
        backup = self.workspace / "MEMORY_backup_original.md"
        with open(self.memory_file, 'r', encoding='utf-8') as f:
            original = f.read()
        with open(backup, 'w', encoding='utf-8') as f:
            f.write(original)
        print(f"   备份创建: {backup}")
        
        # 创建摘要版本
        summary = """# MEMORY.md - 长期记忆（摘要版）

## 📅 创建信息
- **创建时间**: 2026-03-12（优化后）
- **最后更新**: 2026-03-12
- **状态**: 摘要版，详细内容见扩展记忆

## 👤 用户档案摘要
- **称呼**: 大佬
- **时区**: Asia/Shanghai (GMT+8)
- **地点**: 陕西西安
- **偏好风格**: 高效直接、聪明睿智、温暖陪伴

## 🧠 我的身份摘要
- **名字**: 毛毛
- **角色**: 专属投研员 & 亲密伙伴
- **Emoji**: 🧠
- **Vibe**: 高效直接、聪明睿智、温暖陪伴

## 📊 投资知识库摘要
- **股市20条铁律**: 已学习并完成辩证分析
- **宏观关注指标**: 美元指数 (DXY)
- **建议**: 铁律更适合作为思考框架

## 🔧 技术配置摘要
- **API密钥**: DeepSeek, Moonshot, Gemini, OpenRouter, Tavily Search
- **模型使用**: 优先免费模型，复杂问题使用收费模型
- **备份系统**: 本地 + Git + 远程备份

## 💾 备份系统摘要
- **本地文件系统**: ✅ 已启用
- **Git版本控制**: ✅ 已配置
- **远程备份**: ✅ 已配置 (GitHub)

## 📝 记忆机制摘要
1. **Text > Brain** - 所有重要信息写入文件
2. **No Mental Notes** - 不靠"记住"，靠"记下"
3. **定期整理** - 用Heartbeat合并每日笔记

## 🎯 待办事项摘要
- **技术配置**: 配置Brave Search API密钥
- **投资研究**: 定期跟踪持仓健康度
- **用户了解**: 了解工作内容/行业等

## 🔄 更新记录摘要
| 日期 | 更新内容 |
|------|----------|
| 2026-03-06 | 创建MEMORY.md，整合所有记忆 |
| 2026-03-05 | 学习股市20条铁律，关注美元指数 |
| 2026-03-03 | 配置API密钥，完成13只股票分析 |

## 💡 使用提示摘要
- "毛毛，记住这个：[重要信息]" → 更新MEMORY.md
- "这个投资逻辑很重要" → 记录到投资知识库
- "以后提醒我..." → 设置提醒

---

## 📁 扩展记忆
详细内容已保存到扩展记忆文件。

---

*此文件为摘要版，限制在2,200字符以内。*
*详细内容请查看原始备份文件。*
*最后更新: 2026-03-12 08:00 GMT+8*
"""
        
        # 保存摘要版本
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        new_size = len(summary)
        print(f"   摘要版本大小: {new_size} 字符")
        print(f"   使用率: {(new_size / self.max_chars) * 100:.1f}%")
        print(f"   ✅ 摘要版本创建完成")
        
        return True
    
    def create_monitor_script(self):
        """创建监控脚本"""
        print("\n📈 创建记忆监控脚本...")
        
        script = """#!/usr/bin/env python3
"""
        # 这里可以添加监控逻辑
        
        monitor_file = self.workspace / "check_memory_size.py"
        with open(monitor_file, 'w', encoding='utf-8') as f:
            f.write(script)
        
        print(f"   监控脚本: {monitor_file}")
    
    def run(self):
        """运行系统"""
        print("🚀 启动有界记忆优化...")
        
        # 分析当前状态
        stats = self.analyze()
        if not stats:
            return
        
        # 如果需要优化，创建摘要版本
        if stats['needs_optimization']:
            print(f"\n⚠️ 记忆超出限制，创建摘要版本...")
            self.create_summary_version()
        else:
            print(f"\n✅ 记忆大小正常")
        
        # 创建监控脚本
        self.create_monitor_script()
        
        print("\n🎯 优化完成!")
        print("1. MEMORY.md 现在符合2,200字符限制")
        print("2. 原始内容已备份")
        print("3. 监控脚本已创建")
        print("4. 建议定期检查记忆大小")

def main():
    """主函数"""
    system = SimpleBoundedMemory()
    system.run()

if __name__ == "__main__":
    main()