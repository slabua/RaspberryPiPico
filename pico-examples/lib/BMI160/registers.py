# register definitions
CHIP_ID           = const(0x00)
PMU_STATUS        = const(0x03)
GYRO_X_L          = const(0x0C)
GYRO_X_H          = const(0x0D)
GYRO_Y_L          = const(0x0E)
GYRO_Y_H          = const(0x0F)
GYRO_Z_L          = const(0x10)
GYRO_Z_H          = const(0x11)
ACCEL_X_L         = const(0x12)
ACCEL_X_H         = const(0x13)
ACCEL_Y_L         = const(0x14)
ACCEL_Y_H         = const(0x15)
ACCEL_Z_L         = const(0x16)
ACCEL_Z_H         = const(0x17)
STATUS            = const(0x1B)
INT_STATUS_0      = const(0x1C)
INT_STATUS_1      = const(0x1D)
INT_STATUS_2      = const(0x1E)
INT_STATUS_3      = const(0x1F)
TEMP_L            = const(0x20)
TEMP_H            = const(0x21)
FIFO_LENGTH_0     = const(0x22)
FIFO_LENGTH_1     = const(0x23)
FIFO_DATA         = const(0x24)
ACCEL_CONF        = const(0X40)
ACCEL_RANGE       = const(0X41)
GYRO_CONF         = const(0X42)
GYRO_RANGE        = const(0X43)
FIFO_CONFIG_0     = const(0x46)
FIFO_CONFIG_1     = const(0x47)
INT_EN_0          = const(0x50)
INT_EN_1          = const(0x51)
INT_EN_2          = const(0x52)
INT_OUT_CTRL      = const(0x53)
INT_LATCH         = const(0x54)
INT_MAP_0         = const(0x55)
INT_MAP_1         = const(0x56)
INT_MAP_2         = const(0x57)
INT_LOWHIGH_0     = const(0x5A)
INT_LOWHIGH_1     = const(0x5B)
INT_LOWHIGH_2     = const(0x5C)
INT_LOWHIGH_3     = const(0x5D)
INT_LOWHIGH_4     = const(0x5E)
INT_MOTION_0      = const(0x5F)
INT_MOTION_1      = const(0x60)
INT_MOTION_2      = const(0x61)
INT_MOTION_3      = const(0x62)
INT_TAP_0         = const(0x63)
INT_TAP_1         = const(0x64)
FOC_CONF          = const(0x69)
OFFSET_0          = const(0x71)
OFFSET_1          = const(0x72)
OFFSET_2          = const(0x73)
OFFSET_3          = const(0x74)
OFFSET_4          = const(0x75)
OFFSET_5          = const(0x76)
OFFSET_6          = const(0x77)
STEP_CNT_L        = const(0x78)
STEP_CNT_H        = const(0x79)
STEP_CONF_0       = const(0x7A)
STEP_CONF_1       = const(0x7B)
STEP_CONF_0_NOR   = const(0x15)
STEP_CONF_0_SEN   = const(0x2D)
STEP_CONF_0_ROB   = const(0x1D)
STEP_CONF_1_NOR   = const(0x03)
STEP_CONF_1_SEN   = const(0x00)
STEP_CONF_1_ROB   = const(0x07)
CMD               = const(0x7E)