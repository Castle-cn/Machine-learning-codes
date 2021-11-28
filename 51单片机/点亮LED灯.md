## LED灯

​		开发板上LED模块电路如下图所示:

![QQ截图20211105094107](E:\markdown\51单片机\pics\QQ截图20211105094107.png)

​		   ==要让 LED 发光即对应的阴极管脚应该为低电平，若为高电平则熄灭。==



#### LED点亮实验

```c
#include "reg52.h"

//P2 ^ x 用来控制引脚 P2.x
sbit LED1 = P2 ^ 0;

void main(){
	LED1 = 0;	//LED1 端口设置为低电平
	while(1){
	
	}	
}
```



#### LED闪烁实验

延时函数:

```c
typedef unsigned int u16; 
typedef unsigned char u8;

//如果 ten_us 等于 1，则 while 循环执行一次，调用该函数延时时间大 约 10us
void delay_10us(u16 ten_us) {
    while (ten_us--) {
    };
}
```



LED闪烁:

```c
sbit LED1 = P2 ^ 0;

void main() {
        while (1) {
        //点亮
        LED1 = 0;
        //延时大约450ms
        delay_10us(50000);
        //熄灭
        LED1 = 1;
        delay_10us(50000);
    }
}
```



LED流水灯:

```c
#define LED_PORT P2 //使用宏定义 P2 端口

void main() {
    u8 i = 0;
    while (1) {
        for (i = 0; i < 8; i++) {
            //将 0000 0001 进行左移, 因为低电平亮灯, 所以进行取反
            LED_PROT = ~(0x01 << i);
            delay_10us(50000);
        }
    }
}
```

