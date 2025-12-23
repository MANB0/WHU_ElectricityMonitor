# WHU_ElectricityMonitor
推送武汉大学学生宿舍电费情况，在低于阈值时发送邮件

# 使用方法
## 获取请求
首先打开网址，选择到你的宿舍：[水电服务平台](http://zwhqbsd.whu.edu.cn/MobilePayWeb/#/entrance)

当你打开以下界面后，使用F12唤出控制台

<img width="3837" height="1883" alt="image" src="https://github.com/user-attachments/assets/ac85f563-ff38-446a-b5fe-b51ffb21ad87" />

在控制台中，依次点击“网络”——“Fetch/XDR”，然后此时刷新界面，你就能够得到多个请求

<img width="980" height="638" alt="image" src="https://github.com/user-attachments/assets/77f0e140-23a1-4688-8dbf-bb985c3d7ec5" />

点击倒数第二个请求，也就是名为GetReserve?MeterID=3002.001520.1的，记录该条记录中的如下信息：

- 常规
  - 请求URL
  - 请求方法
- 请求标头
  - Accept
  - Authorization
  - Host
  - Connection（此项也有可能为Proxy-Connection）
  - Referer
  - User-Agent

## 修改power_monitor.py

在文件中，你需要修改两部分：发送邮箱、电费监控

### 发送邮箱

这里建议直接使用你的QQ邮箱，生成
