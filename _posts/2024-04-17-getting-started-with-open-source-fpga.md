---
layout: post
title: Getting Started with Open Source FPGA
date: 2024-04-17 00:50 +0800
---

I'm currently using the iCESugar open source FPGA board. Using Quartus on Parallels Desktop or other virtual machines can be quite a hassle. However, there are fortunately other, more convenient ways to learn FPGA. This tutorial will walk you through setting up the toolchain and writing your first Verilog code on macOS or Linux.

## Installion

### Install iceStorm Tools

Once you have installed the [IceStrom Tools](https://clifford.at/icestorm?cmplz-force-reload=1713287338221), you will have all the tools needed for analyzing and creating bitstream files. Bitstream files are the final output of the FPGA design process. They are essentially configuration files that dictate how the FPGA's internal logic blocks and routing paths should be connected to implement a specific design. Think of it like a set of instructions that "program" the FPGA to behave in a particular way.

> Note: The `iceprog` program that take your generated bitstream file and sent it to the FPGA, may not work on macOS. In that case, you should use `icesporg` instead. You can download from [here](https://github.com/wuxx/icesugar/tree/master/tools). If you run into any trouble with the pre-built binary file, building it from the source code is always an option.
{: .prompt-info }

dfasdasd

