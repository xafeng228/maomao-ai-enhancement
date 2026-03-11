#!/bin/bash
echo "🔒 智能安全检查 v2.0"
echo "===================="

# 检查真实的密钥（排除示例）
echo "1. 检查真实的硬编码密钥..."
real_found=0

# 检查OpenAI密钥（排除示例）
if grep -r "sk-" --include="*.py" --include="*.md" --include="*.txt" . 2>/dev/null | grep -v "example" | grep -v "your_" | grep -v "placeholder" | grep -q "sk-"; then
    echo "❌ 发现可能的真实OpenAI密钥"
    real_found=1
else
    echo "✅ 没有发现真实的OpenAI密钥"
fi

# 检查GitHub令牌（排除示例）
if grep -r "ghp_" --include="*.py" --include="*.md" --include="*.txt" . 2>/dev/null | grep -v "example" | grep -v "your_" | grep -v "placeholder" | grep -q "ghp_"; then
    echo "❌ 发现可能的真实GitHub令牌"
    real_found=1
else
    echo "✅ 没有发现真实的GitHub令牌"
fi

echo ""
echo "2. 检查敏感文件管理..."
if [ -f ".gitignore" ] && grep -q "^\\.env$" .gitignore; then
    echo "✅ .gitignore正确配置了.env"
else
    echo "❌ .gitignore配置有问题"
    real_found=1
fi

if [ -f ".env.example" ] && ! [ -f ".env" ]; then
    echo "✅ 只有示例文件，没有真实的.env文件"
else
    if [ -f ".env" ]; then
        echo "⚠️  发现.env文件，请检查是否包含真实密钥"
        # 检查.env文件内容
        if grep -q "your_" .env || grep -q "example" .env || grep -q "placeholder" .env; then
            echo "  ✅ .env文件看起来是示例"
        else
            echo "  ❌ .env文件可能包含真实密钥！"
            real_found=1
        fi
    fi
fi

echo ""
echo "3. 最终安全评估..."
if [ $real_found -eq 0 ]; then
    echo "🎉 安全检查通过！"
    echo "✅ 项目可以安全地部署到GitHub"
    echo "✅ 没有发现真实的敏感信息"
    echo "✅ 配置管理正确"
    exit 0
else
    echo "❌ 安全检查失败！"
    echo ""
    echo "🚨 需要立即修复："
    echo "1. 移除所有硬编码的真实API密钥"
    echo "2. 确保只有.env.example（示例文件）"
    echo "3. 确认.gitignore包含.env"
    echo "4. 重新运行安全检查"
    exit 1
fi
