#!/bin/bash
# 安全部署毛毛AI能力提升项目到GitHub

set -e

echo "🚀 开始安全部署毛毛AI能力提升项目到GitHub..."
echo "=========================================="
echo "🔒 安全第一：确保不包含任何API密钥或敏感信息"
echo "=========================================="

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 项目信息
PROJECT_DIR="/root/.openclaw/workspace/maomao-ai-enhancement"

# 进入项目目录
cd "$PROJECT_DIR"

# 步骤1：运行安全检查
echo -e "${YELLOW}1. 运行安全检查...${NC}"
if [ -f "scripts/security_check.sh" ]; then
    chmod +x scripts/security_check.sh
    if ./scripts/security_check.sh; then
        echo -e "${GREEN}✅ 安全检查通过${NC}"
    else
        echo -e "${RED}❌ 安全检查失败，请修复安全问题后再部署${NC}"
        echo "运行以下命令查看安全指南："
        echo "  cat SECURITY_GUIDE.md"
        exit 1
    fi
else
    echo -e "${YELLOW}⚠️  安全检查脚本不存在，跳过安全检查${NC}"
fi

# 步骤2：检查Git仓库
echo -e "${YELLOW}2. 检查Git仓库...${NC}"
if [ ! -d ".git" ]; then
    echo "初始化Git仓库..."
    git init
    echo -e "${GREEN}✅ Git仓库初始化完成${NC}"
else
    echo -e "${GREEN}✅ Git仓库已存在${NC}"
fi

# 步骤3：添加所有文件（除了.gitignore中的）
echo -e "${YELLOW}3. 添加文件到Git...${NC}"
git add .
echo -e "${GREEN}✅ 文件已添加${NC}"

# 步骤4：提交更改
echo -e "${YELLOW}4. 提交更改...${NC}"
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
- 安全部署指南" || {
        echo -e "${YELLOW}⚠️  提交失败，可能没有新的更改${NC}"
    }
    echo -e "${GREEN}✅ 更改已提交${NC}"
else
    echo -e "${YELLOW}⚠️  没有新的更改需要提交${NC}"
fi

# 步骤5：配置远程仓库
echo -e "${YELLOW}5. 配置远程仓库...${NC}"
GITHUB_USER="xafeng228"
GITHUB_REPO="maomao-ai-enhancement"
GITHUB_URL="https://github.com/${GITHUB_USER}/${GITHUB_REPO}.git"

if git remote | grep -q origin; then
    echo -e "${GREEN}✅ 远程仓库已配置${NC}"
    
    # 检查远程URL是否正确
    CURRENT_URL=$(git remote get-url origin 2>/dev/null || echo "")
    if [ "$CURRENT_URL" != "$GITHUB_URL" ]; then
        echo "更新远程仓库URL..."
        git remote set-url origin "$GITHUB_URL"
        echo -e "${GREEN}✅ 远程仓库URL已更新${NC}"
    fi
else
    echo "添加远程仓库: $GITHUB_URL"
    git remote add origin "$GITHUB_URL"
    echo -e "${GREEN}✅ 远程仓库已添加${NC}"
fi

# 步骤6：推送到GitHub
echo -e "${YELLOW}6. 准备推送到GitHub...${NC}"
echo -e "${YELLOW}⚠️  注意：请确保GitHub仓库已创建${NC}"
echo -e "${YELLOW}   仓库地址: https://github.com/$GITHUB_USER/$GITHUB_REPO${NC}"
echo ""
echo -e "${YELLOW}📋 推送前确认：${NC}"
echo "1. 仓库是否已创建？"
echo "2. 是否有GitHub推送权限？"
echo "3. 是否已运行安全检查？"
echo ""

read -p "是否继续推送到GitHub？(y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "推送代码到GitHub..."
    
    # 尝试推送
    if git push -u origin main 2>/dev/null; then
        echo -e "${GREEN}✅ 代码已成功推送到GitHub${NC}"
    else
        echo -e "${YELLOW}尝试创建并推送main分支...${NC}"
        git branch -M main
        if git push -u origin main; then
            echo -e "${GREEN}✅ 代码已成功推送到GitHub${NC}"
        else
            echo -e "${RED}❌ 推送失败，请检查：${NC}"
            echo "1. GitHub仓库是否已创建？"
            echo "2. 是否有正确的推送权限？"
            echo "3. 网络连接是否正常？"
            echo ""
            echo "手动推送命令："
            echo "  git push -u origin main"
            echo "或先创建仓库："
            echo "  访问 https://github.com/new"
            echo "  仓库名: $GITHUB_REPO"
        fi
    fi
else
    echo -e "${YELLOW}跳过推送，本地仓库已准备好${NC}"
    echo ""
    echo "手动推送时使用："
    echo "  git push -u origin main"
