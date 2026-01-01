import sys
from filer import copy_static_files
from generator import generate_pages_recursively 

def main():
    print("Begin Site Genereation")
    
    # Get base path from command line arguments or use default root directory
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    
    print("Copying Static Files...")
    copy_static_files("static", "docs", clear_dest=True)
    print("Static Files Copied.")
    
    print("Generating Pages...")
    generate_pages_recursively(basepath, "content", "template.html", "docs")
    print("Pages Generated.")
    
if __name__ == "__main__":
    main()
    