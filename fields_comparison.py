
# import pandas as pd

# import os
 
# def compare_fields(mapping_file, input_folder, output_excel):

#     # Load mapping file and compute expected_columns

#     try:

#         mapping_data = pd.read_excel(mapping_file, sheet_name=None, header=1)

#         for sheet in mapping_data:

#             mapping_data[sheet].columns = mapping_data[sheet].columns.map(str)

#     except Exception as e:

#         print(f"Error reading the mapping file: {e}")

#         return False
 
#     expected_columns = {}

#     specific_words = list(mapping_data.keys())  # Entities are the sheet names
 
#     for entity_name, sheet_data in mapping_data.items():

#         position_column = None
 
#         # Special case: POE uses "Acct"

#         if entity_name == 'POE' and 'Acct' in sheet_data.columns:

#             position_column = 'Acct'

#         else:

#             for column in sheet_data.columns:

#                 if 'Position' in column:

#                     position_column = column

#                     break
 
#         if position_column:

#             positions = pd.to_numeric(sheet_data[position_column], errors='coerce').dropna()

#             if not positions.empty:

#                 max_pos = int(positions.max())

#                 expected_columns[entity_name] = max_pos

#             else:

#                 expected_columns[entity_name] = 0

#         else:

#             expected_columns[entity_name] = 0
 
#     # Process input files and collect actual counts

#     entity_results = {}

#     try:

#         for filename in os.listdir(input_folder):

#             if filename.endswith(".txt"):

#                 file_path = os.path.join(input_folder, filename)

#                 file_content = None
 
#                 try:

#                     with open(file_path, 'r', encoding='utf-8', errors='replace') as file:

#                         file_content = file.readlines()

#                 except UnicodeDecodeError:

#                     try:

#                         with open(file_path, 'r', encoding='latin1', errors='replace') as file:

#                             file_content = file.readlines()

#                     except UnicodeDecodeError as e:

#                         print(f"Error decoding file {file_path}: {e}")

#                         continue
 
#                 if file_content is None:

#                     continue
 
#                 for line in file_content:

#                     columns = line.strip().split('|')

#                     entity_name = columns[0].strip() if len(columns) > 0 else None
 
#                     if entity_name:

#                         actual_columns_count = len(columns)

#                         key = (filename, entity_name)
 
#                         if key not in entity_results:

#                             entity_results[key] = {

#                                 "expected": expected_columns.get(entity_name, "Not Found"),

#                                 "actual": actual_columns_count,

#                                 "status": "Pass" if actual_columns_count == expected_columns.get(entity_name, 0) else "Fail"

#                             }

#                         else:

#                             if actual_columns_count != entity_results[key]["actual"]:

#                                 entity_results[key]["status"] = "Varying"

#     except Exception as e:

#         print(f"Error processing files in folder: {e}")

#         return False
 
#     # Build final entity list = union of mapping + input

#     all_entities = sorted(set(expected_columns.keys()) | {e for (_, e) in entity_results.keys()})
 
#     fields_comparison_data = []

#     for entity in all_entities:

#         saas_fields = expected_columns.get(entity, "Not Found")

#         input_fields = "Not Found"
 
#         matching_results = [res for (f, e), res in entity_results.items() if e == entity]
 
#         if matching_results:

#             unique_values = set(

#                 res["actual"] if res["status"] != "Varying" else "Varying"

#                 for res in matching_results

#             )

#             if len(unique_values) == 1:

#                 input_fields = unique_values.pop()

#             else:

#                 input_fields = "Varying across files"
 
#         fields_comparison_data.append({

#             "Entity name": entity,

#             "SAAS sheet (number of fields)": saas_fields,

#             "output (number of fields)": input_fields

#         })
 
#     fields_comparison_df = pd.DataFrame(fields_comparison_data).sort_values(by="Entity name", ignore_index=True)
 
#     try:

#         with pd.ExcelWriter(output_excel) as writer:

#             fields_comparison_df.to_excel(writer, sheet_name='Fields Comparison', index=False)

#         print(f"Success: Fields comparison saved to {output_excel}")

#     except Exception as e:

