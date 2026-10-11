from machine import Pin, I2C
import struct
import time

def clear_screen():
    print("\x1b[2J\x1b[H", end="")

i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)

devices = i2c.scan()

print("I2C Devices found: ", devices)

# wake the mpu sensor up cuz it starts in sleep mode

MPU_ADDR = 0x68
PWR_MGMT_1 = 0x6B

i2c.writeto_mem(MPU_ADDR, PWR_MGMT_1, b"\x00")

while True:
    ACCEL_XOUT_H = 0x3B

    raw_data = i2c.readfrom_mem(MPU_ADDR, ACCEL_XOUT_H, 14)

    accel_x, accel_y, accel_z, temp, gyro_x, gyro_y, gyro_z = struct.unpack(">hhhhhhh", raw_data)

    acc_x_g = accel_x / 16384.0
    acc_y_g = accel_y / 16384.0
    acc_z_g = accel_z / 16384.0

    gyro_x_deg = gyro_x / 131.0
    gyro_y_deg = gyro_y / 131.0
    gyro_z_deg = gyro_z / 131.0

    print(f"Accel (g)   : X={acc_x_g:.2f}, Y={acc_y_g:.2f}, Z={acc_z_g:.2f}")
    print(f"Gyro (deg/s): X={gyro_x_deg:.1f}, Y={gyro_y_deg:.1f}, Z={gyro_z_deg:.1f}")
    time.sleep(0.5)