import vars

def change(file_param, old_target_host, new_target_host):
    with open(file_param, "r") as file:
        file_lines = file.readlines()
        for index, line in enumerate(file_lines, 1):
            if "target_host" in line:
                file_lines[index - 1] = f"{'target_host = "'}{new_target_host}{'"\n'}"
    with open(file_param, "w") as file:
        file.writelines(file_lines)