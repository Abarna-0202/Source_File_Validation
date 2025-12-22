# 📄 Source File Validation Tool
This repository contains a Python-based utility to **automate validation of source files** based on a set of predefined rules and configurations. It reads incoming data files, performs checks, and generates easy-to-understand summary reports to assist in data correction and processing.
---
## 🚀 How It Works
1. A source file is placed inside the `Input File` folder.
2. On running the main script, the tool:
   - Reads configurations from `config.yaml`
   - Validates the structure and contents of the source file(s)
   - Applies specific rules, checks for empty columns, expected fields, and mappings
   - Generates output reports in Excel format, including:
     - Consolidated data summary
     - Count of records per sheet
     - Empty column analysis
     - Mapped column summary (if mapping is provided)
3. Any existing output reports are automatically archived with a timestamp to keep previous results.
---
## 📁 Folder Structure
plaintext
├── Main.py                      # Main entry point for execution\n
├── config.yaml                  # Config file with folder paths and validation settings
├── Text_To_Excel.py             # Core validation and transformation logic
├── Source_File_Analysis.py      # Mapping-based analysis module
├── archive_existing_outputs.py  # Handles archiving of old outputs
├── /Input File/                      # Input folder for source files
├── /Output File/                     # Output folder for generated reports
├── /Atrchive/                    # Auto-archived old output files
🧰 Features
✅ Auto-detects and installs required dependencies (pandas, openpyxl, PyYAML)
✅ Modular code design
✅ Archives previous output automatically
✅ Configurable validation logic
✅ Excel output for easy analysis

🛠️ Setup & Usage
Step 1: Clone the repository
git clone <your-bitbucket-repo-url>
cd dev-qa-repo
Step 2: Place your input files
Drop your .xlsx or .csv source files into the configured input folder.
Step 3: Run the tool
python Main.py
Step 4: Review output reports
Generated files will be found in the configured output folder.
⚙️ Configuration (config.yaml)
All important paths and rules are defined in config.yaml. You can customize:
Input/output/archive folder paths
Expected columns per sheet
Specific keywords to flag
Mapping file path (for entity-column mapping)
📦 Dependencies
These will be automatically installed on first run:
pandas
openpyxl
PyYAML 