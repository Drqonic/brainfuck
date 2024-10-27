import os
import sys


def count_occurrences(file_contents, file_index, character):
	count = 0

	while file_index + count < len(file_contents) and file_contents[file_index + count] == character:
		count += 1

	return count


def main():
	if len(sys.argv) < 2:
		sys.exit(f"Usage: {sys.argv[0]} <File Name>")

	filename = sys.argv[1]

	output_code = [
		"section .data",
		"	buffer db 0",
		"section .bss",
		"	cells resb 30000",
		"section .text",
		"	global _start",
		"_start:",
		"	lea rdi, [cells]",
		"	xor rax, rax",
		"	mov rcx, 30000",
		"	rep stosb",
		"	lea rdi, [cells]"
	]

	with open(filename, "r") as in_fd:
		file_index = 0
		file_contents = in_fd.read()

		loop_count = 0
		loop_stack = []

		while len(file_contents) > file_index:
			character = file_contents[file_index]

			count = count_occurrences(file_contents, file_index, character)

			if character == ">":
				output_code.append(f"	add rdi, {count}")
			elif character == "<":
				output_code.append(f"	sub rdi, {count}")
			elif character == "+":
				output_code.append(f"	add byte [rdi], {count}")
			elif character == "-":
				output_code.append(f"	sub byte [rdi], {count}")
			elif character == ".":
				output_code.append("	push rdi")
				output_code.append("	mov dil, [rdi]")
				output_code.append("	mov [buffer], dil")
				output_code.append("	mov rax, 1")
				output_code.append("	mov rdi, 1")
				output_code.append("	mov rsi, buffer")
				output_code.append("	mov rdx, 1")
				output_code.append("	syscall")
				output_code.append("	pop rdi")
			elif character == ",":
				for _ in range(count):
					output_code.append("	push rdi")
					output_code.append("	mov rax, 0")
					output_code.append("	mov rdi, 0")
					output_code.append("	lea rsi, [cells]")
					output_code.append("	mov rdx, 1")
					output_code.append("	syscall")
					output_code.append("	pop rdi")
			elif character == "[":
				for _ in range(count):
					output_code.append(f"loop_start_{loop_count}:")
					output_code.append("	cmp byte [rdi], 0")
					output_code.append(f"	jz loop_end_{loop_count}")

					loop_stack.append(loop_count)

					loop_count += 1
			elif character == "]":
				for _ in range(count):
					open_loop = loop_stack.pop()

					output_code.append("	cmp byte [rdi], 0")
					output_code.append(f"	jnz loop_start_{open_loop}")
					output_code.append(f"loop_end_{open_loop}:")

			file_index += count

	output_code.extend([
		"	mov rax, 60",
		"	xor rdi, rdi",
		"	syscall"
	])

	output_filename = filename.rsplit('.', 1)[0]

	with open(output_filename + ".asm", "w") as out_fd:
		out_fd.write("\r\n".join(output_code))

	os.system(f"nasm -f elf64 {output_filename}.asm")
	os.system(f"ld -s -o {output_filename} {output_filename}.o")
	os.system(f"rm {output_filename}.asm {output_filename}.o")


if __name__ == "__main__":
	main()
