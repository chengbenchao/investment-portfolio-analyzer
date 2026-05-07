#!/bin/bash
# 遗留脚本：cron 配置路径已过时，需重写后才能作为正式入口
# 设置定时任务来获取A股实时数据

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FETCH_SCRIPT="$SCRIPT_DIR/fetch_real_data.py"
LOG_FILE="$SCRIPT_DIR/stock_data.log"

echo "📊 A股实时数据定时任务设置"
echo "================================"
echo ""

# 检查Python脚本是否存在
if [ ! -f "$FETCH_SCRIPT" ]; then
    echo "❌ 错误: 找不到脚本 $FETCH_SCRIPT"
    exit 1
fi

# 确保脚本可执行
chmod +x "$FETCH_SCRIPT"

# 设置cron任务（每30分钟执行一次）
CRON_JOB="*/30 * * * * cd '$SCRIPT_DIR' && python '$FETCH_SCRIPT' >> '$LOG_FILE' 2>&1"

echo "📝 建议的定时任务配置:"
echo ""
echo "方案1: 每30分钟获取一次 (推荐)"
echo "$CRON_JOB"
echo ""
echo "方案2: 每小时获取一次 (更节省)"
echo "0 * * * * cd '$SCRIPT_DIR' && python '$FETCH_SCRIPT' >> '$LOG_FILE' 2>&1"
echo ""
echo "方案3: 每天开盘期间每10分钟获取一次"
echo "*/10 9-15 * * 1-5 cd '$SCRIPT_DIR' && python '$FETCH_SCRIPT' >> '$LOG_FILE' 2>&1"
echo ""
echo "💡 使用方法:"
echo "1. 运行 'crontab -e' 编辑定时任务"
echo "2. 把上面的某一行添加到文件末尾"
echo "3. 保存退出"
echo ""
echo "📋 查看当前定时任务: crontab -l"
echo "📂 日志文件位置: $LOG_FILE"
echo ""

# 尝试直接添加到cron（可选）
read -p "🔧 要自动添加方案1的定时任务吗？(y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 先检查是否已存在
    (crontab -l 2>/dev/null | grep -v -F "$FETCH_SCRIPT" ; echo "$CRON_JOB") | crontab -
    if [ $? -eq 0 ]; then
        echo "✅ 定时任务已添加成功！"
        echo "📊 当前定时任务:"
        crontab -l
    else
        echo "❌ 添加失败，请手动添加"
    fi
else
    echo "👌 好的，请手动添加"
fi