#         print(f"Error writing fields comparison to Excel: {e}")

#         return False
 
#     return True
 
 
# if __name__ == "__main__":

#     mapping_file = "Saas_Legacy_Migration.xlsx"

#     input_folder = "Input File"

#     output_excel = "output_entity_check.xlsx"

#     compare_fields(mapping_file, input_folder, output_excel)

## crt code before change - above


# import pandas as pd

# import os
 
# def compare_fields(mapping_file, input_folder, output_excel):
 
#     # -----------------------------

#     # Load mapping file

#     # -----------------------------

#     try:

#         mapping_data = pd.read_excel(mapping_file, sheet_name=None, header=1)

#         for sheet in mapping_data:

#             mapping_data[sheet].columns = mapping_data[sheet].columns.map(str)

#     except Exception as e:

#         print(f"Error reading mapping file: {e}")

#         return False
 
#     # -----------------------------

#     # Build expected column counts

#     # -----------------------------

#     expected_columns = {}
 
#     for entity_name, sheet_data in mapping_data.items():

#         position_column = None
 
#         if entity_name == "POE" and "Acct" in sheet_data.columns:

#             position_column = "Acct"

#         else:

#             for col in sheet_data.columns:

#                 if "Position" in col:

#                     position_column = col

#                     break
 
#         if position_column:

#             positions = pd.to_numeric(sheet_data[position_column], errors="coerce").dropna()

#             expected_columns[entity_name] = int(positions.max()) if not positions.empty else 0

#         else:

#             expected_columns[entity_name] = 0
 
#     # -----------------------------

#     # Process input files

#     # -----------------------------

#     entity_results = {}

#     varying_records = []    # Detailed varying list

#     variation_map = {}      # For option A summary
 
#     try:

#         for filename in os.listdir(input_folder):

#             if filename.endswith(".txt"):

#                 file_path = os.path.join(input_folder, filename)
 
#                 # keep EXACT encoding logic you used

#                 try:

#                     with open(file_path, "r", encoding="utf-8", errors="replace") as file:

#                         lines = file.readlines()

#                 except Exception:

#                     with open(file_path, "r", encoding="latin1", errors="replace") as file:

#                         lines = file.readlines()
 
#                 record_number = 0

#                 line_entity_counts = {}
 
#                 for line in lines:

#                     record_number += 1

#                     columns = line.strip().split("|")

#                     entity_name = columns[0].strip() if columns else None
 
#                     if not entity_name:

#                         continue
 
#                     actual_count = len(columns)

#                     expected_count = expected_columns.get(entity_name, 0)
 
#                     key = (filename, entity_name)
 
#                     # Track each record count

#                     if key not in line_entity_counts:

#                         line_entity_counts[key] = []

#                     line_entity_counts[key].append((record_number, actual_count))
 
#                     # Entity summary

#                     if key not in entity_results:

#                         entity_results[key] = {

#                             "expected": expected_count,

#                             "actual": actual_count,

#                             "status": "Pass" if actual_count == expected_count else "Fail"

#                         }

#                     else:

#                         if actual_count != entity_results[key]["actual"]:

#                             entity_results[key]["status"] = "Varying"
 
#                 # Build variation map for summary

#                 for key, rec_list in line_entity_counts.items():

#                     filename, entity = key

#                     counts = {cnt for (_, cnt) in rec_list}
 
#                     if len(counts) > 1:  # varying

#                         expected_count = expected_columns.get(entity, 0)
 
#                         # Collect record-level details

#                         for (rec_no, cnt) in rec_list:

#                             varying_records.append({

#                                 "Filename": filename,

#                                 "Entity": entity,

#                                 "Record Number": rec_no,

#                                 "Actual Field Count": cnt,

#                                 "Expected Field Count": expected_count,

#                                 "Difference": cnt - expected_count

#                             })
 
#                         # Build summary variation map

#                         if entity not in variation_map:

#                             variation_map[entity] = {

#                                 "expected": expected_count,

#                                 "actual_values": set(),

#                                 "count": 0

#                             }
 
#                         variation_map[entity]["actual_values"].update(counts)

