#!/bin/bash
# 毛毛AI增强系统 - Web界面启动脚本

echo "🧠 毛毛AI增强系统 - Web界面启动"
echo "============================================================"
echo "🎯 第一阶段优化扩展: 基础Web界面"
echo "⏰ 开始时间: $(date '+%H:%M:%S GMT+8')"
echo "============================================================"

# 检查Python环境
echo "🔍 检查Python环境..."
python3 --version
if [ $? -ne 0 ]; then
    echo "❌ Python3未安装"
    exit 1
fi

# 检查FastAPI依赖
echo "🔍 检查FastAPI依赖..."
if ! python3 -c "import fastapi" 2>/dev/null; then
    echo "⚠️ FastAPI未安装，正在安装..."
    pip3 install fastapi uvicorn[standard]
else
    echo "✅ FastAPI已安装"
fi

# 创建必要的目录
echo "📁 创建目录结构..."
mkdir -p /root/.openclaw/workspace/maomao-enhanced-system/web_interface/backend
mkdir -p /root/.openclaw/workspace/maomao-enhanced-system/web_interface/frontend

# 检查后端文件
echo "🔍 检查后端文件..."
if [ -f "/root/.openclaw/workspace/maomao-enhanced-system/web_interface/backend/main.py" ]; then
    echo "✅ 后端文件存在"
else
    echo "❌ 后端文件不存在"
    exit 1
fi

# 检查前端文件
echo "🔍 检查前端文件..."
if [ -f "/root/.openclaw/workspace/maomao-enhanced-system/web_interface/frontend/index.html" ]; then
    echo "✅ 前端文件存在"
else
    echo "❌ 前端文件不存在"
    exit 1
fi

# 启动后端服务
echo "🚀 启动后端服务..."
cd /root/.openclaw/workspace/maomao-enhanced-system/web_interface/backend

# 检查是否已经在运行
if lsof -i:8000 >/dev/null 2>&1; then
    echo "⚠️ 端口8000已被占用，尝试停止现有服务..."
    pkill -f "uvicorn.*8000" 2>/dev/null
    sleep 2
fi

# 启动服务
echo "🌐 启动FastAPI服务..."
python3 main.py &
BACKEND_PID=$!

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 5

# 检查服务是否启动成功
if curl -s http://127.0.0.1:8000/health >/dev/null 2>&1; then
    echo "✅ 后端服务启动成功 (PID: $BACKEND_PID)"
else
    echo "❌ 后端服务启动失败"
    exit 1
fi

# 显示访问信息
echo ""
echo "============================================================"
echo "🎉 毛毛AI增强系统Web界面启动成功!"
echo "============================================================"
echo "🌐 访问地址:"
echo "   前端界面: file:///root/.openclaw/workspace/maomao-enhanced-system/web_interface/frontend/index.html"
echo "   后端API: http://127.0.0.1:8000"
echo "   API文档: http://127.0.0.1:8000/docs"
echo ""
echo "📊 系统信息:"
echo "   版本: 3.0.0-alpha"
echo "   阶段: 第一阶段优化扩展"
echo "   进度: 33% (多渠道推送 ✅ | Web界面 🔄 | 文件导入 ⏳)"
echo ""
echo "🔧 功能说明:"
echo "   1. 系统状态监控"
echo "   2. 四维提升展示"
echo "   3. 优化扩展进度"
echo "   4. 自选股管理"
echo "   5. 股票分析(开发中)"
echo ""
echo "🛑 停止服务:"
echo "   kill $BACKEND_PID"
echo "   或运行: pkill -f 'uvicorn.*8000'"
echo "============================================================"

# 保存PID到文件
echo $BACKEND_PID > /tmp/maomao_web_backend.pid

# 等待用户输入退出
echo ""
read -p "按Enter键停止服务..." </dev/tty

# 停止服务
echo "🛑 停止后端服务..."
kill $BACKEND_PID 2>/dev/null
pkill -f "uvicorn.*8000" 2>/dev/null

echo "✅ 服务已停止"
echo "============================================================"