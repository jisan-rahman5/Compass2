import os

# Removed 'static' from ignored directories
IGNORE_DIRS = {'venv', '.venv', '__pycache__', '.git', 'migrations', 'media'}
# Added txt, md, json for docs/requirements
ALLOWED_EXTENSIONS = {'.py', '.html', '.css', '.js', '.txt', '.md', '.json'}

root_dir = r"c:\Users\jisan\OneDrive\Desktop\compass-2"
output_file = os.path.join(root_dir, "codebase_for_ai.txt")

with open(output_file, "w", encoding="utf-8") as out:
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Remove ignored directories from traversal
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]
        
        for file in filenames:
            ext = os.path.splitext(file)[1].lower()
            # Exclude our own script, the output itself, and the database file
            if ext in ALLOWED_EXTENSIONS and file not in ["export_for_ai.py", "codebase_for_ai.txt", "db.sqlite3"]:
                file_path = os.path.join(dirpath, file)
                rel_path = os.path.relpath(file_path, root_dir)
                
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        
                    out.write(f"--- File: {rel_path} ---\n")
                    out.write(content)
                    out.write("\n\n")
                except Exception as e:
                    pass

print(f"Successfully generated {output_file}")
