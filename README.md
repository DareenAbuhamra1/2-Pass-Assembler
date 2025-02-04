# 2-Pass Assembler
## A simple 2-Pass Assembler for SIC machine in python 

The 2-PassAssembler-2.py file includes:
  1) The operation code table (OPTAB)
  2) Pass 1 function (pass_one)
  3) Pass 2 function (pass_two)
  4) Pass 1 and Pass 2 calls

My code works with three files:
  1) "copy.txt" which includes the source program, In this case it's a program that reads a record from input, processes it, and writes it to output.      This file is used as input to Pass 1.
  2) "copy_inter.txt" which is the intermediate file between Pass 1 and Pass 2. Pass 1 writes this file, it contains each source statement along with      its assigned address. This file is used as input to Pass 2.
  3) "copy_obj.txt" which is the final result of Pass 2, The object code made by Pass 2 is written in this file.

Data Structures used in the code:
  1) Dictionaries: OPTAB and SYMTAB
  2) Lists: intermediate lines in Pass 1, text records and object program in Pass 2

* OPTAB is used to lookup mnemonic operation codes and translate them to their machine language equivalents.
* During Pass 1, OPTAB is used to look up and validate operation codes in the source program. In Pass 2, it is used to translate the operation codes to machine language.
* SYMTAB is used to store values (addresses) assigned to labels.

Pass 1 function (define symbols):
  1) Assign addresses to all statements in the program.
  2) Save the values (addresses) assigned to all labels for use in Pass 2.
  3) Perform some processing of assembler directives. (This includes processing that affects address assignment, such as determining the length of         data areas defined by BYTE, RESW, etc.)

Pass 2 function (assemble instructions and generate object program):
  1) Assemble instructions (translating operation codes and looking up addresses).
  2) Generate data values defined by BYTE, WORD, etc.
  3) Generate the object codes and Write the object program.

The object program:
<pre>
  Header record:
    Col. 1        H
    Col. 2-7      Program name
    Col. 8-13     Starting address of object program (hexadecimal)
    Col. 14-19    Length of object program in bytes (hexadecimal)


  Text record:
    Col. 1        T
    Col. 2-7      Starting address for object code in this record (hexadecimal)
    Col. 8-9      Length of object code in this record in bytes (hexadecimal)
    Col. 10-69    Object code, represented in hexadecimal (2 columns per byte of object code)


  End record:
    Col. 1        E
    Col. 2-7      Address of first executable instruction in object program (hexadecimal)

  For better readability, The symbol ^ is used to separate fields.

------------------------------------------------------------------------------------------------------------------------------------------------------
REFERENCE
System Software An Introduction To Systems Programming by Leland L. Beck
</pre>
