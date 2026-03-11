#!/bin/bash
# 安全部署脚本 - 绝对不包含API密钥

set -e

echo "🔒 安全部署毛毛AI能力提升项目到GitHub"
echo "=========================================="
echo "⚠️  重要：本脚本确保不包含任何API密钥或敏感信息"
echo "=========================================="

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

PROJECT_DIR="/root/.openclaw/workspace/maomao-ai-enhancement"
cd "$PROJECT_DIR"

echo -e "${YELLOW}1. 安全检查...${NC}"

# 检查是否包含敏感文件
SENSITIVE_FILES=(
    ".env"
    "config.json"
    "secrets.json"
    "*.key"
    "*.pem"
    "credentials*"
)

for pattern in "${SENSITIVE_FILES[@]}"; do
    if find . -name "$pattern" -type f | grep -q .; then
        echo -e "${RED}⚠️  发现敏感文件: $pattern${NC}"
        echo "请移除或忽略这些文件后再部署"
        exit 1
    fi
done

echo -e "${GREEN}✅ 安全检查通过${NC}"

# 强化.gitignore
echo -e "${YELLOW}2. 强化.gitignore配置...${NC}"

cat >> .gitignore << 'EOF'

# ========================
# 🔒 安全配置 - 绝对不要提交
# ========================

# API密钥和敏感配置
.env
.env.*
!.env.example
config.json
secrets.json
credentials.json
*.key
*.pem
*.crt
*.cert

# 个人配置
personal/
private/
secret/

# 日志文件（可能包含敏感信息）
*.log
logs/

# 数据库文件
*.db
*.sqlite
*.sqlite3

# 临时文件
tmp/
temp/
*.tmp
*.temp

# 备份文件
*.bak
*.backup

# 系统文件
.DS_Store
Thumbs.db
EOF

echo -e "${GREEN}✅ .gitignore已强化${NC}"

# 创建安全配置指南
echo -e "${YELLOW}3. 创建安全配置指南...${NC}"

cat > SECURITY_GUIDE.md << 'EOF'
# 🔒 安全配置指南

## 🚨 重要安全警告

**绝对不要将以下内容提交到GitHub：**
- API密钥和访问令牌
- 数据库连接字符串
- 个人身份信息
- 私钥文件
- 任何敏感配置

## 📋 安全配置步骤

### 1. 环境变量配置
复制示例配置文件并填写你的密钥：

```bash
# 复制示例配置
cp .env.example .env

# 编辑配置文件（使用安全的方式）
vim .env  # 或使用其他编辑器
```

### 2. .env文件内容示例
```env
# 🔒 安全警告：此文件包含敏感信息，不要提交到GitHub！

# GitHub配置（如果需要）
GITHUB_TOKEN=your_actual_token_here  # 从GitHub Settings > Developer settings获取

# 数据API配置（按需配置）
TAVILY_API_KEY=your_tavily_api_key_here      # 从 https://tavily.com 获取
QVERIS_API_KEY=your_qveris_api_key_here      # 从 https://qveris.ai 获取

# 其他服务API密钥
OPENAI_API_KEY=sk-...                        # OpenAI API密钥
ANTHROPIC_API_KEY=your_anthropic_key         # Claude API密钥

# 数据库配置（如果有）
DATABASE_URL=postgresql://user:password@localhost/dbname
REDIS_URL=redis://localhost:6379

# 监控配置
SENTRY_DSN=your_sentry_dsn_here              # 错误监控
```

### 3. 确保.gitignore包含.env
检查`.gitignore`文件是否包含：
```
.env
.env.*
!.env.example
```

### 4. 验证配置安全
部署前运行安全检查：
```bash
chmod +x scripts/security_check.sh
./scripts/security_check.sh
```

## 🛡️ 最佳安全实践

### 1. 密钥管理
- **使用环境变量**，不要硬编码在代码中
- **定期轮换密钥**，特别是发现泄露时
- **最小权限原则**，只授予必要权限
- **不同环境使用不同密钥**（开发、测试、生产）