#                         variation_map[entity]["count"] += len(rec_list)
 
#     except Exception as e:

#         print(f"Error processing files: {e}")

#         return False
 
#     # -----------------------------

#     # Fields Comparison sheet

#     # -----------------------------

#     all_entities = sorted(set(expected_columns.keys()) | {e for (_, e) in entity_results.keys()})
 
#     fields_comparison = []
 
#     for entity in all_entities:

#         saas_fields = expected_columns.get(entity, "Not Found")

#         matching_results = [res for (f, e), res in entity_results.items() if e == entity]
 
#         if not matching_results:

#             input_fields = "Not Found"

#         else:

#             unique_values = set(

#                 res["actual"] if res["status"] != "Varying" else "Varying"

#                 for res in matching_results

#             )

#             input_fields = unique_values.pop() if len(unique_values) == 1 else "Varying across files"
 
#         fields_comparison.append({

#             "Entity name": entity,

#             "SAAS sheet (number of fields)": saas_fields,

#             "output (number of fields)": input_fields

#         })
 
#     fields_comparison_df = pd.DataFrame(fields_comparison)
 
#     # -----------------------------

#     # Varying Records sheet

#     # -----------------------------

#     varying_records_df = pd.DataFrame(varying_records)
 
#     # -----------------------------

#     # Option A: Varying Fields Summary sheet

#     # -----------------------------

#     summary_rows = []

#     for entity, info in variation_map.items():

#         summary_rows.append({

#             "Entity": entity,

#             "Expected Fields": info["expected"],

#             "Unique Actual Field Counts": ", ".join(str(x) for x in sorted(info["actual_values"])),

#             "Count of Varied Records": info["count"]

#         })
 
#     summary_df = pd.DataFrame(summary_rows)
 
#     # -----------------------------

#     # Write Excel file

#     # -----------------------------

#     try:

#         with pd.ExcelWriter(output_excel) as writer:

#             fields_comparison_df.to_excel(writer, sheet_name="Fields Comparison", index=False)
 
#             if not varying_records_df.empty:

#                 varying_records_df.to_excel(writer, sheet_name="Varying Records", index=False)
 
#             if not summary_df.empty:

#                 summary_df.to_excel(writer, sheet_name="Varying Fields Summary", index=False)
 
#         print(f"Success: output saved → {output_excel}")
 
#     except Exception as e:

#         print(f"Error writing output: {e}")

#         return False
 
#     return True
 
 
# # Run

# if __name__ == "__main__":

#     compare_fields(

#         mapping_file="Saas_Legacy_Migration.xlsx",

#         input_folder="Input File",

#         output_excel="output_entity_check.xlsx"

#     )

## working crtly upto how many are varying 


# import pandas as pd

# import os

# import re
 
# def compare_fields(mapping_file, input_folder, output_excel):
 
#     # -----------------------------

#     # Load mapping file

#     # -----------------------------

#     try:

#         mapping_data = pd.read_excel(mapping_file, sheet_name=None, header=1)

#         for sheet in mapping_data:

#             mapping_data[sheet].columns = mapping_data[sheet].columns.map(str)

#     except Exception as e:

#         print(f"Error reading mapping file: {e}")

#         return False
 
#     # -----------------------------

#     # Build expected column counts

#     # -----------------------------

#     expected_columns = {}

#     required_fields = {}  # NEW: store required fields per entity
 
#     for entity_name, sheet_data in mapping_data.items():

#         position_column = None
 
#         # Identify position column

#         for col in sheet_data.columns:

#             if "Position" in col:

#                 position_column = col

#                 break
 
#         # Extract expected max position

#         if position_column:

#             positions = pd.to_numeric(sheet_data[position_column], errors="coerce").dropna()

#             expected_columns[entity_name] = int(positions.max()) if not positions.empty else 0

#         else:

#             expected_columns[entity_name] = 0
 
#         # Extract required fields (Yes, yes?, YES, yes ?, etc.)

#         req_fields = []

#         for _, row in sheet_data.iterrows():

#             req_val = str(row.get("Required?", "")).strip().lower()

#             if re.match(r"yes", req_val):   # treat yes, yes?, yes! etc as required

