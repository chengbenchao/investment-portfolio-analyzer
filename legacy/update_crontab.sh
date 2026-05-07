#!/bin/bash
# 遗留脚本：cron 覆盖逻辑仍依赖旧命令，需重写后才能正式使用
# 更新定时任务配置，添加A股数据自动更新

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
UPDATE_SCRIPT="$SCRIPT_DIR/fetch_real_data.py"
LOG_FILE="$SCRIPT_DIR/logs/data_update.log"

echo "📊 设置A股数据自动更新定时任务"
echo "================================"

# 创建日志目录
mkdir -p "$SCRIPT_DIR/logs"

# 备份当前crontab
crontab -l > "$SCRIPT_DIR/logs/crontab_backup_$(date +%Y%m%d_%H%M%S).txt" 2>/dev/null

# 新的定时任务配置
NEW_CRONTAB=$(cat <<EOF
# 原有的定时任务
*/2 * * * * /usr/bin/python3 /home/crontab.py > /dev/null 2>&1

# A股数据自动更新 - 工作日交易时间每小时更新一次
# 上午 9:30-11:30，下午 13:00-15:00
0 9-11 * * 1-5 cd $SCRIPT_DIR && python $UPDATE_SCRIPT >> $LOG_FILE 2>&1
0 13-15 * * 1-5 cd $SCRIPT_DIR && python $UPDATE_SCRIPT >> $LOG_FILE 2>&1

# 每天收盘后也更新一次（15:30）
30 15 * * 1-5 cd $SCRIPT_DIR && python $UPDATE_SCRIPT >> $LOG_FILE 2>&1
EOF
)

# 更新crontab
echo "$NEW_CRONTAB" | crontab -

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 定时任务更新成功！"
    echo ""
    echo "📋 当前定时任务配置："
    echo "------------------------"
    crontab -l
    echo ""
    echo "📂 日志文件：$LOG_FILE"
    echo ""
    echo "💡 使用说明："
    echo "  - 工作日交易时间每小时自动更新A股数据"
    echo "  - 更新日志保存在 logs/data_update.log"
    echo "  - 查看定时任务：crontab -l"
    echo "  - 编辑定时任务：crontab -e"
else
    echo "❌ 更新失败，请检查配置"
fi