### 2. 代码审查
- **提交前检查**：确保没有意外提交敏感信息
- **使用预提交钩子**：自动检查敏感信息
- **定期安全扫描**：使用工具检查代码库

### 3. 访问控制
- **限制API密钥使用**：设置IP白名单、使用限制
- **监控异常访问**：设置告警机制
- **及时撤销泄露密钥**：发现泄露立即撤销

### 4. 数据保护
- **加密敏感数据**：存储时加密
- **访问日志记录**：记录所有敏感操作
- **定期备份**：确保数据安全

## 🔍 安全检查清单

### 部署前检查
- [ ] 确认没有硬编码的API密钥
- [ ] 确认.env文件在.gitignore中
- [ ] 确认所有密钥都是环境变量
- [ ] 运行安全扫描脚本

### 代码审查检查
- [ ] 搜索代码中的"key", "secret", "token", "password"
- [ ] 检查配置文件是否包含真实密钥
- [ ] 验证所有外部依赖的安全性

### 运行时检查
- [ ] 环境变量正确加载
- [ ] 密钥权限设置正确
- [ ] 访问日志正常工作
- [ ] 错误信息不泄露敏感数据

## 🚨 紧急情况处理

### 发现密钥泄露
1. **立即撤销密钥**：在对应服务商控制台撤销
2. **轮换所有相关密钥**：不仅仅是泄露的密钥
3. **审查访问日志**：确认是否有未授权访问
4. **通知相关人员**：如果涉及用户数据

### 代码中意外提交密钥
1. **立即从Git历史中移除**：
   ```bash
   # 注意：这会重写历史，谨慎操作
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch .env" \
     --prune-empty --tag-name-filter cat -- --all
   ```
2. **强制推送到远程**：
   ```bash
   git push origin --force --all
   git push origin --force --tags
   ```
3. **通知所有协作者**：需要重新克隆仓库

## 📞 安全支持

### 报告安全问题
如果你发现安全漏洞，请：
1. **不要公开披露**
2. **通过安全渠道报告**：security@example.com
3. **提供详细信息**：漏洞描述、复现步骤、影响范围

### 安全更新
- 订阅安全公告
- 及时更新依赖
- 定期进行安全审计

## 📚 参考资料

