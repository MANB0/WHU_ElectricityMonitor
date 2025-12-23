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
  - Cookie
  - Accept
  - authorization
  - Host
  - Connection（此项也有可能为Proxy-Connection）
  - Referer
  - User-Agent
 
同时，根据GetReserve?MeterID=3002.001520.1也可以得到你的MeterID为3002.001520.1

## 修改power_monitor.py

在文件中，你需要修改两部分：邮箱配置、爬虫配置

### 邮箱配置

这里建议直接使用你的QQ邮箱，生成授权码后填入对应位置即可。RECEIVER_EMAILS中，你可以加入多个邮箱，使你的室友也能够收到邮件。

<img width="753" height="241" alt="image" src="https://github.com/user-attachments/assets/7ed90dd7-879f-4ba8-b2c7-f7949d82a445" />


### 爬虫配置

将前文中记录的信息依次填入对应的位置即可

<img width="1084" height="599" alt="image" src="https://github.com/user-attachments/assets/edc5b6b0-6674-4447-aca4-79bdea62cb20" />


完成以上配置后，你还可以自定义电费阈值MIN_BALANCE

## 操作

### 手动执行

在你对应的python环境下，安装requests软件包后，运行脚本即可

### 自动执行

你也可以将该文件上传到你的服务器上，然后使用crontab自动任务来进行执行

同时，如果没有服务器你也可以利用 **GitHub Actions** 来进行定时执行，具体的操作我没试过，可以问问ai
