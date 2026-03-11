#!/bin/bash
# 简化版安全检查脚本

echo "🔍 运行简化安全检查..."
echo "======================"

# 检查常见的敏感模式
echo "检查硬编码的API密钥模式..."
PATTERNS=(
    "sk-[a-zA-Z0-9]{48}"
    "AKIA[0-9A-Z]{16}"
    "gh[pous]_[A-Za-z0-9_]{36}"
)

FOUND=0
for pattern in "${PATTERNS[@]}"; do
    if grep -r -n -i --include="*.py" --include="*.js" --include="*.json" \
        --include="*.yml" --include="*.yaml" --include="*.md" \
        -E "$pattern" . 2>/dev/null | grep -v ".git" | grep -v "SECURITY_GUIDE.md" | head -5; then
        echo "⚠️  可能发现硬编码的密钥模式: $pattern"
        FOUND=1
    fi
done

# 检查敏感文件
echo "检查敏感文件..."
if find . -name ".env" -type f 2>/dev/null | grep -q .; then
    echo "⚠️  发现.env文件，请确保不包含真实密钥"
    FOUND=1
fi

if find . -name "*.key" -o -name "*.pem" -o -name "secrets.json" 2>/dev/null | grep -q .; then
    echo "⚠️  发现密钥文件"
    find . -name "*.key" -o -name "*.pem" -o -name "secrets.json" 2>/dev/null
    FOUND=1
fi

# 检查.gitignore
echo "检查.gitignore配置..."
if ! grep -q "^\\.env$" .gitignore 2>/dev/null; then
    echo "⚠️  .gitignore中没有包含.env文件"
    FOUND=1
fi

# 结果
if [ $FOUND -eq 0 ]; then
    echo "✅ 安全检查通过！没有发现明显的安全问题"
    exit 0
else
    echo "❌ 安全检查发现潜在问题"
    echo ""
    echo "📋 修复建议："
    echo "1. 确保没有硬编码的API密钥"
    echo "2. 敏感文件应该在.gitignore中"
    echo "3. 使用环境变量管理配置"
    exit 1
fi