#                 field_name = row.get("Description", "")

#                 pos = row.get(position_column, None)

#                 if pd.notna(pos):

#                     req_fields.append((field_name, int(pos)))
 
#         required_fields[entity_name] = req_fields
 
#     # -----------------------------

#     # Process input files

#     # -----------------------------

#     entity_results = {}

#     varying_records = []
 
#     required_failed_records = []     # NEW – Detailed failed required-field records

#     required_summary_map = {}        # NEW – Summary counts per entity
 
#     try:

#         for filename in os.listdir(input_folder):

#             if filename.endswith(".txt"):

#                 file_path = os.path.join(input_folder, filename)
 
#                 # Read using your EXACT encoding logic

#                 try:

#                     with open(file_path, "r", encoding="utf-8", errors="replace") as file:

#                         lines = file.readlines()

#                 except Exception:

#                     with open(file_path, "r", encoding="latin1", errors="replace") as file:

#                         lines = file.readlines()
 
#                 record_number = 0
 
#                 for line in lines:

#                     record_number += 1

#                     columns = line.strip().split("|")

#                     entity_name = columns[0].strip() if columns else None
 
#                     if not entity_name:

#                         continue
 
#                     actual_count = len(columns)

#                     expected_count = expected_columns.get(entity_name, 0)
 
#                     # Track entity summary

#                     key = (filename, entity_name)

#                     if key not in entity_results:

#                         entity_results[key] = {

#                             "expected": expected_count,

#                             "actual": actual_count,

#                             "status": "Pass" if actual_count == expected_count else "Fail"

#                         }

#                     else:

#                         if actual_count != entity_results[key]["actual"]:

#                             entity_results[key]["status"] = "Varying"
 
#                     # -----------------------------

#                     # REQUIRED FIELD VALIDATION

#                     # -----------------------------

#                     if entity_name not in required_summary_map:

#                         required_summary_map[entity_name] = {

#                             "required_fields": len(required_fields.get(entity_name, [])),

#                             "total_records": 0,

#                             "failed_records": 0,

#                             "fail_instances": 0

#                         }
 
#                     required_summary_map[entity_name]["total_records"] += 1
 
#                     missing = []

#                     for field_name, pos in required_fields.get(entity_name, []):

#                         idx = pos - 1

#                         value = columns[idx].strip() if idx < len(columns) else ""
 
#                         if value == "" or value.lower() == "null":

#                             missing.append((field_name, pos, value))
 
#                     if missing:

#                         required_summary_map[entity_name]["failed_records"] += 1

#                         required_summary_map[entity_name]["fail_instances"] += len(missing)
 
#                         for field_name, pos, value in missing:

#                             required_failed_records.append({

#                                 "Filename": filename,

#                                 "Entity": entity_name,

#                                 "Record Number": record_number,

#                                 "Missing Field": field_name,

#                                 "Position": pos,

#                                 "Actual Value": value,

#                                 "Status": "Fail"

#                             })
 
#     except Exception as e:

#         print(f"Error processing files: {e}")

#         return False
 
#     # -----------------------------

#     # Existing Fields Comparison Sheet

#     # -----------------------------

#     all_entities = sorted(set(expected_columns.keys()) |

#                           {e for (_, e) in entity_results.keys()})
 
#     fields_comparison = []

#     for entity in all_entities:

#         saas_fields = expected_columns.get(entity, "Not Found")

#         matching_results = [res for (f, e), res in entity_results.items() if e == entity]
 
#         if not matching_results:

#             input_fields = "Not Found"

#         else:

#             unique_values = set(

#                 res["actual"] if res["status"] != "Varying"

#                 else "Varying"

#                 for res in matching_results

#             )

#             input_fields = unique_values.pop() if len(unique_values) == 1 else "Varying across files"
 
#         fields_comparison.append({

#             "Entity name": entity,

#             "SAAS sheet (number of fields)": saas_fields,

#             "output (number of fields)": input_fields

#         })
 
#     fields_comparison_df = pd.DataFrame(fields_comparison)
 
#     # -----------------------------

#     # Required Failed Records Sheet

