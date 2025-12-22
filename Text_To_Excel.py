# import pandas as pd
# import os
# from datetime import datetime

# def column_number_to_letter(column_number):
#     """Convert a 1-based column number to an Excel column letter."""
#     if column_number <= 0:
#         return ''
#     column_letter = ''
#     while column_number > 0:
#         column_number, remainder = divmod(column_number - 1, 26)
#         column_letter = chr(65 + remainder) + column_letter
#     return column_letter

# import pandas as pd
# import os
# from datetime import datetime

# def column_number_to_letter(column_number):
#     """Convert a 1-based column number to an Excel column letter."""
#     if column_number <= 0:
#         return ''
#     column_letter = ''
#     while column_number > 0:
#         column_number, remainder = divmod(column_number - 1, 26)
#         column_letter = chr(65 + remainder) + column_letter
#     return column_letter

# def process_and_validate_files(expected_columns, specific_words, input_folder, output_excel, count_of_records_excel, empty_columns_summary_excel):
#     summary = []
#     validation_results = []
#     empty_column_summary = []
#     entity_results = {}
#     entity_counts = {}
#     trnh_sum = 0
#     column_sums = {}
#     column_counts = {}
#     column_values = {}
#     trnh_distinct_counts = {}  # Dictionary to store counts of distinct values in the 4th column
#     acct_is_disputed_not_null_count = 0  # Counter for non-null IS_DISPUTED
#     trnh_prnapplyamt_prndueagency_null_count = 0  # Counter for null PRNAPPLYAMT and PRNDUEAGENCY
#     trnh_aftracctdte_past_count = 0  # Counter for past dates in AFTRACCTDTE
#     trnh_aftracctdte_present_count = 0  # Counter for present dates in AFTRACCTDTE
#     trnh_aftracctdte_future_count = 0  # Counter for future dates in AFTRACCTDTE
#     trnh_ainintapplyamt_sum = 0  # Sum of AININTAPPLYAMT
#     trnh_ainintapplyamt_count = 0  # Count of non-zero AININTAPPLYAMT

#     column_names = [
#         'PRNAPPLYAMT', 'PRNDUEAGENCY', 'PRNDUECLIENT', 'INTAPPLYAMT', 'INTDUEAGENCY', 'INTDUECLIENT',
#         'LI3BALAPPLYAMT', 'LI3BALDUEAGENCY', 'LIBBALDUECLIENT', 'L14BALAPPLYAMT', 'LI4BALDUEAGENCY',
#         'LI4BALDUECLIENT', 'AININTAPDI VAMT', 'AININTDUEAGENCY', 'AININTDUECLIENT', 'MS1APPLYAMT',
#         'MS1DUEAGENCY', 'MS1DUECLIENT'
#     ]

#     bal_column_names = [
#         'PRN_INITIALBALANCE', 'INT_INITIALBALANCE', 'LI3_INITIALBALANCE', 'LI4_INITIALBALANCE', 
#         'PRN_CURRENTBALANCE', 'INT_CURRENTBALANCE', 'MS1_CURRENTBALANCE','AIN_CURRENTBALANCE'
#     ]

#     party_column_names = [
#         'ARENLITFCRAFLAG', 'ARENLITTCPAFLAG', 'ARENLITFDCPAFLAG', 'ARENLITFILEDATE'
#     ]

#     poe_column_names = [
#         'Name of employer without NULL values', 'Name of employer with NULL values'
#     ]

#     acct_column_names = [
#         'IS_DISPUTED'
#     ]

#     for name in column_names:
#         column_sums[name] = 0
#         column_counts[name] = 0
#         column_values[name] = []

#     try:
#         for filename in os.listdir(input_folder):
#             if filename.endswith(".txt"):
#                 file_path = os.path.join(input_folder, filename)
#                 file_content = None
#                 try:
#                     with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
#                         file_content = file.readlines()
#                     print(f"Successfully decoded file {file_path} with UTF-8 (errors replaced).")
#                 except UnicodeDecodeError as e:
#                     print(f"Error decoding file {file_path} with UTF-8: {e}")
#                     try:
#                         with open(file_path, 'r', encoding='latin1', errors='replace') as file:
#                             file_content = file.readlines()
#                         print(f"Successfully decoded file {file_path} with LATIN1 (errors replaced).")
#                     except UnicodeDecodeError as e:
#                         print(f"Error decoding file {file_path} with LATIN1: {e}")
#                         continue

#                 if file_content is None:
#                     print(f"Failed to decode file {file_path}. Skipping.")
#                     continue

#                 empty_counts = {}
#                 for line in file_content:
#                     columns = line.strip().split('|')
#                     if len(columns) > 0:
#                         entity_name = columns[0].strip()
#                     else:
#                         entity_name = None
#                     if entity_name in specific_words:
#                         actual_columns_count = len(columns)
#                         expected_columns_count = expected_columns.get(entity_name, 0)
#                         if (filename, entity_name) not in entity_results:
#                             entity_results[(filename, entity_name)] = {"expected": expected_columns_count, "status": "Pass"}
#                         if actual_columns_count != expected_columns_count:
#                             entity_results[(filename, entity_name)]["status"] = "Fail"
#                         for i, column_value in enumerate(columns):
#                             if i > 0:
#                                 column_letter = column_number_to_letter(i + 1)
#                                 if not column_value.strip():
#                                     key = (filename, entity_name, column_letter)
#                                     if key in empty_counts:
#                                         empty_counts[key] += 1
#                                     else:
#                                         empty_counts[key] = 1
#                         if entity_name not in entity_counts:
#                             entity_counts[entity_name] = 0
#                         entity_counts[entity_name] += 1
#                         if entity_name == 'TRNH' and len(columns) > 24:
#                             try:
#                                 trnh_sum += float(columns[4].strip())
#                                 # Update the count of distinct values in the 4th column
#                                 aftrtyp = columns[3].strip()
#                                 if aftrtyp in trnh_distinct_counts:
#                                     trnh_distinct_counts[aftrtyp] += 1
#                                 else:
#                                     trnh_distinct_counts[aftrtyp] = 1
#                                 # Check if both PRNAPPLYAMT and PRNDUEAGENCY are null
#                                 if not columns[12].strip() and not columns[13].strip():
#                                     trnh_prnapplyamt_prndueagency_null_count += 1
#                                 # Check the date in the 7th column
#                                 aftracctdte = columns[6].strip()
#                                 if aftracctdte:
#                                     aftracctdte_date = datetime.strptime(aftracctdte, '%m-%d-%Y')
#                                     today = datetime.today()
#                                     if aftracctdte_date < today:
#                                         trnh_aftracctdte_past_count += 1
#                                     elif aftracctdte_date == today:
#                                         trnh_aftracctdte_present_count += 1
#                                     else:
#                                         trnh_aftracctdte_future_count += 1
#                                 # Calculate sum and count for AININTAPPLYAMT (25th column)
#                                 ainintapplyamt = columns[24].strip()
#                                 if ainintapplyamt:
#                                     trnh_ainintapplyamt_sum += float(ainintapplyamt)
#                                     trnh_ainintapplyamt_count += 1
#                             except ValueError:
#                                 pass
#                         for idx, name in enumerate(column_names, start=12):
#                             if entity_name == 'TRNH' and len(columns) > idx:
#                                 try:
#                                     value = float(columns[idx].strip())
#                                     column_sums[name] += value
#                                     if value != 0:
#                                         column_values[name].append(value)
#                                         column_counts[name] += 1
#                                 except ValueError:
#                                     pass
#                         if entity_name == 'ACCT' and len(columns) > 36:
#                             is_disputed = columns[35].strip()
#                             if is_disputed:
#                                 acct_is_disputed_not_null_count += 1

#                 for (file_name, entity_name, column_letter), count in empty_counts.items():
#                     empty_column_summary.append({
#                         'Source File': file_name,
#                         'Customer entity name': entity_name,
#                         'Column Name': column_letter,
#                         'Status': 'Fail',
#                         'Empty Count': count
#                     })

#                 with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
#                     file_content = file.read()

#                 for word in specific_words:
#                     if word in file_content:
#                         validation_results.append({"File Name": filename, "Entity": word, "Status": "Pass"})
#                     else:
#                         validation_results.append({"File Name": filename, "Entity": word, "Status": "Fail"})

#         print("Entity Results:", entity_results)
#         print("Summary List:", summary)

#         if not entity_results:
#             print("No entity results to process.")
#             return False

#         for (filename, entity_name), result in entity_results.items():
#             summary.append({
#                 'File Name': filename,
#                 'Entity Name': entity_name,
#                 'Expected Columns': result["expected"],
#                 'Status': result["status"]
#             })

#         if not summary:
#             print("No data to process for summary.")
#             return False

#         summary_df = pd.DataFrame(summary).sort_values(by=['File Name', 'Entity Name'])
#         validation_df = pd.DataFrame(validation_results).sort_values(by=['File Name', 'Entity'])
#         empty_column_df = pd.DataFrame(empty_column_summary).sort_values(by='Empty Count', ascending=False)
#         empty_column_df = empty_column_df[['Source File', 'Customer entity name', 'Column Name', 'Status', 'Empty Count']]

#         try:
#             with pd.ExcelWriter(output_excel) as writer:
#                 summary_df.to_excel(writer, sheet_name='Column Summary', index=False)
#                 validation_df.to_excel(writer, sheet_name='Validation Results', index=False)
#             print(f"Success: Results saved to {output_excel}")
#         except Exception as e:
#             print(f"Error writing to Excel: {e}")
#             return False

#         try:
#             with pd.ExcelWriter(empty_columns_summary_excel) as writer:
#                 empty_column_df.to_excel(writer, sheet_name='Empty Columns Summary', index=False)
#             print(f"Success: Empty Columns Summary saved to {empty_columns_summary_excel}")
#         except Exception as e:
#             print(f"Error writing to Excel: {e}")
#             return False

#         entity_count_df = pd.DataFrame(list(entity_counts.items()), columns=['Entity Name', 'Count of Records'])

#         analysis_data = {
#             'Requirement': [f'Sum of {name}' for name in column_names] + [f'{name}_count' for name in column_names] + [
#                 'Sum of AFTRAMT', 'Sum of AININTAPPLYAMT', 'Count of AININTAPPLYAMT'
#             ],
#             'Value': list(column_sums.values()) + list(column_counts.values()) + [trnh_sum, trnh_ainintapplyamt_sum, trnh_ainintapplyamt_count]
#         }

#         # Add distinct counts of AFTRTYP to analysis_data
#         for aftrtyp, count in trnh_distinct_counts.items():
#             analysis_data['Requirement'].append(f'Count of distinct AFTRTYP: {aftrtyp}')
#             analysis_data['Value'].append(count)

#         # Add count of PRNAPPLYAMT and PRNDUEAGENCY with value null
#         analysis_data['Requirement'].append('Count of PRNAPPLYAMT and PRNDUEAGENCY with value null')
#         analysis_data['Value'].append(trnh_prnapplyamt_prndueagency_null_count)

#         # Add counts of AFTRACCTDTE with past, present, and future dates
#         analysis_data['Requirement'].append('AFTRACCTDTE with PAST DATE')
#         analysis_data['Value'].append(trnh_aftracctdte_past_count)
#         analysis_data['Requirement'].append('AFTRACCTDTE with PRESENT DATE')
#         analysis_data['Value'].append(trnh_aftracctdte_present_count)
#         analysis_data['Requirement'].append('AFTRACCTDTE with FUTURE DATE')
#         analysis_data['Value'].append(trnh_aftracctdte_future_count)

#         analysis_df = pd.DataFrame(analysis_data)

#         try:
#             with pd.ExcelWriter(count_of_records_excel) as writer:
#                 entity_count_df.to_excel(writer, sheet_name='Count of Records', index=False)
#                 analysis_df.to_excel(writer, sheet_name='Analysis of TRNH', index=False)
#             print(f"Success: Entity counts, TRNH sum, and analysis results saved to {count_of_records_excel}")
#         except Exception as e:
#             print(f"Error writing to Excel: {e}")
#             return False

#         # Now process 'BAL' data
#         bal_sums = {name: 0 for name in bal_column_names}
#         bal_counts = {name: 0 for name in bal_column_names}

#         try:
#             for filename in os.listdir(input_folder):
#                 if filename.endswith(".txt"):
#                     file_path = os.path.join(input_folder, filename)
#                     with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
#                         lines = file.readlines()
#                     for line in lines:
#                         columns = line.strip().split('|')
#                         if len(columns) > 0:
#                             entity_name = columns[0].strip()
#                         else:
#                             entity_name = None
#                         if entity_name == 'BAL':
#                             for idx, name in zip([2, 3, 4, 5, 8, 9, 20], bal_column_names):
#                                 if len(columns) > idx:
#                                     try:
#                                         bal_value = float(columns[idx].strip())
#                                         bal_sums[name] += bal_value
#                                         if bal_value != 0:
#                                             bal_counts[name] += 1
#                                     except ValueError:
#                                         pass

#         except Exception as e:
#             print(f"Error processing 'BAL' data in folder: {e}")
#             return False

#         bal_analysis_data = []
#         for name in bal_column_names:
#             bal_analysis_data.append({'Requirement': f'Sum of {name}', 'Value': bal_sums[name]})
#             bal_analysis_data.append({'Requirement': f'Count of {name}', 'Value': bal_counts[name]})

#         bal_analysis_df = pd.DataFrame(bal_analysis_data)

#         try:
#             with pd.ExcelWriter(count_of_records_excel, engine='openpyxl', mode='a') as writer:
#                 bal_analysis_df.to_excel(writer, sheet_name='Analysis of BAL', index=False)
#             print(f"Success: 'Analysis of BAL' results saved to {count_of_records_excel}")
#         except Exception as e:
#             print(f"Error writing 'Analysis of BAL' to Excel: {e}")
#             return False

