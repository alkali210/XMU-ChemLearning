import serial
import time

ser = serial.Serial('COM4', 38400, timeout=1)

full_data = ""
last_time = time.time()
timeout = 0.5  # 0.5秒无新数据则结束

print("等待接收数据...")
while True:
    if ser.in_waiting:
        chunk = ser.read(ser.in_waiting).decode('utf-8')
        full_data += chunk
        last_time = time.time()
    else:
        if time.time() - last_time > timeout and full_data:
            break
    time.sleep(0.01)

print("完整数据:", full_data)
ser.close()