#     # -----------------------------

#     required_failed_df = pd.DataFrame(required_failed_records)
 
#     # -----------------------------

#     # Required Summary Sheet

#     # -----------------------------

#     summary_rows = []

#     for entity, info in required_summary_map.items():

#         summary_rows.append({

#             "Entity": entity,

#             "Required Fields Count": info["required_fields"],

#             "Total Records": info["total_records"],

#             "Failed Records": info["failed_records"],

#             "Passed Records": info["total_records"] - info["failed_records"],

#             "Total Missing Instances": info["fail_instances"]

#         })

#     required_summary_df = pd.DataFrame(summary_rows)
 
#     # -----------------------------

#     # WRITE OUTPUT EXCEL

#     # -----------------------------

#     try:

#         with pd.ExcelWriter(output_excel) as writer:

#             fields_comparison_df.to_excel(writer, sheet_name="Fields Comparison", index=False)
 
#             # NEW SHEET 1

#             required_failed_df.to_excel(writer, sheet_name="Required – Failed Records", index=False)
 
#             # NEW SHEET 2

#             required_summary_df.to_excel(writer, sheet_name="Required Summary", index=False)
 
#         print(f"Success: output saved → {output_excel}")
 
#     except Exception as e:

#         print(f"Error writing output: {e}")

#         return False
 
#     return True
 
 
# # Run

# if __name__ == "__main__":

#     compare_fields(

#         mapping_file="Saas_Legacy_Migration.xlsx",

#         input_folder="Input File",

#         output_excel="output_entity_check.xlsx"

#     )


# import pandas as pd
# import os
# import re
 
# def compare_fields(mapping_file, input_folder, output_excel):
 
#     # -----------------------------
#     # Load mapping file
#     # -----------------------------
#     try:
#         mapping_data = pd.read_excel(mapping_file, sheet_name=None, header=1)
#         for sheet in mapping_data:
#             mapping_data[sheet].columns = mapping_data[sheet].columns.map(str)
#     except Exception as e:
#         print(f"Error reading mapping file: {e}")
#         return False
 
#     # -----------------------------
#     # Build expected column counts & required fields
#     # -----------------------------
#     expected_columns = {}
#     required_fields = {}
 
#     for entity_name, sheet_data in mapping_data.items():
#         position_column = None
#         for col in sheet_data.columns:
#             if "Position" in col:
#                 position_column = col
#                 break
 
#         # Expected max columns
#         if position_column:
#             positions = pd.to_numeric(sheet_data[position_column], errors="coerce").dropna()
#             expected_columns[entity_name] = int(positions.max()) if not positions.empty else 0
#         else:
#             expected_columns[entity_name] = 0
 
#         # Required fields
#         req_fields = []
#         for _, row in sheet_data.iterrows():
#             req_val = str(row.get("Required?", "")).strip().lower()
#             if re.match(r"yes", req_val):
#                 field_name = row.get("Description", "")
#                 pos = row.get(position_column, None)
#                 if pd.notna(pos):
#                     req_fields.append((field_name, int(pos)))
#         required_fields[entity_name] = req_fields
 
#     # -----------------------------
#     # Process input files
#     # -----------------------------
#     entity_results = {}
#     required_failed_records = []
#     required_summary_map = {}
#     varying_records = []
#     variation_map = {}
 
#     try:
#         for filename in os.listdir(input_folder):
#             if not filename.endswith(".txt"):
#                 continue
#             file_path = os.path.join(input_folder, filename)
#             try:
#                 with open(file_path, "r", encoding="utf-8", errors="replace") as file:
#                     lines = file.readlines()
#             except Exception:
#                 with open(file_path, "r", encoding="latin1", errors="replace") as file:
#                     lines = file.readlines()
 
#             record_number = 0
#             line_entity_counts = {}
 
#             for line in lines:
#                 record_number += 1
#                 columns = line.strip().split("|")
#                 entity_name = columns[0].strip() if columns else None
#                 if not entity_name:
#                     continue
 
#                 actual_count = len(columns)
#                 expected_count = expected_columns.get(entity_name, 0)
#                 key = (filename, entity_name)
 
