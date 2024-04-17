---
layout: post
title: Digital Clock By 51MCU
date: '2023-01-20 02:40:42 +0800'
categories: [MCU]
tags: [Intel 8051]
---
# Implement Digital Clock by STC89C52

## Preface
The final problem combinate all the function learned before, such as nixie tubes, alarm, buzzer and timers, etc. To finish this task, we should link all previous program modules carefully.

> There are four modes for this clock. The first mode display current time,
> the second mode display the alarm time, the third mode is used to set  current time and the fourth mode is to set alarm time.

> 1. Display(nixie tubes):
>    - Mode 1: Display current time in "hour.minute" format, and the dot flash every 0.5 second.
>    - Mode 2: When the stopwatch time is under one minute, display in "second.100 parts of a second" format, the dot flash every 0.25 second; Otherwise display in "minute.second" format. the dot flash every one second.
>    - Mode 3: Display current time in "hour.minute" format, the number which are going to be changed flash once per 0.5 second.
>    - Mode 4: Just like mode 3, but change the alarm time.
> 2. Keys:
>    - Mode 1:
>      - Key 1: Change to Mode 2;
>      - Key 2: Check the alarm time/the current time;
>      - Key 3: Turn on/off the alarm(display "ON" or "OFF" in nixie tubes for 1s);
>    - Mode 2:
>      - Key 1: Change to Mode 3;
>      - Key 2: Start/Stop the stopwatch;
>      - Key 3: Record current time when the stopwatch is running; Otherwise reset the stopwatch.
>      - Key 4: If there are more than one lap, display the lap one by one; if reach the last lap, reset all lap;
>    - Mode 3:
>      - Key 1: Change to Mode 4;
>      - Key 2: Switch the address of the time will be changed;
>      - Key 3: Current number on the address plus one;
>      - Key 4: Confirm the change;
>    - Mode 4:
>       - Key 1: Change to Mode 1;
>       - Key 2,3,4: As Mode 3;
> 3. Other functions:
>   - When the key is pressed, the buzzer beeps briefly; report punctually(about 2s);
>   - At the beginning of the program, read the alarm time from EEPROM; Save  the modified alarm time into EEPROM;

## Program Modules
I will break the whole program into several blocks, each block has their own usage and finally combinate these blocks together.

### Timers
We will use two timers, one for the UART module, one for the rest functions which can save a lot effort by using timer.
#### Timer0
```c
#include <REGX52.H>

void Timer0_Init(void)		//1ms@11.0592MHz
{
  TMOD &= 0xF0;		//Set timer work mode
  TMOD |= 0x01;		//Set timer work mode
  TL0 = 0x66;		//Initial timer value
  TH0 = 0xFC;		//Initial timer value
  TF0 = 0;		//Clear TF0 flag
  TR0 = 1;		//Timer0 start run
  ET0 = 1;
  EA = 1;
  PT0 = 0;
}
```
```c
void Timer0_Routine() interrupt 1
{
  static unsigned int T0Count1;
  TL0 = 0x18;
  TH0 = 0xFC;
  /*
      other modules;
  */
}
```
#### UART Timer
The second Timer is used for the UART fuction(Timer1).
Set `UART` first:
```c
void Uart_Init(void)		//4800bps@11.0592MHz
{
  PCON |= 0x80;		//Enable SMOD bit
  SCON = 0x50;		//8 bits and variable baudrate
  TMOD &= 0x0F;		//Set timer work mode
  TMOD |= 0x20;		//Set timer work mode
  TL1 = 0xF4;		//Initial timer value
  TH1 = 0xF4;		//Set reload value
  ET1 = 0;		//Disable Timer%d interrupt
  TR1 = 1;		//Timer1 start run
  EA = 1;
  ES = 1;
}
```
**Note: Make sure you choose your MCU Frequency correctly. Usually it's 12MHz or 11.0592MHz.**
#### Timer Conflict
If you use these two timers at the same time, you probably find that the `UART_Timer` will make `Timer0` slower and the `Nixie` module will be affected so the nixie tubes will flick. So it's better only use `UART_Init` when should use. In other words, only should you use `UART_Init` in `Mode 3` and `Mode 4`. In `Mode 1` and `Mode 2` you should 'antiinit' the UART module.
```c
void Uart_antiInit(void)
{
  TR1 = 0;               //Disable the timer1
}
```

