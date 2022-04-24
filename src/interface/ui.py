from rich import print

def banner() -> str:
    """ Return the content from banner.txt as tool banner """

    file_path: str = "src/interface/banner.txt"
    
    with open(file_path) as banner:
        lines: str = banner.read()

        print(f"[cyan][b]{lines}[/][/]")