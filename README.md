# 2-Pass Assembler
## A simple 2 Pass Assembler for SIC machine in python 

The 2-PassAssembler-2.py file includes:
1) The operation code table (OPTAB)
2) Pass 1 function (pass_one)
3) Pass 2 function (pass_two)
4) Pass 1 and Pass 2 calls

My code works with three files:
1) "copy.txt" which includes the source program, In this case it's a program that reads a record from input, processes it, and writes it to output.
2) "copy_inter.txt" which is the intermediate file between Pass 1 and Pass 2. Pass 1 writes this file, it contains each source statement along with its assigned address. This file is used as input to Pass 2.
3) "copy_obj.txt" which is the final result of Pass 2, The object code made by Pass 2 is written in this file.

Data Structures used in the code:
1) Dictionaries: OPTAB and SYMTAB
2) Lists: intermediate lines in Pass 1, text records and object program in Pass 2