#         # Now process 'PRTY' data
#         party_counts = {name: 0 for name in party_column_names}
#         arenprisflag_counts = {'Y': 0, 'N': 0}
#         arenbnkrpt_counts = {'Y': 0, 'N': 0}
#         arendeced_counts = {'Y': 0, 'N': 0}
#         arenfnm_null_counts = 0
#         arenlnm_null_counts = 0
#         both_null_counts = 0  # New counter for both columns being null

#         try:
#             for filename in os.listdir(input_folder):
#                 if filename.endswith(".txt"):
#                     file_path = os.path.join(input_folder, filename)
#                     with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
#                         lines = file.readlines()
#                     for line in lines:
#                         columns = line.strip().split('|')
#                         if len(columns) > 0:
#                             entity_name = columns[0].strip()
#                         else:
#                             entity_name = None
#                         if entity_name == 'PRTY' and len(columns) > 101:
#                             try:
#                                 for idx, name in zip([98, 99, 100, 101], party_column_names):
#                                     party_value = columns[idx].strip()
#                                     if party_value:
#                                         party_counts[name] += 1
#                                 arenprisflag_value = columns[94].strip()
#                                 if arenprisflag_value == 'Y':
#                                     arenprisflag_counts['Y'] += 1
#                                 elif arenprisflag_value == 'N':
#                                     arenprisflag_counts['N'] += 1
#                                 arenbnkrpt_value = columns[33].strip()
#                                 if arenbnkrpt_value == 'Y':
#                                     arenbnkrpt_counts['Y'] += 1
#                                 elif arenbnkrpt_value == 'N':
#                                     arenbnkrpt_counts['N'] += 1
#                                 arendeced_value = columns[28].strip()
#                                 if arendeced_value == 'Y':
#                                     arendeced_counts['Y'] += 1
#                                 elif arendeced_value == 'N':
#                                     arendeced_counts['N'] += 1
#                                 # Check for null values in 6th and 8th columns
#                                 arenfnm_value = columns[5].strip()
#                                 arenlnm_value = columns[7].strip()
#                                 if not arenfnm_value:
#                                     arenfnm_null_counts += 1
#                                 if not arenlnm_value:
#                                     arenlnm_null_counts += 1
#                                 if not arenfnm_value and not arenlnm_value:
#                                     both_null_counts += 1
#                             except ValueError:
#                                 pass

#         except Exception as e:
#             print(f"Error processing 'PRTY' data in folder: {e}")
#             return False

#         party_analysis_data = []
#         for name in party_column_names:
#             party_analysis_data.append({'Requirement': f'Count of {name}', 'Value': party_counts[name]})
#         party_analysis_data.append({'Requirement': 'Count of ARENPRISFLAG Y', 'Value': arenprisflag_counts['Y']})
#         party_analysis_data.append({'Requirement': 'Count of ARENPRISFLAG N', 'Value': arenprisflag_counts['N']})
#         party_analysis_data.append({'Requirement': 'Count of ARENBNKRPT Y', 'Value': arenbnkrpt_counts['Y']})
#         party_analysis_data.append({'Requirement': 'Count of ARENBNKRPT N', 'Value': arenbnkrpt_counts['N']})
#         party_analysis_data.append({'Requirement': 'Count of ARENDECEASED Y', 'Value': arendeced_counts['Y']})
#         party_analysis_data.append({'Requirement': 'Count of ARENDECEASED N', 'Value': arendeced_counts['N']})
#         party_analysis_data.append({'Requirement': 'Count of ARENFNM with null data', 'Value': arenfnm_null_counts})
#         party_analysis_data.append({'Requirement': 'Count of ARENLNM with null data', 'Value': arenlnm_null_counts})
#         party_analysis_data.append({'Requirement': 'Count of both first and lastname Null', 'Value': both_null_counts})

#         party_analysis_df = pd.DataFrame(party_analysis_data)

#         try:
#             with pd.ExcelWriter(count_of_records_excel, engine='openpyxl', mode='a') as writer:
#                 party_analysis_df.to_excel(writer, sheet_name='Analysis of PARTY_INFO', index=False)
#             print(f"Success: 'Analysis of PARTY_INFO' results saved to {count_of_records_excel}")
#         except Exception as e:
#             print(f"Error writing 'Analysis of PARTY_INFO' to Excel: {e}")
#             return False

#         # Now process 'POE' data
#         poe_counts = {name: 0 for name in poe_column_names}

#         try:
#             for filename in os.listdir(input_folder):
#                 if filename.endswith(".txt"):
#                     file_path = os.path.join(input_folder, filename)
#                     with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
#                         lines = file.readlines()
#                     for line in lines:
#                         columns = line.strip().split('|')
#                         if len(columns) > 0:
#                             entity_name = columns[0].strip()
#                         else:
#                             entity_name = None
#                         if entity_name == 'POE' and len(columns) > 3:
#                             employer_name = columns[3].strip()
#                             if employer_name:
#                                 poe_counts['Name of employer without NULL values'] += 1
#                             else:
#                                 poe_counts['Name of employer with NULL values'] += 1

#         except Exception as e:
#             print(f"Error processing 'POE' data in folder: {e}")
#             return False

#         poe_analysis_data = [
#             {'Requirement': 'Name of employer without NULL values', 'Value': poe_counts['Name of employer without NULL values']},
#             {'Requirement': 'Name of employer with NULL values', 'Value': poe_counts['Name of employer with NULL values']}
#         ]

#         poe_analysis_df = pd.DataFrame(poe_analysis_data)

#         try:
#             with pd.ExcelWriter(count_of_records_excel, engine='openpyxl', mode='a') as writer:
#                 poe_analysis_df.to_excel(writer, sheet_name='Analysis of POE', index=False)
#             print(f"Success: 'Analysis of POE' results saved to {count_of_records_excel}")
#         except Exception as e:
#             print(f"Error writing 'Analysis of POE' to Excel: {e}")
#             return False

#         # Create 'Analysis of ACCT' sheet
#         acct_analysis_data = [
#             {'Requirement': 'Count of IS_DISPUTED not NULL', 'Value': acct_is_disputed_not_null_count}
#         ]
#         acct_analysis_df = pd.DataFrame(acct_analysis_data)

#         try:
#             with pd.ExcelWriter(count_of_records_excel, engine='openpyxl', mode='a') as writer:
#                 acct_analysis_df.to_excel(writer, sheet_name='Analysis of ACCT', index=False)
#             print(f"Success: 'Analysis of ACCT' results saved to {count_of_records_excel}")
#         except Exception as e:
#             print(f"Error writing 'Analysis of ACCT' to Excel: {e}")
#             return False

#     except Exception as e:
#         print(f"Error processing files in folder: {e}")
#         return False

#     return True

# # original working file - above


# import pandas as pd
# import os
# from datetime import datetime
# from collections import defaultdict

# def column_number_to_letter(column_number):
#     """Convert a 1-based column number to an Excel column letter."""
#     if column_number <= 0:
#         return ''
#     column_letter = ''
#     while column_number > 0:
#         column_number, remainder = divmod(column_number - 1, 26)
#         column_letter = chr(65 + remainder) + column_letter
#     return column_letter

# def process_and_validate_files(expected_columns, specific_words, input_folder,
#                                output_excel, count_of_records_excel, empty_columns_summary_excel,
#                                mapping_file_path=None):
#     """
#     Restored original logic + streaming entity counting.
#     - expected_columns: dict (preferred) OR used for expected column counts
#     - mapping_file_path: optional path to Saas_Legacy_Migration.xlsx (if expected_columns not provided)
#     """

#     # init variables (original)
#     summary = []
#     validation_results = []
#     empty_column_summary = []
#     entity_results = {}
#     # entity_counts will be computed by streaming (fast)
#     entity_counts = {}
#     trnh_sum = 0
#     column_sums = {}
#     column_counts = {}
#     column_values = {}
#     trnh_distinct_counts = {}  # Dictionary to store counts of distinct values in the 4th column
#     acct_is_disputed_not_null_count = 0  # Counter for non-null IS_DISPUTED
#     trnh_prnapplyamt_prndueagency_null_count = 0  # Counter for null PRNAPPLYAMT and PRNDUEAGENCY
#     trnh_aftracctdte_past_count = 0  # Counter for past dates in AFTRACCTDTE
#     trnh_aftracctdte_present_count = 0  # Counter for present dates in AFTRACCTDTE
#     trnh_aftracctdte_future_count = 0  # Counter for future dates in AFTRACCTDTE
#     trnh_ainintapplyamt_sum = 0  # Sum of AININTAPPLYAMT
#     trnh_ainintapplyamt_count = 0  # Count of non-zero AININTAPPLYAMT

#     column_names = [
#         'PRNAPPLYAMT', 'PRNDUEAGENCY', 'PRNDUECLIENT', 'INTAPPLYAMT', 'INTDUEAGENCY', 'INTDUECLIENT',
#         'LI3BALAPPLYAMT', 'LI3BALDUEAGENCY', 'LIBBALDUECLIENT', 'L14BALAPPLYAMT', 'LI4BALDUEAGENCY',
#         'LI4BALDUECLIENT', 'AININTAPDI VAMT', 'AININTDUEAGENCY', 'AININTDUECLIENT', 'MS1APPLYAMT',
#         'MS1DUEAGENCY', 'MS1DUECLIENT'
#     ]

#     bal_column_names = [
#         'PRN_INITIALBALANCE', 'INT_INITIALBALANCE', 'LI3_INITIALBALANCE', 'LI4_INITIALBALANCE',
#         'PRN_CURRENTBALANCE', 'INT_CURRENTBALANCE', 'MS1_CURRENTBALANCE','AIN_CURRENTBALANCE'
#     ]

#     party_column_names = [
#         'ARENLITFCRAFLAG', 'ARENLITTCPAFLAG', 'ARENLITFDCPAFLAG', 'ARENLITFILEDATE'
#     ]

#     poe_column_names = [
#         'Name of employer without NULL values', 'Name of employer with NULL values'
#     ]

#     acct_column_names = [
#         'IS_DISPUTED'
#     ]

#     for name in column_names:
#         column_sums[name] = 0
#         column_counts[name] = 0
#         column_values[name] = []

#     # ---------------------------
#     # Determine mapping_data and SAAS entity list (preserve old behavior)
#     # ---------------------------
#     mapping_data = None
#     try:
#         if isinstance(expected_columns, dict) and expected_columns:
#             mapping_data = expected_columns
#             print("Using mapping data provided in expected_columns (dict).")
#         else:
#             if mapping_file_path and os.path.exists(mapping_file_path):
#                 mapping_data = pd.read_excel(mapping_file_path, sheet_name=None, header=1, engine='openpyxl')
#                 # normalize column names in mapping_data
#                 for s in mapping_data:
#                     try:
#                         mapping_data[s].columns = mapping_data[s].columns.map(str).str.strip()
#                     except Exception:
#                         pass
#                 print(f"Loaded mapping file: {mapping_file_path}")
#             else:
#                 mapping_data = expected_columns if isinstance(expected_columns, dict) else {}
#                 print("Mapping file path not provided or not found; using expected_columns if available.")

#         if isinstance(mapping_data, dict):
#             all_saas_entities = list(mapping_data.keys())
#         else:
#             all_saas_entities = []
#     except Exception as e:
#         print(f"Error preparing mapping data: {e}")
#         all_saas_entities = []

#     print(f"Total SAAS entities available: {len(all_saas_entities)}")

#     # ---------------------------
#     # First pass: original per-line checks (empty columns, TRNH sums, validations)
#     # We'll stream files line-by-line to avoid readlines memory issues.
#     # We'll NOT increment entity_counts here (we'll compute counts separately in a streaming pass below).
#     # ---------------------------
#     try:
#         files = [f for f in os.listdir(input_folder) if f.lower().endswith(".txt")]
#         if not files:
#             print(f"No .txt files found in input folder: {input_folder}")
#             return False

#         consolidated_records = []  # minimal consolidated info (filename, entity, column_count)

#         for filename in files:
#             file_path = os.path.join(input_folder, filename)
#             print(f"Processing file for validations: {filename}")

#             # Attempt utf-8, fallback latin1
#             fh = None
#             try:
#                 fh = open(file_path, 'r', encoding='utf-8', errors='replace')
#             except Exception:
#                 try:
#                     fh = open(file_path, 'r', encoding='latin1', errors='replace')
#                 except Exception as e:
#                     print(f"Unable to open file {file_path}: {e}")
#                     continue

#             with fh:
#                 empty_counts = {}
#                 for raw_line in fh:
#                     line = raw_line.rstrip("\n\r")
#                     if not line:
#                         continue
#                     columns = line.split('|')
#                     entity_name = columns[0].strip() if len(columns) > 0 else None

#                     # original specific_words check for expected column count
#                     if entity_name in specific_words:
#                         actual_columns_count = len(columns)
#                         expected_columns_count = expected_columns.get(entity_name, 0) if isinstance(expected_columns, dict) else 0
#                         key = (filename, entity_name)
#                         if key not in entity_results:
#                             entity_results[key] = {"expected": expected_columns_count, "status": "Pass"}
#                         if actual_columns_count != expected_columns_count:
#                             entity_results[key]["status"] = "Fail"
#                         # empty columns detection (i>0)
#                         for i, column_value in enumerate(columns):
#                             if i > 0:
#                                 column_letter = column_number_to_letter(i + 1)
#                                 if not str(column_value).strip():
#                                     ec_key = (filename, entity_name, column_letter)
#                                     empty_counts[ec_key] = empty_counts.get(ec_key, 0) + 1