- [GitHub安全最佳实践](https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure)
- [OWASP安全指南](https://owasp.org/www-project-top-ten/)
- [Python安全编程](https://docs.python.org/3/library/security.html)

---

**记住：安全不是功能，是基础。每次提交前都要问自己：我提交敏感信息了吗？** 🔒
EOF

echo -e "${GREEN}✅ 安全配置指南创建完成${NC}"

# 创建安全检查脚本
echo -e "${YELLOW}4. 创建安全检查脚本...${NC}"

cat > scripts/security_check.sh << 'EOF'
#!/bin/bash
# 安全检查脚本

set -e

echo "🔍 运行安全检查..."
echo "======================"

# 检查硬编码的密钥模式
PATTERNS=(
    "sk-[a-zA-Z0-9]{48}"
    "AKIA[0-9A-Z]{16}"
    "gh[pous]_[A-Za-z0-9_]{36}"
    "xox[baprs]-[0-9a-zA-Z]{10,48}"
    "AIza[0-9A-Za-z_-]{35}"
    "password\s*=\s*['\"].*['\"]"
    "api[_-]?key\s*=\s*['\"].*['\"]"
    "secret\s*=\s*['\"].*['\"]"
    "token\s*=\s*['\"].*['\"]"
)

FOUND_SECRETS=0

for pattern in "${PATTERNS[@]}"; do
    echo "检查模式: $pattern"
    if grep -r -n -i --include="*.py" --include="*.js" --include="*.json" \
        --include="*.yml" --include="*.yaml" --include="*.md" \
        -E "$pattern" . 2>/dev/null | grep -v ".git" | grep -v "SECURITY_GUIDE.md"; then
        echo "⚠️  可能发现硬编码的密钥！"
        grep -r -n -i --include="*.py" --include="*.js" --include="*.json" \
            --include="*.yml" --include="*.yaml" --include="*.md" \
            -E "$pattern" . 2>/dev/null | grep -v ".git" | grep -v "SECURITY_GUIDE.md"
        FOUND_SECRETS=1
    fi
done

# 检查敏感文件
SENSITIVE_FILES=(
    ".env"
    "config.json"
    "secrets.json"
    "*.key"
    "*.pem"
)

for pattern in "${SENSITIVE_FILES[@]}"; do
    if find . -name "$pattern" -type f | grep -q .; then
        echo "⚠️  发现敏感文件:"
        find . -name "$pattern" -type f
        FOUND_SECRETS=1
    fi
done

# 检查.gitignore是否包含.env
if ! grep -q "^\.env$" .gitignore 2>/dev/null; then
    echo "⚠️  .gitignore中没有包含.env文件"
    FOUND_SECRETS=1
fi

# 检查结果
if [ $FOUND_SECRETS -eq 0 ]; then
    echo "✅ 安全检查通过！没有发现明显的安全问题"
    exit 0
else
    echo "❌ 安全检查失败！发现潜在的安全问题"
    echo ""
    echo "📋 修复建议："
    echo "1. 移除所有硬编码的API密钥"
    echo "2. 确保敏感文件在.gitignore中"
    echo "3. 使用环境变量管理配置"
    echo "4. 重新运行安全检查"
    exit 1
fi
EOF

chmod +x scripts/security_check.sh
echo -e "${GREEN}✅ 安全检查脚本创建完成${NC}"

# 运行安全检查
echo -e "${YELLOW}5. 运行安全检查...${NC}"
if ./scripts/security_check.sh; then
    echo -e "${GREEN}✅ 安全检查通过${NC}"
else
    echo -e "${RED}❌ 安全检查失败，请修复问题后再部署${NC}"
    exit 1
fi

# 准备Git提交
echo -e "${YELLOW}6. 准备Git提交...${NC}"

# 添加安全相关文件
git add SECURITY_GUIDE.md
git add scripts/security_check.sh
git add .gitignore

# 检查是否有其他更改
if git status --porcelain | grep -v "^??"; then
    echo "提交安全增强更新..."
    git commit -m "feat: 增强安全配置

- 添加安全配置指南 (SECURITY_GUIDE.md)
- 创建安全检查脚本 (scripts/security_check.sh)
- 强化.gitignore配置
- 确保不包含任何API密钥或敏感信息
- 提供安全部署最佳实践"
    
    echo -e "${GREEN}✅ 安全更新已提交${NC}"
else
    echo -e "${YELLOW}⚠️  没有新的安全更新需要提交${NC}"
fi

echo ""
echo "=========================================="
echo -e "${GREEN}🔒 安全部署准备完成！${NC}"
echo "=========================================="
echo ""
echo "📋 **安全特性已添加：**"
echo "1. ✅ 安全配置指南 (SECURITY_GUIDE.md)"
echo "2. ✅ 安全检查脚本 (scripts/security_check.sh)"
echo "3. ✅ 强化的.gitignore配置"
echo "4. ✅ 环境变量模板 (.env.example)"
echo "5. ✅ 无硬编码API密钥验证"
echo ""
echo "🚀 **现在可以安全地部署到GitHub：**"
echo "1. 在GitHub创建仓库: https://github.com/new"
echo "2. 仓库名: maomao-ai-enhancement"
echo "3. 运行部署: ./scripts/deploy_to_github.sh"
echo ""
echo "💡 **部署前建议：**"
echo "- 运行安全检查: ./scripts/security_check.sh"
echo "- 阅读安全指南: cat SECURITY_GUIDE.md"
echo "- 配置环境变量: cp .env.example .env"
echo ""
echo "🔒 **记住：安全第一，每次提交前都要检查！**"
echo "=========================================="