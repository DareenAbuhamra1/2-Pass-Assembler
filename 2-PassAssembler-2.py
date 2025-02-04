
#initialize opcode_table
OPTAB = {
    'ADD': '18','COMP':'28','J':'3C','JEQ':'30','JSUB':'48',
    'LDA':'00', 'LDCH':'50','LDL':'08','LDX':'04',
    'RSUB':'4C','STA':'0C','STCH':'54','STL':'14',
    'TD':'E0','TIX':'2C','WD':'DC','RD':'D8','JLT':'38','STX':'10',
}


def pass_one(source_file, intermediate_file):
    
    symtab = {}
    inter_lines = []
    loc_count = 0
    start_add = 0
    error_flag = False
    program_len = 0

    # Read lines from source file
    with open(source_file, 'r') as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()
        if not line or line.startswith('.'):  # Skip comment lines
            continue

        # Split line into parts (label, opcode, operand)
        parts = line.split()
        if len(parts) == 3:
            label, opcode, operand = parts
        elif len(parts) == 2:
            label = None
            opcode, operand = parts
        else:
            label = None
            opcode = parts[0]
            operand = None

        # Handle START directive
        if opcode == 'START':
            start_add = int(operand, 16)  # Convert from base 16 to integer
            loc_count = start_add  # Set loc_count to starting address
            inter_lines.append((label, opcode, operand, format(loc_count, 'X')))
            continue  # Move to the next line

        # Add label to SYMTAB if present
        if label:
            if label in symtab:
                print(f"ERROR: Duplicate label '{label}'")
                error_flag = True
            else:
                symtab[label] = format(loc_count, 'X')

        # Determine the length of the current instruction
        instruction_length = 0
        if opcode in OPTAB:
            instruction_length = 3
        elif opcode == 'WORD':
            instruction_length = 3
        elif opcode == 'RESW':
            instruction_length = 3 * int(operand)
        elif opcode == 'RESB':
            instruction_length = int(operand)
        elif opcode == 'BYTE':
            if operand.startswith("C'"):
                instruction_length = len(operand) - 3  # Subtract C and quotes
            elif operand.startswith("X'"):
                instruction_length = (len(operand) - 3) // 2
            else:
                print(f"ERROR: Invalid operand '{operand}' for BYTE")
                error_flag = True
        elif opcode == 'END':
            inter_lines.append((label, opcode, operand, format(loc_count, 'X')))
            program_len = loc_count - start_add
            break
        else:
            print(f"ERROR: Invalid opcode '{opcode}'")
            error_flag = True

        # Append current line to intermediate file and update location counter
        inter_lines.append((label, opcode, operand, format(loc_count, 'X')))
        loc_count += instruction_length

    # Write intermediate file
    with open(intermediate_file, 'w') as file:
        for line in inter_lines:
            file.write(' '.join(map(lambda x: x if x else '', line)) + '\n')

    if not error_flag:
        print('PASS 1 completed successfully')
    else:
        print('Errors were found in PASS 1')

    return symtab, inter_lines, format(start_add, 'X'), format(program_len, 'X')




def pass_two(intermediate_file, object_file, symtab, optab, start_add, program_len):
    
    text_record = []  
    object_program = []  
    program_name = None
    text_start = start_add  
    current_address = start_add
    error_flag = False

    with open(intermediate_file, 'r') as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()
        if not line:
            continue

        parts = line.split()
        if len(parts) == 4:
            label, opcode, operand, loc = parts
        elif len(parts) == 3:
            label = None
            opcode, operand, loc = parts
        elif len(parts) == 2:
            label = None
            opcode, loc = parts
            operand = None
        else:
            label, opcode, operand, loc = None, None, None, None

        # Start record (H)
        if opcode == 'START':
            program_name = label if label else '      '
            object_program.append(f'H^{program_name:<6}^{start_add:0>6}^{program_len:0>6}')
            continue

        # End record (E)
        if opcode == 'END':
            # Finalize the last text record
            if text_record:
                object_program.append(f'T^{text_start:0>6}^{len("".join(text_record)) // 2:02X}^{"^".join(text_record)}')
            # Add the E record
            if operand:
                end_address = symtab[operand] if operand in symtab else start_add
                object_program.append(f'E^{end_address:0>6}')
            else:
                object_program.append(f'E^')
            break

        obj_code = ''
        # Generate object code for valid opcodes
        if opcode in optab:
            obj_code = optab[opcode]
            if operand:
                if ',' in operand:
                    symbol, index = operand.split(',')
                    if index == 'X' and symbol in symtab:
                        obj_code += f'{int(symtab[symbol], 16) + 0x8000:04X}'
                    else:
                        print(f'ERROR: Undefined symbol or invalid index {operand}')
                        obj_code += '0000'
                        error_flag = True
                elif operand in symtab:
                    obj_code += f'{int(symtab[operand], 16):04X}'
                else:
                    print(f'ERROR: Undefined symbol {operand}')
                    obj_code += '0000'
                    error_flag = True
            else:
                obj_code += '0000'

        elif opcode == 'BYTE':
            if operand.startswith("C'"):
                obj_code = ''.join(f"{ord(c):02X}" for c in operand[2:-1]) #Converts to ASCII then hexa
            elif operand.startswith("X'"):
                obj_code = operand[2:-1]
            else:
                print(f'ERROR: Invalid BYTE operand {operand}')
                error_flag = True

        elif opcode == 'WORD':
            obj_code = f'{int(operand):06X}'

        elif opcode in ['RESB', 'RESW']:
            
            # Flush the current text record and skip reserved space
            if text_record:
                object_program.append(f'T^{text_start:0>6}^{len("".join(text_record)) // 2:02X}^{"^".join(text_record)}')
            text_record = []
            text_start = None
            continue

        else:
            print(f'ERROR: Undefined opcode {opcode}')
            error_flag = True

        # Add object code to text record
        if obj_code:
            if not text_start:
                text_start = loc  # Set new start address for text record
            if len("".join(text_record) + obj_code) > 60:  # Flush text record if max length exceeded
                object_program.append(f'T^{text_start:0>6}^{len("".join(text_record)) //2:02X}^{"^".join(text_record)}')
                text_record = [obj_code]  # Start new record
                text_start = loc
            else:
                text_record.append(obj_code)

    # Write the object program to the file
    with open(object_file, 'w') as outf:
        for record in object_program:
            outf.write(record + '\n')

    if error_flag:
        print("PASS 2 completed with errors.")
    else:
        print("PASS 2 completed successfully.")

    return object_program 





symbol_table,intermediate_lines,start_address,program_length = pass_one('copy.txt','copy_inter.txt')
object_program = pass_two('copy_inter.txt','copy_obj.txt',symbol_table,OPTAB,start_address,program_length)
