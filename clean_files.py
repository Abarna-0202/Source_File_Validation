import io

import os
 
# List of Python files to clean (add all your project files here)

files_to_clean = [

    "Source_File_Analysis.py",

    "analysis.py",

    "analysisdata_check.py",

    "archiveev_outputs.py",

    "Text_To_Excel.py",

    "main.py",

    "fields_comparison.py"

]
 
for file_path in files_to_clean:

    if os.path.exists(file_path):

        with io.open(file_path, "r", encoding="utf-8") as f:

            content = f.read()
 
        cleaned = content.replace("\u00A0", " ")
 
        with io.open(file_path, "w", encoding="utf-8") as f:

            f.write(cleaned)
 
        print(f"✅ Cleaned {file_path}")

    else:

        print(f"⚠️ File not found: {file_path}")
 
print("🎉 All files cleaned successfully!")

 