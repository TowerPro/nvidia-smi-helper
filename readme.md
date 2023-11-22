# nvidia-smi helper

* 目前main分支中存放的是最新的代码

## 基础功能：nVidia-smi Helper
* 前端页面显示卡号，gpu在线情况，使用情况已经使用者的姓名和pid
* 有三个颜色显示：
    * 红色：gpu offline
    * 橙色：gpu正常使用，但是不建议再添加程序
    * 绿色：gpu正常使用，可以在评估后继续添加程序（设置阈值60%）

## 进阶功能
* 设置了抢卡功能，当3、5号卡空闲时（指完全没有程序在运行）会自动运行fuckGPU.sh脚本
* 可以手动开关抢卡功能，进入网页页面，连续点击h1标签（也就是nVidia-smi Helper）5次，可以看关抢卡功能
    * 可以F12进入console，会打印出rob gpu on/off的信息
    * 该功能的使用方式：抢到卡了，但是fuckGPU.sh脚本跑的程序不是自己想要的，可以先关闭抢卡功能，之后kill对应进程，再挂上自己的程序，最后再连续点击5次开启抢卡脚本
    * 再开启是可以保证训练完之后这张卡的所有者还是自己

## 程序使用
* 运行run.sh开始程序，可以设置为开启自启
* fuckGPU.sh可以替换为自己的训练脚本