#                     # TRNH checks (preserve)
#                     if entity_name == 'TRNH' and len(columns) > 24:
#                         try:
#                             trnh_sum += float(columns[4].strip() or 0)
#                         except Exception:
#                             pass
#                         aftrtyp = columns[3].strip()
#                         trnh_distinct_counts[aftrtyp] = trnh_distinct_counts.get(aftrtyp, 0) + 1
#                         if not columns[12].strip() and not columns[13].strip():
#                             trnh_prnapplyamt_prndueagency_null_count += 1
#                         aftracctdte = columns[6].strip()
#                         if aftracctdte:
#                             try:
#                                 aftracctdte_date = datetime.strptime(aftracctdte, '%m-%d-%Y')
#                                 today = datetime.today()
#                                 if aftracctdte_date < today:
#                                     trnh_aftracctdte_past_count += 1
#                                 elif aftracctdte_date == today:
#                                     trnh_aftracctdte_present_count += 1
#                                 else:
#                                     trnh_aftracctdte_future_count += 1
#                             except Exception:
#                                 pass
#                         ainintapplyamt = columns[24].strip()
#                         if ainintapplyamt:
#                             try:
#                                 trnh_ainintapplyamt_sum += float(ainintapplyamt)
#                                 trnh_ainintapplyamt_count += 1
#                             except Exception:
#                                 pass

#                     # TRNH column sums
#                     for idx, name in enumerate(column_names, start=12):
#                         if entity_name == 'TRNH' and len(columns) > idx:
#                             try:
#                                 value = float(columns[idx].strip() or 0)
#                                 column_sums[name] += value
#                                 if value != 0:
#                                     column_values[name].append(value)
#                                     column_counts[name] += 1
#                             except Exception:
#                                 pass

#                     # ACCT IS_DISPUTED counter
#                     if entity_name == 'ACCT' and len(columns) > 36:
#                         is_disputed = columns[35].strip()
#                         if is_disputed:
#                             acct_is_disputed_not_null_count += 1

#                     # minimal consolidated info
#                     consolidated_records.append([filename, entity_name, len(columns)])

#                 # after file processed, append empty_counts entries
#                 for (f_nm, ent_nm, col_let), cnt in empty_counts.items():
#                     empty_column_summary.append({
#                         'Source File': f_nm,
#                         'Customer entity name': ent_nm,
#                         'Column Name': col_let,
#                         'Status': 'Fail',
#                         'Empty Count': cnt
#                     })

#                 # validation_results based on file content (originally read whole file)
#                 try:
#                     with open(file_path, 'r', encoding='utf-8', errors='replace') as rf:
#                         whole = rf.read()
#                 except Exception:
#                     try:
#                         with open(file_path, 'r', encoding='latin1', errors='replace') as rf:
#                             whole = rf.read()
#                     except Exception:
#                         whole = ''
#                 for word in specific_words:
#                     if word in whole:
#                         validation_results.append({"File Name": filename, "Entity": word, "Status": "Pass"})
#                     else:
#                         validation_results.append({"File Name": filename, "Entity": word, "Status": "Fail"})

#     except Exception as e:
#         print(f"Error processing files in folder: {e}")
#         return False

#     # Build summary list (Column Summary) from entity_results (same as original)
#     if not entity_results:
#         print("No entity results to process.")
#         # still proceed to counts and other outputs (to avoid silent failure)
#     for (filename, entity_name), result in entity_results.items():
#         summary.append({
#             'File Name': filename,
#             'Entity Name': entity_name,
#             'Expected Columns': result["expected"],
#             'Status': result["status"]
#         })

#     if not summary and not validation_results:
#         print("No data to process for summary.")
#         # Continue so that counts etc. still get created (to match previous behavior)
#     # Create DataFrames
#     summary_df = pd.DataFrame(summary).sort_values(by=['File Name', 'Entity Name']) if summary else pd.DataFrame()
#     validation_df = pd.DataFrame(validation_results).sort_values(by=['File Name', 'Entity']) if validation_results else pd.DataFrame()
#     empty_column_df = pd.DataFrame(empty_column_summary).sort_values(by='Empty Count', ascending=False) if empty_column_summary else pd.DataFrame()
#     if not empty_column_df.empty:
#         # Keep column order
#         cols = ['Source File', 'Customer entity name', 'Column Name', 'Status', 'Empty Count']
#         existing_cols = [c for c in cols if c in empty_column_df.columns]
#         empty_column_df = empty_column_df[existing_cols]

#     # Write Column Summary + Validation Results to output_excel (same as original)
#     try:
#         with pd.ExcelWriter(output_excel) as writer:
#             if not summary_df.empty:
#                 summary_df.to_excel(writer, sheet_name='Column Summary', index=False)
#             if not validation_df.empty:
#                 validation_df.to_excel(writer, sheet_name='Validation Results', index=False)
#         print(f"Success: Results saved to {output_excel}")
#     except Exception as e:
#         print(f"Error writing to Excel (output_excel): {e}")
#         return False

#     # Write Empty Columns Summary
#     try:
#         with pd.ExcelWriter(empty_columns_summary_excel) as writer:
#             if not empty_column_df.empty:
#                 empty_column_df.to_excel(writer, sheet_name='Empty Columns Summary', index=False)
#             else:
#                 # write empty DF to preserve sheet presence
#                 pd.DataFrame(columns=['Source File', 'Customer entity name', 'Column Name', 'Status', 'Empty Count']).to_excel(writer, sheet_name='Empty Columns Summary', index=False)
#         print(f"Success: Empty Columns Summary saved to {empty_columns_summary_excel}")
#     except Exception as e:
#         print(f"Error writing to Excel (empty_columns_summary): {e}")
#         return False

#     # ---------------------------
#     # Now compute entity_counts using efficient streaming (counts for all SAAS entities)
#     # ---------------------------
#     try:
#         # If mapping_data had sheets, use those; else we count all entities encountered
#         saas_entities = list(mapping_data.keys()) if isinstance(mapping_data, dict) and mapping_data else None
#         counts = defaultdict(int)
#         for filename in [f for f in os.listdir(input_folder) if f.lower().endswith('.txt')]:
#             fp = os.path.join(input_folder, filename)
#             try:
#                 with open(fp, 'r', encoding='utf-8', errors='replace') as fh:
#                     for raw_line in fh:
#                         line = raw_line.strip()
#                         if not line or '|' not in line:
#                             continue
#                         ent = line.split('|', 1)[0].strip()
#                         if not ent:
#                             continue
#                         if saas_entities:
#                             if ent in saas_entities:
#                                 counts[ent] += 1
#                         else:
#                             counts[ent] += 1
#             except Exception:
#                 # fallback latin1
#                 try:
#                     with open(fp, 'r', encoding='latin1', errors='replace') as fh:
#                         for raw_line in fh:
#                             line = raw_line.strip()
#                             if not line or '|' not in line:
#                                 continue
#                             ent = line.split('|', 1)[0].strip()
#                             if not ent:
#                                 continue
#                             if saas_entities:
#                                 if ent in saas_entities:
#                                     counts[ent] += 1
#                             else:
#                                 counts[ent] += 1
#                 except Exception:
#                     continue
#         entity_counts = dict(counts)
#     except Exception as e:
#         print(f"Error while counting entities (streaming): {e}")
#         entity_counts = entity_counts or {}

#     # Build entity_count_df and TRNH analysis
#     try:
#         entity_count_df = pd.DataFrame(list(entity_counts.items()), columns=['Entity Name', 'Count of Records'])

#         analysis_data = {
#             'Requirement': [f'Sum of {name}' for name in column_names] + [f'{name}_count' for name in column_names] + [
#                 'Sum of AFTRAMT', 'Sum of AININTAPPLYAMT', 'Count of AININTAPPLYAMT'
#             ],
#             'Value': list(column_sums.values()) + list(column_counts.values()) + [trnh_sum, trnh_ainintapplyamt_sum, trnh_ainintapplyamt_count]
#         }

#         # Add distinct counts of AFTRTYP to analysis_data
#         for aftrtyp, count in trnh_distinct_counts.items():
#             analysis_data['Requirement'].append(f'Count of distinct AFTRTYP: {aftrtyp}')
#             analysis_data['Value'].append(count)

#         # Add count of PRNAPPLYAMT and PRNDUEAGENCY with value null
#         analysis_data['Requirement'].append('Count of PRNAPPLYAMT and PRNDUEAGENCY with value null')
#         analysis_data['Value'].append(trnh_prnapplyamt_prndueagency_null_count)

#         # Add counts of AFTRACCTDTE with past, present, and future dates
#         analysis_data['Requirement'].append('AFTRACCTDTE with PAST DATE')
#         analysis_data['Value'].append(trnh_aftracctdte_past_count)
#         analysis_data['Requirement'].append('AFTRACCTDTE with PRESENT DATE')
#         analysis_data['Value'].append(trnh_aftracctdte_present_count)
#         analysis_data['Requirement'].append('AFTRACCTDTE with FUTURE DATE')
#         analysis_data['Value'].append(trnh_aftracctdte_future_count)

#         analysis_df = pd.DataFrame(analysis_data)

#         # Write Count of Records and TRNH analysis
#         with pd.ExcelWriter(count_of_records_excel, engine='openpyxl' if count_of_records_excel.lower().endswith('.xlsx') else None) as writer:
#             entity_count_df.to_excel(writer, sheet_name='Count of Records', index=False)
#             analysis_df.to_excel(writer, sheet_name='Analysis of TRNH', index=False)

#         print(f"Success: Entity counts, TRNH sum, and analysis results saved to {count_of_records_excel}")
#     except Exception as e:
#         print(f"Error writing count_of_records Excel: {e}")
#         return False

#     # ---------------------------
#     # BAL analysis (stream files again to avoid large memory)
#     # ---------------------------
#     try:
#         bal_sums = {name: 0 for name in bal_column_names}
#         bal_counts = {name: 0 for name in bal_column_names}

#         for filename in [f for f in os.listdir(input_folder) if f.lower().endswith('.txt')]:
#             fp = os.path.join(input_folder, filename)
#             try:
#                 with open(fp, 'r', encoding='utf-8', errors='replace') as fh:
#                     for raw in fh:
#                         parts = raw.rstrip("\n\r").split("|")
#                         entity_name = parts[0].strip() if len(parts) > 0 else None
#                         if entity_name == 'BAL':
#                             for idx, name in zip([2, 3, 4, 5, 8, 9, 20], bal_column_names):
#                                 if len(parts) > idx:
#                                     try:
#                                         bal_value = float(parts[idx].strip() or 0)
#                                         bal_sums[name] += bal_value
#                                         if bal_value != 0:
#                                             bal_counts[name] += 1
#                                     except Exception:
#                                         pass
#             except Exception:
#                 continue

#         bal_analysis_data = []
#         for name in bal_column_names:
#             bal_analysis_data.append({'Requirement': f'Sum of {name}', 'Value': bal_sums[name]})
#             bal_analysis_data.append({'Requirement': f'Count of {name}', 'Value': bal_counts[name]})

#         with pd.ExcelWriter(count_of_records_excel, engine='openpyxl', mode='a') as writer:
#             pd.DataFrame(bal_analysis_data).to_excel(writer, sheet_name='Analysis of BAL', index=False)

#         print(f"Success: 'Analysis of BAL' results saved to {count_of_records_excel}")
#     except Exception as e:
#         print(f"Error processing 'BAL' data in folder: {e}")
#         return False

#     # ---------------------------
#     # PRTY analysis
#     # ---------------------------
#     try:
#         party_counts = {name: 0 for name in party_column_names}
#         arenprisflag_counts = {'Y': 0, 'N': 0}
#         arenbnkrpt_counts = {'Y': 0, 'N': 0}
#         arendeced_counts = {'Y': 0, 'N': 0}
#         arenfnm_null_counts = 0
#         arenlnm_null_counts = 0
#         both_null_counts = 0

#         for filename in [f for f in os.listdir(input_folder) if f.lower().endswith('.txt')]:
#             fp = os.path.join(input_folder, filename)
#             try:
#                 with open(fp, 'r', encoding='utf-8', errors='replace') as fh:
#                     for raw in fh:
#                         parts = raw.rstrip("\n\r").split("|")
#                         entity_name = parts[0].strip() if len(parts) > 0 else None
#                         if entity_name == 'PRTY' and len(parts) > 101:
#                             try:
#                                 for idx, name in zip([98, 99, 100, 101], party_column_names):
#                                     party_value = parts[idx].strip()
#                                     if party_value:
#                                         party_counts[name] += 1
#                                 arenprisflag_value = parts[94].strip()
#                                 if arenprisflag_value == 'Y':
#                                     arenprisflag_counts['Y'] += 1
#                                 elif arenprisflag_value == 'N':
#                                     arenprisflag_counts['N'] += 1
#                                 arenbnkrpt_value = parts[33].strip()
#                                 if arenbnkrpt_value == 'Y':
#                                     arenbnkrpt_counts['Y'] += 1
#                                 elif arenbnkrpt_value == 'N':
#                                     arenbnkrpt_counts['N'] += 1
#                                 arendeced_value = parts[28].strip()
#                                 if arendeced_value == 'Y':
#                                     arendeced_counts['Y'] += 1
#                                 elif arendeced_value == 'N':
#                                     arendeced_counts['N'] += 1
#                                 arenfnm_value = parts[5].strip()
#                                 arenlnm_value = parts[7].strip()
#                                 if not arenfnm_value:
#                                     arenfnm_null_counts += 1
#                                 if not arenlnm_value:
#                                     arenlnm_null_counts += 1
#                                 if not arenfnm_value and not arenlnm_value:
#                                     both_null_counts += 1
#                             except Exception:
#                                 pass
#             except Exception:
#                 continue