#                 # Track entity summary
#                 if key not in entity_results:
#                     entity_results[key] = {
#                         "expected": expected_count,
#                         "actual": actual_count,
#                         "status": "Pass" if actual_count == expected_count else "Fail"
#                     }
#                 else:
#                     if actual_count != entity_results[key]["actual"]:
#                         entity_results[key]["status"] = "Varying"
 
#                 # For Field Comparison Summary (Varying Records)
#                 if key not in line_entity_counts:
#                     line_entity_counts[key] = []
#                 line_entity_counts[key].append((record_number, actual_count))
 
#                 # Required Field Validation
#                 if entity_name not in required_summary_map:
#                     required_summary_map[entity_name] = {
#                         "required_fields": len(required_fields.get(entity_name, [])),
#                         "total_records": 0,
#                         "failed_records": 0,
#                         "fail_instances": 0
#                     }
#                 required_summary_map[entity_name]["total_records"] += 1
 
#                 missing = []
#                 for field_name, pos in required_fields.get(entity_name, []):
#                     idx = pos - 1
#                     value = columns[idx].strip() if idx < len(columns) else ""
#                     if value == "" or value.lower() == "null":
#                         missing.append((field_name, pos, value))
 
#                 if missing:
#                     required_summary_map[entity_name]["failed_records"] += 1
#                     required_summary_map[entity_name]["fail_instances"] += len(missing)
 
#                     for field_name, pos, value in missing:
#                         required_failed_records.append({
#                             "Filename": filename,
#                             "Entity": entity_name,
#                             "Record Number": record_number,
#                             "Missing Field": field_name,
#                             "Position": pos,
#                             "Actual Value": value,
#                             "Status": "Fail"
#                         })
 
#             # Build Varying Records & Summary Map
#             for key, rec_list in line_entity_counts.items():
#                 filename, entity = key
#                 counts = {cnt for (_, cnt) in rec_list}
 
#                 if len(counts) > 1:
#                     # Varying records details
#                     for (rec_no, cnt) in rec_list:
#                         varying_records.append({
#                             "Filename": filename,
#                             "Entity": entity,
#                             "Record Number": rec_no,
#                             "Actual Field Count": cnt,
#                             "Expected Field Count": expected_columns.get(entity, 0),
#                             "Difference": cnt - expected_columns.get(entity, 0)
#                         })
 
#                     # Varying summary
#                     if entity not in variation_map:
#                         variation_map[entity] = {
#                             "expected": expected_columns.get(entity, 0),
#                             "actual_values": set(),
#                             "count": 0
#                         }
 
#                     variation_map[entity]["actual_values"].update(counts)
#                     variation_map[entity]["count"] += len(rec_list)
 
#     except Exception as e:
#         print(f"Error processing files: {e}")
#         return False
 
#     # -----------------------------
#     # Fields Comparison Sheet
#     # -----------------------------
#     all_entities = sorted(set(expected_columns.keys()) | {e for (_, e) in entity_results.keys()})
#     fields_comparison = []
 
#     for entity in all_entities:
#         saas_fields = expected_columns.get(entity, "Not Found")
#         matching_results = [res for (f, e), res in entity_results.items() if e == entity]
 
#         if not matching_results:
#             input_fields = "Not Found"
#         else:
#             unique_values = set(
#                 res["actual"] if res["status"] != "Varying" else "Varying"
#                 for res in matching_results
#             )
#             input_fields = unique_values.pop() if len(unique_values) == 1 else "Varying across files"
 
#         fields_comparison.append({
#             "Entity name": entity,
#             "SAAS sheet (number of fields)": saas_fields,
#             "output (number of fields)": input_fields
#         })
 
#     fields_comparison_df = pd.DataFrame(fields_comparison)
 
#     # -----------------------------
#     # Required Failed Records Sheet
#     # -----------------------------
#     required_failed_df = pd.DataFrame(required_failed_records)
 
#     # -----------------------------
#     # Required Summary Sheet
#     # -----------------------------
#     summary_rows = []
 
