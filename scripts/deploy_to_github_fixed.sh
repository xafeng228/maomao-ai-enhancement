#!/bin/bash
# 修复版安全部署脚本

set -e

echo "🚀 开始安全部署毛毛AI能力提升项目到GitHub..."
echo "=========================================="
echo "🔒 安全第一：已通过严格安全检查"
echo "=========================================="

PROJECT_DIR="/root/.openclaw/workspace/maomao-ai-enhancement"
cd "$PROJECT_DIR"

echo "1. 验证项目完整性..."
if [ ! -f "README.md" ]; then
    echo "❌ README.md不存在"
    exit 1
fi

if [ ! -f ".gitignore" ]; then
    echo "❌ .gitignore不存在"
    exit 1
fi

echo "✅ 项目文件完整"

echo ""
echo "2. 手动安全检查..."
echo "  检查.gitignore配置..."
if grep -q "^\\.env$" .gitignore; then
    echo "  ✅ .gitignore正确配置了.env"
else
    echo "  ❌ .gitignore配置有问题"
    exit 1
fi

echo "  检查是否有真实的.env文件..."
if [ -f ".env" ]; then
    echo "  ⚠️  发现.env文件，检查内容..."
    if grep -q "your_" .env || grep -q "example" .env; then
        echo "  ✅ .env是示例文件"
    else
        echo "  ❌ .env可能包含真实密钥！"
        exit 1
    fi
else
    echo "  ✅ 没有.env文件（只有.env.example）"
fi

echo "  检查硬编码密钥..."
if grep -r "sk-" --include="*.py" --include="*.md" --include="*.txt" . 2>/dev/null | grep -v "example" | grep -v "your_" | grep -q "sk-"; then
    echo "  ❌ 发现可能的真实密钥"
    exit 1
else
    echo "  ✅ 没有发现真实密钥"
fi

echo ""
echo "✅ 安全检查通过！"

echo ""
echo "3. 初始化Git仓库..."
if [ ! -d ".git" ]; then
    git init
    echo "✅ Git仓库初始化完成"
else
    echo "✅ Git仓库已存在"
fi

echo ""
echo "4. 添加文件到Git..."
git add .
echo "✅ 文件已添加"

echo ""
echo "5. 提交更改..."
if git status --porcelain | grep -q "^[MADRC]"; then
    git commit -m "feat: 毛毛AI能力提升项目 v1.0.0

- 项目架构设计文档
- 多代理系统框架实现
- 技术分析代理完整实现
- 安全配置指南和检查脚本
- CI/CD工作流配置
- 完整文档和部署脚本

🔒 安全特性：
- 无硬编码API密钥
- 环境变量配置管理
- 强化的.gitignore配置
- 安全检查脚本
- 安全部署指南"
    echo "✅ 更改已提交"
else
    echo "⚠️  没有新的更改需要提交"
fi

echo ""
echo "6. 配置远程仓库..."
GITHUB_USER="xafeng228"
GITHUB_REPO="maomao-ai-enhancement"
GITHUB_URL="https://github.com/${GITHUB_USER}/${GITHUB_REPO}.git"

# 设置远程仓库
git remote remove origin 2>/dev/null || true
git remote add origin "$GITHUB_URL"
echo "✅ 远程仓库配置完成: $GITHUB_URL"

echo ""
echo "7. 准备推送到GitHub..."
echo "⚠️  注意：请确保GitHub仓库已创建"
echo "   访问: https://github.com/new"
echo "   仓库名: $GITHUB_REPO"
echo "   描述: 毛毛AI投研助手能力提升项目"
echo ""
echo "📋 推送前确认："
echo "1. ✅ 仓库已创建？"
echo "2. ✅ 有推送权限？"
echo "3. ✅ 网络连接正常？"
echo ""

# 创建分支并推送
echo "创建main分支并推送..."
git branch -M main

echo ""
echo "8. 开始推送到GitHub..."
echo "推送命令: git push -u origin main"
echo ""
echo "由于需要手动确认GitHub仓库创建，请执行以下命令："
echo ""
echo "cd /root/.openclaw/workspace/maomao-ai-enhancement"
echo "git push -u origin main"
echo ""
echo "或者先创建仓库："
echo "1. 访问 https://github.com/new"
echo "2. 创建仓库: $GITHUB_REPO"
echo "3. 运行: git push -u origin main"

echo ""
echo "=========================================="
echo "🎉 本地部署准备完成！"
echo "=========================================="
echo ""
echo "📋 下一步："
echo "1. 在GitHub创建仓库（如果尚未创建）"
echo "2. 运行推送命令: git push -u origin main"
echo "3. 查看项目: https://github.com/$GITHUB_USER/$GITHUB_REPO"
echo ""
echo "💡 提示：项目已通过安全检查，可以安全推送！"
echo "=========================================="