### Nixie Using Timer
The nixie module is essential. The basic usage of nixie tubes are simple, but in this problem we should modify it a little bit.
The second address in the nixie tubes should display the dot with the number at the same time. Also sometime you may want display nothing(not even be ligthed).
```c
unsigned char TimeSetFlashDot, TimeSetFlashNum;
// show on or off stop flash and delay 1000ms;
unsigned char ShowOnOff = 0;
// location start with 1;
unsigned char Nixie_Buf[9] ={0, 10, 10, 10, 10, 10, 10, 10, 10};
//	                   'O'&'0'   '1'   '2'   '3'   '4'   '5'   '6'   '7'   '8'   '9'   ' '   'F'    'N'
unsigned char NixieTable[] = {0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x07, 0x7F, 0x6F, 0x00, 0x71, 0x37};
// All number with dot.
unsigned char NixieTable_Float[] = {0xBF, 0x86, 0xDB, 0xCF, 0xE6, 0xED, 0xFD,0x87, 0xFF, 0xEF, 0x00};

void Nixie_SetBuf(unsigned char Location, Number)
{
  Nixie_Buf[Location] = Number;
}

void Nixie_Scan(unsigned char Location, Number)
{
  P0 = 0x00;
  switch (Location)
  {
    case 1:
      P2_4=1, P2_3=1, P2_2=1;
      break;
    case 2:
      P2_4=1, P2_3=1, P2_2=0;
      break;
    case 3:
      P2_4=1, P2_3=0, P2_2=1;
      break;
    case 4:
      P2_4=1, P2_3=0, P2_2=0;
      break;
    case 5:
      P2_4=0, P2_3=1, P2_2=1;
      break;
    case 6:
      P2_4=0, P2_3=1, P2_2=0;
      break;
    case 7:
      P2_4=0, P2_3=0, P2_2=1;
      break;
    case 8:
      P2_4=0, P2_3=0, P2_2=0;
      break;
  }
  if (Location == 2) {
    if (TimeSetFlashDot == 0 &    ShowOnOff == 0)
      P0 = NixieTable_Float[Number];
    else
      P0 = NixieTable[Number];
  }
  else
    P0 = NixieTable[Number];
}

void Nixie_Loop(void)
{
  static unsigned char i = 1;
  Nixie_Scan(i, Nixie_Buf[i]);
  i++;
  if (i >= 9)
    i = 1;
}
```

### EEPROM
Using `AT24C02` to save the alarm time to make sure the time will not be lost when restart.
```c
#include <REGX52.H>
#include <I2C.H>

#define AT24C02_ADDRESS                         0xA0

void AT24C02_WriteByte(unsigned char WordAddress, Data);
unsigned char AT24C02_ReadByte(unsigned char WordAddress);

void AT24C02_WriteByte(unsigned char WordAddress, Data)
{
  I2C_Start();
  I2C_SendByte(AT24C02_ADDRESS);
  I2C_ReceiveAck();
  I2C_SendByte(WordAddress);
  I2C_ReceiveAck();
  I2C_SendByte(Data);
  I2C_ReceiveAck();
  I2C_Stop();
}

unsigned char AT24C02_ReadByte(unsigned char WordAddress)
{
  unsigned char Data;
  I2C_Start();
  I2C_SendByte(AT24C02_ADDRESS);
  I2C_ReceiveAck();
  I2C_SendByte(WordAddress);
  I2C_ReceiveAck();
  I2C_Start();
  I2C_SendByte(AT24C02_ADDRESS | 0x01);
  I2C_ReceiveAck();
  Data = I2C_ReceiveByte();
  I2C_SendAck(1);
  I2C_Stop();
  return Data;
}
```

## Notes
- Remember that `DS1302` only support to second. Unfortunately you should write the stopwatch by yourself using Timer0.
- When programming, you will face so many different modes to display. So it's a good idea to make the other four nixie tubes useful.
- You can't let one `Timer` do too much tasks, that will slow your whole program down.