#     for entity, info in required_summary_map.items():
#         summary_rows.append({
#             "Entity": entity,
#             "Required Fields Count": info["required_fields"],
#             "Total Records": info["total_records"],
#             "Failed Records": info["failed_records"],
#             "Passed Records": info["total_records"] - info["failed_records"],
#             "Total Missing Instances": info["fail_instances"]
#         })
 
#     required_summary_df = pd.DataFrame(summary_rows)
 
#     # -----------------------------
#     # Field Comparison Summary Sheet
#     # -----------------------------
#     varying_records_df = pd.DataFrame(varying_records)
 
#     varying_summary_rows = []
#     for entity, info in variation_map.items():
#         varying_summary_rows.append({
#             "Entity": entity,
#             "Expected Fields": info["expected"],
#             "Unique Actual Field Counts": ", ".join(str(x) for x in sorted(info["actual_values"])),
#             "Count of Varied Records": info["count"]
#         })
 
#     varying_summary_df = pd.DataFrame(varying_summary_rows)
 
#     # -----------------------------
#     # Write Excel
#     # -----------------------------
#     try:
#         with pd.ExcelWriter(output_excel) as writer:
#             fields_comparison_df.to_excel(writer, sheet_name="Fields Comparison", index=False)
#             required_failed_df.to_excel(writer, sheet_name="Required – Failed Records", index=False)
#             required_summary_df.to_excel(writer, sheet_name="Required Summary", index=False)
 
#             if not varying_records_df.empty:
#                 varying_records_df.to_excel(writer, sheet_name="Field Comparison Summary", index=False)
 
#             if not varying_summary_df.empty:
#                 # FIXED: shorter name to avoid >31 chars Excel limit
#                 varying_summary_df.to_excel(writer, sheet_name="Varying Summary", index=False)
 
#         print(f"Success: output saved → {output_excel}")
 
#     except Exception as e:
#         print(f"Error writing output: {e}")
#         return False
 
#     return True
 
 
# # Run
# if __name__ == "__main__":
#     compare_fields(
#         mapping_file="Saas_Legacy_Migration.xlsx",
#         input_folder="Input File",
#         output_excel="output_entity_check.xlsx"
#     )


## last updated


import pandas as pd
import os
import re


