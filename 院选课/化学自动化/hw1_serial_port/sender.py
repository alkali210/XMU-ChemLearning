import serial
import time

# 修改为你的COM口号（Windows下如 'COM3'，Linux下如 '/dev/ttyUSB0'）
ser = serial.Serial('COM4', 38400, timeout=1)

# 等待连接稳定
time.sleep(2)

# 构造要发送的信息
name = "CHR"  # 替换为你的名字
date_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
message = f"Name: {name}, DateTime: {date_time}\n"

# 发送数据（需编码为字节）
ser.write(message.encode('utf-8'))

print("发送完成:", message)

ser.close()