#         party_analysis_data = []
#         for name in party_column_names:
#             party_analysis_data.append({'Requirement': f'Count of {name}', 'Value': party_counts[name]})
#         party_analysis_data.append({'Requirement': 'Count of ARENPRISFLAG Y', 'Value': arenprisflag_counts['Y']})
#         party_analysis_data.append({'Requirement': 'Count of ARENPRISFLAG N', 'Value': arenprisflag_counts['N']})
#         party_analysis_data.append({'Requirement': 'Count of ARENBNKRPT Y', 'Value': arenbnkrpt_counts['Y']})
#         party_analysis_data.append({'Requirement': 'Count of ARENBNKRPT N', 'Value': arenbnkrpt_counts['N']})
#         party_analysis_data.append({'Requirement': 'Count of ARENDECEASED Y', 'Value': arendeced_counts['Y']})
#         party_analysis_data.append({'Requirement': 'Count of ARENDECEASED N', 'Value': arendeced_counts['N']})
#         party_analysis_data.append({'Requirement': 'Count of ARENFNM with null data', 'Value': arenfnm_null_counts})
#         party_analysis_data.append({'Requirement': 'Count of ARENLNM with null data', 'Value': arenlnm_null_counts})
#         party_analysis_data.append({'Requirement': 'Count of both first and lastname Null', 'Value': both_null_counts})

#         with pd.ExcelWriter(count_of_records_excel, engine='openpyxl', mode='a') as writer:
#             pd.DataFrame(party_analysis_data).to_excel(writer, sheet_name='Analysis of PARTY_INFO', index=False)

#         print(f"Success: 'Analysis of PARTY_INFO' results saved to {count_of_records_excel}")
#     except Exception as e:
#         print(f"Error processing 'PRTY' data in folder: {e}")
#         return False

#     # ---------------------------
#     # POE analysis
#     # ---------------------------
#     try:
#         poe_counts = {name: 0 for name in poe_column_names}
#         for filename in [f for f in os.listdir(input_folder) if f.lower().endswith('.txt')]:
#             fp = os.path.join(input_folder, filename)
#             try:
#                 with open(fp, 'r', encoding='utf-8', errors='replace') as fh:
#                     for raw in fh:
#                         parts = raw.rstrip("\n\r").split("|")
#                         entity_name = parts[0].strip() if len(parts) > 0 else None
#                         if entity_name == 'POE' and len(parts) > 3:
#                             employer_name = parts[3].strip()
#                             if employer_name:
#                                 poe_counts['Name of employer without NULL values'] += 1
#                             else:
#                                 poe_counts['Name of employer with NULL values'] += 1
#             except Exception:
#                 continue

#         poe_analysis_data = [
#             {'Requirement': 'Name of employer without NULL values', 'Value': poe_counts['Name of employer without NULL values']},
#             {'Requirement': 'Name of employer with NULL values', 'Value': poe_counts['Name of employer with NULL values']}
#         ]
#         with pd.ExcelWriter(count_of_records_excel, engine='openpyxl', mode='a') as writer:
#             pd.DataFrame(poe_analysis_data).to_excel(writer, sheet_name='Analysis of POE', index=False)

#         print(f"Success: 'Analysis of POE' results saved to {count_of_records_excel}")
#     except Exception as e:
#         print(f"Error processing 'POE' data in folder: {e}")
#         return False

#     # ---------------------------
#     # ACCT analysis
#     # ---------------------------
#     try:
#         acct_analysis_data = [
#             {'Requirement': 'Count of IS_DISPUTED not NULL', 'Value': acct_is_disputed_not_null_count}
#         ]
#         with pd.ExcelWriter(count_of_records_excel, engine='openpyxl', mode='a') as writer:
#             pd.DataFrame(acct_analysis_data).to_excel(writer, sheet_name='Analysis of ACCT', index=False)
#         print(f"Success: 'Analysis of ACCT' results saved to {count_of_records_excel}")
#     except Exception as e:
#         print(f"Error writing 'Analysis of ACCT' to Excel: {e}")
#         return False

#     return True




# import pandas as pd
# import os
# from datetime import datetime
# from collections import defaultdict

# def column_number_to_letter(column_number):
#     """Convert a 1-based column number to an Excel column letter."""
#     if column_number <= 0:
#         return ''
#     column_letter = ''
#     while column_number > 0:
#         column_number, remainder = divmod(column_number - 1, 26)
#         column_letter = chr(65 + remainder) + column_letter
#     return column_letter

# def process_and_validate_files(expected_columns, specific_words, input_folder,
#                                output_excel, count_of_records_excel, empty_columns_summary_excel,
#                                mapping_file_path=None):
#     """
#     Process files:
#     - Validate columns
#     - Count entities including zero
#     - Report empty columns
#     - TRNH, BAL, PRTY, POE, ACCT analysis
#     """
#     summary = []
#     validation_results = []
#     empty_column_summary = []
#     entity_results = {}
#     entity_counts = {}
#     trnh_sum = 0
#     column_sums = {}
#     column_counts = {}
#     column_values = {}
#     trnh_distinct_counts = {}
#     acct_is_disputed_not_null_count = 0
#     trnh_prnapplyamt_prndueagency_null_count = 0
#     trnh_aftracctdte_past_count = 0
#     trnh_aftracctdte_present_count = 0
#     trnh_aftracctdte_future_count = 0
#     trnh_ainintapplyamt_sum = 0
#     trnh_ainintapplyamt_count = 0

#     column_names = [
#         'PRNAPPLYAMT', 'PRNDUEAGENCY', 'PRNDUECLIENT', 'INTAPPLYAMT', 'INTDUEAGENCY', 'INTDUECLIENT',
#         'LI3BALAPPLYAMT', 'LI3BALDUEAGENCY', 'LIBBALDUECLIENT', 'L14BALAPPLYAMT', 'LI4BALDUEAGENCY',
#         'LI4BALDUECLIENT', 'AININTAPDI VAMT', 'AININTDUEAGENCY', 'AININTDUECLIENT', 'MS1APPLYAMT',
#         'MS1DUEAGENCY', 'MS1DUECLIENT'
#     ]

#     bal_column_names = [
#         'PRN_INITIALBALANCE', 'INT_INITIALBALANCE', 'LI3_INITIALBALANCE', 'LI4_INITIALBALANCE',
#         'PRN_CURRENTBALANCE', 'INT_CURRENTBALANCE', 'MS1_CURRENTBALANCE','AIN_CURRENTBALANCE'
#     ]

#     party_column_names = [
#         'ARENLITFCRAFLAG', 'ARENLITTCPAFLAG', 'ARENLITFDCPAFLAG', 'ARENLITFILEDATE'
#     ]

#     poe_column_names = [
#         'Name of employer without NULL values', 'Name of employer with NULL values'
#     ]

#     acct_column_names = [
#         'IS_DISPUTED'
#     ]

#     for name in column_names:
#         column_sums[name] = 0
#         column_counts[name] = 0
#         column_values[name] = []

#     # Load mapping_data / SAAS entities
#     mapping_data = None
#     try:
#         if isinstance(expected_columns, dict) and expected_columns:
#             mapping_data = expected_columns
#         elif mapping_file_path and os.path.exists(mapping_file_path):
#             mapping_data = pd.read_excel(mapping_file_path, sheet_name=None, header=1, engine='openpyxl')
#             for s in mapping_data:
#                 try:
#                     mapping_data[s].columns = mapping_data[s].columns.map(str).str.strip()
#                 except Exception:
#                     pass
#         else:
#             mapping_data = expected_columns if isinstance(expected_columns, dict) else {}
#         if isinstance(mapping_data, dict):
#             all_saas_entities = list(mapping_data.keys())
#         else:
#             all_saas_entities = []
#     except Exception as e:
#         print(f"Error preparing mapping data: {e}")
#         all_saas_entities = []

#     print(f"Total SAAS entities available: {len(all_saas_entities)}")

#     # First pass: validation and empty columns
#     try:
#         files = [f for f in os.listdir(input_folder) if f.lower().endswith(".txt")]
#         if not files:
#             print(f"No .txt files found in input folder: {input_folder}")
#             return False

#         for filename in files:
#             file_path = os.path.join(input_folder, filename)
#             print(f"Processing file for validations: {filename}")

#             try:
#                 fh = open(file_path, 'r', encoding='utf-8', errors='replace')
#             except Exception:
#                 try:
#                     fh = open(file_path, 'r', encoding='latin1', errors='replace')
#                 except Exception as e:
#                     print(f"Unable to open file {file_path}: {e}")
#                     continue

#             with fh:
#                 empty_counts = {}
#                 for raw_line in fh:
#                     line = raw_line.rstrip("\n\r")
#                     if not line:
#                         continue
#                     columns = line.split('|')
#                     entity_name = columns[0].strip() if len(columns) > 0 else None

#                     # Column count validation
#                     if entity_name in specific_words:
#                         actual_columns_count = len(columns)
#                         expected_columns_count = expected_columns.get(entity_name, 0) if isinstance(expected_columns, dict) else 0
#                         key = (filename, entity_name)
#                         if key not in entity_results:
#                             entity_results[key] = {"expected": expected_columns_count, "status": "Pass"}
#                         if actual_columns_count != expected_columns_count:
#                             entity_results[key]["status"] = "Fail"
#                         for i, column_value in enumerate(columns):
#                             if i > 0 and not str(column_value).strip():
#                                 ec_key = (filename, entity_name, column_number_to_letter(i + 1))
#                                 empty_counts[ec_key] = empty_counts.get(ec_key, 0) + 1

#                     # TRNH checks
#                     if entity_name == 'TRNH' and len(columns) > 24:
#                         try:
#                             trnh_sum += float(columns[4].strip() or 0)
#                         except Exception:
#                             pass
#                         aftrtyp = columns[3].strip()
#                         trnh_distinct_counts[aftrtyp] = trnh_distinct_counts.get(aftrtyp, 0) + 1
#                         if not columns[12].strip() and not columns[13].strip():
#                             trnh_prnapplyamt_prndueagency_null_count += 1
#                         aftracctdte = columns[6].strip()
#                         if aftracctdte:
#                             try:
#                                 aftracctdte_date = datetime.strptime(aftracctdte, '%m-%d-%Y')
#                                 today = datetime.today()
#                                 if aftracctdte_date < today:
#                                     trnh_aftracctdte_past_count += 1
#                                 elif aftracctdte_date == today:
#                                     trnh_aftracctdte_present_count += 1
#                                 else:
#                                     trnh_aftracctdte_future_count += 1
#                             except Exception:
#                                 pass
#                         ainintapplyamt = columns[24].strip()
#                         if ainintapplyamt:
#                             try:
#                                 trnh_ainintapplyamt_sum += float(ainintapplyamt)
#                                 trnh_ainintapplyamt_count += 1
#                             except Exception:
#                                 pass

#                     # TRNH column sums
#                     for idx, name in enumerate(column_names, start=12):
#                         if entity_name == 'TRNH' and len(columns) > idx:
#                             try:
#                                 value = float(columns[idx].strip() or 0)
#                                 column_sums[name] += value
#                                 if value != 0:
#                                     column_values[name].append(value)
#                                     column_counts[name] += 1
#                             except Exception:
#                                 pass

#                     # ACCT IS_DISPUTED
#                     if entity_name == 'ACCT' and len(columns) > 36:
#                         is_disputed = columns[35].strip()
#                         if is_disputed:
#                             acct_is_disputed_not_null_count += 1

#                 # Add empty columns
#                 for (f_nm, ent_nm, col_let), cnt in empty_counts.items():
#                     empty_column_summary.append({
#                         'Source File': f_nm,
#                         'Customer entity name': ent_nm,
#                         'Column Name': col_let,
#                         'Status': 'Fail',
#                         'Empty Count': cnt
#                     })

#                 # Validation based on specific words
#                 try:
#                     with open(file_path, 'r', encoding='utf-8', errors='replace') as rf:
#                         whole = rf.read()
#                 except Exception:
#                     try:
#                         with open(file_path, 'r', encoding='latin1', errors='replace') as rf:
#                             whole = rf.read()
#                     except Exception:
#                         whole = ''
#                 for word in specific_words:
#                     if word in whole:
#                         validation_results.append({"File Name": filename, "Entity": word, "Status": "Pass"})
#                     else:
#                         validation_results.append({"File Name": filename, "Entity": word, "Status": "Fail"})

#     except Exception as e:
#         print(f"Error processing files in folder: {e}")
#         return False

#     # Build summaries
#     for (filename, entity_name), result in entity_results.items():
#         summary.append({
#             'File Name': filename,
#             'Entity Name': entity_name,
#             'Expected Columns': result["expected"],
#             'Status': result["status"]
#         })

#     summary_df = pd.DataFrame(summary).sort_values(by=['File Name', 'Entity Name']) if summary else pd.DataFrame()
#     validation_df = pd.DataFrame(validation_results).sort_values(by=['File Name', 'Entity']) if validation_results else pd.DataFrame()
#     empty_column_df = pd.DataFrame(empty_column_summary) if empty_column_summary else pd.DataFrame(
#         columns=['Source File', 'Customer entity name', 'Column Name', 'Status', 'Empty Count'])

#     # Write Column Summary + Validation Results
#     with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
#         if not summary_df.empty:
#             summary_df.to_excel(writer, sheet_name='Column Summary', index=False)
#         if not validation_df.empty:
#             validation_df.to_excel(writer, sheet_name='Validation Results', index=False)

