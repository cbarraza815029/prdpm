from pathlib import Path
import vars
import ip_host

def main():
    file = "vars.py"
    file_dir = Path(__file__).parent.resolve()
    file_abs_path = f"{file_dir}{"/"}{file}"
    
    print(f"{'Current IP/ hostname: '}{vars.target_host}")
    usr_input = input("New IP/ hostname: ").strip()
    if usr_input == "exit" or usr_input == "e":
        print("Returning to main menu...")
        print("")
    else:
        ip_host.change(file_abs_path, vars.target_host, usr_input)
        print(f"{'Success! IP address/ hostname changed from '}{'"'}{vars.target_host}{'"'}{' to '}{'"'}{usr_input}{'"'}")
        vars.target_host = usr_input
        print("")