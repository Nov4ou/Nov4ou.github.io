---
title: Getting Started with Open Source FPGA
date: 2024-04-17 00:50 +0800
categories: [Electronics Engineering]
tags: [FPGA]
---

I'm currently using the iCESugar open source FPGA board. Using Quartus on Parallels Desktop or other virtual machines can be quite a hassle. However, there are fortunately other, more convenient ways to learn FPGA. This tutorial will walk you through setting up the toolchain and writing your first Verilog code on macOS or Linux.

## Installion

### Install iceStorm Tools

Once you have installed the [IceStrom Tools](https://clifford.at/icestorm?cmplz-force-reload=1713287338221), you will have all the tools needed for analyzing and creating bitstream files. Bitstream files are the final output of the FPGA design process. They are essentially configuration files that dictate how the FPGA's internal logic blocks and routing paths should be connected to implement a specific design. Think of it like a set of instructions that "program" the FPGA to behave in a particular way.

> Note: The `iceprog` program that take your generated bitstream file and sent it to the FPGA, may not work on macOS. In that case, you should use `icesporg` instead. You can download from [here](https://github.com/wuxx/icesugar/tree/master/tools). If you run into any trouble with the pre-built binary file, building it from the source code is always an option.
{: .prompt-info }

## Create a project template

To set up a basic complete FPGA project, you'll need three key files:

1. Verilog Code File `.v`: This file houses the logic and functionality of your design, expressed in the Verilog hardware description language.
2. Physical Constraints File `.pcf`: Bridging the gap between your design and the physical FPGA chip, this file maps your design's inputs and outputs to specific pins on the FPGA package.
3. Project Manager `Makefile`: Acting as the conductor of your project, the Makefile automates the build process, ensuring all the design steps are executed seamlessly and efficiently.

### Verliog
Use the blink program as an example:
```verilog
module blink_test (
	input CLK,
	output LED_G,
	output LED_R,
	output LED_B
);

//-- Modify this value for changing the blink frequency
localparam N = 14;  //-- N<=21 Fast, N>=23 Slow

reg [N:0] counter;
always @(posedge CLK)
  counter <= counter + 1;

assign LED_G = counter[N];
assign LED_R = counter[N-1];
assign LED_B = counter[N-2];

endmodule
```
This program makes the RGB blink allowing you to control the frequency. Those input and output are mapped in the `.pcf` file to match the physical input/output pins on the board.

### icesugar.pcf

This file acts as a translator, mapping the input and output signals defined in your Verilog code to their corresponding physical pins on the FPGA chip. You can remove any extraneous content, keeping only the essential pin mappings for the signals actively used in your design – for instance, the CLK (clock) and LED_G (green LED) pins.

``` 
# Clock signal
set_io CLK 16

# RGB LED pins
set_io LED_R 18
set_io LED_G 12
set_io LED_B 14

# Additional pin assignments...
```

### MakeFile 

``` make
NAME = blink

all: sim sint

sim: $(NAME)_tb.vcd

sint: $(NAME).bin

$(NAME)_tb.vcd: $(NAME).v $(NAME)_tb.v
	
	#-- Compilar
	iverilog -o $(NAME)_tb.out $(NAME).v $(NAME)_tb.v

	#-- Simular
	./$(NAME)_tb.out
	
	#-- Ver visualmente la simulacion con gtkwave
	gtkwave $(NAME)_tb.vcd $(NAME)_tb.gtkw &
	

$(NAME).bin: icesugar.pcf $(NAME).v 
	
	#-- Sintesis
	yosys -p "synth_ice40 -blif $(NAME).blif" $(NAME).v
	
	#-- Place & route
	arachne-pnr -d 5k -P sg48 -p icesugar.pcf $(NAME).blif -o $(NAME).txt
	
	#-- Generar binario final, listo para descargar en fgpa
	icepack $(NAME).txt $(NAME).bin

upload:
	icesprog $(NAME).bin

clean:
	rm -f *.bin *.txt *.blif *.out *.vcd *~

.PHONY: all clean
```

With these three files, you can synthesis your project and upload the `.bin` file to your board:
> Ensure you use the right programming tool for uploading the binary file. You can change the tools by editing the `MakeFile` file.
{: .prompt-warning }

```console
make sint
make upload
```

Here is the result:

<image src="/assets/img/IMG_4809.gif" alt="FPGA"/> 


<!-- <script src="https://utteranc.es/client.js"
        repo="Nov4ou/Nov4ou.github.io"
        issue-term="pathname"
        theme="github-dark"
        crossorigin="anonymous"
        async>
</script> -->