#     # Write Empty Columns Summary
#     with pd.ExcelWriter(empty_columns_summary_excel, engine='openpyxl') as writer:
#         empty_column_df.to_excel(writer, sheet_name='Empty Columns Summary', index=False)

#     # Count entities including zeros
#     saas_entities = list(mapping_data.keys()) if isinstance(mapping_data, dict) and mapping_data else None
#     counts = defaultdict(int)
#     for filename in [f for f in os.listdir(input_folder) if f.lower().endswith('.txt')]:
#         fp = os.path.join(input_folder, filename)
#         for enc in ['utf-8', 'latin1']:
#             try:
#                 with open(fp, 'r', encoding=enc, errors='replace') as fh:
#                     for raw_line in fh:
#                         line = raw_line.strip()
#                         if not line or '|' not in line:
#                             continue
#                         ent = line.split('|', 1)[0].strip()
#                         if not ent:
#                             continue
#                         if saas_entities:
#                             if ent in saas_entities:
#                                 counts[ent] += 1
#                         else:
#                             counts[ent] += 1
#                 break
#             except Exception:
#                 continue
#     if saas_entities:
#         for ent in saas_entities:
#             if ent not in counts:
#                 counts[ent] = 0
#     entity_counts = dict(counts)

#     # Build final analysis Excel
#     entity_count_df = pd.DataFrame(list(entity_counts.items()), columns=['Entity Name', 'Count of Records'])

#     analysis_data = {
#         'Requirement': [f'Sum of {name}' for name in column_names] + [f'{name}_count' for name in column_names] + [
#             'Sum of AFTRAMT', 'Sum of AININTAPPLYAMT', 'Count of AININTAPPLYAMT'
#         ],
#         'Value': list(column_sums.values()) + list(column_counts.values()) + [trnh_sum, trnh_ainintapplyamt_sum, trnh_ainintapplyamt_count]
#     }
#     for aftrtyp, count in trnh_distinct_counts.items():
#         analysis_data['Requirement'].append(f'Count of distinct AFTRTYP: {aftrtyp}')
#         analysis_data['Value'].append(count)
#     analysis_data['Requirement'].append('Count of PRNAPPLYAMT and PRNDUEAGENCY with value null')
#     analysis_data['Value'].append(trnh_prnapplyamt_prndueagency_null_count)
#     analysis_data['Requirement'].append('AFTRACCTDTE with PAST DATE')
#     analysis_data['Value'].append(trnh_aftracctdte_past_count)
#     analysis_data['Requirement'].append('AFTRACCTDTE with PRESENT DATE')
#     analysis_data['Value'].append(trnh_aftracctdte_present_count)
#     analysis_data['Requirement'].append('AFTRACCTDTE with FUTURE DATE')
#     analysis_data['Value'].append(trnh_aftracctdte_future_count)

#     analysis_df = pd.DataFrame(analysis_data)

#     with pd.ExcelWriter(count_of_records_excel, engine='openpyxl') as writer:
#         entity_count_df.to_excel(writer, sheet_name='Count of Records', index=False)
#         analysis_df.to_excel(writer, sheet_name='TRNH Analysis', index=False)

#     return True




# import pandas as pd
# import os
# from datetime import datetime
# from collections import defaultdict

# def column_number_to_letter(column_number):
#     """Convert a 1-based column number to an Excel column letter."""
#     if column_number <= 0:
#         return ''
#     column_letter = ''
#     while column_number > 0:
#         column_number, remainder = divmod(column_number - 1, 26)
#         column_letter = chr(65 + remainder) + column_letter
#     return column_letter

# def process_and_validate_files(expected_columns, specific_words, input_folder,
#                                output_excel, count_of_records_excel, empty_columns_summary_excel,
#                                mapping_file_path=None):
#     """
#     Process files:
#     - Validate columns
#     - Count entities including zero
#     - Report empty columns
#     - TRNH, BAL, PRTY, POE, ACCT analysis
#     """
#     summary = []
#     validation_results = []
#     empty_column_summary = []
#     entity_results = {}
#     entity_counts = {}
#     trnh_sum = 0
#     column_sums = {}
#     column_counts = {}
#     column_values = {}
#     trnh_distinct_counts = {}
#     acct_is_disputed_not_null_count = 0
#     trnh_prnapplyamt_prndueagency_null_count = 0
#     trnh_aftracctdte_past_count = 0
#     trnh_aftracctdte_present_count = 0
#     trnh_aftracctdte_future_count = 0
#     trnh_ainintapplyamt_sum = 0
#     trnh_ainintapplyamt_count = 0

#     column_names = [
#         'PRNAPPLYAMT', 'PRNDUEAGENCY', 'PRNDUECLIENT', 'INTAPPLYAMT', 'INTDUEAGENCY', 'INTDUECLIENT',
#         'LI3BALAPPLYAMT', 'LI3BALDUEAGENCY', 'LIBBALDUECLIENT', 'L14BALAPPLYAMT', 'LI4BALDUEAGENCY',
#         'LI4BALDUECLIENT', 'AININTAPDI VAMT', 'AININTDUEAGENCY', 'AININTDUECLIENT', 'MS1APPLYAMT',
#         'MS1DUEAGENCY', 'MS1DUECLIENT'
#     ]

#     bal_column_names = [
#         'PRN_INITIALBALANCE', 'INT_INITIALBALANCE', 'LI3_INITIALBALANCE', 'LI4_INITIALBALANCE',
#         'PRN_CURRENTBALANCE', 'INT_CURRENTBALANCE', 'MS1_CURRENTBALANCE','AIN_CURRENTBALANCE'
#     ]

#     party_column_names = [
#         'ARENLITFCRAFLAG', 'ARENLITTCPAFLAG', 'ARENLITFDCPAFLAG', 'ARENLITFILEDATE'
#     ]

#     poe_column_names = [
#         'Name of employer without NULL values', 'Name of employer with NULL values'
#     ]

#     acct_column_names = [
#         'IS_DISPUTED'
#     ]

#     # Initialize sums, counts, and value lists
#     for name in column_names:
#         column_sums[name] = 0
#         column_counts[name] = 0
#         column_values[name] = []

#     # Load mapping data if provided
#     mapping_data = expected_columns if isinstance(expected_columns, dict) else {}
#     all_saas_entities = list(mapping_data.keys()) if mapping_data else []

#     print(f"Total SAAS entities available: {len(all_saas_entities)}")

#     # ----------------
#     # Process all files
#     # ----------------
#     try:
#         files = [f for f in os.listdir(input_folder) if f.lower().endswith(".txt")]
#         if not files:
#             print(f"No .txt files found in input folder: {input_folder}")
#             return False

#         for filename in files:
#             file_path = os.path.join(input_folder, filename)
#             print(f"Processing file: {filename}")
#             # Try UTF-8 first, then Latin1
#             try:
#                 fh = open(file_path, 'r', encoding='utf-8', errors='replace')
#             except:
#                 fh = open(file_path, 'r', encoding='latin1', errors='replace')

#             with fh:
#                 empty_counts = {}
#                 for raw_line in fh:
#                     line = raw_line.strip()
#                     if not line:
#                         continue
#                     columns = line.split('|')
#                     entity_name = columns[0].strip() if len(columns) > 0 else None

#                     # ----------------
#                     # Validation & empty columns
#                     # ----------------
#                     if entity_name in specific_words:
#                         actual_columns_count = len(columns)
#                         expected_columns_count = expected_columns.get(entity_name, 0) if isinstance(expected_columns, dict) else 0
#                         key = (filename, entity_name)
#                         if key not in entity_results:
#                             entity_results[key] = {"expected": expected_columns_count, "status": "Pass"}
#                         if actual_columns_count != expected_columns_count:
#                             entity_results[key]["status"] = "Fail"
#                         for i, column_value in enumerate(columns):
#                             if i > 0 and not str(column_value).strip():
#                                 ec_key = (filename, entity_name, column_number_to_letter(i + 1))
#                                 empty_counts[ec_key] = empty_counts.get(ec_key, 0) + 1

#                     # ----------------
#                     # TRNH analysis
#                     # ----------------
#                     if entity_name == 'TRNH' and len(columns) > 24:
#                         try:
#                             trnh_sum += float(columns[4].strip() or 0)
#                         except:
#                             pass
#                         aftrtyp = columns[3].strip()
#                         trnh_distinct_counts[aftrtyp] = trnh_distinct_counts.get(aftrtyp, 0) + 1
#                         if not columns[12].strip() and not columns[13].strip():
#                             trnh_prnapplyamt_prndueagency_null_count += 1
#                         aftracctdte = columns[6].strip()
#                         if aftracctdte:
#                             try:
#                                 aftracctdte_date = datetime.strptime(aftracctdte, '%m-%d-%Y')
#                                 today = datetime.today()
#                                 if aftracctdte_date < today:
#                                     trnh_aftracctdte_past_count += 1
#                                 elif aftracctdte_date == today:
#                                     trnh_aftracctdte_present_count += 1
#                                 else:
#                                     trnh_aftracctdte_future_count += 1
#                             except:
#                                 pass
#                         ainintapplyamt = columns[24].strip()
#                         if ainintapplyamt:
#                             try:
#                                 trnh_ainintapplyamt_sum += float(ainintapplyamt)
#                                 trnh_ainintapplyamt_count += 1
#                             except:
#                                 pass

#                     # ----------------
#                     # TRNH column sums
#                     # ----------------
#                     for idx, name in enumerate(column_names, start=12):
#                         if entity_name == 'TRNH' and len(columns) > idx:
#                             try:
#                                 value = float(columns[idx].strip() or 0)
#                                 column_sums[name] += value
#                                 if value != 0:
#                                     column_values[name].append(value)
#                                     column_counts[name] += 1
#                             except:
#                                 pass

#                     # ----------------
#                     # ACCT analysis
#                     # ----------------
#                     if entity_name == 'ACCT' and len(columns) > 36:
#                         is_disputed = columns[35].strip()
#                         if is_disputed:
#                             acct_is_disputed_not_null_count += 1

#                 # Add empty column summary
#                 for (f_nm, ent_nm, col_let), cnt in empty_counts.items():
#                     empty_column_summary.append({
#                         'Source File': f_nm,
#                         'Customer entity name': ent_nm,
#                         'Column Name': col_let,
#                         'Status': 'Fail',
#                         'Empty Count': cnt
#                     })

#         # ----------------
#         # Entity counts including zero
#         # ----------------
#         saas_entities = all_saas_entities
#         counts = defaultdict(int)
#         for filename in files:
#             fp = os.path.join(input_folder, filename)
#             for enc in ['utf-8', 'latin1']:
#                 try:
#                     with open(fp, 'r', encoding=enc, errors='replace') as fh:
#                         for raw_line in fh:
#                             line = raw_line.strip()
#                             if not line or '|' not in line:
#                                 continue
#                             ent = line.split('|', 1)[0].strip()
#                             if not ent:
#                                 continue
#                             if saas_entities:
#                                 if ent in saas_entities:
#                                     counts[ent] += 1
#                             else:
#                                 counts[ent] += 1
#                     break
#                 except:
#                     continue
#         if saas_entities:
#             for ent in saas_entities:
#                 if ent not in counts:
#                     counts[ent] = 0
#         entity_counts = dict(counts)

#         # ----------------
#         # TRNH Analysis dataframe
#         # ----------------
#         analysis_data = {
#             'Requirement': [f'Sum of {name}' for name in column_names] + [f'{name}_count' for name in column_names] + [
#                 'Sum of AFTRAMT', 'Sum of AININTAPPLYAMT', 'Count of AININTAPPLYAMT'
#             ],
#             'Value': list(column_sums.values()) + list(column_counts.values()) + [trnh_sum, trnh_ainintapplyamt_sum, trnh_ainintapplyamt_count]
#         }
#         for aftrtyp, count in trnh_distinct_counts.items():
#             analysis_data['Requirement'].append(f'Count of distinct AFTRTYP: {aftrtyp}')
#             analysis_data['Value'].append(count)
#         analysis_data['Requirement'].append('Count of PRNAPPLYAMT and PRNDUEAGENCY with value null')
#         analysis_data['Value'].append(trnh_prnapplyamt_prndueagency_null_count)
#         analysis_data['Requirement'].append('AFTRACCTDTE with PAST DATE')
#         analysis_data['Value'].append(trnh_aftracctdte_past_count)
#         analysis_data['Requirement'].append('AFTRACCTDTE with PRESENT DATE')
#         analysis_data['Value'].append(trnh_aftracctdte_present_count)
#         analysis_data['Requirement'].append('AFTRACCTDTE with FUTURE DATE')
#         analysis_data['Value'].append(trnh_aftracctdte_future_count)

#         analysis_df = pd.DataFrame(analysis_data)
#         entity_count_df = pd.DataFrame(list(entity_counts.items()), columns=['Entity Name', 'Count of Records'])

#         # ----------------
#         # BAL Analysis
#         # ----------------
#         bal_sums = {name: 0 for name in bal_column_names}
#         bal_counts = {name: 0 for name in bal_column_names}
#         for filename in files:
#             file_path = os.path.join(input_folder, filename)
#             with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
#                 lines = file.readlines()
#             for line in lines:
#                 columns = line.strip().split('|')
#                 entity_name = columns[0].strip() if len(columns) > 0 else None
#                 if entity_name == 'BAL':
#                     for idx, name in zip([2, 3, 4, 5, 8, 9, 20], bal_column_names):
#                         if len(columns) > idx:
#                             try:
#                                 bal_value = float(columns[idx].strip() or 0)
#                                 bal_sums[name] += bal_value
#                                 if bal_value != 0:
#                                     bal_counts[name] += 1
#                             except:
#                                 pass
#         bal_analysis_df = pd.DataFrame([{'Requirement': f'Sum of {name}', 'Value': bal_sums[name]} for name in bal_column_names] +
#                                        [{'Requirement': f'Count of {name}', 'Value': bal_counts[name]} for name in bal_column_names])

