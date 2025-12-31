from filer import copy_static_files

def main():
    print("Begin Site Genereation")
    
    print("Copying Static Files...")
    copy_static_files("static", "public", clear_dest=True)
    print("Static Files Copied.")
    
if __name__ == "__main__":
    main()
    