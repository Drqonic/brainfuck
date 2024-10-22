import sys
import getch


def main():
	if len(sys.argv) < 2:
		sys.exit(f"Usage: {sys.argv[0]} <File Name>")

	filename = sys.argv[1]

	with open(filename, "r") as fd:
		cell_pointer = 0
		cells = dict()

		file_index = 0
		file_contents = fd.read()

		loop_stack = []

		while len(file_contents) > file_index:
			character = file_contents[file_index]

			if not cells.get(cell_pointer):
				cells[cell_pointer] = 0

			old_cell_pointer = cell_pointer

			if character == ">":
				cell_pointer += 1
			elif character == "<":
				cell_pointer -= 1
			elif character == "+":
				cells[cell_pointer] = (cells[cell_pointer] + 1) % 256
			elif character == "-":
				cells[cell_pointer] = (cells[cell_pointer] - 1) % 256
			elif character == ".":
				sys.stdout.write(chr(cells[cell_pointer]))
				sys.stdout.flush()
			elif character == ",":
				cells[cell_pointer] = ord(getch.getch())
			elif character == "[":
				if cells[cell_pointer] == 0:
					open_loops = 1

					while open_loops > 0:
						file_index += 1

						if file_contents[file_index] == "[":
							open_loops += 1
						elif file_contents[file_index] == "]":
							open_loops -= 1
				else:
					loop_stack.append(file_index)
			elif character == "]":
				if cells[cell_pointer] > 0:
					file_index = loop_stack[-1]
				else:
					loop_stack.pop()

			if cells.get(old_cell_pointer) == 0:
				del cells[old_cell_pointer]
				
			file_index += 1


if __name__ == "__main__":
	main()