#         # ----------------
#         # PRTY Analysis
#         # ----------------
#         party_counts = {name: 0 for name in party_column_names}
#         arenprisflag_counts = {'Y': 0, 'N': 0}
#         arenbnkrpt_counts = {'Y': 0, 'N': 0}
#         arendeced_counts = {'Y': 0, 'N': 0}
#         arenfnm_null_counts = 0
#         arenlnm_null_counts = 0
#         both_null_counts = 0

#         for filename in files:
#             file_path = os.path.join(input_folder, filename)
#             with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
#                 lines = file.readlines()
#             for line in lines:
#                 columns = line.strip().split('|')
#                 entity_name = columns[0].strip() if len(columns) > 0 else None
#                 if entity_name == 'PRTY' and len(columns) > 101:
#                     try:
#                         for idx, name in zip([98, 99, 100, 101], party_column_names):
#                             party_value = columns[idx].strip()
#                             if party_value:
#                                 party_counts[name] += 1
#                         arenprisflag_value = columns[94].strip()
#                         if arenprisflag_value == 'Y':
#                             arenprisflag_counts['Y'] += 1
#                         elif arenprisflag_value == 'N':
#                             arenprisflag_counts['N'] += 1
#                         arenbnkrpt_value = columns[33].strip()
#                         if arenbnkrpt_value == 'Y':
#                             arenbnkrpt_counts['Y'] += 1
#                         elif arenbnkrpt_value == 'N':
#                             arenbnkrpt_counts['N'] += 1
#                         arendeced_value = columns[28].strip()
#                         if arendeced_value == 'Y':
#                             arendeced_counts['Y'] += 1
#                         elif arendeced_value == 'N':
#                             arendeced_counts['N'] += 1
#                         arenfnm_value = columns[5].strip()
#                         arenlnm_value = columns[7].strip()
#                         if not arenfnm_value:
#                             arenfnm_null_counts += 1
#                         if not arenlnm_value:
#                             arenlnm_null_counts += 1
#                         if not arenfnm_value and not arenlnm_value:
#                             both_null_counts += 1
#                     except:
#                         pass

#         party_analysis_data = []
#         for name in party_column_names:
#             party_analysis_data.append({'Requirement': f'Count of {name}', 'Value': party_counts[name]})
#         party_analysis_data.extend([
#             {'Requirement': 'Count of ARENPRISFLAG Y', 'Value': arenprisflag_counts['Y']},
#             {'Requirement': 'Count of ARENPRISFLAG N', 'Value': arenprisflag_counts['N']},
#             {'Requirement': 'Count of ARENBNKRPT Y', 'Value': arenbnkrpt_counts['Y']},
#             {'Requirement': 'Count of ARENBNKRPT N', 'Value': arenbnkrpt_counts['N']},
#             {'Requirement': 'Count of ARENDECEASED Y', 'Value': arendeced_counts['Y']},
#             {'Requirement': 'Count of ARENDECEASED N', 'Value': arendeced_counts['N']},
#             {'Requirement': 'Count of ARENFNM with null data', 'Value': arenfnm_null_counts},
#             {'Requirement': 'Count of ARENLNM with null data', 'Value': arenlnm_null_counts},
#             {'Requirement': 'Count of both first and lastname Null', 'Value': both_null_counts}
#         ])
#         party_analysis_df = pd.DataFrame(party_analysis_data)

#         # ----------------
#         # POE Analysis
#         # ----------------
#         poe_counts = {name: 0 for name in poe_column_names}
#         for filename in files:
#             file_path = os.path.join(input_folder, filename)
#             with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
#                 lines = file.readlines()
#             for line in lines:
#                 columns = line.strip().split('|')
#                 entity_name = columns[0].strip() if len(columns) > 0 else None
#                 if entity_name == 'POE' and len(columns) > 3:
#                     employer_name = columns[3].strip()
#                     if employer_name:
#                         poe_counts['Name of employer without NULL values'] += 1
#                     else:
#                         poe_counts['Name of employer with NULL values'] += 1
#         poe_analysis_df = pd.DataFrame([
#             {'Requirement': 'Name of employer without NULL values', 'Value': poe_counts['Name of employer without NULL values']},
#             {'Requirement': 'Name of employer with NULL values', 'Value': poe_counts['Name of employer with NULL values']}
#         ])

#         # ----------------
#         # ACCT Analysis
#         # ----------------
#         acct_analysis_df = pd.DataFrame([
#             {'Requirement': 'Count of IS_DISPUTED not NULL', 'Value': acct_is_disputed_not_null_count}
#         ])

#         # ----------------
#         # Write all Excel sheets
#         # ----------------
#         with pd.ExcelWriter(count_of_records_excel, engine='openpyxl') as writer:
#             entity_count_df.to_excel(writer, sheet_name='Count of Records', index=False)
#             analysis_df.to_excel(writer, sheet_name='Analysis of TRNH', index=False)
#             bal_analysis_df.to_excel(writer, sheet_name='Analysis of BAL', index=False)
#             party_analysis_df.to_excel(writer, sheet_name='Analysis of PARTY_INFO', index=False)
#             poe_analysis_df.to_excel(writer, sheet_name='Analysis of POE', index=False)
#             acct_analysis_df.to_excel(writer, sheet_name='Analysis of ACCT', index=False)

#         with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
#             if summary:
#                 pd.DataFrame(summary).to_excel(writer, sheet_name='Column Summary', index=False)
#             if validation_results:
#                 pd.DataFrame(validation_results).to_excel(writer, sheet_name='Validation Results', index=False)

#         with pd.ExcelWriter(empty_columns_summary_excel, engine='openpyxl') as writer:
#             pd.DataFrame(empty_column_summary).to_excel(writer, sheet_name='Empty Columns Summary', index=False)

#         print("All analysis completed successfully.")

#     except Exception as e:
#         print(f"Error processing files: {e}")
#         return False

#     return True





# import pandas as pd
# import os
# from datetime import datetime
# from collections import defaultdict


# def column_number_to_letter(column_number):
#     """Convert a 1-based column number to an Excel column letter."""
#     if column_number <= 0:
#         return ''
#     column_letter = ''
#     while column_number > 0:
#         column_number, remainder = divmod(column_number - 1, 26)
#         column_letter = chr(65 + remainder) + column_letter
#     return column_letter


# def process_and_validate_files(expected_columns, specific_words, input_folder,
#                                output_excel, count_of_records_excel, empty_columns_summary_excel):
#     """
#     Process .txt files:
#     - Validate column count
#     - Count records (including zero)
#     - Report empty columns (clean logic from friend)
#     - Full analysis: TRNH, BAL, PRTY, POE, ACCT
#     """
#     # --- Containers ---
#     summary = []
#     validation_results = []
#     empty_column_summary = []
#     entity_results = {}
#     entity_counts = defaultdict(int)  # Use defaultdict to auto-init

#     # TRNH-specific
#     trnh_sum = 0
#     column_sums = {}
#     column_counts = {}
#     column_values = {}
#     trnh_distinct_counts = {}
#     acct_is_disputed_not_null_count = 0
#     trnh_prnapplyamt_prndueagency_null_count = 0
#     trnh_aftracctdte_past_count = 0
#     trnh_aftracctdte_present_count = 0
#     trnh_aftracctdte_future_count = 0
#     trnh_ainintapplyamt_sum = 0
#     trnh_ainintapplyamt_count = 0

#     # Column definitions
#     column_names = [
#         'PRNAPPLYAMT', 'PRNDUEAGENCY', 'PRNDUECLIENT', 'INTAPPLYAMT', 'INTDUEAGENCY', 'INTDUECLIENT',
#         'LI3BALAPPLYAMT', 'LI3BALDUEAGENCY', 'LIBBALDUECLIENT', 'L14BALAPPLYAMT', 'LI4BALDUEAGENCY',
#         'LI4BALDUECLIENT', 'AININTAPDI VAMT', 'AININTDUEAGENCY', 'AININTDUECLIENT', 'MS1APPLYAMT',
#         'MS1DUEAGENCY', 'MS1DUECLIENT'
#     ]
#     bal_column_names = [
#         'PRN_INITIALBALANCE', 'INT_INITIALBALANCE', 'LI3_INITIALBALANCE', 'LI4_INITIALBALANCE',
#         'PRN_CURRENTBALANCE', 'INT_CURRENTBALANCE', 'MS1_CURRENTBALANCE', 'AIN_CURRENTBALANCE'
#     ]
#     party_column_names = [
#         'ARENLITFCRAFLAG', 'ARENLITTCPAFLAG', 'ARENLITFDCPAFLAG', 'ARENLITFILEDATE'
#     ]
#     poe_column_names = [
#         'Name of employer without NULL values', 'Name of employer with NULL values'
#     ]

#     # Initialize TRNH column trackers
#     for name in column_names:
#         column_sums[name] = 0
#         column_counts[name] = 0
#         column_values[name] = []

#     # --- Process all .txt files ---
#     try:
#         txt_files = [f for f in os.listdir(input_folder) if f.lower().endswith(".txt")]
#         if not txt_files:
#             print(f"No .txt files found in {input_folder}")
#             return False

#         # First pass: validation, empty columns, TRNH, ACCT, entity counts
#         for filename in txt_files:
#             file_path = os.path.join(input_folder, filename)
#             print(f"Processing: {filename}")

#             # Try UTF-8, fallback to Latin1
#             file_content = None
#             for encoding in ['utf-8', 'latin1']:
#                 try:
#                     with open(file_path, 'r', encoding=encoding, errors='replace') as f:
#                         file_content = f.readlines()
#                     print(f"  → Decoded with {encoding}")
#                     break
#                 except Exception as e:
#                     print(f"  → Failed with {encoding}: {e}")

#             if file_content is None:
#                 print(f"  → Skipping {filename} (could not read)")
#                 continue

#             # Per-file empty column tracker
#             empty_counts = {}

#             for raw_line in file_content:
#                 line = raw_line.strip()
#                 if not line:
#                     continue
#                 columns = line.split('|')
#                 if not columns:
#                     continue

#                 entity_name = columns[0].strip()

#                 # --- 1. Column Count Validation + Empty Column Tracking ---
#                 if entity_name in specific_words:
#                     actual_count = len(columns)
#                     expected_count = expected_columns.get(entity_name, 0)
#                     key = (filename, entity_name)

#                     if key not in entity_results:
#                         entity_results[key] = {"expected": expected_count, "status": "Pass"}
#                     if actual_count != expected_count:
#                         entity_results[key]["status"] = "Fail"

#                     # Empty column tracking (clean logic from friend's first version)
#                     for i, col_val in enumerate(columns):
#                         if i > 0 and not str(col_val).strip():
#                             col_letter = column_number_to_letter(i + 1)
#                             ec_key = (filename, entity_name, col_letter)
#                             empty_counts[ec_key] = empty_counts.get(ec_key, 0) + 1

#                 # --- 2. Entity Count (including zero later) ---
#                 entity_counts[entity_name] += 1

#                 # --- 3. TRNH Analysis ---
#                 if entity_name == 'TRNH' and len(columns) > 24:
#                     try:
#                         # AFTRAMT (5th column, index 4)
#                         trnh_sum += float(columns[4].strip() or 0)

#                         # AFTRTYP (4th column, index 3)
#                         aftrtyp = columns[3].strip()
#                         trnh_distinct_counts[aftrtyp] = trnh_distinct_counts.get(aftrtyp, 0) + 1

#                         # PRNAPPLYAMT (13th) and PRNDUEAGENCY (14th)
#                         if not columns[12].strip() and not columns[13].strip():
#                             trnh_prnapplyamt_prndueagency_null_count += 1

#                         # AFTRACCTDTE (7th column, index 6)
#                         aftracctdte = columns[6].strip()
#                         if aftracctdte:
#                             try:
#                                 d = datetime.strptime(aftracctdte, '%m-%d-%Y')
#                                 today = datetime.today()
#                                 if d < today:
#                                     trnh_aftracctdte_past_count += 1
#                                 elif d == today:
#                                     trnh_aftracctdte_present_count += 1
#                                 else:
#                                     trnh_aftracctdte_future_count += 1
#                             except:
#                                 pass

#                         # AININTAPPLYAMT (25th column, index 24)
#                         ain_val = columns[24].strip()
#                         if ain_val:
#                             trnh_ainintapplyamt_sum += float(ain_val)
#                             trnh_ainintapplyamt_count += 1

#                     except:
#                         pass

#                     # TRNH column sums (from index 12 onward)
#                     for idx, name in enumerate(column_names, start=12):
#                         if len(columns) > idx:
#                             try:
#                                 val = float(columns[idx].strip() or 0)
#                                 column_sums[name] += val
#                                 if val != 0:
#                                     column_values[name].append(val)
#                                     column_counts[name] += 1
#                             except:
#                                 pass

#                 # --- 4. ACCT Analysis ---
#                 if entity_name == 'ACCT' and len(columns) > 36:
#                     if columns[35].strip():
#                         acct_is_disputed_not_null_count += 1

#             # --- After processing all lines: append empty column summary ---
#             for (f, e, c), cnt in empty_counts.items():
#                 empty_column_summary.append({
#                     'Source File': f,
#                     'Customer entity name': e,
#                     'Column Name': c,
#                     'Status': 'Fail',
#                     'Empty Count': cnt
#                 })

