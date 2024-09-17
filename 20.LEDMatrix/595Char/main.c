#include<reg51.h>
#include<intrins.h>

sbit SRCLK=P3^6;
sbit RCLK=P3^5;
sbit SER=P3^4;

//--定义要使用的IO口--//
#define COMMONPORTS		P0


unsigned char code TAB[8]  = {0x7f,0xbf,0xdf,0xef,0xf7,0xfb,0xfd,0xfe};
unsigned int thutu = 0, check = 0, en = 0;
unsigned char  dulieu[8];   // chua packet


void delay(unsigned int time)
{
  unsigned int i,j;
  for(i=0;i<time;i++)
    for(j=0;j<50;j++);
}

void init (void)
{
	SCON=0X50;			//serial mode 1 Ren=1
	TMOD=0X20;			//timer 1 mode 2
	
	TH1=0xFD;				//baud 9600
	TL1=0xFD;
	ES=1;						//cho phep ngat
	EA=1;						
	TR1=1;					//bat timer 1
}


void serial_ISR (void) interrupt 4
{
	if (RI==1)
	{
		if(thutu==8)
		thutu = 0;
	dulieu[thutu] = SBUF;
	thutu++;
		RI = 0;
	}
}

void Hc595SendByte(unsigned char dat)
{
	unsigned char a;
	SRCLK=0;
	RCLK=0;
	for(a=0;a<8;a++)
	{
		SER=dat>>7;
		dat<<=1;

		SRCLK=1;
		_nop_();
		_nop_();
		SRCLK=0;	
	}

	RCLK=1;
	_nop_();
	_nop_();
	RCLK=0;
}

void main()
{	
 	unsigned char tab;
	unsigned int  i;
	init();
	while(1)
	{	
		for(i= 0; i<15; i++ )   //两个字之间的扫描间隔时间
		{
			for(tab=0;tab<8;tab++)
			{	

				Hc595SendByte(0x00);			     //消隐																
				COMMONPORTS	= TAB[tab];				 //输出字码	
				Hc595SendByte(dulieu[tab]);	
				delay(1);		
			}
			 
		}

	}	
}
