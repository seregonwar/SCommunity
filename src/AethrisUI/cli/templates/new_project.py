from pathlib import Path

def create_project_structure(name: str):
    """
    Crea la struttura base di un nuovo progetto
    """
    project_dir = Path(name)
    project_dir.mkdir(exist_ok=True)
    
    # Crea le directory principali
    (project_dir / "src").mkdir()
    (project_dir / "tests").mkdir()
    (project_dir / "assets").mkdir()
    
    # Crea i file di base
    (project_dir / "src" / "__init__.py").touch()
    (project_dir / "src" / "main.py").write_text("""
from aethris import Window, Container, Button, Text

def main():
    window = Window("My App", (800, 600))
    
    window.render(
        Container({
            "children": [
                Text("Hello, World!"),
                Button({
                    "text": "Click me",
                    "onClick": lambda: print("Clicked!")
                })
            ]
        })
    )
    
    window.run()

if __name__ == "__main__":
    main()
    """) 