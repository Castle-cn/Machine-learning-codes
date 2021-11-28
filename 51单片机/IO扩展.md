## IO扩展

​		51单片机 IO 口非常有限，如果想要连接更多外围设备，此时可以通过 IO 扩展来实现。

​		使用的芯片是 74HC595。开发板板载 1 个 74HC595 芯片，**仅需单片机 3 个 IO 口即可扩展 8 个**，如果需要还可以将 2 个 74HC595 级联扩展出 16 个 IO，这就实现用少数 IO 资源控制多个设备。

​		开发板上的 74HC595 模块电路如下图所示：

<img src="E:\markdown\51单片机\pics\QQ截图20211111202716.png" alt="QQ截图20211111202716" style="zoom: 67%;" />

- RCLK: 存储寄存器时钟输入

- SRCLK: 移位寄存器时钟输入

- SER: 串行数据输入

	![image-20211112095856365](E:\markdown\51单片机\pics\image-20211112095856365.png)

​		做 LED 点阵实验时，一定要将 LED 点阵旁的 J24 黄色跳线帽短接到 GND一端。

<img src="E:\markdown\51单片机\pics\QQ截图20211111223622.png" alt="QQ截图20211111223622"  />

### 实验代码

```c
#include "public.h"
#define LEDDZ_COL_PORT P0

sbit SRCLK = P3 ^ 6;
sbit RCLK_1 = P3 ^ 5;
sbit SER = P3 ^ 4;

u8 ghc595_buf[8] = {0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80};

/**
 * @brief 向 74HC595 写入一个字节的数据
 * @param dat
 */
void hc595_write_data(u8 dat) {
    u8 i = 0;
    for (i = 0; i < 8; i++) {
        SER = dat >> 7;
        dat <<= 1;
        SRCLK = 0;
        delay_10us(1);
        SRCLK = 1;
        delay_10us(1);
    }
    RCLK_1 = 0;
    delay_10us(1);
    RCLK_1 = 1;
}

void main() {
    u8 i = 0;
    LEDDZ_COL_PORT = 0x00;
    while (1) {
        for (i = 0; i < 8; i++) {
            hc595_write_data(0x00);
            hc595_write_data(ghc595_buf[i]);
            delay_ms(500);
        }
    }
}
```

### 实验现象

​		8*8LED 点阵以一行循环滚动显示