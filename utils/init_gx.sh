#!/usr/bin/expect -f
# 指定该脚本由expect解释器运行，expect是用于自动化交互式命令行程序的工具
# 注意expect语法的注释必须单独一行
# 设置等待响应的超时时间为10秒
set timeout 10
#启动great_expectations init命令，初始化Great Expectations项目
spawn great_expectations init
 # 等待命令行输出包含 “OK to proceed?” 的提示
expect "OK to proceed?*"
# 自动发送“y”并回车，表示确认继续
send "y\r" 
# 等待进程结束（End Of File）
expect eof 