def compare_fields(mapping_file, input_folder, output_excel):

    # --------------------------------------------------
    # Load mapping file
    # --------------------------------------------------
    mapping_data = pd.read_excel(mapping_file, sheet_name=None, header=1)
    for sheet in mapping_data:
        mapping_data[sheet].columns = mapping_data[sheet].columns.map(str)

    # --------------------------------------------------
    # Build expected columns & required fields
    # --------------------------------------------------
    expected_columns = {}
    required_fields = {}

    for entity, sheet in mapping_data.items():
        position_col = next((c for c in sheet.columns if "Position" in c), None)

        if position_col:
            positions = pd.to_numeric(sheet[position_col], errors="coerce").dropna()
            expected_columns[entity] = int(positions.max()) if not positions.empty else 0
        else:
            expected_columns[entity] = 0

        req_list = []
        for _, row in sheet.iterrows():
            if str(row.get("Required?", "")).strip().lower().startswith("yes"):
                pos = row.get(position_col)
                if pd.notna(pos):
                    req_list.append((row.get("Description", ""), int(pos)))

        required_fields[entity] = req_list

    # --------------------------------------------------
    # Result containers
    # --------------------------------------------------
    entity_results = {}
    required_summary = {}
    sample_failed = {}   # max 5 samples per entity
    variation_map = {}
    varying_records = []

    # --------------------------------------------------
    # Process input files (STREAM SAFE)
    # --------------------------------------------------
    for filename in os.listdir(input_folder):
        if not filename.endswith(".txt"):
            continue

        file_path = os.path.join(input_folder, filename)
        record_number = 0
        line_entity_counts = {}

        with open(file_path, "r", encoding="utf-8", errors="replace") as file:
            for line in file:
                record_number += 1
                cols = line.rstrip("\n").split("|")
                entity = cols[0].strip()

                if not entity:
                    continue

                actual_count = len(cols)
                expected_count = expected_columns.get(entity, 0)
                key = (filename, entity)

                # -------- Field count summary --------
                if key not in entity_results:
                    entity_results[key] = {
                        "expected": expected_count,
                        "actual": actual_count,
                        "status": "Pass" if actual_count == expected_count else "Fail"
                    }
                elif actual_count != entity_results[key]["actual"]:
                    entity_results[key]["status"] = "Varying"

                line_entity_counts.setdefault(key, []).append(actual_count)

                # -------- Required field summary --------
                if entity not in required_summary:
                    required_summary[entity] = {
                        "required_fields": len(required_fields.get(entity, [])),
                        "total_records": 0,
                        "failed_records": 0,
                        "fail_instances": 0
                    }

                required_summary[entity]["total_records"] += 1

                missing = []
                for field_name, pos in required_fields.get(entity, []):
                    idx = pos - 1
                    value = cols[idx].strip() if idx < len(cols) else ""
                    if value == "" or value.lower() == "null":
                        missing.append((field_name, pos, value))

                if missing:
                    required_summary[entity]["failed_records"] += 1
                    required_summary[entity]["fail_instances"] += len(missing)

                    # Store only 5 samples
                    if entity not in sample_failed:
                        sample_failed[entity] = []

                    if len(sample_failed[entity]) < 5:
                        f, p, v = missing[0]
                        sample_failed[entity].append({
                            "Filename": filename,
                            "Record Number": record_number,
                            "Missing Field": f,
                            "Position": p,
                            "Actual Value": v
                        })

        # -------- Varying field counts --------
        for (fname, entity), counts in line_entity_counts.items():
            unique = set(counts)
            if len(unique) > 1:
                variation_map.setdefault(entity, {
                    "expected": expected_columns.get(entity, 0),
                    "actual_values": set(),
                    "count": 0
                })
                variation_map[entity]["actual_values"].update(unique)
                variation_map[entity]["count"] += len(counts)

    # --------------------------------------------------
    # Output DataFrames
    # --------------------------------------------------
    fields_comp = []
    for entity in expected_columns:
        matches = [v for (f, e), v in entity_results.items() if e == entity]
        input_val = "Not Found" if not matches else (
            "Varying" if any(m["status"] == "Varying" for m in matches)
            else matches[0]["actual"]
        )

        fields_comp.append({
            "Entity": entity,
            "SAAS Fields": expected_columns[entity],
            "Input Fields": input_val
        })

    fields_df = pd.DataFrame(fields_comp)

    summary_df = pd.DataFrame([
        {
            "Entity": e,
            "Required Fields": v["required_fields"],
            "Total Records": v["total_records"],
            "Failed Records": v["failed_records"],
            "Passed Records": v["total_records"] - v["failed_records"],
            "Missing Instances": v["fail_instances"]
        }
        for e, v in required_summary.items()
    ])

    sample_df = pd.DataFrame([
        {"Entity": e, **row}
        for e, rows in sample_failed.items()
        for row in rows
    ])

    varying_df = pd.DataFrame([
        {
            "Entity": e,
            "Expected Fields": v["expected"],
            "Actual Field Counts": ", ".join(map(str, sorted(v["actual_values"]))),
            "Varied Records": v["count"]
        }
        for e, v in variation_map.items()
    ])

    # --------------------------------------------------
    # Write Excel (FAST)
    # --------------------------------------------------
    with pd.ExcelWriter(output_excel) as writer:
        fields_df.to_excel(writer, sheet_name="Fields Comparison", index=False)
        summary_df.to_excel(writer, sheet_name="Required Summary", index=False)
        if not sample_df.empty:
            sample_df.to_excel(writer, sheet_name="Failed Samples (5)", index=False)
        if not varying_df.empty:
            varying_df.to_excel(writer, sheet_name="Varying Summary", index=False)

    print(f"Validation completed → {output_excel}")
    return True


# --------------------------------------------------
# Run
# --------------------------------------------------
if __name__ == "__main__":
    compare_fields(
        mapping_file="Saas_Legacy_Migration.xlsx",
        input_folder="Input File",
        output_excel="output_entity_check.xlsx"
    )
 