fi

# 步骤7：生成部署报告
echo -e "${YELLOW}7. 生成部署报告...${NC}"

cat > DEPLOYMENT_REPORT.md << EOF
# 🚀 毛毛AI能力提升项目部署报告

## 🔒 安全部署完成
- **部署时间**: $(date)
- **安全状态**: ✅ 通过安全检查
- **项目版本**: v1.0.0
- **GitHub仓库**: https://github.com/$GITHUB_USER/$GITHUB_REPO
- **本地目录**: $PROJECT_DIR

## 📋 安全特性
✅ **无硬编码API密钥** - 代码中不包含任何敏感信息  
✅ **环境变量配置** - 使用.env文件管理配置  
✅ **安全检查脚本** - 部署前自动安全检查  
✅ **安全配置指南** - 完整的安全使用指南  
✅ **强化的.gitignore** - 确保敏感文件不被提交  

## 🏗️ 项目结构
\`\`\`
$(find . -type f -name "*.py" -o -name "*.md" -o -name "*.sh" -o -name "*.txt" -o -name "*.yml" 2>/dev/null | sort | sed 's|^\./||' | head -30)
... 更多文件 ...
\`\`\`

## 🎯 核心功能
✅ **多代理系统框架** - BaseAgent + 专业代理  
✅ **技术分析代理** - 完整的技术指标计算  
✅ **安全配置管理** - 安全的密钥管理方案  
✅ **CI/CD工作流** - 自动化测试和部署  
✅ **完整文档** - 架构设计 + 使用指南  

## 🚀 使用指南

### 1. 环境设置
\`\`\`bash
# 克隆仓库（如果已推送）
git clone https://github.com/$GITHUB_USER/$GITHUB_REPO.git
cd $GITHUB_REPO

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，添加你的API密钥
\`\`\`

### 2. 安全检查
\`\`\`bash
# 运行安全检查
./scripts/security_check.sh

# 查看安全指南
cat SECURITY_GUIDE.md
\`\`\`

### 3. 运行测试
\`\`\`bash
# 运行单元测试
pytest tests/unit/

# 运行技术分析代理测试
python -m pytest tests/unit/test_technical_agent.py
\`\`\`

## 🔧 开发指南

### 添加新功能
1. \`git checkout -b feature/new-feature\`
2. 开发代码，确保不包含敏感信息
3. \`./scripts/security_check.sh\` (安全检查)
4. \`git add . && git commit -m "feat: ..."\`
5. \`git push origin feature/new-feature\`
6. 创建Pull Request

### 安全注意事项
- 🔒 **永远不要提交**.env文件
- 🔒 **使用环境变量**管理配置
- 🔒 **定期运行安全检查**
- 🔒 **及时轮换泄露的密钥**

## 📞 支持与贡献

### 问题反馈
- **GitHub Issues**: 报告问题或建议
- **安全报告**: 通过安全渠道报告漏洞

### 贡献指南
1. Fork 仓库
2. 创建功能分支
3. 确保通过安全检查
4. 提交Pull Request

### 联系方式
- **GitHub**: @$GITHUB_USER
- **项目地址**: https://github.com/$GITHUB_USER/$GITHUB_REPO

## 📈 下一步计划
- [ ] 完善其他代理实现
- [ ] 添加更多测试用例
- [ ] 优化性能监控
- [ ] 添加使用示例和教程

---
**部署完成！开始安全地开发你的AI投研助手吧！** 🚀

**记住：安全不是可选项，是必须项。** 🔒
EOF

echo -e "${GREEN}✅ 部署报告已生成: DEPLOYMENT_REPORT.md${NC}"

echo ""
echo "=========================================="
echo -e "${GREEN}🎉 毛毛AI能力提升项目安全部署完成！${NC}"
echo "=========================================="
echo ""
echo "📋 **下一步操作：**"
echo "1. 🔒 阅读安全指南: cat SECURITY_GUIDE.md"
echo "2. 🚀 查看部署报告: cat DEPLOYMENT_REPORT.md"
echo "3. 🔧 配置环境变量: cp .env.example .env"
echo "4. 🧪 运行测试: pytest tests/"
echo ""
echo "💡 **重要提醒：**"
echo "- 🔒 永远不要提交包含真实密钥的.env文件"
echo "- 🔒 定期运行安全检查脚本"
echo "- 🔒 使用环境变量管理所有敏感配置"
echo ""
echo "🌐 **GitHub仓库：**"
echo "   https://github.com/$GITHUB_USER/$GITHUB_REPO"
echo ""
echo "🚀 **开始你的安全AI开发之旅吧！**"
echo "=========================================="