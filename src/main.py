from filer import copy_static_files
from generator import generate_page 

def main():
    print("Begin Site Genereation")
    
    print("Copying Static Files...")
    copy_static_files("static", "public", clear_dest=True)
    print("Static Files Copied.")
    
    print("Generating Pages...")
    generate_page("content/index.md", "template.html", "public/index.html")
    print("Pages Generated.")
    
if __name__ == "__main__":
    main()
    