#             # --- Validation: check if specific_words appear in file ---
#             whole_file = ''.join(file_content)
#             for word in specific_words:
#                 status = "Pass" if word in whole_file else "Fail"
#                 validation_results.append({
#                     "File Name": filename,
#                     "Entity": word,
#                     "Status": status
#                 })

#         # --- Build Summary from entity_results ---
#         for (filename, entity_name), result in entity_results.items():
#             summary.append({
#                 'File Name': filename,
#                 'Entity Name': entity_name,
#                 'Expected Columns': result["expected"],
#                 'Status': result["status"]
#             })

#         # --- DataFrames ---
#         summary_df = pd.DataFrame(summary).sort_values(by=['File Name', 'Entity Name'])
#         validation_df = pd.DataFrame(validation_results).sort_values(by=['File Name', 'Entity'])
#         empty_column_df = pd.DataFrame(empty_column_summary)
#         if not empty_column_df.empty:
#             empty_column_df = empty_column_df[['Source File', 'Customer entity name', 'Column Name', 'Status', 'Empty Count']]
#             empty_column_df = empty_column_df.sort_values(by='Empty Count', ascending=False)

#         # --- Write validation + summary + empty columns ---
#         try:
#             with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
#                 summary_df.to_excel(writer, sheet_name='Column Summary', index=False)
#                 validation_df.to_excel(writer, sheet_name='Validation Results', index=False)
#             print(f"Success: Validation & Summary → {output_excel}")
#         except Exception as e:
#             print(f"Error writing validation/summary: {e}")
#             return False

#         try:
#             with pd.ExcelWriter(empty_columns_summary_excel, engine='openpyxl') as writer:
#                 empty_column_df.to_excel(writer, sheet_name='Empty Columns Summary', index=False)
#             print(f"Success: Empty Columns → {empty_columns_summary_excel}")
#         except Exception as e:
#             print(f"Error writing empty columns: {e}")
#             return False

#         # --- Entity Count DF (include zero counts from expected_columns) ---
#         if isinstance(expected_columns, dict):
#             for ent in expected_columns.keys():
#                 if ent not in entity_counts:
#                     entity_counts[ent] = 0
#         entity_count_df = pd.DataFrame(list(entity_counts.items()), columns=['Entity Name', 'Count of Records'])

#         # --- TRNH Analysis DF ---
#         analysis_data = {
#             'Requirement': [f'Sum of {name}' for name in column_names] +
#                            [f'{name}_count' for name in column_names] +
#                            ['Sum of AFTRAMT', 'Sum of AININTAPPLYAMT', 'Count of AININTAPPLYAMT'],
#             'Value': list(column_sums.values()) + list(column_counts.values()) +
#                      [trnh_sum, trnh_ainintapplyamt_sum, trnh_ainintapplyamt_count]
#         }
#         for typ, cnt in trnh_distinct_counts.items():
#             analysis_data['Requirement'].append(f'Count of distinct AFTRTYP: {typ}')
#             analysis_data['Value'].append(cnt)
#         analysis_data['Requirement'].append('Count of PRNAPPLYAMT and PRNDUEAGENCY with value null')
#         analysis_data['Value'].append(trnh_prnapplyamt_prndueagency_null_count)
#         analysis_data['Requirement'].append('AFTRACCTDTE with PAST DATE')
#         analysis_data['Value'].append(trnh_aftracctdte_past_count)
#         analysis_data['Requirement'].append('AFTRACCTDTE with PRESENT DATE')
#         analysis_data['Value'].append(trnh_aftracctdte_present_count)
#         analysis_data['Requirement'].append('AFTRACCTDTE with FUTURE DATE')
#         analysis_data['Value'].append(trnh_aftracctdte_future_count)
#         trnh_analysis_df = pd.DataFrame(analysis_data)

#         # --- Second pass: BAL, PRTY, POE ---
#         bal_sums = {name: 0 for name in bal_column_names}
#         bal_counts = {name: 0 for name in bal_column_names}
#         party_counts = {name: 0 for name in party_column_names}
#         arenprisflag_counts = {'Y': 0, 'N': 0}
#         arenbnkrpt_counts = {'Y': 0, 'N': 0}
#         arendeced_counts = {'Y': 0, 'N': 0}
#         arenfnm_null = arenlnm_null = both_null = 0
#         poe_counts = {name: 0 for name in poe_column_names}

#         for filename in txt_files:
#             file_path = os.path.join(input_folder, filename)
#             try:
#                 with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
#                     lines = f.readlines()
#             except:
#                 with open(file_path, 'r', encoding='latin1', errors='replace') as f:
#                     lines = f.readlines()

#             for line in lines:
#                 cols = line.strip().split('|')
#                 if not cols:
#                     continue
#                 ent = cols[0].strip()

#                 # BAL
#                 if ent == 'BAL':
#                     for idx, name in zip([2,3,4,5,8,9,20], bal_column_names):
#                         if len(cols) > idx:
#                             try:
#                                 v = float(cols[idx].strip() or 0)
#                                 bal_sums[name] += v
#                                 if v != 0:
#                                     bal_counts[name] += 1
#                             except:
#                                 pass

#                 # PRTY
#                 if ent == 'PRTY' and len(cols) > 101:
#                     try:
#                         for idx, name in zip([98,99,100,101], party_column_names):
#                             if cols[idx].strip():
#                                 party_counts[name] += 1
#                         # Flags
#                         if cols[94].strip() == 'Y': arenprisflag_counts['Y'] += 1
#                         elif cols[94].strip() == 'N': arenprisflag_counts['N'] += 1
#                         if cols[33].strip() == 'Y': arenbnkrpt_counts['Y'] += 1
#                         elif cols[33].strip() == 'N': arenbnkrpt_counts['N'] += 1
#                         if cols[28].strip() == 'Y': arendeced_counts['Y'] += 1
#                         elif cols[28].strip() == 'N': arendeced_counts['N'] += 1
#                         # Names
#                         fnm = cols[5].strip()
#                         lnm = cols[7].strip()
#                         if not fnm: arenfnm_null += 1
#                         if not lnm: arenlnm_null += 1
#                         if not fnm and not lnm: both_null += 1
#                     except:
#                         pass

#                 # POE
#                 if ent == 'POE' and len(cols) > 3:
#                     emp = cols[3].strip()
#                     key = 'Name of employer without NULL values' if emp else 'Name of employer with NULL values'
#                     poe_counts[key] += 1

#         # --- Build BAL, PRTY, POE, ACCT DFs ---
#         bal_analysis_data = []
#         for name in bal_column_names:
#             bal_analysis_data.append({'Requirement': f'Sum of {name}', 'Value': bal_sums[name]})
#             bal_analysis_data.append({'Requirement': f'Count of {name}', 'Value': bal_counts[name]})
#         bal_analysis_df = pd.DataFrame(bal_analysis_data)

#         party_analysis_data = []
#         for name in party_column_names:
#             party_analysis_data.append({'Requirement': f'Count of {name}', 'Value': party_counts[name]})
#         party_analysis_data.extend([
#             {'Requirement': 'Count of ARENPRISFLAG Y', 'Value': arenprisflag_counts['Y']},
#             {'Requirement': 'Count of ARENPRISFLAG N', 'Value': arenprisflag_counts['N']},
#             {'Requirement': 'Count of ARENBNKRPT Y', 'Value': arenbnkrpt_counts['Y']},
#             {'Requirement': 'Count of ARENBNKRPT N', 'Value': arenbnkrpt_counts['N']},
#             {'Requirement': 'Count of ARENDECEASED Y', 'Value': arendeced_counts['Y']},
#             {'Requirement': 'Count of ARENDECEASED N', 'Value': arendeced_counts['N']},
#             {'Requirement': 'Count of ARENFNM with null data', 'Value': arenfnm_null},
#             {'Requirement': 'Count of ARENLNM with null data', 'Value': arenlnm_null},
#             {'Requirement': 'Count of both first and lastname Null', 'Value': both_null},
#         ])
#         party_analysis_df = pd.DataFrame(party_analysis_data)

#         poe_analysis_df = pd.DataFrame([
#             {'Requirement': k, 'Value': v} for k, v in poe_counts.items()
#         ])

#         acct_analysis_df = pd.DataFrame([
#             {'Requirement': 'Count of IS_DISPUTED not NULL', 'Value': acct_is_disputed_not_null_count}
#         ])

#         # --- Write all analysis sheets ---
#         try:
#             with pd.ExcelWriter(count_of_records_excel, engine='openpyxl') as writer:
#                 entity_count_df.to_excel(writer, sheet_name='Count of Records', index=False)
#                 trnh_analysis_df.to_excel(writer, sheet_name='Analysis of TRNH', index=False)
#                 bal_analysis_df.to_excel(writer, sheet_name='Analysis of BAL', index=False)
#                 party_analysis_df.to_excel(writer, sheet_name='Analysis of PARTY_INFO', index=False)
#                 poe_analysis_df.to_excel(writer, sheet_name='Analysis of POE', index=False)
#                 acct_analysis_df.to_excel(writer, sheet_name='Analysis of ACCT', index=False)
#             print(f"Success: All analysis → {count_of_records_excel}")
#         except Exception as e:
#             print(f"Error writing analysis Excel: {e}")
#             return False

#     except Exception as e:
#         print(f"Unexpected error: {e}")
#         return False

#     return True


import pandas as pd
import os
from datetime import datetime
from collections import defaultdict


def column_number_to_letter(column_number):
    """Convert a 1-based column number to an Excel column letter."""
    if column_number <= 0:
        return ''
    column_letter = ''
    while column_number > 0:
        column_number, remainder = divmod(column_number - 1, 26)
        column_letter = chr(65 + remainder) + column_letter
    return column_letter


# =============================================================================
# HARD-CODED LIST OF ALL ENTITIES (from your Fields Comparison output)
# =============================================================================
ALL_ENTITIES = [
    '10C', '10M', '12', '14', '16', '17', '19', '20A', '20B', '20C', '20F', '20IC',
    '20R', '20T', '27', '28', '29', '45', '50', '51', '61CW', '70', '71', '75',
    '80', '99-Template', 'ACCT', 'ACT (2)', 'ACTH', 'AKA', 'ANOT', 'ATTY', 'BAL',
    'CALLH', 'CLAIM', 'CLMLN', 'CUSTACCT', 'CUSTPER','Change Log', 'EMAIL', 'ENC',
    'Field Definitions', 'File Specifications', 'INS', 'ITMZ', 'Initial Setup',
    'LACTN', 'LCASE', 'LCNOT', 'LDOC', 'LJDG', 'LTRH', 'Lists', 'MED -obsolete',
    'PA', 'PADD', 'PAT', 'PDTR', 'PHN', 'PNOT', 'POE', 'PRTY', 'PRTY Flags',
    'PS', 'PSC', 'PSK', 'RST', 'Record Ids', 'TIG', 'TRNH','TIGDATA', 'Transaction Types (2)',
    'Translations'
]


def process_and_validate_files(expected_columns, specific_words, input_folder,
                               output_excel, count_of_records_excel, empty_columns_summary_excel):
    """
    Process .txt files:
    - Validate column count
    - Count records (including zero)
    - Report empty columns
    - Full analysis: TRNH, BAL, PRTY, POE, ACCT
    """
    # --- Containers ---
    summary = []
    validation_results = []
    empty_column_summary = []
    entity_results = {}
    entity_counts = defaultdict(int)  # Will be filled from files

    # TRNH-specific
    trnh_sum = 0
    column_sums = {}
    column_counts = {}
    trnh_distinct_counts = {}
    acct_is_disputed_not_null_count = 0
    trnh_prnapplyamt_prndueagency_null_count = 0
    trnh_aftracctdte_past_count = 0
    trnh_aftracctdte_present_count = 0
    trnh_aftracctdte_future_count = 0
    trnh_ainintapplyamt_sum = 0
    trnh_ainintapplyamt_count = 0

    # Column definitions
    column_names = [
        'PRNAPPLYAMT', 'PRNDUEAGENCY', 'PRNDUECLIENT', 'INTAPPLYAMT', 'INTDUEAGENCY', 'INTDUECLIENT',
        'LI3BALAPPLYAMT', 'LI3BALDUEAGENCY', 'LIBBALDUECLIENT', 'L14BALAPPLYAMT', 'LI4BALDUEAGENCY',
        'LI4BALDUECLIENT', 'AININTAPDI VAMT', 'AININTDUEAGENCY', 'AININTDUECLIENT', 'MS1APPLYAMT',
        'MS1DUEAGENCY', 'MS1DUECLIENT'
    ]
    bal_column_names = [
        'PRN_INITIALBALANCE', 'INT_INITIALBALANCE', 'LI3_INITIALBALANCE', 'LI4_INITIALBALANCE',
        'PRN_CURRENTBALANCE', 'INT_CURRENTBALANCE', 'MS1_CURRENTBALANCE', 'AIN_CURRENTBALANCE'
    ]
    party_column_names = [
        'ARENLITFCRAFLAG', 'ARENLITTCPAFLAG', 'ARENLITFDCPAFLAG', 'ARENLITFILEDATE'
    ]
    poe_column_names = [
        'Name of employer without NULL values', 'Name of employer with NULL values'
    ]

    # Initialize TRNH column trackers
    for name in column_names:
        column_sums[name] = 0
        column_counts[name] = 0

    # --- Process all .txt files ---
    try:
        txt_files = [f for f in os.listdir(input_folder) if f.lower().endswith(".txt")]
        if not txt_files:
            print(f"No .txt files found in {input_folder}")
            return False

        # First pass: validation, empty columns, TRNH, ACCT, entity counts
        for filename in txt_files:
            file_path = os.path.join(input_folder, filename)
            print(f"Processing: {filename}")

            file_content = None
            for encoding in ['utf-8', 'latin1']:
                try:
                    with open(file_path, 'r', encoding=encoding, errors='replace') as f:
                        file_content = f.readlines()
                    print(f"  Decoded with {encoding}")
                    break
                except Exception as e:
                    print(f"  Failed with {encoding}: {e}")

            if file_content is None:
                print(f"  Skipping {filename} (could not read)")
                continue

            empty_counts = {}

            for raw_line in file_content:
                line = raw_line.strip()
                if not line:
                    continue
                columns = line.split('|')
                if not columns:
                    continue

                entity_name = columns[0].strip()

                # --- 1. Column Count Validation + Empty Column Tracking ---
                if entity_name in specific_words:
                    actual_count = len(columns)
                    expected_count = expected_columns.get(entity_name, 0)
                    key = (filename, entity_name)

                    if key not in entity_results:
                        entity_results[key] = {"expected": expected_count, "status": "Pass"}
                    if actual_count != expected_count:
                        entity_results[key]["status"] = "Fail"

                    # Empty column tracking
                    for i, col_val in enumerate(columns):
                        if i > 0 and not str(col_val).strip():
                            col_letter = column_number_to_letter(i + 1)
                            ec_key = (filename, entity_name, col_letter)
                            empty_counts[ec_key] = empty_counts.get(ec_key, 0) + 1

                # --- 2. Entity Count ---
                entity_counts[entity_name] += 1

                # --- 3. TRNH Analysis ---
                if entity_name == 'TRNH' and len(columns) > 24:
                    try:
                        trnh_sum += float(columns[4].strip() or 0)
                        aftrtyp = columns[3].strip()
                        trnh_distinct_counts[aftrtyp] = trnh_distinct_counts.get(aftrtyp, 0) + 1

                        if not columns[12].strip() and not columns[13].strip():
                            trnh_prnapplyamt_prndueagency_null_count += 1

                        aftracctdte = columns[6].strip()
                        if aftracctdte:
                            try:
                                d = datetime.strptime(aftracctdte, '%m-%d-%Y')
                                today = datetime.today()
                                if d < today:
                                    trnh_aftracctdte_past_count += 1
                                elif d == today:
                                    trnh_aftracctdte_present_count += 1
                                else:
                                    trnh_aftracctdte_future_count += 1
                            except:
                                pass

                        ain_val = columns[24].strip()
                        if ain_val:
                            trnh_ainintapplyamt_sum += float(ain_val)
                            trnh_ainintapplyamt_count += 1

                    except:
                        pass

                    for idx, name in enumerate(column_names, start=12):
                        if len(columns) > idx:
                            try:
                                val = float(columns[idx].strip() or 0)
                                column_sums[name] += val
                                if val != 0:
                                    column_counts[name] += 1
                            except:
                                pass

                # --- 4. ACCT Analysis ---
                if entity_name == 'ACCT' and len(columns) > 36:
                    if columns[35].strip():
                        acct_is_disputed_not_null_count += 1

            # Append empty column summary
            for (f, e, c), cnt in empty_counts.items():
                empty_column_summary.append({
                    'Source File': f,
                    'Customer entity name': e,
                    'Column Name': c,
                    'Status': 'Fail',
                    'Empty Count': cnt
                })

            # Validation: check if entity appears in file
            whole_file = ''.join(file_content)
            for word in specific_words:
                status = "Pass" if word in whole_file else "Fail"
                validation_results.append({
                    "File Name": filename,
                    "Entity": word,
                    "Status": status
                })

        # --- Build Summary ---
        for (filename, entity_name), result in entity_results.items():
            summary.append({
                'File Name': filename,
                'Entity Name': entity_name,
                'Expected Columns': result["expected"],
                'Status': result["status"]
            })

        # --- DataFrames ---
        summary_df = pd.DataFrame(summary).sort_values(by=['File Name', 'Entity Name'])
        validation_df = pd.DataFrame(validation_results).sort_values(by=['File Name', 'Entity'])
        empty_column_df = pd.DataFrame(empty_column_summary)
        if not empty_column_df.empty:
            empty_column_df = empty_column_df[['Source File', 'Customer entity name', 'Column Name', 'Status', 'Empty Count']]
            empty_column_df = empty_column_df.sort_values(by='Empty Count', ascending=False)

        # --- Write validation + summary + empty columns ---
        try:
            with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
                summary_df.to_excel(writer, sheet_name='Column Summary', index=False)
                validation_df.to_excel(writer, sheet_name='Validation Results', index=False)
            print(f"Success: Validation & Summary -> {output_excel}")
        except Exception as e:
            print(f"Error writing validation/summary: {e}")
            return False

        try:
            with pd.ExcelWriter(empty_columns_summary_excel, engine='openpyxl') as writer:
                empty_column_df.to_excel(writer, sheet_name='Empty Columns Summary', index=False)
            print(f"Success: Empty Columns -> {empty_columns_summary_excel}")
        except Exception as e:
            print(f"Error writing empty columns: {e}")
            return False

        # --- UPDATED: COUNT OF RECORDS - HARD-CODED ALL ENTITIES ---
        entity_count_data = [
            {"Entity Name": ent, "Count of Records": entity_counts.get(ent, 0)}
            for ent in ALL_ENTITIES
        ]
        entity_count_df = pd.DataFrame(entity_count_data)

        # --- TRNH Analysis DF ---
        analysis_data = {
            'Requirement': [f'Sum of {name}' for name in column_names] +
                           [f'{name}_count' for name in column_names] +
                           ['Sum of AFTRAMT', 'Sum of AININTAPPLYAMT', 'Count of AININTAPPLYAMT'],
            'Value': list(column_sums.values()) + list(column_counts.values()) +
                     [trnh_sum, trnh_ainintapplyamt_sum, trnh_ainintapplyamt_count]
        }
        for typ, cnt in trnh_distinct_counts.items():
            analysis_data['Requirement'].append(f'Count of distinct AFTRTYP: {typ}')
            analysis_data['Value'].append(cnt)
        analysis_data['Requirement'].append('Count of PRNAPPLYAMT and PRNDUEAGENCY with value null')
        analysis_data['Value'].append(trnh_prnapplyamt_prndueagency_null_count)
        analysis_data['Requirement'].append('AFTRACCTDTE with PAST DATE')
        analysis_data['Value'].append(trnh_aftracctdte_past_count)
        analysis_data['Requirement'].append('AFTRACCTDTE with PRESENT DATE')
        analysis_data['Value'].append(trnh_aftracctdte_present_count)
        analysis_data['Requirement'].append('AFTRACCTDTE with FUTURE DATE')
        analysis_data['Value'].append(trnh_aftracctdte_future_count)
        trnh_analysis_df = pd.DataFrame(analysis_data)

        # --- Second pass: BAL, PRTY, POE ---
        bal_sums = {name: 0 for name in bal_column_names}
        bal_counts = {name: 0 for name in bal_column_names}
        party_counts = {name: 0 for name in party_column_names}
        arenprisflag_counts = {'Y': 0, 'N': 0}
        arenbnkrpt_counts = {'Y': 0, 'N': 0}
        arendeced_counts = {'Y': 0, 'N': 0}
        arenfnm_null = arenlnm_null = both_null = 0
        poe_counts = {name: 0 for name in poe_column_names}

        for filename in txt_files:
            file_path = os.path.join(input_folder, filename)
            try:
                with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                    lines = f.readlines()
            except:
                with open(file_path, 'r', encoding='latin1', errors='replace') as f:
                    lines = f.readlines()

            for line in lines:
                cols = line.strip().split('|')
                if not cols:
                    continue
                ent = cols[0].strip()

                # BAL
                if ent == 'BAL':
                    for idx, name in zip([2,3,4,5,8,9,20], bal_column_names):
                        if len(cols) > idx:
                            try:
                                v = float(cols[idx].strip() or 0)
                                bal_sums[name] += v
                                if v != 0:
                                    bal_counts[name] += 1
                            except:
                                pass

                # PRTY
                if ent == 'PRTY' and len(cols) > 101:
                    try:
                        for idx, name in zip([98,99,100,101], party_column_names):
                            if cols[idx].strip():
                                party_counts[name] += 1
                        if cols[94].strip() == 'Y': arenprisflag_counts['Y'] += 1
                        elif cols[94].strip() == 'N': arenprisflag_counts['N'] += 1
                        if cols[33].strip() == 'Y': arenbnkrpt_counts['Y'] += 1
                        elif cols[33].strip() == 'N': arenbnkrpt_counts['N'] += 1
                        if cols[28].strip() == 'Y': arendeced_counts['Y'] += 1
                        elif cols[28].strip() == 'N': arendeced_counts['N'] += 1
                        fnm = cols[5].strip()
                        lnm = cols[7].strip()
                        if not fnm: arenfnm_null += 1
                        if not lnm: arenlnm_null += 1
                        if not fnm and not lnm: both_null += 1
                    except:
                        pass

                # POE
                if ent == 'POE' and len(cols) > 3:
                    emp = cols[3].strip()
                    key = 'Name of employer without NULL values' if emp else 'Name of employer with NULL values'
                    poe_counts[key] += 1

        # --- Build BAL, PRTY, POE, ACCT DFs ---
        bal_analysis_data = []
        for name in bal_column_names:
            bal_analysis_data.append({'Requirement': f'Sum of {name}', 'Value': bal_sums[name]})
            bal_analysis_data.append({'Requirement': f'Count of {name}', 'Value': bal_counts[name]})
        bal_analysis_df = pd.DataFrame(bal_analysis_data)

        party_analysis_data = []
        for name in party_column_names:
            party_analysis_data.append({'Requirement': f'Count of {name}', 'Value': party_counts[name]})
        party_analysis_data.extend([
            {'Requirement': 'Count of ARENPRISFLAG Y', 'Value': arenprisflag_counts['Y']},
            {'Requirement': 'Count of ARENPRISFLAG N', 'Value': arenprisflag_counts['N']},
            {'Requirement': 'Count of ARENBNKRPT Y', 'Value': arenbnkrpt_counts['Y']},
            {'Requirement': 'Count of ARENBNKRPT N', 'Value': arenbnkrpt_counts['N']},
            {'Requirement': 'Count of ARENDECEASED Y', 'Value': arendeced_counts['Y']},
            {'Requirement': 'Count of ARENDECEASED N', 'Value': arendeced_counts['N']},
            {'Requirement': 'Count of ARENFNM with null data', 'Value': arenfnm_null},
            {'Requirement': 'Count of ARENLNM with null data', 'Value': arenlnm_null},
            {'Requirement': 'Count of both first and lastname Null', 'Value': both_null},
        ])
        party_analysis_df = pd.DataFrame(party_analysis_data)

        poe_analysis_df = pd.DataFrame([{'Requirement': k, 'Value': v} for k, v in poe_counts.items()])
        acct_analysis_df = pd.DataFrame([{'Requirement': 'Count of IS_DISPUTED not NULL', 'Value': acct_is_disputed_not_null_count}])

        # --- Write all analysis sheets ---
        try:
            with pd.ExcelWriter(count_of_records_excel, engine='openpyxl') as writer:
                entity_count_df.to_excel(writer, sheet_name='Count of Records', index=False)
                trnh_analysis_df.to_excel(writer, sheet_name='Analysis of TRNH', index=False)
                bal_analysis_df.to_excel(writer, sheet_name='Analysis of BAL', index=False)
                party_analysis_df.to_excel(writer, sheet_name='Analysis of PARTY_INFO', index=False)
                poe_analysis_df.to_excel(writer, sheet_name='Analysis of POE', index=False)
                acct_analysis_df.to_excel(writer, sheet_name='Analysis of ACCT', index=False)
            print(f"Success: All analysis -> {count_of_records_excel}")
        except Exception as e:
            print(f"Error writing analysis Excel: {e}")
            return False

    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

    return True


# =============================================================================
# MAIN
# =============================================================================
if __name__ == "__main__":
    mapping_file = "Saas_Legacy_Migration.xlsx"
    input_folder = "Input File"
    output_excel = "output_validation_summary.xlsx"
    count_of_records_excel = "output_count_analysis.xlsx"
    empty_columns_summary_excel = "output_empty_columns.xlsx"

    # Load mapping (only to get expected columns for validation)
    expected_columns = {}
    specific_words = ALL_ENTITIES  # Use hard-coded list for validation too

    try:
        mapping_data = pd.read_excel(mapping_file, sheet_name=None, header=1)
        for sheet in mapping_data:
            mapping_data[sheet].columns = mapping_data[sheet].columns.map(str)

        for entity_name, sheet_data in mapping_data.items():
            position_column = None
            if entity_name == 'POE' and 'Acct' in sheet_data.columns:
                position_column = 'Acct'
            else:
                for column in sheet_data.columns:
                    if 'Position' in column:
                        position_column = column
                        break
            if position_column:
                positions = pd.to_numeric(sheet_data[position_column], errors='coerce').dropna()
                expected_columns[entity_name] = int(positions.max()) if not positions.empty else 0
            else:
                expected_columns[entity_name] = 0
    except Exception as e:
        print(f"Warning: Could not read mapping file. Using default expected columns = 0. Error: {e}")
        # Still proceed — expected_columns will be 0 for all

    # Run analysis
    success = process_and_validate_files(
        expected_columns=expected_columns,
        specific_words=specific_words,
        input_folder=input_folder,
        output_excel=output_excel,
        count_of_records_excel=count_of_records_excel,
        empty_columns_summary_excel=empty_columns_summary_excel
    )

    print("All processing completed." if success else "Processing failed.")