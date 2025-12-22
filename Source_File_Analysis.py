# # # # # ## crt code

# # # # # import pandas as pd
# # # # # import os
# # # # # import re
# # # # # from concurrent.futures import ThreadPoolExecutor
# # # # # from datetime import datetime

# # # # # def process_single_file(filename, input_folder, mapping_data):
# # # # #     """
# # # # #     Process a single .txt file to analyze required columns, missing entities, and file issues.
# # # # #     Includes new validations with a dedicated summary, dynamically using mapping positions.
# # # # #     """
# # # # #     file_path = os.path.join(input_folder, filename)
# # # # #     analysis_results = []
# # # # #     missing_entities = set()
# # # # #     file_issues = []
# # # # #     new_validation_issues = []

# # # # #     try:
# # # # #         df = pd.read_csv(file_path, sep="|", header=None, dtype=str, engine="python", on_bad_lines='skip')
# # # # #     except Exception as e:
# # # # #         print(f"Error reading file {file_path}: {e}")
# # # # #         return analysis_results, missing_entities, file_issues, new_validation_issues

# # # # #     if df.empty:
# # # # #         print(f"File {filename} is empty.")
# # # # #         return analysis_results, missing_entities, file_issues, new_validation_issues

# # # # #     df.iloc[:, 0] = df.iloc[:, 0].str.strip()
# # # # #     decimal_pattern = re.compile(r'^\.\d+$')

# # # # #     # DECIMAL ISSUE
# # # # #     decimal_issue_count = 0
# # # # #     decimal_issue_entities = set()
# # # # #     for col in df.columns[1:]:
# # # # #         sample_size = min(1000, len(df))
# # # # #         sample_data = df[col].iloc[:sample_size].astype(str)
# # # # #         mask = sample_data.apply(lambda x: bool(decimal_pattern.match(x)) if pd.notna(x) else False)
# # # # #         if mask.any():
# # # # #             decimal_issue_count += df[col].astype(str).apply(lambda x: bool(decimal_pattern.match(x)) if pd.notna(x) else False).sum()
# # # # #             decimal_issue_entities.update(df.iloc[mask.index[mask], 0].dropna().unique())

# # # # #     if decimal_issue_count > 0:
# # # # #         file_issues.append({
# # # # #             'INPUT FILE': filename,
# # # # #             'Requirement': 'Decimal Issues Count',
# # # # #             'Count': decimal_issue_count,
# # # # #             'Entities': ', '.join(decimal_issue_entities) if decimal_issue_entities else None
# # # # #         })

# # # # #     # EMPTY REC_ID
# # # # #     rec_id_empty = df.iloc[:, 1].isna() | (df.iloc[:, 1].str.strip() == '')
# # # # #     record_id_issue_count = rec_id_empty.sum()
# # # # #     if record_id_issue_count > 0:
# # # # #         file_issues.append({
# # # # #             'INPUT FILE': filename,
# # # # #             'Requirement': 'Count of Empty REC_ID',
# # # # #             'Count': record_id_issue_count,
# # # # #             'Entities': None
# # # # #         })

# # # # #     # ITMZ - Itemization Date (position 3)
# # # # #     itmz_df = df[df.iloc[:,0]=='ITMZ']
# # # # #     itmz_date_null_count = 0
# # # # #     if not itmz_df.empty:
# # # # #         itmz_date = itmz_df.iloc[:, 2].fillna('').astype(str).str.strip()
# # # # #         itmz_date_null_count = (itmz_date=='').sum()
# # # # #         if itmz_date_null_count > 0:
# # # # #             file_issues.append({
# # # # #                 'INPUT FILE': filename,
# # # # #                 'Requirement': 'Itemization Date Null Count',
# # # # #                 'Count': itmz_date_null_count,
# # # # #                 'Entities': 'ITMZ'
# # # # #             })
# # # # #     new_validation_issues.append({
# # # # #         'File': filename,
# # # # #         'Requirement': 'Itemization Date Null Count',
# # # # #         'Status': 'Success' if itmz_date_null_count==0 else 'Fail',
# # # # #         'Count': itmz_date_null_count,
# # # # #         'Entities': 'ITMZ' if itmz_date_null_count>0 else None
# # # # #     })

# # # # #     # ACCT: Account_ID invalid (column index 1, which is position 2 in 1-based)
# # # # #     acct_df = df[df.iloc[:, 0] == 'ACCT']
# # # # #     acct_invalid_count = 0
# # # # #     if not acct_df.empty:
# # # # #         print(f"ACCT records found: {len(acct_df)}")
# # # # #         # Column index 1 is the 2nd column
# # # # #         acct_id = acct_df.iloc[:, 1].fillna('').astype(str).str.strip()
# # # # #         print(f"ACCT ID values: {acct_id.tolist()}")
# # # # #         acct_invalid = (acct_id == '') | (acct_id.str.len() < 4)
# # # # #         acct_invalid_count = acct_invalid.sum()
# # # # #         print(f"ACCT invalid count: {acct_invalid_count}")
       
# # # # #         if acct_invalid_count > 0:
# # # # #             file_issues.append({
# # # # #                 'INPUT FILE': filename,
# # # # #                 'Requirement': 'Account_ID Invalid Count (Null or Length <4)',
# # # # #                 'Count': acct_invalid_count,
# # # # #                 'Entities': 'ACCT'
# # # # #             })
# # # # #     else:
# # # # #         print("No ACCT records found")
   
# # # # #     new_validation_issues.append({
# # # # #         'File': filename,
# # # # #         'Requirement': 'Account_ID Invalid Count (Null or Length <4)',
# # # # #         'Status': 'Success' if acct_invalid_count == 0 else 'Fail',
# # # # #         'Count': acct_invalid_count,
# # # # #         'Entities': 'ACCT' if acct_invalid_count > 0 else None
# # # # #     })

# # # # #     # ACCT: Statute Expiration Date (column index 6, which is position 7 in 1-based)
# # # # #     exp_null_count = 0
# # # # #     if not acct_df.empty:
# # # # #         # Column index 6 is the 7th column
# # # # #         exp_date = acct_df.iloc[:, 6].fillna('').astype(str).str.strip()
# # # # #         print(f"Expiration date values: {exp_date.tolist()}")
# # # # #         exp_null_count = (exp_date == '').sum()
# # # # #         print(f"Expiration null count: {exp_null_count}")
       
# # # # #         if exp_null_count > 0:
# # # # #             file_issues.append({
# # # # #                 'INPUT FILE': filename,
# # # # #                 'Requirement': 'Statute Expiration Date Null Count',
# # # # #                 'Count': exp_null_count,
# # # # #                 'Entities': 'ACCT'
# # # # #             })
   
# # # # #     new_validation_issues.append({
# # # # #         'File': filename,
# # # # #         'Requirement': 'Statute Expiration Date Null Count',
# # # # #         'Status': 'Success' if exp_null_count == 0 else 'Fail',
# # # # #         'Count': exp_null_count,
# # # # #         'Entities': 'ACCT' if exp_null_count > 0 else None
# # # # #     })

# # # # #     # TRNH - AFTRTYP (position 4)
# # # # #     trnh_df = df[df.iloc[:,0]=='TRNH']
# # # # #     if not trnh_df.empty:
# # # # #         aftrtyp = trnh_df.iloc[:,3].fillna('').astype(str).str.strip()
# # # # #         aftrtyp_null_count = (aftrtyp=='').sum()
# # # # #     else:
# # # # #         aftrtyp_null_count = 0
# # # # #     new_validation_issues.append({
# # # # #         'File': filename,
# # # # #         'Requirement': 'AFTRTYP Null Count',
# # # # #         'Status': 'Success' if aftrtyp_null_count==0 else 'Fail',
# # # # #         'Count': aftrtyp_null_count,
# # # # #         'Entities': 'TRNH' if aftrtyp_null_count>0 else None
# # # # #     })

# # # # #     # CALLH - PhoneNumber (position 9)
# # # # #     callh_df = df[df.iloc[:,0]=='CALLH']
# # # # #     if not callh_df.empty:
# # # # #         phone = callh_df.iloc[:,8].fillna('').astype(str).str.strip()
# # # # #         phone_null_count = (phone=='').sum()
# # # # #     else:
# # # # #         phone_null_count = 0
# # # # #     new_validation_issues.append({
# # # # #         'File': filename,
# # # # #         'Requirement': 'PhoneNumber Null Count',
# # # # #         'Status': 'Success' if phone_null_count==0 else 'Fail',
# # # # #         'Count': phone_null_count,
# # # # #         'Entities': 'CALLH' if phone_null_count>0 else None
# # # # #     })

# # # # #     # PRTY: Both Firstname (column index 5) and Lastname (column index 7)
# # # # #     prty_df = df[df.iloc[:, 0] == 'PRTY']
# # # # #     both_null_count = 0
# # # # #     if not prty_df.empty:
# # # # #         print(f"PRTY records found: {len(prty_df)}")
# # # # #         # Column index 5 is the 6th column (Firstname)
# # # # #         first_name = prty_df.iloc[:, 5].fillna('').astype(str).str.strip()
# # # # #         # Column index 7 is the 8th column (Lastname)  
# # # # #         last_name = prty_df.iloc[:, 7].fillna('').astype(str).str.strip()
       
# # # # #         print(f"Firstname values: {first_name.tolist()}")
# # # # #         print(f"Lastname values: {last_name.tolist()}")
       
# # # # #         both_null = (first_name == '') & (last_name == '')
# # # # #         both_null_count = both_null.sum()
# # # # #         print(f"Both null count: {both_null_count}")
       
# # # # #         if both_null_count > 0:
# # # # #             file_issues.append({
# # # # #                 'INPUT FILE': filename,
# # # # #                 'Requirement': 'Both Firstname and Lastname Null Count',
# # # # #                 'Count': both_null_count,
# # # # #                 'Entities': 'PRTY'
# # # # #             })
# # # # #     else:
# # # # #         print("No PRTY records found")
   
# # # # #     new_validation_issues.append({
# # # # #         'File': filename,
# # # # #         'Requirement': 'Both Firstname and Lastname Null Count',
# # # # #         'Status': 'Success' if both_null_count == 0 else 'Fail',
# # # # #         'Count': both_null_count,
# # # # #         'Entities': 'PRTY' if both_null_count > 0 else None
# # # # #     })

# # # # #     # REQUIRED COLUMNS BASED ON MAPPING
# # # # #     for entity_name, group in df.groupby(df.iloc[:,0]):
# # # # #         if entity_name not in mapping_data:
# # # # #             missing_entities.add(entity_name)
# # # # #             continue
# # # # #         sheet_data = mapping_data[entity_name]
# # # # #         position_column = None
# # # # #         required_column = None
# # # # #         for col in sheet_data.columns:
# # # # #             if 'position' in col.lower():
# # # # #                 position_column = col
# # # # #             if 'required?' in col.lower():
# # # # #                 required_column = col
# # # # #         if not position_column or not required_column:
# # # # #             continue
# # # # #         required_mask = sheet_data[required_column].str.lower()=='yes'
# # # # #         required_positions = pd.to_numeric(sheet_data.loc[required_mask, position_column], errors='coerce').dropna().astype(int).tolist()
# # # # #         if not required_positions:
# # # # #             continue
# # # # #         entity_cols = group.iloc[:,1:]
# # # # #         for pos in required_positions:
# # # # #             if pos > entity_cols.shape[1]:
# # # # #                 continue
# # # # #             col_data = entity_cols.iloc[:, pos-1].fillna('').astype(str).str.strip()
# # # # #             status = 'Fail' if (col_data=='').any() else 'Pass'
# # # # #             analysis_results.append({
# # # # #                 'Entity': entity_name,
# # # # #                 'File': filename,
# # # # #                 'Column Number': pos,
# # # # #                 'Status': status
# # # # #             })

# # # # #     return analysis_results, missing_entities, file_issues, new_validation_issues

# # # # # def analyze_required_columns(mapping_file, input_folder, output_file):
# # # # #     if not os.path.exists(mapping_file):
# # # # #         print(f"Mapping file {mapping_file} does not exist.")
# # # # #         return
# # # # #     if not os.path.exists(input_folder):
# # # # #         print(f"Input folder {input_folder} does not exist.")
# # # # #         return
# # # # #     try:
# # # # #         mapping_data = pd.read_excel(mapping_file, sheet_name=None, header=1, engine='openpyxl')
# # # # #         for sheet in mapping_data:
# # # # #             mapping_data[sheet].columns = mapping_data[sheet].columns.map(str).str.strip()
# # # # #     except Exception as e:
# # # # #         print(f"Error reading mapping file {mapping_file}: {e}")
# # # # #         return

# # # # #     txt_files = [f for f in os.listdir(input_folder) if f.lower().endswith(".txt")]
# # # # #     if not txt_files:
# # # # #         print(f"No .txt files found in {input_folder}.")
# # # # #         return

# # # # #     all_analysis_results = []
# # # # #     all_missing_entities = set()
# # # # #     all_file_issues = []
# # # # #     all_new_validation_issues = []

# # # # #     try:
# # # # #         with ThreadPoolExecutor(max_workers=os.cpu_count() or 4) as executor:
# # # # #             futures = [executor.submit(process_single_file, filename, input_folder, mapping_data) for filename in txt_files]
# # # # #             for future in futures:
# # # # #                 file_results, file_missing, file_issues, new_issues = future.result()
# # # # #                 all_analysis_results.extend(file_results)
# # # # #                 all_missing_entities.update(file_missing)
# # # # #                 all_file_issues.extend(file_issues)
# # # # #                 all_new_validation_issues.extend(new_issues)
# # # # #     except Exception as e:
# # # # #         print(f"Error during parallel processing: {e}")
# # # # #         return

# # # # #     analysis_df = pd.DataFrame(all_analysis_results)
# # # # #     missing_entities_df = pd.DataFrame(list(all_missing_entities), columns=['Missing Entities in SAAS mapping sheet'])
# # # # #     file_issues_df = pd.DataFrame(all_file_issues)
# # # # #     validation_summary_df = pd.DataFrame(all_new_validation_issues)

# # # # #     if not validation_summary_df.empty and validation_summary_df['Count'].sum()==0:
# # # # #         print("All new validations successful! No issues found.")

# # # # #     try:
# # # # #         with pd.ExcelWriter(output_file, engine="xlsxwriter") as writer:
# # # # #             analysis_df.to_excel(writer, sheet_name='Required_Columns_Summary', index=False)
# # # # #             missing_entities_df.to_excel(writer, sheet_name='Missing_Entities', index=False)
# # # # #             file_issues_df.to_excel(writer, sheet_name='Frequent_File_Issues', index=False)
# # # # #             validation_summary_df.to_excel(writer, sheet_name='Validation_Summary', index=False)
# # # # #         print(f"Success: Analysis results saved to {output_file}")
# # # # #     except Exception as e:
# # # # #         print(f"Error writing to {output_file}: {e}")

# # # # # if __name__ == "__main__":
# # # # #     mapping_file = "Saas_Legacy_Migration.xlsx"
# # # # #     input_folder = "Input File"
# # # # #     output_file = "Source_File_Analysis.xlsx"
# # # # #     start_time = datetime.now()
# # # # #     analyze_required_columns(mapping_file, input_folder, output_file)
# # # # #     end_time = datetime.now()
# # # # #     print(f"Time taken: {end_time - start_time}")


# # # # import pandas as pd
# # # # import os
# # # # import re
# # # # from concurrent.futures import ThreadPoolExecutor
# # # # from datetime import datetime

# # # # def process_single_file(filename, input_folder, mapping_data):
# # # #     """
# # # #     Process a single .txt file to analyze required columns, missing entities, and file issues.
# # # #     Includes new validations with a dedicated summary, dynamically using mapping positions.
# # # #     """
# # # #     file_path = os.path.join(input_folder, filename)
# # # #     analysis_results = []
# # # #     missing_entities = set()
# # # #     file_issues = []
# # # #     new_validation_issues = []

# # # #     try:
# # # #         df = pd.read_csv(file_path, sep="|", header=None, dtype=str, engine="python", on_bad_lines='skip')
# # # #     except Exception as e:
# # # #         print(f"Error reading file {file_path}: {e}")
# # # #         return analysis_results, missing_entities, file_issues, new_validation_issues

# # # #     if df.empty:
# # # #         print(f"File {filename} is empty.")
# # # #         return analysis_results, missing_entities, file_issues, new_validation_issues

# # # #     df.iloc[:, 0] = df.iloc[:, 0].str.strip()
# # # #     decimal_pattern = re.compile(r'^\.\d+$')

# # # #     # DECIMAL ISSUE
# # # #     decimal_issue_count = 0
# # # #     decimal_issue_entities = set()
# # # #     for col in df.columns[1:]:
# # # #         sample_size = min(1000, len(df))
# # # #         sample_data = df[col].iloc[:sample_size].astype(str)
# # # #         mask = sample_data.apply(lambda x: bool(decimal_pattern.match(x)) if pd.notna(x) else False)
# # # #         if mask.any():
# # # #             decimal_issue_count += df[col].astype(str).apply(lambda x: bool(decimal_pattern.match(x)) if pd.notna(x) else False).sum()
# # # #             decimal_issue_entities.update(df.iloc[mask.index[mask], 0].dropna().unique())

# # # #     if decimal_issue_count > 0:
# # # #         file_issues.append({
# # # #             'INPUT FILE': filename,
# # # #             'Requirement': 'Decimal Issues Count',
# # # #             'Count': decimal_issue_count,
# # # #             'Entities': ', '.join(decimal_issue_entities) if decimal_issue_entities else None
# # # #         })

# # # #     # EMPTY REC_ID
# # # #     rec_id_empty = df.iloc[:, 1].isna() | (df.iloc[:, 1].str.strip() == '')
# # # #     record_id_issue_count = rec_id_empty.sum()
# # # #     if record_id_issue_count > 0:
# # # #         file_issues.append({
# # # #             'INPUT FILE': filename,
# # # #             'Requirement': 'Count of Empty REC_ID',
# # # #             'Count': record_id_issue_count,
# # # #             'Entities': None
# # # #         })

# # # #     # ITMZ - Itemization Date (position 3)
# # # #     itmz_df = df[df.iloc[:,0]=='ITMZ']
# # # #     if not itmz_df.empty:
# # # #         itmz_date = itmz_df.iloc[:, 2].fillna('').astype(str).str.strip()
# # # #         itmz_date_null_count = (itmz_date=='').sum()
# # # #         if itmz_date_null_count > 0:
# # # #             file_issues.append({
# # # #                 'INPUT FILE': filename,
# # # #                 'Requirement': 'Itemization Date Null Count',
# # # #                 'Count': itmz_date_null_count,
# # # #                 'Entities': 'ITMZ'
# # # #             })
# # # #         new_validation_issues.append({
# # # #             'File': filename,
# # # #             'Requirement': 'Itemization Date Null Count',
# # # #             'Status': 'Success' if itmz_date_null_count==0 else 'Fail',
# # # #             'Count': itmz_date_null_count,
# # # #             'Entities': 'ITMZ' if itmz_date_null_count>0 else None
# # # #         })
# # # #     else:
# # # #         new_validation_issues.append({
# # # #             'File': filename,
# # # #             'Requirement': 'Itemization Date Null Count',
# # # #             'Status': 'No Records Found',
# # # #             'Count': None,
# # # #             'Entities': None
# # # #         })

# # # #     # ACCT: Account_ID invalid (position 2)
# # # #     acct_df = df[df.iloc[:, 0] == 'ACCT']
# # # #     if not acct_df.empty:
# # # #         acct_id = acct_df.iloc[:, 1].fillna('').astype(str).str.strip()
# # # #         acct_invalid = (acct_id == '') | (acct_id.str.len() < 4)
# # # #         acct_invalid_count = acct_invalid.sum()

# # # #         if acct_invalid_count > 0:
# # # #             file_issues.append({
# # # #                 'INPUT FILE': filename,
# # # #                 'Requirement': 'Account_ID Invalid Count (Null or Length <4)',
# # # #                 'Count': acct_invalid_count,
# # # #                 'Entities': 'ACCT'
# # # #             })

# # # #         new_validation_issues.append({
# # # #             'File': filename,
# # # #             'Requirement': 'Account_ID Invalid Count (Null or Length <4)',
# # # #             'Status': 'Success' if acct_invalid_count == 0 else 'Fail',
# # # #             'Count': acct_invalid_count,
# # # #             'Entities': 'ACCT' if acct_invalid_count > 0 else None
# # # #         })
# # # #     else:
# # # #         new_validation_issues.append({
# # # #             'File': filename,
# # # #             'Requirement': 'Account_ID Invalid Count (Null or Length <4)',
# # # #             'Status': 'No Records Found',
# # # #             'Count': None,
# # # #             'Entities': None
# # # #         })

# # # #     # ACCT: Statute Expiration Date (position 7)
# # # #     if not acct_df.empty:
# # # #         exp_date = acct_df.iloc[:, 6].fillna('').astype(str).str.strip()
# # # #         exp_null_count = (exp_date == '').sum()

# # # #         if exp_null_count > 0:
# # # #             file_issues.append({
# # # #                 'INPUT FILE': filename,
# # # #                 'Requirement': 'Statute Expiration Date Null Count',
# # # #                 'Count': exp_null_count,
# # # #                 'Entities': 'ACCT'
# # # #             })

# # # #         new_validation_issues.append({
# # # #             'File': filename,
# # # #             'Requirement': 'Statute Expiration Date Null Count',
# # # #             'Status': 'Success' if exp_null_count == 0 else 'Fail',
# # # #             'Count': exp_null_count,
# # # #             'Entities': 'ACCT' if exp_null_count > 0 else None
# # # #         })
# # # #     else:
# # # #         new_validation_issues.append({
# # # #             'File': filename,
# # # #             'Requirement': 'Statute Expiration Date Null Count',
# # # #             'Status': 'No Records Found',
# # # #             'Count': None,
# # # #             'Entities': None
# # # #         })

# # # #     # TRNH - AFTRTYP (position 4)
# # # #     trnh_df = df[df.iloc[:,0]=='TRNH']
# # # #     if not trnh_df.empty:
# # # #         aftrtyp = trnh_df.iloc[:,3].fillna('').astype(str).str.strip()
# # # #         aftrtyp_null_count = (aftrtyp=='').sum()
# # # #         new_validation_issues.append({
# # # #             'File': filename,
# # # #             'Requirement': 'AFTRTYP Null Count',
# # # #             'Status': 'Success' if aftrtyp_null_count==0 else 'Fail',
# # # #             'Count': aftrtyp_null_count,
# # # #             'Entities': 'TRNH' if aftrtyp_null_count>0 else None
# # # #         })
# # # #     else:
# # # #         new_validation_issues.append({
# # # #             'File': filename,
# # # #             'Requirement': 'AFTRTYP Null Count',
# # # #             'Status': 'No Records Found',
# # # #             'Count': None,
# # # #             'Entities': None
# # # #         })

# # # #     # CALLH - PhoneNumber (position 9)
# # # #     callh_df = df[df.iloc[:,0]=='CALLH']
# # # #     if not callh_df.empty:
# # # #         phone = callh_df.iloc[:,8].fillna('').astype(str).str.strip()
# # # #         phone_null_count = (phone=='').sum()
# # # #         new_validation_issues.append({
# # # #             'File': filename,
# # # #             'Requirement': 'PhoneNumber Null Count',
# # # #             'Status': 'Success' if phone_null_count==0 else 'Fail',
# # # #             'Count': phone_null_count,
# # # #             'Entities': 'CALLH' if phone_null_count>0 else None
# # # #         })
# # # #     else:
# # # #         new_validation_issues.append({
# # # #             'File': filename,
# # # #             'Requirement': 'PhoneNumber Null Count',
# # # #             'Status': 'No Records Found',
# # # #             'Count': None,
# # # #             'Entities': None
# # # #         })

# # # #     # PRTY: Both Firstname (col 6) and Lastname (col 8)
# # # #     prty_df = df[df.iloc[:, 0] == 'PRTY']
# # # #     if not prty_df.empty:
# # # #         first_name = prty_df.iloc[:, 5].fillna('').astype(str).str.strip()
# # # #         last_name = prty_df.iloc[:, 7].fillna('').astype(str).str.strip()
# # # #         both_null = (first_name == '') & (last_name == '')
# # # #         both_null_count = both_null.sum()

# # # #         if both_null_count > 0:
# # # #             file_issues.append({
# # # #                 'INPUT FILE': filename,
# # # #                 'Requirement': 'Both Firstname and Lastname Null Count',
# # # #                 'Count': both_null_count,
# # # #                 'Entities': 'PRTY'
# # # #             })

# # # #         new_validation_issues.append({
# # # #             'File': filename,
# # # #             'Requirement': 'Both Firstname and Lastname Null Count',
# # # #             'Status': 'Success' if both_null_count == 0 else 'Fail',
# # # #             'Count': both_null_count,
# # # #             'Entities': 'PRTY' if both_null_count > 0 else None
# # # #         })
# # # #     else:
# # # #         new_validation_issues.append({
# # # #             'File': filename,
# # # #             'Requirement': 'Both Firstname and Lastname Null Count',
# # # #             'Status': 'No Records Found',
# # # #             'Count': None,
# # # #             'Entities': None
# # # #         })

# # # #     # REQUIRED COLUMNS BASED ON MAPPING
# # # #     for entity_name, group in df.groupby(df.iloc[:,0]):
# # # #         if entity_name not in mapping_data:
# # # #             missing_entities.add(entity_name)
# # # #             continue
# # # #         sheet_data = mapping_data[entity_name]
# # # #         position_column = None
# # # #         required_column = None
# # # #         for col in sheet_data.columns:
# # # #             if 'position' in col.lower():
# # # #                 position_column = col
# # # #             if 'required?' in col.lower():
# # # #                 required_column = col
# # # #         if not position_column or not required_column:
# # # #             continue
# # # #         required_mask = sheet_data[required_column].str.lower()=='yes'
# # # #         required_positions = pd.to_numeric(sheet_data.loc[required_mask, position_column], errors='coerce').dropna().astype(int).tolist()
# # # #         if not required_positions:
# # # #             continue
# # # #         entity_cols = group.iloc[:,1:]
# # # #         for pos in required_positions:
# # # #             if pos > entity_cols.shape[1]:
# # # #                 continue
# # # #             col_data = entity_cols.iloc[:, pos-1].fillna('').astype(str).str.strip()
# # # #             status = 'Fail' if (col_data=='').any() else 'Pass'
# # # #             analysis_results.append({
# # # #                 'Entity': entity_name,
# # # #                 'File': filename,
# # # #                 'Column Number': pos,
# # # #                 'Status': status
# # # #             })

# # # #     return analysis_results, missing_entities, file_issues, new_validation_issues

# # # # def analyze_required_columns(mapping_file, input_folder, output_file):
# # # #     if not os.path.exists(mapping_file):
# # # #         print(f"Mapping file {mapping_file} does not exist.")
# # # #         return
# # # #     if not os.path.exists(input_folder):
# # # #         print(f"Input folder {input_folder} does not exist.")
# # # #         return
# # # #     try:
# # # #         mapping_data = pd.read_excel(mapping_file, sheet_name=None, header=1, engine='openpyxl')
# # # #         for sheet in mapping_data:
# # # #             mapping_data[sheet].columns = mapping_data[sheet].columns.map(str).str.strip()
# # # #     except Exception as e:
# # # #         print(f"Error reading mapping file {mapping_file}: {e}")
# # # #         return

# # # #     txt_files = [f for f in os.listdir(input_folder) if f.lower().endswith(".txt")]
# # # #     if not txt_files:
# # # #         print(f"No .txt files found in {input_folder}.")
# # # #         return

# # # #     all_analysis_results = []
# # # #     all_missing_entities = set()
# # # #     all_file_issues = []
# # # #     all_new_validation_issues = []

# # # #     try:
# # # #         with ThreadPoolExecutor(max_workers=os.cpu_count() or 4) as executor:
# # # #             futures = [executor.submit(process_single_file, filename, input_folder, mapping_data) for filename in txt_files]
# # # #             for future in futures:
# # # #                 file_results, file_missing, file_issues, new_issues = future.result()
# # # #                 all_analysis_results.extend(file_results)
# # # #                 all_missing_entities.update(file_missing)
# # # #                 all_file_issues.extend(file_issues)
# # # #                 all_new_validation_issues.extend(new_issues)
# # # #     except Exception as e:
# # # #         print(f"Error during parallel processing: {e}")
# # # #         return

# # # #     analysis_df = pd.DataFrame(all_analysis_results)
# # # #     missing_entities_df = pd.DataFrame(list(all_missing_entities), columns=['Missing Entities in SAAS mapping sheet'])
# # # #     file_issues_df = pd.DataFrame(all_file_issues)
# # # #     validation_summary_df = pd.DataFrame(all_new_validation_issues)

# # # #     if not validation_summary_df.empty and validation_summary_df['Count'].notna().sum()>0 and validation_summary_df['Count'].fillna(0).sum()==0:
# # # #         print("All new validations successful! No issues found.")

# # # #     try:
# # # #         with pd.ExcelWriter(output_file, engine="xlsxwriter") as writer:
# # # #             analysis_df.to_excel(writer, sheet_name='Required_Columns_Summary', index=False)
# # # #             missing_entities_df.to_excel(writer, sheet_name='Missing_Entities', index=False)
# # # #             file_issues_df.to_excel(writer, sheet_name='Frequent_File_Issues', index=False)
# # # #             validation_summary_df.to_excel(writer, sheet_name='Validation_Summary', index=False)
# # # #         print(f"Success: Analysis results saved to {output_file}")
# # # #     except Exception as e:
# # # #         print(f"Error writing to {output_file}: {e}")

# # # # if __name__ == "__main__":
# # # #     mapping_file = "Saas_Legacy_Migration.xlsx"
# # # #     input_folder = "Input File"
# # # #     output_file = "Source_File_Analysis.xlsx"
# # # #     start_time = datetime.now()
# # # #     analyze_required_columns(mapping_file, input_folder, output_file)
# # # #     end_time = datetime.now()
# # # #     print(f"Time taken: {end_time - start_time}")

# # # # # above is crt code



# # # # import pandas as pd
# # # # import os
# # # # import re
# # # # from concurrent.futures import ThreadPoolExecutor
# # # # from datetime import datetime

# # # # def process_single_file(filename, input_folder, mapping_data):
# # # #     """
# # # #     Process a single .txt file to analyze required columns, missing entities, and file issues.
# # # #     Includes new validations with a dedicated summary, dynamically using mapping positions.
# # # #     """
# # # #     file_path = os.path.join(input_folder, filename)
# # # #     analysis_results = []
# # # #     missing_entities = set()
# # # #     file_issues = []
# # # #     new_validation_issues = []

# # # #     try:
# # # #         df = pd.read_csv(file_path, sep="|", header=None, dtype=str, engine="python", on_bad_lines='skip')
# # # #     except Exception as e:
# # # #         print(f"Error reading file {file_path}: {e}")
# # # #         return analysis_results, missing_entities, file_issues, new_validation_issues

# # # #     if df.empty:
# # # #         print(f"File {filename} is empty.")
# # # #         return analysis_results, missing_entities, file_issues, new_validation_issues

# # # #     df.iloc[:, 0] = df.iloc[:, 0].str.strip()
# # # #     decimal_pattern = re.compile(r'^\.\d+$')

# # # #     # DECIMAL ISSUE
# # # #     decimal_issue_count = 0
# # # #     decimal_issue_entities = set()
# # # #     for col in df.columns[1:]:
# # # #         sample_size = min(1000, len(df))
# # # #         sample_data = df[col].iloc[:sample_size].astype(str)
# # # #         mask = sample_data.apply(lambda x: bool(decimal_pattern.match(x)) if pd.notna(x) else False)
# # # #         if mask.any():
# # # #             decimal_issue_count += df[col].astype(str).apply(lambda x: bool(decimal_pattern.match(x)) if pd.notna(x) else False).sum()
# # # #             decimal_issue_entities.update(df.iloc[mask.index[mask], 0].dropna().unique())

# # # #     if decimal_issue_count > 0:
# # # #         file_issues.append({
# # # #             'INPUT FILE': filename,
# # # #             'Requirement': 'Decimal Issues Count',
# # # #             'Count': decimal_issue_count,
# # # #             'Entities': ', '.join(decimal_issue_entities) if decimal_issue_entities else None
# # # #         })

# # # #     # EMPTY REC_ID
# # # #     rec_id_empty = df.iloc[:, 1].isna() | (df.iloc[:, 1].str.strip() == '')
# # # #     record_id_issue_count = rec_id_empty.sum()
# # # #     if record_id_issue_count > 0:
# # # #         file_issues.append({
# # # #             'INPUT FILE': filename,
# # # #             'Requirement': 'Count of Empty REC_ID',
# # # #             'Count': record_id_issue_count,
# # # #             'Entities': None
# # # #         })

# # # #     # ITMZ - Itemization Date (position 3)
# # # #     itmz_df = df[df.iloc[:,0]=='ITMZ']
# # # #     if not itmz_df.empty:
# # # #         itmz_date = itmz_df.iloc[:, 2].fillna('').astype(str).str.strip()
# # # #         itmz_date_null_count = (itmz_date=='').sum()
# # # #         if itmz_date_null_count > 0:
# # # #             file_issues.append({
# # # #                 'INPUT FILE': filename,
# # # #                 'Requirement': 'Itemization Date Null Count',
# # # #                 'Count': itmz_date_null_count,
# # # #                 'Entities': 'ITMZ'
# # # #             })
# # # #         new_validation_issues.append({
# # # #             'File': filename,
# # # #             'Requirement': 'Itemization Date Null Count',
# # # #             'Status': 'Success' if itmz_date_null_count==0 else 'Fail',
# # # #             'Count': itmz_date_null_count,
# # # #             'Entities': 'ITMZ' if itmz_date_null_count>0 else None
# # # #         })
# # # #     else:
# # # #         new_validation_issues.append({
# # # #             'File': filename,
# # # #             'Requirement': 'Itemization Date Null Count',
# # # #             'Status': 'No Records Found',
# # # #             'Count': None,
# # # #             'Entities': None
# # # #         })

# # # #     # ACCT: Account_ID invalid (using ARACCLACCT)
# # # #     acct_df = df[df.iloc[:, 0] == 'ACCT']
# # # #     if not acct_df.empty and 'ACCT' in mapping_data:
# # # #         acct_sheet = mapping_data['ACCT']
# # # #         # Initialize variables to avoid undefined errors
# # # #         rm_column = None
# # # #         position_column = None
# # # #         aracclacct_pos = None

# # # #         # Find RM Column or fallback to Description
# # # #         for col in acct_sheet.columns:
# # # #             if 'rm column' in col.lower():
# # # #                 rm_column = col
# # # #                 break
# # # #         if rm_column is None:
# # # #             rm_column = 'Description'  # Fallback

# # # #         # Find Position column
# # # #         for col in acct_sheet.columns:
# # # #             if 'position' in col.lower():
# # # #                 position_column = col
# # # #                 break

# # # #         if position_column:
# # # #             # Get position for ARACCLACCT
# # # #             aracclacct_mask = acct_sheet[rm_column].str.upper() == 'ARACCLACCT'

# # # #             if aracclacct_mask.any():
# # # #                 try:
# # # #                     aracclacct_pos = int(acct_sheet.loc[aracclacct_mask, position_column].iloc[0]) - 1
# # # #                 except (ValueError, IndexError) as e:
# # # #                     print(f"Error retrieving ARACCLACCT position for {filename}: {e}")
# # # #                     aracclacct_pos = None

# # # #             if aracclacct_pos is not None and aracclacct_pos < acct_df.shape[1]:
# # # #                 # Extract Account_ID
# # # #                 acct_id = acct_df.iloc[:, aracclacct_pos].fillna('').astype(str).str.strip()
# # # #                 acct_invalid_count = (acct_id == '').sum()

# # # #                 print(f"Account_ID (ARACCLACCT) values: {acct_id.tolist()}")
# # # #                 print(f"Account_ID null count: {acct_invalid_count}")

# # # #                 if acct_invalid_count > 0:
# # # #                     file_issues.append({
# # # #                         'INPUT FILE': filename,
# # # #                         'Requirement': 'Account_ID Null Count',
# # # #                         'Count': acct_invalid_count,
# # # #                         'Entities': 'ACCT'
# # # #                     })

# # # #                 new_validation_issues.append({
# # # #                     'File': filename,
# # # #                     'Requirement': 'Account_ID Null Count',
# # # #                     'Status': 'Success' if acct_invalid_count == 0 else 'Fail',
# # # #                     'Count': acct_invalid_count,
# # # #                     'Entities': 'ACCT' if acct_invalid_count > 0 else None
# # # #                 })
# # # #             else:
# # # #                 # Fallback to original position (index 1)
# # # #                 acct_pos = 1
# # # #                 acct_invalid_count = 0
# # # #                 if acct_df.shape[1] > acct_pos:
# # # #                     acct_id = acct_df.iloc[:, acct_pos].fillna('').astype(str).str.strip()
# # # #                     acct_invalid_count = (acct_id == '').sum()
# # # #                     print(f"Fallback: Account_ID values (index 1): {acct_id.tolist()}")
# # # #                     print(f"Fallback: Account_ID null count: {acct_invalid_count}")
# # # #                 else:
# # # #                     acct_invalid_count = len(acct_df)  # All records invalid if insufficient columns
# # # #                     print(f"Fallback: Insufficient columns for Account_ID (index 1). Counted as null: {acct_invalid_count}")

# # # #                 if acct_invalid_count > 0:
# # # #                     file_issues.append({
# # # #                         'INPUT FILE': filename,
# # # #                         'Requirement': 'Account_ID Null Count',
# # # #                         'Count': acct_invalid_count,
# # # #                         'Entities': 'ACCT'
# # # #                     })

# # # #                 new_validation_issues.append({
# # # #                     'File': filename,
# # # #                     'Requirement': 'Account_ID Null Count',
# # # #                     'Status': 'Success' if acct_invalid_count == 0 else 'Fail',
# # # #                     'Count': acct_invalid_count,
# # # #                     'Entities': 'ACCT' if acct_invalid_count > 0 else None
# # # #                 })
# # # #         else:
# # # #             # Fallback if no position column
# # # #             acct_pos = 1
# # # #             acct_invalid_count = 0
# # # #             if acct_df.shape[1] > acct_pos:
# # # #                 acct_id = acct_df.iloc[:, acct_pos].fillna('').astype(str).str.strip()
# # # #                 acct_invalid_count = (acct_id == '').sum()
# # # #                 print(f"Fallback: Account_ID values (index 1): {acct_id.tolist()}")
# # # #                 print(f"Fallback: Account_ID null count: {acct_invalid_count}")
# # # #             else:
# # # #                 acct_invalid_count = len(acct_df)  # All records invalid if insufficient columns
# # # #                 print(f"Fallback: Insufficient columns for Account_ID (index 1). Counted as null: {acct_invalid_count}")

# # # #             if acct_invalid_count > 0:
# # # #                 file_issues.append({
# # # #                     'INPUT FILE': filename,
# # # #                     'Requirement': 'Account_ID Null Count',
# # # #                     'Count': acct_invalid_count,
# # # #                     'Entities': 'ACCT'
# # # #                 })

# # # #             new_validation_issues.append({
# # # #                 'File': filename,
# # # #                 'Requirement': 'Account_ID Null Count',
# # # #                 'Status': 'Success' if acct_invalid_count == 0 else 'Fail',
# # # #                 'Count': acct_invalid_count,
# # # #                 'Entities': 'ACCT' if acct_invalid_count > 0 else None
# # # #             })
# # # #     else:
# # # #         new_validation_issues.append({
# # # #             'File': filename,
# # # #             'Requirement': 'Account_ID Null Count',
# # # #             'Status': 'No Records Found',
# # # #             'Count': None,
# # # #             'Entities': None
# # # #         })

# # # #     # ACCT: Statute Expiration Date (calculated using ARACSTATUTEBASEDTE and ARACCNVLPYDTE)
# # # #     if not acct_df.empty and 'ACCT' in mapping_data:
# # # #         acct_sheet = mapping_data['ACCT']
# # # #         # Initialize variables to avoid undefined errors
# # # #         rm_column = None
# # # #         position_column = None
# # # #         statute_pos = None
# # # #         cnvlpy_pos = None

# # # #         # Find RM Column or fallback to Description
# # # #         for col in acct_sheet.columns:
# # # #             if 'rm column' in col.lower():
# # # #                 rm_column = col
# # # #                 break
# # # #         if rm_column is None:
# # # #             rm_column = 'Description'  # Fallback

# # # #         # Find Position column
# # # #         for col in acct_sheet.columns:
# # # #             if 'position' in col.lower():
# # # #                 position_column = col
# # # #                 break

# # # #         if position_column:
# # # #             # Get positions for ARACSTATUTEBASEDTE and ARACCNVLPYDTE
# # # #             statute_mask = acct_sheet[rm_column].str.upper() == 'ARACSTATUTEBASEDTE'
# # # #             cnvlpy_mask = acct_sheet[rm_column].str.upper() == 'ARACCNVLPYDTE'

# # # #             if statute_mask.any() and cnvlpy_mask.any():
# # # #                 try:
# # # #                     statute_pos = int(acct_sheet.loc[statute_mask, position_column].iloc[0]) - 1
# # # #                     cnvlpy_pos = int(acct_sheet.loc[cnvlpy_mask, position_column].iloc[0]) - 1
# # # #                 except (ValueError, IndexError) as e:
# # # #                     print(f"Error retrieving positions for {filename}: {e}")
# # # #                     statute_pos = None
# # # #                     cnvlpy_pos = None

# # # #             if statute_pos is not None and cnvlpy_pos is not None and statute_pos < acct_df.shape[1] and cnvlpy_pos < acct_df.shape[1]:
# # # #                 # Extract dates
# # # #                 statute_date = acct_df.iloc[:, statute_pos].fillna('').astype(str).str.strip()
# # # #                 cnvlpy_date = acct_df.iloc[:, cnvlpy_pos].fillna('').astype(str).str.strip()

# # # #                 # Count null/invalid cases
# # # #                 empty_mask = (statute_date == '') | (cnvlpy_date == '')
# # # #                 exp_null_count = empty_mask.sum()

# # # #                 # Check for invalid dates in non-empty records
# # # #                 non_empty_mask = ~empty_mask
# # # #                 if non_empty_mask.any():
# # # #                     try:
# # # #                         statute_dt = pd.to_datetime(statute_date[non_empty_mask], errors='coerce')
# # # #                         cnvlpy_dt = pd.to_datetime(cnvlpy_date[non_empty_mask], errors='coerce')
# # # #                         invalid_date_mask = statute_dt.isna() | cnvlpy_dt.isna()
# # # #                         exp_null_count += invalid_date_mask.sum()
# # # #                     except Exception as e:
# # # #                         print(f"Error parsing dates for {filename}: {e}")
# # # #                         exp_null_count += non_empty_mask.sum()  # Treat all as invalid if parsing fails

# # # #                 print(f"Statute date (ARACSTATUTEBASEDTE) values: {statute_date.tolist()}")
# # # #                 print(f"Cnvlpy date (ARACCNVLPYDTE) values: {cnvlpy_date.tolist()}")
# # # #                 print(f"Expiration null count: {exp_null_count}")

# # # #                 if exp_null_count > 0:
# # # #                     file_issues.append({
# # # #                         'INPUT FILE': filename,
# # # #                         'Requirement': 'Statute Expiration Date Null Count',
# # # #                         'Count': exp_null_count,
# # # #                         'Entities': 'ACCT'
# # # #                     })

# # # #                 new_validation_issues.append({
# # # #                     'File': filename,
# # # #                     'Requirement': 'Statute Expiration Date Null Count',
# # # #                     'Status': 'Success' if exp_null_count == 0 else 'Fail',
# # # #                     'Count': exp_null_count,
# # # #                     'Entities': 'ACCT' if exp_null_count > 0 else None
# # # #                 })
# # # #             else:
# # # #                 # Fallback to original logic (check index 6)
# # # #                 exp_pos = 6
# # # #                 exp_null_count = 0
# # # #                 if acct_df.shape[1] > exp_pos:
# # # #                     exp_date = acct_df.iloc[:, exp_pos].fillna('').astype(str).str.strip()
# # # #                     exp_null_count = (exp_date == '').sum()
# # # #                     print(f"Fallback: Expiration date values (index 6): {exp_date.tolist()}")
# # # #                     print(f"Fallback: Expiration null count: {exp_null_count}")
# # # #                 else:
# # # #                     exp_null_count = len(acct_df)  # All records invalid if insufficient columns
# # # #                     print(f"Fallback: Insufficient columns for expiration date (index 6). Counted as null: {exp_null_count}")

# # # #                 if exp_null_count > 0:
# # # #                     file_issues.append({
# # # #                         'INPUT FILE': filename,
# # # #                         'Requirement': 'Statute Expiration Date Null Count',
# # # #                         'Count': exp_null_count,
# # # #                         'Entities': 'ACCT'
# # # #                     })

# # # #                 new_validation_issues.append({
# # # #                     'File': filename,
# # # #                     'Requirement': 'Statute Expiration Date Null Count',
# # # #                     'Status': 'Success' if exp_null_count == 0 else 'Fail',
# # # #                     'Count': exp_null_count,
# # # #                     'Entities': 'ACCT' if exp_null_count > 0 else None
# # # #                 })
# # # #         else:
# # # #             # Fallback if no position column
# # # #             exp_pos = 6
# # # #             exp_null_count = 0
# # # #             if acct_df.shape[1] > exp_pos:
# # # #                 exp_date = acct_df.iloc[:, exp_pos].fillna('').astype(str).str.strip()
# # # #                 exp_null_count = (exp_date == '').sum()
# # # #                 print(f"Fallback: Expiration date values (index 6): {exp_date.tolist()}")
# # # #                 print(f"Fallback: Expiration null count: {exp_null_count}")
# # # #             else:
# # # #                 exp_null_count = len(acct_df)  # All records invalid if insufficient columns
# # # #                 print(f"Fallback: Insufficient columns for expiration date (index 6). Counted as null: {exp_null_count}")

# # # #             if exp_null_count > 0:
# # # #                 file_issues.append({
# # # #                     'INPUT FILE': filename,
# # # #                     'Requirement': 'Statute Expiration Date Null Count',
# # # #                     'Count': exp_null_count,
# # # #                     'Entities': 'ACCT'
# # # #                 })

# # # #             new_validation_issues.append({
# # # #                 'File': filename,
# # # #                 'Requirement': 'Statute Expiration Date Null Count',
# # # #                 'Status': 'Success' if exp_null_count == 0 else 'Fail',
# # # #                 'Count': exp_null_count,
# # # #                 'Entities': 'ACCT' if exp_null_count > 0 else None
# # # #             })
# # # #     else:
# # # #         new_validation_issues.append({
# # # #             'File': filename,
# # # #             'Requirement': 'Statute Expiration Date Null Count',
# # # #             'Status': 'No Records Found',
# # # #             'Count': None,
# # # #             'Entities': None
# # # #         })

# # # #     # TRNH - AFTRTYP (position 4)
# # # #     trnh_df = df[df.iloc[:,0]=='TRNH']
# # # #     if not trnh_df.empty:
# # # #         aftrtyp = trnh_df.iloc[:,3].fillna('').astype(str).str.strip()
# # # #         aftrtyp_null_count = (aftrtyp=='').sum()
# # # #         new_validation_issues.append({
# # # #             'File': filename,
# # # #             'Requirement': 'AFTRTYP Null Count',
# # # #             'Status': 'Success' if aftrtyp_null_count==0 else 'Fail',
# # # #             'Count': aftrtyp_null_count,
# # # #             'Entities': 'TRNH' if aftrtyp_null_count>0 else None
# # # #         })
# # # #     else:
# # # #         new_validation_issues.append({
# # # #             'File': filename,
# # # #             'Requirement': 'AFTRTYP Null Count',
# # # #             'Status': 'No Records Found',
# # # #             'Count': None,
# # # #             'Entities': None
# # # #         })

# # # #     # CALLH - PhoneNumber (position 9)
# # # #     callh_df = df[df.iloc[:,0]=='CALLH']
# # # #     if not callh_df.empty:
# # # #         phone = callh_df.iloc[:,8].fillna('').astype(str).str.strip()
# # # #         phone_null_count = (phone=='').sum()
# # # #         new_validation_issues.append({
# # # #             'File': filename,
# # # #             'Requirement': 'PhoneNumber Null Count',
# # # #             'Status': 'Success' if phone_null_count==0 else 'Fail',
# # # #             'Count': phone_null_count,
# # # #             'Entities': 'CALLH' if phone_null_count>0 else None
# # # #         })
# # # #     else:
# # # #         new_validation_issues.append({
# # # #             'File': filename,
# # # #             'Requirement': 'PhoneNumber Null Count',
# # # #             'Status': 'No Records Found',
# # # #             'Count': None,
# # # #             'Entities': None
# # # #         })

# # # #     # PRTY: Both Firstname (col 6) and Lastname (col 8)
# # # #     prty_df = df[df.iloc[:, 0] == 'PRTY']
# # # #     if not prty_df.empty:
# # # #         first_name = prty_df.iloc[:, 5].fillna('').astype(str).str.strip()
# # # #         last_name = prty_df.iloc[:, 7].fillna('').astype(str).str.strip()
# # # #         both_null = (first_name == '') & (last_name == '')
# # # #         both_null_count = both_null.sum()

# # # #         if both_null_count > 0:
# # # #             file_issues.append({
# # # #                 'INPUT FILE': filename,
# # # #                 'Requirement': 'Both Firstname and Lastname Null Count',
# # # #                 'Count': both_null_count,
# # # #                 'Entities': 'PRTY'
# # # #             })

# # # #         new_validation_issues.append({
# # # #             'File': filename,
# # # #             'Requirement': 'Both Firstname and Lastname Null Count',
# # # #             'Status': 'Success' if both_null_count == 0 else 'Fail',
# # # #             'Count': both_null_count,
# # # #             'Entities': 'PRTY' if both_null_count > 0 else None
# # # #         })
# # # #     else:
# # # #         new_validation_issues.append({
# # # #             'File': filename,
# # # #             'Requirement': 'Both Firstname and Lastname Null Count',
# # # #             'Status': 'No Records Found',
# # # #             'Count': None,
# # # #             'Entities': None
# # # #         })

# # # #     # REQUIRED COLUMNS BASED ON MAPPING
# # # #     for entity_name, group in df.groupby(df.iloc[:,0]):
# # # #         if entity_name not in mapping_data:
# # # #             missing_entities.add(entity_name)
# # # #             continue
# # # #         sheet_data = mapping_data[entity_name]
# # # #         position_column = None
# # # #         required_column = None
# # # #         for col in sheet_data.columns:
# # # #             if 'position' in col.lower():
# # # #                 position_column = col
# # # #             if 'required?' in col.lower():
# # # #                 required_column = col
# # # #         if not position_column or not required_column:
# # # #             continue
# # # #         required_mask = sheet_data[required_column].str.lower()=='yes'
# # # #         required_positions = pd.to_numeric(sheet_data.loc[required_mask, position_column], errors='coerce').dropna().astype(int).tolist()
# # # #         if not required_positions:
# # # #             continue
# # # #         entity_cols = group.iloc[:,1:]
# # # #         for pos in required_positions:
# # # #             if pos > entity_cols.shape[1]:
# # # #                 continue
# # # #             col_data = entity_cols.iloc[:, pos-1].fillna('').astype(str).str.strip()
# # # #             status = 'Fail' if (col_data=='').any() else 'Pass'
# # # #             analysis_results.append({
# # # #                 'Entity': entity_name,
# # # #                 'File': filename,
# # # #                 'Column Number': pos,
# # # #                 'Status': status
# # # #             })

# # # #     return analysis_results, missing_entities, file_issues, new_validation_issues

# # # # def analyze_required_columns(mapping_file, input_folder, output_file):
# # # #     if not os.path.exists(mapping_file):
# # # #         print(f"Mapping file {mapping_file} does not exist.")
# # # #         return
# # # #     if not os.path.exists(input_folder):
# # # #         print(f"Input folder {input_folder} does not exist.")
# # # #         return
# # # #     try:
# # # #         mapping_data = pd.read_excel(mapping_file, sheet_name=None, header=1, engine='openpyxl')
# # # #         for sheet in mapping_data:
# # # #             mapping_data[sheet].columns = mapping_data[sheet].columns.map(str).str.strip()
# # # #     except Exception as e:
# # # #         print(f"Error reading mapping file {mapping_file}: {e}")
# # # #         return

# # # #     txt_files = [f for f in os.listdir(input_folder) if f.lower().endswith(".txt")]
# # # #     if not txt_files:
# # # #         print(f"No .txt files found in {input_folder}.")
# # # #         return

# # # #     all_analysis_results = []
# # # #     all_missing_entities = set()
# # # #     all_file_issues = []
# # # #     all_new_validation_issues = []

# # # #     try:
# # # #         with ThreadPoolExecutor(max_workers=os.cpu_count() or 4) as executor:
# # # #             futures = [executor.submit(process_single_file, filename, input_folder, mapping_data) for filename in txt_files]
# # # #             for future in futures:
# # # #                 file_results, file_missing, file_issues, new_issues = future.result()
# # # #                 all_analysis_results.extend(file_results)
# # # #                 all_missing_entities.update(file_missing)
# # # #                 all_file_issues.extend(file_issues)
# # # #                 all_new_validation_issues.extend(new_issues)
# # # #     except Exception as e:
# # # #         print(f"Error during parallel processing: {e}")
# # # #         return

# # # #     analysis_df = pd.DataFrame(all_analysis_results)
# # # #     missing_entities_df = pd.DataFrame(list(all_missing_entities), columns=['Missing Entities in SAAS mapping sheet'])
# # # #     file_issues_df = pd.DataFrame(all_file_issues)
# # # #     validation_summary_df = pd.DataFrame(all_new_validation_issues)

# # # #     if not validation_summary_df.empty and validation_summary_df['Count'].notna().sum()>0 and validation_summary_df['Count'].fillna(0).sum()==0:
# # # #         print("All new validations successful! No issues found.")

# # # #     try:
# # # #         with pd.ExcelWriter(output_file, engine="xlsxwriter") as writer:
# # # #             analysis_df.to_excel(writer, sheet_name='Required_Columns_Summary', index=False)
# # # #             missing_entities_df.to_excel(writer, sheet_name='Missing_Entities', index=False)
# # # #             file_issues_df.to_excel(writer, sheet_name='Frequent_File_Issues', index=False)
# # # #             validation_summary_df.to_excel(writer, sheet_name='Validation_Summary', index=False)
# # # #         print(f"Success: Analysis results saved to {output_file}")
# # # #     except Exception as e:
# # # #         print(f"Error writing to {output_file}: {e}")

# # # # if __name__ == "__main__":
# # # #     mapping_file = "Saas_Legacy_Migration.xlsx"
# # # #     input_folder = "Input File"
# # # #     output_file = r"C:\Users\AbarnaV\Python\dev-qa-repo2 - Copy\dev-qa-repo\Output Folder\Source_File_Analysis.xlsx"
# # # #     start_time = datetime.now()
# # # #     analyze_required_columns(mapping_file, input_folder, output_file)
# # # #     end_time = datetime.now()
# # # #     print(f"Time taken: {end_time - start_time}")

# # # 20

# # # 20
# # # import pandas as pd
# # # import os
# # # import re
# # # from concurrent.futures import ThreadPoolExecutor
# # # from datetime import datetime

# # # def process_single_file(filename, input_folder, mapping_data):
# # #     """
# # #     Process a single .txt file to analyze required columns, missing entities, and file issues.
# # #     Includes new validations with a dedicated summary, dynamically using mapping positions.
# # #     """
# # #     file_path = os.path.join(input_folder, filename)
# # #     analysis_results = []
# # #     missing_entities = set()
# # #     file_issues = []
# # #     new_validation_issues = []

# # #     try:
# # #         df = pd.read_csv(file_path, sep="|", header=None, dtype=str, engine="python", on_bad_lines='skip')
# # #     except Exception as e:
# # #         print(f"Error reading file {file_path}: {e}")
# # #         return analysis_results, missing_entities, file_issues, new_validation_issues

# # #     if df.empty:
# # #         print(f"File {filename} is empty.")
# # #         return analysis_results, missing_entities, file_issues, new_validation_issues

# # #     df.iloc[:, 0] = df.iloc[:, 0].str.strip()
# # #     decimal_pattern = re.compile(r'^\.\d+$')

# # #     # DECIMAL ISSUE
# # #     decimal_issue_count = 0
# # #     decimal_issue_entities = set()
# # #     for col in df.columns[1:]:
# # #         sample_size = min(1000, len(df))
# # #         sample_data = df[col].iloc[:sample_size].astype(str)
# # #         mask = sample_data.apply(lambda x: bool(decimal_pattern.match(x)) if pd.notna(x) else False)
# # #         if mask.any():
# # #             decimal_issue_count += df[col].astype(str).apply(lambda x: bool(decimal_pattern.match(x)) if pd.notna(x) else False).sum()
# # #             decimal_issue_entities.update(df.iloc[mask.index[mask], 0].dropna().unique())

# # #     if decimal_issue_count > 0:
# # #         file_issues.append({
# # #             'INPUT FILE': filename,
# # #             'Requirement': 'Decimal Issues Count',
# # #             'Count': decimal_issue_count,
# # #             'Entities': ', '.join(decimal_issue_entities) if decimal_issue_entities else None
# # #         })

# # #     # EMPTY REC_ID
# # #     rec_id_empty = df.iloc[:, 1].isna() | (df.iloc[:, 1].str.strip() == '')
# # #     record_id_issue_count = rec_id_empty.sum()
# # #     if record_id_issue_count > 0:
# # #         file_issues.append({
# # #             'INPUT FILE': filename,
# # #             'Requirement': 'Count of Empty REC_ID',
# # #             'Count': record_id_issue_count,
# # #             'Entities': None
# # #         })

# # #     # ITMZ - Itemization Date (position 3)
# # #     itmz_df = df[df.iloc[:,0]=='ITMZ']
# # #     if not itmz_df.empty:
# # #         itmz_date = itmz_df.iloc[:, 2].fillna('').astype(str).str.strip()
# # #         itmz_date_null_count = (itmz_date=='').sum()
# # #         if itmz_date_null_count > 0:
# # #             file_issues.append({
# # #                 'INPUT FILE': filename,
# # #                 'Requirement': 'Itemization Date Null Count',
# # #                 'Count': itmz_date_null_count,
# # #                 'Entities': 'ITMZ'
# # #             })
# # #         new_validation_issues.append({
# # #             'File': filename,
# # #             'Requirement': 'Itemization Date Null Count',
# # #             'Status': 'Success' if itmz_date_null_count==0 else 'Fail',
# # #             'Count': itmz_date_null_count,
# # #             'Entities': 'ITMZ' if itmz_date_null_count>0 else None
# # #         })
# # #     else:
# # #         new_validation_issues.append({
# # #             'File': filename,
# # #             'Requirement': 'Itemization Date Null Count',
# # #             'Status': 'No Records Found',
# # #             'Count': None,
# # #             'Entities': None
# # #         })

# # #     # ACCT: Account_ID invalid (position 2)
# # #     acct_df = df[df.iloc[:, 0] == 'ACCT']
# # #     if not acct_df.empty:
# # #         acct_id = acct_df.iloc[:, 1].fillna('').astype(str).str.strip()
# # #         acct_invalid = (acct_id == '') | (acct_id.str.len() < 4)
# # #         acct_invalid_count = acct_invalid.sum()

# # #         if acct_invalid_count > 0:
# # #             file_issues.append({
# # #                 'INPUT FILE': filename,
# # #                 'Requirement': 'Account_ID Invalid Count (Null or Length <4)',
# # #                 'Count': acct_invalid_count,
# # #                 'Entities': 'ACCT'
# # #             })

# # #         new_validation_issues.append({
# # #             'File': filename,
# # #             'Requirement': 'Account_ID Invalid Count (Null or Length <4)',
# # #             'Status': 'Success' if acct_invalid_count == 0 else 'Fail',
# # #             'Count': acct_invalid_count,
# # #             'Entities': 'ACCT' if acct_invalid_count > 0 else None
# # #         })
# # #     else:
# # #         new_validation_issues.append({
# # #             'File': filename,
# # #             'Requirement': 'Account_ID Invalid Count (Null or Length <4)',
# # #             'Status': 'No Records Found',
# # #             'Count': None,
# # #             'Entities': None
# # #         })

# # #     # ACCT: Account Number (ARACCLACCT) Null Check
# # #     acct_num_null_count = 0
# # #     if not acct_df.empty and 'ACCT' in mapping_data:
# # #         acct_sheet = mapping_data['ACCT']
# # #         # Find RM Column or fallback to Description
# # #         rm_column = None
# # #         for col in acct_sheet.columns:
# # #             if 'rm column' in col.lower():
# # #                 rm_column = col
# # #                 break
# # #         if rm_column is None:
# # #             rm_column = 'Description'  # Fallback

# # #         # Find Position column
# # #         position_column = None
# # #         for col in acct_sheet.columns:
# # #             if 'position' in col.lower():
# # #                 position_column = col
# # #                 break

# # #         if position_column is not None:
# # #             # Get position for ARACCLACCT
# # #             acct_num_mask = acct_sheet[rm_column].str.upper() == 'ARACCLACCT'
# # #             acct_num_pos = None

# # #             if acct_num_mask.any():
# # #                 acct_num_pos = int(acct_sheet.loc[acct_num_mask, position_column].values[0]) - 1

# # #             if acct_num_pos is not None and acct_num_pos < acct_df.shape[1]:
# # #                 # Extract account number
# # #                 acct_num = acct_df.iloc[:, acct_num_pos].fillna('').astype(str).str.strip()
# # #                 acct_num_null_count = (acct_num == '').sum()

# # #                 print(f"Account Number (ARACCLACCT) values: {acct_num.tolist()}")
# # #                 print(f"Account Number null count: {acct_num_null_count}")

# # #                 if acct_num_null_count > 0:
# # #                     file_issues.append({
# # #                         'INPUT FILE': filename,
# # #                         'Requirement': 'Account Number Null Count',
# # #                         'Count': acct_num_null_count,
# # #                         'Entities': 'ACCT'
# # #                     })

# # #                 new_validation_issues.append({
# # #                     'File': filename,
# # #                     'Requirement': 'Account Number Null Count',
# # #                     'Status': 'Success' if acct_num_null_count == 0 else 'Fail',
# # #                     'Count': acct_num_null_count,
# # #                     'Entities': 'ACCT' if acct_num_null_count > 0 else None
# # #                 })
# # #             else:
# # #                 # Fallback to position 2 (index 1, same as Account_ID)
# # #                 acct_num_pos = 1
# # #                 if acct_df.shape[1] > acct_num_pos:
# # #                     acct_num = acct_df.iloc[:, acct_num_pos].fillna('').astype(str).str.strip()
# # #                     acct_num_null_count = (acct_num == '').sum()
# # #                     print(f"Fallback: Account Number values (index 1): {acct_num.tolist()}")
# # #                     print(f"Fallback: Account Number null count: {acct_num_null_count}")

# # #                     if acct_num_null_count > 0:
# # #                         file_issues.append({
# # #                             'INPUT FILE': filename,
# # #                             'Requirement': 'Account Number Null Count',
# # #                             'Count': acct_num_null_count,
# # #                             'Entities': 'ACCT'
# # #                         })

# # #                     new_validation_issues.append({
# # #                         'File': filename,
# # #                         'Requirement': 'Account Number Null Count',
# # #                         'Status': 'Success' if acct_num_null_count == 0 else 'Fail',
# # #                         'Count': acct_num_null_count,
# # #                         'Entities': 'ACCT' if acct_num_null_count > 0 else None
# # #                     })
# # #                 else:
# # #                     acct_num_null_count = len(acct_df)  # All records invalid if insufficient columns
# # #                     print(f"Fallback: Insufficient columns for Account Number. Counted as null: {acct_num_null_count}")
# # #                     file_issues.append({
# # #                         'INPUT FILE': filename,
# # #                         'Requirement': 'Account Number Null Count',
# # #                         'Count': acct_num_null_count,
# # #                         'Entities': 'ACCT'
# # #                     })

# # #                     new_validation_issues.append({
# # #                         'File': filename,
# # #                         'Requirement': 'Account Number Null Count',
# # #                         'Status': 'Fail',
# # #                         'Count': acct_num_null_count,
# # #                         'Entities': 'ACCT'
# # #                     })
# # #         else:
# # #             # Fallback if no position column
# # #             acct_num_pos = 1
# # #             if acct_df.shape[1] > acct_num_pos:
# # #                 acct_num = acct_df.iloc[:, acct_num_pos].fillna('').astype(str).str.strip()
# # #                 acct_num_null_count = (acct_num == '').sum()
# # #                 print(f"Fallback: Account Number values (index 1): {acct_num.tolist()}")
# # #                 print(f"Fallback: Account Number null count: {acct_num_null_count}")

# # #                 if acct_num_null_count > 0:
# # #                     file_issues.append({
# # #                         'INPUT FILE': filename,
# # #                         'Requirement': 'Account Number Null Count',
# # #                         'Count': acct_num_null_count,
# # #                         'Entities': 'ACCT'
# # #                     })

# # #                 new_validation_issues.append({
# # #                     'File': filename,
# # #                     'Requirement': 'Account Number Null Count',
# # #                     'Status': 'Success' if acct_num_null_count == 0 else 'Fail',
# # #                     'Count': acct_num_null_count,
# # #                     'Entities': 'ACCT' if acct_num_null_count > 0 else None
# # #                 })
# # #             else:
# # #                 acct_num_null_count = len(acct_df)  # All records invalid if insufficient columns
# # #                 print(f"Fallback: Insufficient columns for Account Number. Counted as null: {acct_num_null_count}")
# # #                 file_issues.append({
# # #                     'INPUT FILE': filename,
# # #                     'Requirement': 'Account Number Null Count',
# # #                     'Count': acct_num_null_count,
# # #                     'Entities': 'ACCT'
# # #                 })

# # #                 new_validation_issues.append({
# # #                     'File': filename,
# # #                     'Requirement': 'Account Number Null Count',
# # #                     'Status': 'Fail',
# # #                     'Count': acct_num_null_count,
# # #                     'Entities': 'ACCT'
# # #                 })
# # #     else:
# # #         new_validation_issues.append({
# # #             'File': filename,
# # #             'Requirement': 'Account Number Null Count',
# # #             'Status': 'No Records Found',
# # #             'Count': None,
# # #             'Entities': None
# # #         })

# # #     # ACCT: Statute Expiration Date (calculated using ARACSTATUTEBASEDTE and ARACCNVLPYDTE)
# # #     exp_null_count = 0
# # #     if not acct_df.empty and 'ACCT' in mapping_data:
# # #         acct_sheet = mapping_data['ACCT']
# # #         # Find RM Column or fallback to Description
# # #         rm_column = None
# # #         for col in acct_sheet.columns:
# # #             if 'rm column' in col.lower():
# # #                 rm_column = col
# # #                 break
# # #         if rm_column is None:
# # #             rm_column = 'Description'  # Fallback

# # #         # Find Position column
# # #         position_column = None
# # #         for col in acct_sheet.columns:
# # #             if 'position' in col.lower():
# # #                 position_column = col
# # #                 break

# # #         if position_column is not None:
# # #             # Get positions for ARACSTATUTEBASEDTE and ARACCNVLPYDTE
# # #             statute_mask = acct_sheet[rm_column].str.upper() == 'ARACSTATUTEBASEDTE'
# # #             cnvlpy_mask = acct_sheet[rm_column].str.upper() == 'ARACCNVLPYDTE'

# # #             statute_pos = None
# # #             cnvlpy_pos = None

# # #             if statute_mask.any():
# # #                 statute_pos = int(acct_sheet.loc[statute_mask, position_column].values[0]) - 1
# # #             if cnvlpy_mask.any():
# # #                 cnvlpy_pos = int(acct_sheet.loc[cnvlpy_mask, position_column].values[0]) - 1

# # #             if statute_pos is not None and cnvlpy_pos is not None and statute_pos < acct_df.shape[1] and cnvlpy_pos < acct_df.shape[1]:
# # #                 # Extract dates
# # #                 statute_date = acct_df.iloc[:, statute_pos].fillna('').str.strip()
# # #                 cnvlpy_date = acct_df.iloc[:, cnvlpy_pos].fillna('').str.strip()

# # #                 # Count null/invalid cases
# # #                 empty_mask = (statute_date == '') | (cnvlpy_date == '')
# # #                 exp_null_count = empty_mask.sum()

# # #                 # For non-empty dates, check if they are valid
# # #                 non_empty_mask = ~empty_mask
# # #                 if non_empty_mask.any():
# # #                     try:
# # #                         statute_dt = pd.to_datetime(statute_date[non_empty_mask], errors='coerce')
# # #                         cnvlpy_dt = pd.to_datetime(cnvlpy_date[non_empty_mask], errors='coerce')
# # #                         invalid_date_mask = statute_dt.isna() | cnvlpy_dt.isna()
# # #                         exp_null_count += invalid_date_mask.sum()
# # #                     except Exception as e:
# # #                         print(f"Error parsing dates for {filename}: {e}")
# # #                         exp_null_count += non_empty_mask.sum()  # Treat all as invalid if parsing fails

# # #                 print(f"Statute date (ARACSTATUTEBASEDTE) values: {statute_date.tolist()}")
# # #                 print(f"Cnvlpy date (ARACCNVLPYDTE) values: {cnvlpy_date.tolist()}")
# # #                 print(f"Expiration null count: {exp_null_count}")

# # #                 if exp_null_count > 0:
# # #                     file_issues.append({
# # #                         'INPUT FILE': filename,
# # #                         'Requirement': 'Statute Expiration Date Null Count',
# # #                         'Count': exp_null_count,
# # #                         'Entities': 'ACCT'
# # #                     })

# # #                 new_validation_issues.append({
# # #                     'File': filename,
# # #                     'Requirement': 'Statute Expiration Date Null Count',
# # #                     'Status': 'Success' if exp_null_count == 0 else 'Fail',
# # #                     'Count': exp_null_count,
# # #                     'Entities': 'ACCT' if exp_null_count > 0 else None
# # #                 })
# # #             else:
# # #                 # Fallback to current logic if positions not found or insufficient columns
# # #                 exp_pos = 6
# # #                 if acct_df.shape[1] > exp_pos:
# # #                     exp_date = acct_df.iloc[:, exp_pos].fillna('').astype(str).str.strip()
# # #                     exp_null_count = (exp_date == '').sum()
# # #                     print(f"Fallback: Expiration date values (index 6): {exp_date.tolist()}")
# # #                     print(f"Fallback: Expiration null count: {exp_null_count}")

# # #                     if exp_null_count > 0:
# # #                         file_issues.append({
# # #                             'INPUT FILE': filename,
# # #                             'Requirement': 'Statute Expiration Date Null Count',
# # #                             'Count': exp_null_count,
# # #                             'Entities': 'ACCT'
# # #                         })

# # #                     new_validation_issues.append({
# # #                         'File': filename,
# # #                         'Requirement': 'Statute Expiration Date Null Count',
# # #                         'Status': 'Success' if exp_null_count == 0 else 'Fail',
# # #                         'Count': exp_null_count,
# # #                         'Entities': 'ACCT' if exp_null_count > 0 else None
# # #                     })
# # #                 else:
# # #                     exp_null_count = len(acct_df)  # All records invalid if insufficient columns
# # #                     print(f"Fallback: Insufficient columns for expiration date. Counted as null: {exp_null_count}")
# # #                     file_issues.append({
# # #                         'INPUT FILE': filename,
# # #                         'Requirement': 'Statute Expiration Date Null Count',
# # #                         'Count': exp_null_count,
# # #                         'Entities': 'ACCT'
# # #                     })

# # #                     new_validation_issues.append({
# # #                         'File': filename,
# # #                         'Requirement': 'Statute Expiration Date Null Count',
# # #                         'Status': 'Fail',
# # #                         'Count': exp_null_count,
# # #                         'Entities': 'ACCT'
# # #                     })
# # #         else:
# # #             # Fallback if no position column
# # #             exp_pos = 6
# # #             if acct_df.shape[1] > exp_pos:
# # #                 exp_date = acct_df.iloc[:, exp_pos].fillna('').astype(str).str.strip()
# # #                 exp_null_count = (exp_date == '').sum()
# # #                 print(f"Fallback: Expiration date values (index 6): {exp_date.tolist()}")
# # #                 print(f"Fallback: Expiration null count: {exp_null_count}")

# # #                 if exp_null_count > 0:
# # #                     file_issues.append({
# # #                         'INPUT FILE': filename,
# # #                         'Requirement': 'Statute Expiration Date Null Count',
# # #                         'Count': exp_null_count,
# # #                         'Entities': 'ACCT'
# # #                     })

# # #                 new_validation_issues.append({
# # #                     'File': filename,
# # #                     'Requirement': 'Statute Expiration Date Null Count',
# # #                     'Status': 'Success' if exp_null_count == 0 else 'Fail',
# # #                     'Count': exp_null_count,
# # #                     'Entities': 'ACCT' if exp_null_count > 0 else None
# # #                 })
# # #             else:
# # #                 exp_null_count = len(acct_df)  # All records invalid if insufficient columns
# # #                 print(f"Fallback: Insufficient columns for expiration date. Counted as null: {exp_null_count}")
# # #                 file_issues.append({
# # #                     'INPUT FILE': filename,
# # #                     'Requirement': 'Statute Expiration Date Null Count',
# # #                     'Count': exp_null_count,
# # #                     'Entities': 'ACCT'
# # #                 })

# # #                 new_validation_issues.append({
# # #                     'File': filename,
# # #                     'Requirement': 'Statute Expiration Date Null Count',
# # #                     'Status': 'Fail',
# # #                     'Count': exp_null_count,
# # #                     'Entities': 'ACCT'
# # #                 })
# # #     else:
# # #         new_validation_issues.append({
# # #             'File': filename,
# # #             'Requirement': 'Statute Expiration Date Null Count',
# # #             'Status': 'No Records Found',
# # #             'Count': None,
# # #             'Entities': None
# # #         })

# # #     # TRNH - AFTRTYP (position 4)
# # #     trnh_df = df[df.iloc[:,0]=='TRNH']
# # #     if not trnh_df.empty:
# # #         aftrtyp = trnh_df.iloc[:,3].fillna('').astype(str).str.strip()
# # #         aftrtyp_null_count = (aftrtyp=='').sum()
# # #         new_validation_issues.append({
# # #             'File': filename,
# # #             'Requirement': 'AFTRTYP Null Count',
# # #             'Status': 'Success' if aftrtyp_null_count==0 else 'Fail',
# # #             'Count': aftrtyp_null_count,
# # #             'Entities': 'TRNH' if aftrtyp_null_count>0 else None
# # #         })
# # #     else:
# # #         new_validation_issues.append({
# # #             'File': filename,
# # #             'Requirement': 'AFTRTYP Null Count',
# # #             'Status': 'No Records Found',
# # #             'Count': None,
# # #             'Entities': None
# # #         })

# # #     # PHN - Phone Number (ARPHPHONE) Null Check
# # #     phone_null_count = 0
# # #     phn_df = df[df.iloc[:, 0] == 'PHN']
# # #     if phn_df.empty:
# # #         new_validation_issues.append({
# # #             'File': filename,
# # #             'Requirement': 'Phone Number Null Count',
# # #             'Status': 'No Records Found',
# # #             'Count': None,
# # #             'Entities': None
# # #         })
# # #     elif 'PHN' in mapping_data:
# # #         phn_sheet = mapping_data['PHN']
# # #         # Find Column field (not RM Column or Description)
# # #         column_field = None
# # #         for col in phn_sheet.columns:
# # #             if 'column' in col.lower():
# # #                 column_field = col
# # #                 break
# # #         if column_field is None:
# # #             column_field = 'Column'  # Fallback to exact name

# # #         # Find Position column
# # #         position_column = None
# # #         for col in phn_sheet.columns:
# # #             if 'position' in col.lower():
# # #                 position_column = col
# # #                 break

# # #         if position_column is not None:
# # #             # Get position for ARPHPHONE
# # #             phone_mask = phn_sheet[column_field].str.upper() == 'ARPHPHONE'
# # #             phone_pos = None

# # #             if phone_mask.any():
# # #                 phone_pos = int(phn_sheet.loc[phone_mask, position_column].values[0]) - 1

# # #             if phone_pos is not None and phone_pos < phn_df.shape[1]:
# # #                 # Extract phone number
# # #                 phone_num = phn_df.iloc[:, phone_pos].fillna('').astype(str).str.strip()
# # #                 phone_null_count = (phone_num == '').sum()

# # #                 print(f"Phone Number (ARPHPHONE) values: {phone_num.tolist()}")
# # #                 print(f"Phone Number null count: {phone_null_count}")

# # #                 if phone_null_count > 0:
# # #                     file_issues.append({
# # #                         'INPUT FILE': filename,
# # #                         'Requirement': 'Phone Number Null Count',
# # #                         'Count': phone_null_count,
# # #                         'Entities': 'PHN'
# # #                     })

# # #                 new_validation_issues.append({
# # #                     'File': filename,
# # #                     'Requirement': 'Phone Number Null Count',
# # #                     'Status': 'Success' if phone_null_count == 0 else 'Fail',
# # #                     'Count': phone_null_count,
# # #                     'Entities': 'PHN' if phone_null_count > 0 else None
# # #                 })
# # #             else:
# # #                 # Fallback to position 3 (index 2, typical phone number position in PHN)
# # #                 phone_pos = 2
# # #                 if phn_df.shape[1] > phone_pos:
# # #                     phone_num = phn_df.iloc[:, phone_pos].fillna('').astype(str).str.strip()
# # #                     phone_null_count = (phone_num == '').sum()
# # #                     print(f"Fallback: Phone Number values (index 2): {phone_num.tolist()}")
# # #                     print(f"Fallback: Phone Number null count: {phone_null_count}")

# # #                     if phone_null_count > 0:
# # #                         file_issues.append({
# # #                             'INPUT FILE': filename,
# # #                             'Requirement': 'Phone Number Null Count',
# # #                             'Count': phone_null_count,
# # #                             'Entities': 'PHN'
# # #                         })

# # #                     new_validation_issues.append({
# # #                         'File': filename,
# # #                         'Requirement': 'Phone Number Null Count',
# # #                         'Status': 'Success' if phone_null_count == 0 else 'Fail',
# # #                         'Count': phone_null_count,
# # #                         'Entities': 'PHN' if phone_null_count > 0 else None
# # #                     })
# # #                 else:
# # #                     phone_null_count = len(phn_df)  # All records invalid if insufficient columns
# # #                     print(f"Fallback: Insufficient columns for Phone Number. Counted as null: {phone_null_count}")
# # #                     file_issues.append({
# # #                         'INPUT FILE': filename,
# # #                         'Requirement': 'Phone Number Null Count',
# # #                         'Count': phone_null_count,
# # #                         'Entities': 'PHN'
# # #                     })

# # #                     new_validation_issues.append({
# # #                         'File': filename,
# # #                         'Requirement': 'Phone Number Null Count',
# # #                         'Status': 'Fail',
# # #                         'Count': phone_null_count,
# # #                         'Entities': 'PHN'
# # #                     })
# # #         else:
# # #             # Fallback if no position column
# # #             phone_pos = 2
# # #             if phn_df.shape[1] > phone_pos:
# # #                 phone_num = phn_df.iloc[:, phone_pos].fillna('').astype(str).str.strip()
# # #                 phone_null_count = (phone_num == '').sum()
# # #                 print(f"Fallback: Phone Number values (index 2): {phone_num.tolist()}")
# # #                 print(f"Fallback: Phone Number null count: {phone_null_count}")

# # #                 if phone_null_count > 0:
# # #                     file_issues.append({
# # #                         'INPUT FILE': filename,
# # #                         'Requirement': 'Phone Number Null Count',
# # #                         'Count': phone_null_count,
# # #                         'Entities': 'PHN'
# # #                     })

# # #                 new_validation_issues.append({
# # #                     'File': filename,
# # #                     'Requirement': 'Phone Number Null Count',
# # #                     'Status': 'Success' if phone_null_count == 0 else 'Fail',
# # #                     'Count': phone_null_count,
# # #                     'Entities': 'PHN' if phone_null_count > 0 else None
# # #                 })
# # #             else:
# # #                 phone_null_count = len(phn_df)  # All records invalid if insufficient columns
# # #                 print(f"Fallback: Insufficient columns for Phone Number. Counted as null: {phone_null_count}")
# # #                 file_issues.append({
# # #                     'INPUT FILE': filename,
# # #                     'Requirement': 'Phone Number Null Count',
# # #                     'Count': phone_null_count,
# # #                     'Entities': 'PHN'
# # #                 })

# # #                 new_validation_issues.append({
# # #                     'File': filename,
# # #                     'Requirement': 'Phone Number Null Count',
# # #                     'Status': 'Fail',
# # #                     'Count': phone_null_count,
# # #                     'Entities': 'PHN'
# # #                 })
# # #     else:
# # #         new_validation_issues.append({
# # #             'File': filename,
# # #             'Requirement': 'Phone Number Null Count',
# # #             'Status': 'No Records Found',
# # #             'Count': None,
# # #             'Entities': None
# # #         })

# # #     # PRTY: Both Firstname (col 6) and Lastname (col 8)
# # #     prty_df = df[df.iloc[:, 0] == 'PRTY']
# # #     if not prty_df.empty:
# # #         first_name = prty_df.iloc[:, 5].fillna('').astype(str).str.strip()
# # #         last_name = prty_df.iloc[:, 7].fillna('').astype(str).str.strip()
# # #         both_null = (first_name == '') & (last_name == '')
# # #         both_null_count = both_null.sum()

# # #         if both_null_count > 0:
# # #             file_issues.append({
# # #                 'INPUT FILE': filename,
# # #                 'Requirement': 'Both Firstname and Lastname Null Count',
# # #                 'Count': both_null_count,
# # #                 'Entities': 'PRTY'
# # #             })

# # #         new_validation_issues.append({
# # #             'File': filename,
# # #             'Requirement': 'Both Firstname and Lastname Null Count',
# # #             'Status': 'Success' if both_null_count == 0 else 'Fail',
# # #             'Count': both_null_count,
# # #             'Entities': 'PRTY' if both_null_count > 0 else None
# # #         })
# # #     else:
# # #         new_validation_issues.append({
# # #             'File': filename,
# # #             'Requirement': 'Both Firstname and Lastname Null Count',
# # #             'Status': 'No Records Found',
# # #             'Count': None,
# # #             'Entities': None
# # #         })

# # #     # REQUIRED COLUMNS BASED ON MAPPING
# # #     for entity_name, group in df.groupby(df.iloc[:,0]):
# # #         if entity_name not in mapping_data:
# # #             missing_entities.add(entity_name)
# # #             continue
# # #         sheet_data = mapping_data[entity_name]
# # #         position_column = None
# # #         required_column = None
# # #         for col in sheet_data.columns:
# # #             if 'position' in col.lower():
# # #                 position_column = col
# # #             if 'required?' in col.lower():
# # #                 required_column = col
# # #         if not position_column or not required_column:
# # #             continue
# # #         required_mask = sheet_data[required_column].str.lower()=='yes'
# # #         required_positions = pd.to_numeric(sheet_data.loc[required_mask, position_column], errors='coerce').dropna().astype(int).tolist()
# # #         if not required_positions:
# # #             continue
# # #         entity_cols = group.iloc[:,1:]
# # #         for pos in required_positions:
# # #             if pos > entity_cols.shape[1]:
# # #                 continue
# # #             col_data = entity_cols.iloc[:, pos-1].fillna('').astype(str).str.strip()
# # #             status = 'Fail' if (col_data=='').any() else 'Pass'
# # #             analysis_results.append({
# # #                 'Entity': entity_name,
# # #                 'File': filename,
# # #                 'Column Number': pos,
# # #                 'Status': status
# # #             })

# # #     return analysis_results, missing_entities, file_issues, new_validation_issues

# # # def analyze_required_columns(mapping_file, input_folder, output_file):
# # #     if not os.path.exists(mapping_file):
# # #         print(f"Mapping file {mapping_file} does not exist.")
# # #         return
# # #     if not os.path.exists(input_folder):
# # #         print(f"Input folder {input_folder} does not exist.")
# # #         return
# # #     try:
# # #         mapping_data = pd.read_excel(mapping_file, sheet_name=None, header=1, engine='openpyxl')
# # #         for sheet in mapping_data:
# # #             mapping_data[sheet].columns = mapping_data[sheet].columns.map(str).str.strip()
# # #     except Exception as e:
# # #         print(f"Error reading mapping file {mapping_file}: {e}")
# # #         return

# # #     txt_files = [f for f in os.listdir(input_folder) if f.lower().endswith(".txt")]
# # #     if not txt_files:
# # #         print(f"No .txt files found in {input_folder}.")
# # #         return

# # #     all_analysis_results = []
# # #     all_missing_entities = set()
# # #     all_file_issues = []
# # #     all_new_validation_issues = []

# # #     try:
# # #         with ThreadPoolExecutor(max_workers=os.cpu_count() or 4) as executor:
# # #             futures = [executor.submit(process_single_file, filename, input_folder, mapping_data) for filename in txt_files]
# # #             for future in futures:
# # #                 file_results, file_missing, file_issues, new_issues = future.result()
# # #                 all_analysis_results.extend(file_results)
# # #                 all_missing_entities.update(file_missing)
# # #                 all_file_issues.extend(file_issues)
# # #                 all_new_validation_issues.extend(new_issues)
# # #     except Exception as e:
# # #         print(f"Error during parallel processing: {e}")
# # #         return

# # #     analysis_df = pd.DataFrame(all_analysis_results)
# # #     missing_entities_df = pd.DataFrame(list(all_missing_entities), columns=['Missing Entities in SAAS mapping sheet'])
# # #     file_issues_df = pd.DataFrame(all_file_issues)
# # #     validation_summary_df = pd.DataFrame(all_new_validation_issues)

# # #     if not validation_summary_df.empty and validation_summary_df['Count'].notna().sum()>0 and validation_summary_df['Count'].fillna(0).sum()==0:
# # #         print("All new validations successful! No issues found.")

# # #     try:
# # #         with pd.ExcelWriter(output_file, engine="xlsxwriter") as writer:
# # #             analysis_df.to_excel(writer, sheet_name='Required_Columns_Summary', index=False)
# # #             missing_entities_df.to_excel(writer, sheet_name='Missing_Entities', index=False)
# # #             file_issues_df.to_excel(writer, sheet_name='Frequent_File_Issues', index=False)
# # #             validation_summary_df.to_excel(writer, sheet_name='Validation_Summary', index=False)
# # #         print(f"Success: Analysis results saved to {output_file}")
# # #     except Exception as e:
# # #         print(f"Error writing to {output_file}: {e}")

# # # if __name__ == "__main__":
# # #     mapping_file = "Saas_Legacy_Migration.xlsx"
# # #     input_folder = "Input File"
# # #     output_file = r"C:\Users\AbarnaV\Python\dev-qa-repo2 - Copy\dev-qa-repo\Output Folder\Source_File_Analysis.xlsx"
# # #     start_time = datetime.now()
# # #     analyze_required_columns(mapping_file, input_folder, output_file)
# # #     end_time = datetime.now()
# # #     print(f"Time taken: {end_time - start_time}")



# # import pandas as pd
# # import os
# # import re
# # from concurrent.futures import ThreadPoolExecutor
# # from datetime import datetime

# # def process_single_file(filename, input_folder, mapping_data):
# #     """
# #     Process a single .txt file to analyze required columns, missing entities, and file issues.
# #     Includes new validations with a dedicated summary, dynamically using mapping positions.
# #     """
# #     file_path = os.path.join(input_folder, filename)
# #     analysis_results = []
# #     missing_entities = set()
# #     file_issues = []
# #     new_validation_issues = []

# #     try:
# #         # Use latin1 encoding to handle potential non-UTF-8 characters, skip bad lines
# #         df = pd.read_csv(file_path, sep="|", header=None, dtype=str, engine="python", encoding='latin1', on_bad_lines='skip')
# #     except Exception as e:
# #         return analysis_results, missing_entities, file_issues, new_validation_issues

# #     if df.empty:
# #         return analysis_results, missing_entities, file_issues, new_validation_issues

# #     df.iloc[:, 0] = df.iloc[:, 0].str.strip()
# #     decimal_pattern = re.compile(r'^\.\d+$')

# #     # DECIMAL ISSUE
# #     decimal_issue_count = 0
# #     decimal_issue_entities = set()
# #     for col in df.columns[1:]:
# #         sample_size = min(1000, len(df))
# #         sample_data = df[col].iloc[:sample_size].astype(str)
# #         mask = sample_data.apply(lambda x: bool(decimal_pattern.match(x)) if pd.notna(x) else False)
# #         if mask.any():
# #             decimal_issue_count += df[col].astype(str).apply(lambda x: bool(decimal_pattern.match(x)) if pd.notna(x) else False).sum()
# #             decimal_issue_entities.update(df.iloc[mask.index[mask], 0].dropna().unique())

# #     if decimal_issue_count > 0:
# #         file_issues.append({
# #             'INPUT FILE': filename,
# #             'Requirement': 'Decimal Issues Count',
# #             'Count': decimal_issue_count,
# #             'Entities': ', '.join(decimal_issue_entities) if decimal_issue_entities else None
# #         })

# #     # EMPTY REC_ID
# #     rec_id_empty = df.iloc[:, 1].isna() | (df.iloc[:, 1].str.strip() == '')
# #     record_id_issue_count = rec_id_empty.sum()
# #     if record_id_issue_count > 0:
# #         file_issues.append({
# #             'INPUT FILE': filename,
# #             'Requirement': 'Count of Empty REC_ID',
# #             'Count': record_id_issue_count,
# #             'Entities': None
# #         })

# #     # ITMZ - Itemization Date (position 3)
# #     itmz_df = df[df.iloc[:,0]=='ITMZ']
# #     if not itmz_df.empty:
# #         itmz_date = itmz_df.iloc[:, 2].fillna('').astype(str).str.strip()
# #         itmz_date_null_count = (itmz_date=='').sum()
# #         if itmz_date_null_count > 0:
# #             file_issues.append({
# #                 'INPUT FILE': filename,
# #                 'Requirement': 'Itemization Date Null Count',
# #                 'Count': itmz_date_null_count,
# #                 'Entities': 'ITMZ'
# #             })
# #         new_validation_issues.append({
# #             'File': filename,
# #             'Requirement': 'Itemization Date Null Count',
# #             'Status': 'Success' if itmz_date_null_count==0 else 'Fail',
# #             'Count': itmz_date_null_count,
# #             'Entities': 'ITMZ' if itmz_date_null_count>0 else None
# #         })
# #     else:
# #         new_validation_issues.append({
# #             'File': filename,
# #             'Requirement': 'Itemization Date Null Count',
# #             'Status': 'No Records Found',
# #             'Count': None,
# #             'Entities': None
# #         })

# #     # ACCT: Account_ID invalid (position 2)
# #     acct_df = df[df.iloc[:, 0] == 'ACCT']
# #     if not acct_df.empty:
# #         acct_id = acct_df.iloc[:, 1].fillna('').astype(str).str.strip()
# #         acct_invalid = (acct_id == '') | (acct_id.str.len() < 4)
# #         acct_invalid_count = acct_invalid.sum()

# #         if acct_invalid_count > 0:
# #             file_issues.append({
# #                 'INPUT FILE': filename,
# #                 'Requirement': 'Account_ID Invalid Count (Null or Length <4)',
# #                 'Count': acct_invalid_count,
# #                 'Entities': 'ACCT'
# #             })

# #         new_validation_issues.append({
# #             'File': filename,
# #             'Requirement': 'Account_ID Invalid Count (Null or Length <4)',
# #             'Status': 'Success' if acct_invalid_count == 0 else 'Fail',
# #             'Count': acct_invalid_count,
# #             'Entities': 'ACCT' if acct_invalid_count > 0 else None
# #         })
# #     else:
# #         new_validation_issues.append({
# #             'File': filename,
# #             'Requirement': 'Account_ID Invalid Count (Null or Length <4)',
# #             'Status': 'No Records Found',
# #             'Count': None,
# #             'Entities': None
# #         })

# #     # ACCT: Account Number (ARACCLACCT) Null Check
# #     acct_num_null_count = 0
# #     if not acct_df.empty and 'ACCT' in mapping_data:
# #         acct_sheet = mapping_data['ACCT']
# #         # Find RM Column or fallback to Description
# #         rm_column = None
# #         for col in acct_sheet.columns:
# #             if 'rm column' in col.lower():
# #                 rm_column = col
# #                 break
# #         if rm_column is None:
# #             rm_column = 'Description'  # Fallback

# #         # Find Position column
# #         position_column = None
# #         for col in acct_sheet.columns:
# #             if 'position' in col.lower():
# #                 position_column = col
# #                 break

# #         if position_column is not None:
# #             # Get position for ARACCLACCT
# #             acct_num_mask = acct_sheet[rm_column].str.upper() == 'ARACCLACCT'
# #             acct_num_pos = None

# #             if acct_num_mask.any():
# #                 acct_num_pos = int(acct_sheet.loc[acct_num_mask, position_column].values[0]) - 1

# #             if acct_num_pos is not None and acct_num_pos < acct_df.shape[1]:
# #                 # Extract account number
# #                 acct_num = acct_df.iloc[:, acct_num_pos].fillna('').astype(str).str.strip()
# #                 acct_num_null_count = (acct_num == '').sum()

# #                 if acct_num_null_count > 0:
# #                     file_issues.append({
# #                         'INPUT FILE': filename,
# #                         'Requirement': 'Account Number Null Count',
# #                         'Count': acct_num_null_count,
# #                         'Entities': 'ACCT'
# #                     })

# #                 new_validation_issues.append({
# #                     'File': filename,
# #                     'Requirement': 'Account Number Null Count',
# #                     'Status': 'Success' if acct_num_null_count == 0 else 'Fail',
# #                     'Count': acct_num_null_count,
# #                     'Entities': 'ACCT' if acct_num_null_count > 0 else None
# #                 })
# #             else:
# #                 # Fallback to position 2 (index 1, same as Account_ID)
# #                 acct_num_pos = 1
# #                 if acct_df.shape[1] > acct_num_pos:
# #                     acct_num = acct_df.iloc[:, acct_num_pos].fillna('').astype(str).str.strip()
# #                     acct_num_null_count = (acct_num == '').sum()

# #                     if acct_num_null_count > 0:
# #                         file_issues.append({
# #                             'INPUT FILE': filename,
# #                             'Requirement': 'Account Number Null Count',
# #                             'Count': acct_num_null_count,
# #                             'Entities': 'ACCT'
# #                         })

# #                     new_validation_issues.append({
# #                         'File': filename,
# #                         'Requirement': 'Account Number Null Count',
# #                         'Status': 'Success' if acct_num_null_count == 0 else 'Fail',
# #                         'Count': acct_num_null_count,
# #                         'Entities': 'ACCT' if acct_num_null_count > 0 else None
# #                     })
# #                 else:
# #                     acct_num_null_count = len(acct_df)  # All records invalid if insufficient columns
# #                     file_issues.append({
# #                         'INPUT FILE': filename,
# #                         'Requirement': 'Account Number Null Count',
# #                         'Count': acct_num_null_count,
# #                         'Entities': 'ACCT'
# #                     })

# #                     new_validation_issues.append({
# #                         'File': filename,
# #                         'Requirement': 'Account Number Null Count',
# #                         'Status': 'Fail',
# #                         'Count': acct_num_null_count,
# #                         'Entities': 'ACCT'
# #                     })
# #         else:
# #             # Fallback if no position column
# #             acct_num_pos = 1
# #             if acct_df.shape[1] > acct_num_pos:
# #                 acct_num = acct_df.iloc[:, acct_num_pos].fillna('').astype(str).str.strip()
# #                 acct_num_null_count = (acct_num == '').sum()

# #                 if acct_num_null_count > 0:
# #                     file_issues.append({
# #                         'INPUT FILE': filename,
# #                         'Requirement': 'Account Number Null Count',
# #                         'Count': acct_num_null_count,
# #                         'Entities': 'ACCT'
# #                     })

# #                 new_validation_issues.append({
# #                     'File': filename,
# #                     'Requirement': 'Account Number Null Count',
# #                     'Status': 'Success' if acct_num_null_count == 0 else 'Fail',
# #                     'Count': acct_num_null_count,
# #                     'Entities': 'ACCT' if acct_num_null_count > 0 else None
# #                 })
# #             else:
# #                 acct_num_null_count = len(acct_df)  # All records invalid if insufficient columns
# #                 file_issues.append({
# #                     'INPUT FILE': filename,
# #                     'Requirement': 'Account Number Null Count',
# #                     'Count': acct_num_null_count,
# #                     'Entities': 'ACCT'
# #                 })

# #                 new_validation_issues.append({
# #                     'File': filename,
# #                     'Requirement': 'Account Number Null Count',
# #                     'Status': 'Fail',
# #                     'Count': acct_num_null_count,
# #                     'Entities': 'ACCT'
# #                 })
# #     else:
# #         new_validation_issues.append({
# #             'File': filename,
# #             'Requirement': 'Account Number Null Count',
# #             'Status': 'No Records Found',
# #             'Count': None,
# #             'Entities': None
# #         })

# #     # ACCT: Statute Expiration Date (calculated using ARACSTATUTEBASEDTE and ARACCNVLPYDTE)
# #     exp_null_count = 0
# #     if not acct_df.empty and 'ACCT' in mapping_data:
# #         acct_sheet = mapping_data['ACCT']
# #         # Find RM Column or fallback to Description
# #         rm_column = None
# #         for col in acct_sheet.columns:
# #             if 'rm column' in col.lower():
# #                 rm_column = col
# #                 break
# #         if rm_column is None:
# #             rm_column = 'Description'  # Fallback

# #         # Find Position column
# #         position_column = None
# #         for col in acct_sheet.columns:
# #             if 'position' in col.lower():
# #                 position_column = col
# #                 break

# #         if position_column is not None:
# #             # Get positions for ARACSTATUTEBASEDTE and ARACCNVLPYDTE
# #             statute_mask = acct_sheet[rm_column].str.upper() == 'ARACSTATUTEBASEDTE'
# #             cnvlpy_mask = acct_sheet[rm_column].str.upper() == 'ARACCNVLPYDTE'

# #             statute_pos = None
# #             cnvlpy_pos = None

# #             if statute_mask.any():
# #                 statute_pos = int(acct_sheet.loc[statute_mask, position_column].values[0]) - 1
# #             if cnvlpy_mask.any():
# #                 cnvlpy_pos = int(acct_sheet.loc[cnvlpy_mask, position_column].values[0]) - 1

# #             if statute_pos is not None and cnvlpy_pos is not None and statute_pos < acct_df.shape[1] and cnvlpy_pos < acct_df.shape[1]:
# #                 # Extract dates
# #                 statute_date = acct_df.iloc[:, statute_pos].fillna('').str.strip()
# #                 cnvlpy_date = acct_df.iloc[:, cnvlpy_pos].fillna('').str.strip()

# #                 # Count null/invalid cases
# #                 empty_mask = (statute_date == '') | (cnvlpy_date == '')
# #                 exp_null_count = empty_mask.sum()

# #                 # For non-empty dates, check if they are valid
# #                 non_empty_mask = ~empty_mask
# #                 if non_empty_mask.any():
# #                     try:
# #                         statute_dt = pd.to_datetime(statute_date[non_empty_mask], errors='coerce')
# #                         cnvlpy_dt = pd.to_datetime(cnvlpy_date[non_empty_mask], errors='coerce')
# #                         invalid_date_mask = statute_dt.isna() | cnvlpy_dt.isna()
# #                         exp_null_count += invalid_date_mask.sum()
# #                     except Exception as e:
# #                         exp_null_count += non_empty_mask.sum()  # Treat all as invalid if parsing fails

# #                 if exp_null_count > 0:
# #                     file_issues.append({
# #                         'INPUT FILE': filename,
# #                         'Requirement': 'Statute Expiration Date Null Count',
# #                         'Count': exp_null_count,
# #                         'Entities': 'ACCT'
# #                     })

# #                 new_validation_issues.append({
# #                     'File': filename,
# #                     'Requirement': 'Statute Expiration Date Null Count',
# #                     'Status': 'Success' if exp_null_count == 0 else 'Fail',
# #                     'Count': exp_null_count,
# #                     'Entities': 'ACCT' if exp_null_count > 0 else None
# #                 })
# #             else:
# #                 # Fallback to current logic if positions not found or insufficient columns
# #                 exp_pos = 6
# #                 if acct_df.shape[1] > exp_pos:
# #                     exp_date = acct_df.iloc[:, exp_pos].fillna('').astype(str).str.strip()
# #                     exp_null_count = (exp_date == '').sum()

# #                     if exp_null_count > 0:
# #                         file_issues.append({
# #                             'INPUT FILE': filename,
# #                             'Requirement': 'Statute Expiration Date Null Count',
# #                             'Count': exp_null_count,
# #                             'Entities': 'ACCT'
# #                         })

# #                     new_validation_issues.append({
# #                         'File': filename,
# #                         'Requirement': 'Statute Expiration Date Null Count',
# #                         'Status': 'Success' if exp_null_count == 0 else 'Fail',
# #                         'Count': exp_null_count,
# #                         'Entities': 'ACCT' if exp_null_count > 0 else None
# #                     })
# #                 else:
# #                     exp_null_count = len(acct_df)  # All records invalid if insufficient columns
# #                     file_issues.append({
# #                         'INPUT FILE': filename,
# #                         'Requirement': 'Statute Expiration Date Null Count',
# #                         'Count': exp_null_count,
# #                         'Entities': 'ACCT'
# #                     })

# #                     new_validation_issues.append({
# #                         'File': filename,
# #                         'Requirement': 'Statute Expiration Date Null Count',
# #                         'Status': 'Fail',
# #                         'Count': exp_null_count,
# #                         'Entities': 'ACCT'
# #                     })
# #         else:
# #             # Fallback if no position column
# #             exp_pos = 6
# #             if acct_df.shape[1] > exp_pos:
# #                 exp_date = acct_df.iloc[:, exp_pos].fillna('').astype(str).str.strip()
# #                 exp_null_count = (exp_date == '').sum()

# #                 if exp_null_count > 0:
# #                     file_issues.append({
# #                         'INPUT FILE': filename,
# #                         'Requirement': 'Statute Expiration Date Null Count',
# #                         'Count': exp_null_count,
# #                         'Entities': 'ACCT'
# #                     })

# #                 new_validation_issues.append({
# #                     'File': filename,
# #                     'Requirement': 'Statute Expiration Date Null Count',
# #                     'Status': 'Success' if exp_null_count == 0 else 'Fail',
# #                     'Count': exp_null_count,
# #                     'Entities': 'ACCT' if exp_null_count > 0 else None
# #                 })
# #             else:
# #                 exp_null_count = len(acct_df)  # All records invalid if insufficient columns
# #                 file_issues.append({
# #                     'INPUT FILE': filename,
# #                     'Requirement': 'Statute Expiration Date Null Count',
# #                     'Count': exp_null_count,
# #                     'Entities': 'ACCT'
# #                 })

# #                 new_validation_issues.append({
# #                     'File': filename,
# #                     'Requirement': 'Statute Expiration Date Null Count',
# #                     'Status': 'Fail',
# #                     'Count': exp_null_count,
# #                     'Entities': 'ACCT'
# #                 })
# #     else:
# #         new_validation_issues.append({
# #             'File': filename,
# #             'Requirement': 'Statute Expiration Date Null Count',
# #             'Status': 'No Records Found',
# #             'Count': None,
# #             'Entities': None
# #         })

# #     # TRNH - AFTRTYP (position 4)
# #     trnh_df = df[df.iloc[:,0]=='TRNH']
# #     if not trnh_df.empty:
# #         aftrtyp = trnh_df.iloc[:,3].fillna('').astype(str).str.strip()
# #         aftrtyp_null_count = (aftrtyp=='').sum()
# #         new_validation_issues.append({
# #             'File': filename,
# #             'Requirement': 'AFTRTYP Null Count',
# #             'Status': 'Success' if aftrtyp_null_count==0 else 'Fail',
# #             'Count': aftrtyp_null_count,
# #             'Entities': 'TRNH' if aftrtyp_null_count>0 else None
# #         })
# #     else:
# #         new_validation_issues.append({
# #             'File': filename,
# #             'Requirement': 'AFTRTYP Null Count',
# #             'Status': 'No Records Found',
# #             'Count': None,
# #             'Entities': None
# #         })

# #     # PHN - Phone Number (ARPHPHONE) Null Check
# #     phone_null_count = 0
# #     phn_df = df[df.iloc[:, 0] == 'PHN']
# #     if phn_df.empty:
# #         new_validation_issues.append({
# #             'File': filename,
# #             'Requirement': 'Phone Number Null Count',
# #             'Status': 'No Records Found',
# #             'Count': None,
# #             'Entities': None
# #         })
# #     elif 'PHN' in mapping_data:
# #         phn_sheet = mapping_data['PHN']
# #         # Find Column field (not RM Column or Description)
# #         column_field = None
# #         for col in phn_sheet.columns:
# #             if 'column' in col.lower():
# #                 column_field = col
# #                 break
# #         if column_field is None:
# #             column_field = 'Column'  # Fallback to exact name

# #         # Find Position column
# #         position_column = None
# #         for col in phn_sheet.columns:
# #             if 'position' in col.lower():
# #                 position_column = col
# #                 break

# #         if position_column is not None:
# #             # Get position for ARPHPHONE
# #             phone_mask = phn_sheet[column_field].str.upper() == 'ARPHPHONE'
# #             phone_pos = None

# #             if phone_mask.any():
# #                 phone_pos = int(phn_sheet.loc[phone_mask, position_column].values[0]) - 1

# #             if phone_pos is not None and phone_pos < phn_df.shape[1]:
# #                 # Extract phone number
# #                 phone_num = phn_df.iloc[:, phone_pos].fillna('').astype(str).str.strip()
# #                 phone_null_count = (phone_num == '').sum()

# #                 if phone_null_count > 0:
# #                     file_issues.append({
# #                         'INPUT FILE': filename,
# #                         'Requirement': 'Phone Number Null Count',
# #                         'Count': phone_null_count,
# #                         'Entities': 'PHN'
# #                     })

# #                 new_validation_issues.append({
# #                     'File': filename,
# #                     'Requirement': 'Phone Number Null Count',
# #                     'Status': 'Success' if phone_null_count == 0 else 'Fail',
# #                     'Count': phone_null_count,
# #                     'Entities': 'PHN' if phone_null_count > 0 else None
# #                 })
# #             else:
# #                 # Fallback to position 3 (index 2, typical phone number position in PHN)
# #                 phone_pos = 2
# #                 if phn_df.shape[1] > phone_pos:
# #                     phone_num = phn_df.iloc[:, phone_pos].fillna('').astype(str).str.strip()
# #                     phone_null_count = (phone_num == '').sum()

# #                     if phone_null_count > 0:
# #                         file_issues.append({
# #                             'INPUT FILE': filename,
# #                             'Requirement': 'Phone Number Null Count',
# #                             'Count': phone_null_count,
# #                             'Entities': 'PHN'
# #                         })

# #                     new_validation_issues.append({
# #                         'File': filename,
# #                         'Requirement': 'Phone Number Null Count',
# #                         'Status': 'Success' if phone_null_count == 0 else 'Fail',
# #                         'Count': phone_null_count,
# #                         'Entities': 'PHN' if phone_null_count > 0 else None
# #                     })
# #                 else:
# #                     phone_null_count = len(phn_df)  # All records invalid if insufficient columns
# #                     file_issues.append({
# #                         'INPUT FILE': filename,
# #                         'Requirement': 'Phone Number Null Count',
# #                         'Count': phone_null_count,
# #                         'Entities': 'PHN'
# #                     })

# #                     new_validation_issues.append({
# #                         'File': filename,
# #                         'Requirement': 'Phone Number Null Count',
# #                         'Status': 'Fail',
# #                         'Count': phone_null_count,
# #                         'Entities': 'PHN'
# #                     })
# #         else:
# #             # Fallback if no position column
# #             phone_pos = 2
# #             if phn_df.shape[1] > phone_pos:
# #                 phone_num = phn_df.iloc[:, phone_pos].fillna('').astype(str).str.strip()
# #                 phone_null_count = (phone_num == '').sum()

# #                 if phone_null_count > 0:
# #                     file_issues.append({
# #                         'INPUT FILE': filename,
# #                         'Requirement': 'Phone Number Null Count',
# #                         'Count': phone_null_count,
# #                         'Entities': 'PHN'
# #                     })

# #                 new_validation_issues.append({
# #                     'File': filename,
# #                     'Requirement': 'Phone Number Null Count',
# #                     'Status': 'Success' if phone_null_count == 0 else 'Fail',
# #                     'Count': phone_null_count,
# #                     'Entities': 'PHN' if phone_null_count > 0 else None
# #                 })
# #             else:
# #                 phone_null_count = len(phn_df)  # All records invalid if insufficient columns
# #                 file_issues.append({
# #                     'INPUT FILE': filename,
# #                     'Requirement': 'Phone Number Null Count',
# #                     'Count': phone_null_count,
# #                     'Entities': 'PHN'
# #                 })

# #                 new_validation_issues.append({
# #                     'File': filename,
# #                     'Requirement': 'Phone Number Null Count',
# #                     'Status': 'Fail',
# #                     'Count': phone_null_count,
# #                     'Entities': 'PHN'
# #                 })
# #     else:
# #         new_validation_issues.append({
# #             'File': filename,
# #             'Requirement': 'Phone Number Null Count',
# #             'Status': 'No Records Found',
# #             'Count': None,
# #             'Entities': None
# #         })

# #     # PRTY: Both Firstname (col 6) and Lastname (col 8)
# #     prty_df = df[df.iloc[:, 0] == 'PRTY']
# #     if not prty_df.empty:
# #         first_name = prty_df.iloc[:, 5].fillna('').astype(str).str.strip()
# #         last_name = prty_df.iloc[:, 7].fillna('').astype(str).str.strip()
# #         both_null = (first_name == '') & (last_name == '')
# #         both_null_count = both_null.sum()

# #         if both_null_count > 0:
# #             file_issues.append({
# #                 'INPUT FILE': filename,
# #                 'Requirement': 'Both Firstname and Lastname Null Count',
# #                 'Count': both_null_count,
# #                 'Entities': 'PRTY'
# #             })

# #         new_validation_issues.append({
# #             'File': filename,
# #             'Requirement': 'Both Firstname and Lastname Null Count',
# #             'Status': 'Success' if both_null_count == 0 else 'Fail',
# #             'Count': both_null_count,
# #             'Entities': 'PRTY' if both_null_count > 0 else None
# #         })
# #     else:
# #         new_validation_issues.append({
# #             'File': filename,
# #             'Requirement': 'Both Firstname and Lastname Null Count',
# #             'Status': 'No Records Found',
# #             'Count': None,
# #             'Entities': None
# #         })

# #     # REQUIRED COLUMNS BASED ON MAPPING
# #     for entity_name, group in df.groupby(df.iloc[:,0]):
# #         if entity_name not in mapping_data:
# #             missing_entities.add(entity_name)
# #             continue
# #         sheet_data = mapping_data[entity_name]
# #         position_column = None
# #         required_column = None
# #         for col in sheet_data.columns:
# #             if 'position' in col.lower():
# #                 position_column = col
# #             if 'required?' in col.lower():
# #                 required_column = col
# #         if not position_column or not required_column:
# #             continue
# #         required_mask = sheet_data[required_column].str.lower()=='yes'
# #         required_positions = pd.to_numeric(sheet_data.loc[required_mask, position_column], errors='coerce').dropna().astype(int).tolist()
# #         if not required_positions:
# #             continue
# #         entity_cols = group.iloc[:,1:]
# #         for pos in required_positions:
# #             if pos > entity_cols.shape[1]:
# #                 continue
# #             col_data = entity_cols.iloc[:, pos-1].fillna('').astype(str).str.strip()
# #             status = 'Fail' if (col_data=='').any() else 'Pass'
# #             analysis_results.append({
# #                 'Entity': entity_name,
# #                 'File': filename,
# #                 'Column Number': pos,
# #                 'Status': status
# #             })

# #     return analysis_results, missing_entities, file_issues, new_validation_issues

# # def analyze_required_columns(mapping_file, input_folder, output_file):
# #     if not os.path.exists(mapping_file):
# #         return
# #     if not os.path.exists(input_folder):
# #         return
# #     try:
# #         mapping_data = pd.read_excel(mapping_file, sheet_name=None, header=1, engine='openpyxl')
# #         for sheet in mapping_data:
# #             mapping_data[sheet].columns = mapping_data[sheet].columns.map(str).str.strip()
# #     except Exception as e:
# #         return

# #     txt_files = [f for f in os.listdir(input_folder) if f.lower().endswith(".txt")]
# #     if not txt_files:
# #         return

# #     all_analysis_results = []
# #     all_missing_entities = set()
# #     all_file_issues = []
# #     all_new_validation_issues = []

# #     try:
# #         with ThreadPoolExecutor(max_workers=os.cpu_count() or 4) as executor:
# #             futures = [executor.submit(process_single_file, filename, input_folder, mapping_data) for filename in txt_files]
# #             for future in futures:
# #                 file_results, file_missing, file_issues, new_issues = future.result()
# #                 all_analysis_results.extend(file_results)
# #                 all_missing_entities.update(file_missing)
# #                 all_file_issues.extend(file_issues)
# #                 all_new_validation_issues.extend(new_issues)
# #     except Exception as e:
# #         return

# #     analysis_df = pd.DataFrame(all_analysis_results)
# #     missing_entities_df = pd.DataFrame(list(all_missing_entities), columns=['Missing Entities in SAAS mapping sheet'])
# #     file_issues_df = pd.DataFrame(all_file_issues)
# #     validation_summary_df = pd.DataFrame(all_new_validation_issues)

# #     if not validation_summary_df.empty and validation_summary_df['Count'].notna().sum()>0 and validation_summary_df['Count'].fillna(0).sum()==0:
# #         pass

# #     try:
# #         with pd.ExcelWriter(output_file, engine="xlsxwriter") as writer:
# #             analysis_df.to_excel(writer, sheet_name='Required_Columns_Summary', index=False)
# #             missing_entities_df.to_excel(writer, sheet_name='Missing_Entities', index=False)
# #             file_issues_df.to_excel(writer, sheet_name='Frequent_File_Issues', index=False)
# #             validation_summary_df.to_excel(writer, sheet_name='Validation_Summary', index=False)
# #     except Exception as e:
# #         pass

# # if __name__ == "__main__":
# #     mapping_file = "Saas_Legacy_Migration.xlsx"
# #     input_folder = "Input File"
# #     output_file = r"C:\Users\AbarnaV\Python\dev-qa-repo2 - Copy\dev-qa-repo\Output Folder\Source_File_Analysis.xlsx"
# #     start_time = datetime.now()
# #     analyze_required_columns(mapping_file, input_folder, output_file)
# #     end_time = datetime.now()

# ##above is crt

# import os

# import pandas as pd

# import chardet

# from concurrent.futures import ThreadPoolExecutor, as_completed

# from datetime import datetime
 
 
# def analyze_required_columns(mapping_file, input_folder, output_folder):

#     """

#     High-speed source file analysis with parallel reading,

#     UTF-8/latin-1 fallback, and consolidated Excel output.

#     mapping_file is accepted for compatibility but not used.

#     """

#     _ = mapping_file  # Not used in this optimized version
 
#     # Ensure output folder exists

#     os.makedirs(output_folder, exist_ok=True)
 
#     start_time = datetime.now()

#     print(f"\nStart time: {start_time.strftime('%H:%M:%S')}")
 
#     results = []

#     validation_summary = []
 
#     # Internal function for per-file analysis

#     def analyze_file(file_path):

#         file_name = os.path.basename(file_path)

#         try:

#             # Detect encoding

#             with open(file_path, "rb") as f:

#                 raw_data = f.read(200000)

#                 detected = chardet.detect(raw_data)

#                 encoding = detected.get("encoding") or "utf-8"

#                 if encoding.lower() == "ascii":

#                     encoding = "latin-1"
 
#             # Read safely

#             df = pd.read_csv(

#                 file_path,

#                 sep="|",

#                 encoding=encoding,

#                 on_bad_lines="skip",

#                 low_memory=False,

#             )
 
#             record_count = len(df)

#             col_count = len(df.columns)
 
#             results.append({

#                 "File Name": file_name,

#                 "Record Count": record_count,

#                 "Column Count": col_count,

#             })
 
#             validation_summary.append({

#                 "File": file_name,

#                 "Encoding Used": encoding,

#                 "Status": "Pass",

#                 "Rows Read": record_count,

#                 "Columns": col_count,

#             })
 
#         except Exception as e:

#             validation_summary.append({

#                 "File": file_name,

#                 "Encoding Used": "Unknown",

#                 "Status": "Fail",

#                 "Error": str(e),

#             })
 
#     # Gather all input files

#     all_files = [

#         os.path.join(input_folder, f)

#         for f in os.listdir(input_folder)

#         if f.lower().endswith((".txt", ".csv"))

#     ]
 
#     total_files = len(all_files)

#     print(f"Found {total_files} input files to process...")
 
#     # Process using ThreadPoolExecutor

#     completed = 0

#     with ThreadPoolExecutor(max_workers=8) as executor:

#         futures = {executor.submit(analyze_file, path): path for path in all_files}

#         for future in as_completed(futures):

#             completed += 1

#             if completed % max(1, total_files // 10) == 0 or completed == total_files:

#                 percent = (completed / total_files) * 100

#                 print(f"Progress: {percent:.0f}% ({completed}/{total_files})")
 
#     # Save both results to Excel once at the end

#     result_path = os.path.join(output_folder, "Source_File_Analysis.xlsx")

#     summary_path = os.path.join(output_folder, "Validation_Summary.xlsx")
 
#     pd.DataFrame(results).to_excel(result_path, index=False)

#     pd.DataFrame(validation_summary).to_excel(summary_path, index=False)
 
#     end_time = datetime.now()

#     print(f"\n✅ Source File Analysis saved to: {result_path}")

#     print(f"✅ Validation Summary saved to: {summary_path}")

#     print(f"End time: {end_time.strftime('%H:%M:%S')}")

#     print(f"Time taken: {end_time - start_time}")
 
 
# # -------------------------------------------------------------------

# # Optional standalone run

# # -------------------------------------------------------------------

# if __name__ == "__main__":

#     base_path = r"C:\Users\AbarnaV\Python\dev-qa-repo2 - Copy\dev-qa-repo"

#     input_folder = os.path.join(base_path, "Input File")

#     output_folder = os.path.join(base_path, "Output Folder")

#     mapping_file = os.path.join(base_path, "Mapping.xlsx")  # not used, placeholder
 
#     analyze_required_columns(mapping_file, input_folder, output_folder)

 ## above code is working

	
import os
import re
import chardet
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

# ----------------------
# Configuration
# ----------------------
CHUNKSIZE = 100000  # chunk size to read per pandas.read_csv
MAX_WORKERS = 8     # number of threads
DECIMAL_PATTERN = re.compile(r'^\.\d+$')

# ----------------------
# Helpers
# ----------------------
def detect_encoding(file_path, sample_bytes=200000):
    """Detect encoding using chardet; convert ascii -> latin-1 fallback."""
    try:
        with open(file_path, 'rb') as f:
            raw = f.read(sample_bytes)
        detected = chardet.detect(raw)
        enc = detected.get('encoding') or 'utf-8'
        if enc and enc.lower() == 'ascii':
            return 'latin-1'
        return enc
    except Exception:
        return 'latin-1'

def safe_read_chunked(file_path, encoding):
    """
    Generator yielding DataFrame chunks read from file_path with given encoding.
    Uses engine='python' for robust parsing, on_bad_lines='skip' to handle bad rows.
    """
    try:
        return pd.read_csv(
            file_path,
            sep='|',
            header=None,
            dtype=str,
            encoding=encoding,
            engine='python',
            on_bad_lines='skip',
            chunksize=CHUNKSIZE,
            low_memory=True
        )
    except Exception:
        # final fallback to latin-1
        return pd.read_csv(
            file_path,
            sep='|',
            header=None,
            dtype=str,
            encoding='latin-1',
            engine='python',
            on_bad_lines='skip',
            chunksize=CHUNKSIZE,
            low_memory=True
        )

# ----------------------
# Core per-file processing (chunked)
# ----------------------
def process_single_file(filename, input_folder, mapping_data):
    """
    Process a single .txt file in chunked manner and return:
    (analysis_results, missing_entities, file_issues, new_validation_issues)
    """

    file_path = os.path.join(input_folder, filename)

    # Prepare accumulators
    analysis_results = []         # list of dicts: Entity, File, Column Number, Status
    missing_entities = set()      # set of entity names not found in mapping
    file_issues = []              # list of dicts for Frequent_File_Issues
    new_validation_issues = []    # list of dicts for Validation_Summary rows

    # Precompute mapping required positions per entity for quick checks
    mapping_required_positions = {}  # entity -> list of ints (positions)
    if mapping_data:
        for entity_name, sheet in mapping_data.items():
            pos_col = None
            req_col = None
            for c in sheet.columns:
                if 'position' in c.lower():
                    pos_col = c
                if 'required?' in c.lower():
                    req_col = c
            if pos_col and req_col:
                try:
                    mask = sheet[req_col].astype(str).str.lower() == 'yes'
                    positions = pd.to_numeric(sheet.loc[mask, pos_col], errors='coerce').dropna().astype(int).tolist()
                    if positions:
                        mapping_required_positions[entity_name] = positions
                except Exception:
                    mapping_required_positions[entity_name] = []

    # Per-file state (aggregated across chunks)
    decimal_issue_count = 0
    decimal_issue_entities = set()

    record_id_issue_count = 0

    # ITMZ (pos 3 => col index 2)
    itmz_date_null_count = 0
    itmz_found = False

    # ACCT specifics
    acct_invalid_count = 0
    acct_exp_null_count = 0
    acct_found = False

    # TRNH
    trnh_aftrtyp_null_count = 0
    trnh_found = False

    # CALLH phone pos9 -> index 8
    callh_phone_null_count = 0
    callh_found = False

    # PRTY first+last name checks (col6 idx5, col8 idx7)
    prty_both_null_count = 0
    prty_found = False

    # For mapping-based required column checks:
    # we maintain dict: entity -> pos -> any_empty (True if any empty found)
    required_empty_flags = {}  # entity -> {pos: bool}

    # Start reading file with encoding detection
    encoding = detect_encoding(file_path)
    try:
        chunk_iter = safe_read_chunked(file_path, encoding)
    except Exception as e:
        # reading failed completely
        new_validation_issues.append({
            'File': filename,
            'Requirement': 'File Read',
            'Status': 'Fail',
            'Count': None,
            'Entities': str(e)
        })
        return analysis_results, missing_entities, file_issues, new_validation_issues

    # Iterate chunks
    for chunk in chunk_iter:
        if chunk is None or chunk.shape[0] == 0:
            continue

        # Ensure string dtype and strip entity column
        chunk = chunk.fillna('')  # replace NaN with empty string for checks
        # strip entity column (col 0)
        chunk.iloc[:,0] = chunk.iloc[:,0].astype(str).str.strip()

        # DECIMAL ISSUE: check columns 1..n for values like .12
        for col_idx in chunk.columns[1:]:
            # only sample first up to 1000 rows to speed up (as original)
            sample_size = min(1000, len(chunk))
            sampled = chunk[col_idx].astype(str).iloc[:sample_size]
            mask = sampled.apply(lambda x: bool(DECIMAL_PATTERN.match(x)))
            if mask.any():
                # Count across whole column in chunk
                col_count = chunk[col_idx].astype(str).apply(lambda x: bool(DECIMAL_PATTERN.match(x))).sum()
                decimal_issue_count += int(col_count)
                # collect entities where pattern matches
                # find rows in chunk where this column matches
                matches = chunk.loc[chunk[col_idx].astype(str).apply(lambda x: bool(DECIMAL_PATTERN.match(x))), 0].unique().tolist()
                for e in matches:
                    if e:
                        decimal_issue_entities.add(e)

        # EMPTY REC_ID: second column index 1 is REC_ID
        if 1 in chunk.columns:
            rec_mask = chunk[1].astype(str).str.strip() == ''
            record_id_issue_count += int(rec_mask.sum())
        else:
            # if file has no second column for rows, consider them all as missing REC_ID
            record_id_issue_count += len(chunk)

        # ITMZ
        if 0 in chunk.columns:
            itmz_rows = chunk[chunk[0] == 'ITMZ']
            if not itmz_rows.empty:
                itmz_found = True
                # position 3 => column index 2 (in df headerless)
                if 2 in itmz_rows.columns:
                    itmz_date_null_count += int((itmz_rows[2].astype(str).str.strip() == '').sum())
                else:
                    # all rows missing that column
                    itmz_date_null_count += len(itmz_rows)

        # # ACCT
        # acct_rows = chunk[chunk[0] == 'ACCT'] if 0 in chunk.columns else chunk.iloc[0:0]
        # if not acct_rows.empty:
        #     acct_found = True
        #     # Account ID position 2 -> col index 1
        #     if 1 in acct_rows.columns:
        #         acct_id_series = acct_rows[1].astype(str).str.strip()
        #         acct_invalid_count += int(((acct_id_series == '') | (acct_id_series.str.len() < 4)).sum())
        #     else:
        #         acct_invalid_count += len(acct_rows)
        #     # Statute expiration pos7 -> col index 6
        #     if 6 in acct_rows.columns:
        #         exp_ser = acct_rows[6].astype(str).str.strip()
        #         acct_exp_null_count += int((exp_ser == '').sum())
        #     else:
        #         acct_exp_null_count += len(acct_rows)

                # ACCT

        acct_rows = chunk[chunk[0] == 'ACCT'] if 0 in chunk.columns else chunk.iloc[0:0]

        if not acct_rows.empty:

            acct_found = True

            # Account ID position 5 -> col index 4

            if 4 in acct_rows.columns:

                acct_id_series = acct_rows[4].astype(str).str.strip()

                acct_invalid_count += int(((acct_id_series == '') | (acct_id_series.str.len() < 4)).sum())

            else:

                acct_invalid_count += len(acct_rows)

            # Statute expiration pos7 -> col index 6 (unchanged)

            if 6 in acct_rows.columns:

                exp_ser = acct_rows[6].astype(str).str.strip()

                acct_exp_null_count += int((exp_ser == '').sum())

            else:

                acct_exp_null_count += len(acct_rows)
 

        # TRNH AFTRTYP pos4 -> idx3
        trnh_rows = chunk[chunk[0] == 'TRNH'] if 0 in chunk.columns else chunk.iloc[0:0]
        if not trnh_rows.empty:
            trnh_found = True
            if 3 in trnh_rows.columns:
                trnh_aftrtyp_null_count += int((trnh_rows[3].astype(str).str.strip() == '').sum())
            else:
                trnh_aftrtyp_null_count += len(trnh_rows)

        # CALLH phone pos9 -> idx8
        callh_rows = chunk[chunk[0] == 'CALLH'] if 0 in chunk.columns else chunk.iloc[0:0]
        if not callh_rows.empty:
            callh_found = True
            if 8 in callh_rows.columns:
                callh_phone_null_count += int((callh_rows[8].astype(str).str.strip() == '').sum())
            else:
                callh_phone_null_count += len(callh_rows)

        # PRTY first name col6 idx5 last name col8 idx7
        prty_rows = chunk[chunk[0] == 'PRTY'] if 0 in chunk.columns else chunk.iloc[0:0]
        if not prty_rows.empty:
            prty_found = True
            # prepare series for columns if present
            first_ser = prty_rows[5].astype(str).str.strip() if 5 in prty_rows.columns else pd.Series(['']*len(prty_rows), index=prty_rows.index)
            last_ser = prty_rows[7].astype(str).str.strip() if 7 in prty_rows.columns else pd.Series(['']*len(prty_rows), index=prty_rows.index)
            both_null = ((first_ser == '') & (last_ser == '')).sum()
            prty_both_null_count += int(both_null)

        # Mapping-based required positions: for each entity in mapping_required_positions present in chunk
        if mapping_required_positions:
            # gather unique entity names in chunk
            present_entities = chunk[0].unique().tolist()
            for ent in present_entities:
                if not ent:
                    continue
                if ent not in mapping_required_positions:
                    # track missing entity mapping
                    if ent not in mapping_data:
                        missing_entities.add(ent)
                    continue
                req_positions = mapping_required_positions.get(ent, [])
                if not req_positions:
                    continue
                # initialize flags dict if not exists
                if ent not in required_empty_flags:
                    required_empty_flags[ent] = {p: False for p in req_positions}
                # filter rows for this entity
                mask = chunk[0] == ent
                rows_ent = chunk.loc[mask]
                if rows_ent.empty:
                    continue
                # for each required pos, check column index pos (since df columns: 0 entity, 1 pos1, 2 pos2...)
                for p in req_positions:
                    col_idx = p  # as explained: pos p corresponds to dataframe column index p
                    if col_idx not in rows_ent.columns:
                        # If column not present in this chunk, treat rows as missing for this chunk => mark empty
                        required_empty_flags[ent][p] = True
                    else:
                        # check any empty values in that column for this entity
                        any_empty = (rows_ent[col_idx].astype(str).str.strip() == '').any()
                        if any_empty:
                            required_empty_flags[ent][p] = True

    # ----- after processing all chunks, build outputs -----

    # DECIMAL ISSUE file_issues
    if decimal_issue_count > 0:
        file_issues.append({
            'INPUT FILE': filename,
            'Requirement': 'Decimal Issues Count',
            'Count': decimal_issue_count,
            'Entities': ', '.join(sorted(decimal_issue_entities)) if decimal_issue_entities else None
        })

    # EMPTY REC_ID
    if record_id_issue_count > 0:
        file_issues.append({
            'INPUT FILE': filename,
            'Requirement': 'Count of Empty REC_ID',
            'Count': int(record_id_issue_count),
            'Entities': None
        })

    # ITMZ summary & validation entry
    if itmz_found:
        file_issues.append({
            'INPUT FILE': filename,
            'Requirement': 'Itemization Date Null Count',
            'Count': int(itmz_date_null_count),
            'Entities': 'ITMZ'
        })
        new_validation_issues.append({
            'File': filename,
            'Requirement': 'Itemization Date Null Count',
            'Status': 'Success' if itmz_date_null_count == 0 else 'Fail',
            'Count': int(itmz_date_null_count),
            'Entities': 'ITMZ' if itmz_date_null_count > 0 else None
        })
    else:
        new_validation_issues.append({
            'File': filename,
            'Requirement': 'Itemization Date Null Count',
            'Status': 'No Records Found',
            'Count': None,
            'Entities': None
        })

    # ACCT invalid & exp date
    if acct_found:
        if acct_invalid_count > 0:
            file_issues.append({
                'INPUT FILE': filename,
                'Requirement': 'Account_ID Invalid Count (Null or Length <4)',
                'Count': int(acct_invalid_count),
                'Entities': 'ACCT'
            })
        new_validation_issues.append({
            'File': filename,
            'Requirement': 'Account_ID Invalid Count (Null or Length <4)',
            'Status': 'Success' if acct_invalid_count == 0 else 'Fail',
            'Count': int(acct_invalid_count),
            'Entities': 'ACCT' if acct_invalid_count > 0 else None
        })

        if acct_exp_null_count > 0:
            file_issues.append({
                'INPUT FILE': filename,
                'Requirement': 'Statute Expiration Date Null Count',
                'Count': int(acct_exp_null_count),
                'Entities': 'ACCT'
            })
        new_validation_issues.append({
            'File': filename,
            'Requirement': 'Statute Expiration Date Null Count',
            'Status': 'Success' if acct_exp_null_count == 0 else 'Fail',
            'Count': int(acct_exp_null_count),
            'Entities': 'ACCT' if acct_exp_null_count > 0 else None
        })
    else:
        # no acct records found
        new_validation_issues.append({
            'File': filename,
            'Requirement': 'Account_ID Invalid Count (Null or Length <4)',
            'Status': 'No Records Found',
            'Count': None,
            'Entities': None
        })
        new_validation_issues.append({
            'File': filename,
            'Requirement': 'Statute Expiration Date Null Count',
            'Status': 'No Records Found',
            'Count': None,
            'Entities': None
        })

    # TRNH AFTRTYP
    if trnh_found:
        new_validation_issues.append({
            'File': filename,
            'Requirement': 'AFTRTYP Null Count',
            'Status': 'Success' if trnh_aftrtyp_null_count == 0 else 'Fail',
            'Count': int(trnh_aftrtyp_null_count),
            'Entities': 'TRNH' if trnh_aftrtyp_null_count > 0 else None
        })
    else:
        new_validation_issues.append({
            'File': filename,
            'Requirement': 'AFTRTYP Null Count',
            'Status': 'No Records Found',
            'Count': None,
            'Entities': None
        })

    # CALLH phone
    if callh_found:
        new_validation_issues.append({
            'File': filename,
            'Requirement': 'PhoneNumber Null Count',
            'Status': 'Success' if callh_phone_null_count == 0 else 'Fail',
            'Count': int(callh_phone_null_count),
            'Entities': 'CALLH' if callh_phone_null_count > 0 else None
        })
    else:
        new_validation_issues.append({
            'File': filename,
            'Requirement': 'PhoneNumber Null Count',
            'Status': 'No Records Found',
            'Count': None,
            'Entities': None
        })

    # PRTY both names null
    if prty_found:
        if prty_both_null_count > 0:
            file_issues.append({
                'INPUT FILE': filename,
                'Requirement': 'Both Firstname and Lastname Null Count',
                'Count': int(prty_both_null_count),
                'Entities': 'PRTY'
            })
        new_validation_issues.append({
            'File': filename,
            'Requirement': 'Both Firstname and Lastname Null Count',
            'Status': 'Success' if prty_both_null_count == 0 else 'Fail',
            'Count': int(prty_both_null_count),
            'Entities': 'PRTY' if prty_both_null_count > 0 else None
        })
    else:
        new_validation_issues.append({
            'File': filename,
            'Requirement': 'Both Firstname and Lastname Null Count',
            'Status': 'No Records Found',
            'Count': None,
            'Entities': None
        })

    # Now mapping-based required columns results -> add to analysis_results
    for ent, pos_flags in required_empty_flags.items():
        for pos, any_empty in pos_flags.items():
            status = 'Fail' if any_empty else 'Pass'
            analysis_results.append({
                'Entity': ent,
                'File': filename,
                'Column Number': pos,
                'Status': status
            })

    return analysis_results, missing_entities, file_issues, new_validation_issues

# ----------------------
# Main orchestrator
# ----------------------
def analyze_required_columns(mapping_file, input_folder, output_file):
    """
    Entry function with signature matching your main:
      analyze_required_columns(mapping_file, input_folder, output_file)
    """
    # validate inputs
    if not os.path.exists(mapping_file):
        print(f"Mapping file {mapping_file} does not exist.")
        return
    if not os.path.exists(input_folder):
        print(f"Input folder {input_folder} does not exist.")
        return

    # load mapping data
    try:
        mapping_data = pd.read_excel(mapping_file, sheet_name=None, header=1, engine='openpyxl')
        for sheet in mapping_data:
            mapping_data[sheet].columns = mapping_data[sheet].columns.map(str).str.strip()
    except Exception as e:
        print(f"Error reading mapping file {mapping_file}: {e}")
        return

    # list input txt files
    txt_files = [f for f in os.listdir(input_folder) if f.lower().endswith(".txt")]
    if not txt_files:
        print(f"No .txt files found in {input_folder}.")
        return

    # aggregators
    all_analysis_results = []
    all_missing_entities = set()
    all_file_issues = []
    all_new_validation_issues = []

    # process files in parallel
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(process_single_file, filename, input_folder, mapping_data): filename for filename in txt_files}
        for future in as_completed(futures):
            try:
                file_results, file_missing, file_issues, new_issues = future.result()
            except Exception as e:
                # if a file processing threw unexpected error, log a generic failure entry
                fn = futures[future]
                all_file_issues.append({
                    'INPUT FILE': fn,
                    'Requirement': 'Processing Error',
                    'Count': None,
                    'Entities': None,
                    'Error': str(e)
                })
                continue

            if file_results:
                all_analysis_results.extend(file_results)
            if file_missing:
                all_missing_entities.update(file_missing)
            if file_issues:
                all_file_issues.extend(file_issues)
            if new_issues:
                all_new_validation_issues.extend(new_issues)

    # build DataFrames
    analysis_df = pd.DataFrame(all_analysis_results)
    missing_entities_df = pd.DataFrame(list(all_missing_entities), columns=['Missing Entities in SAAS mapping sheet'])
    file_issues_df = pd.DataFrame(all_file_issues)
    validation_summary_df = pd.DataFrame(all_new_validation_issues)

    # if all validations present and counts show 0, quick message
    if not validation_summary_df.empty and validation_summary_df['Count'].notna().sum() > 0 and validation_summary_df['Count'].fillna(0).sum() == 0:
        print("All new validations successful! No issues found.")

    # write outputs once
    try:
        with pd.ExcelWriter(output_file, engine="xlsxwriter") as writer:
            analysis_df.to_excel(writer, sheet_name='Required_Columns_Summary', index=False)
            missing_entities_df.to_excel(writer, sheet_name='Missing_Entities', index=False)
            file_issues_df.to_excel(writer, sheet_name='Frequent_File_Issues', index=False)
            validation_summary_df.to_excel(writer, sheet_name='Validation_Summary', index=False)
        print(f"Success: Analysis results saved to {output_file}")
    except Exception as e:
        print(f"Error writing to {output_file}: {e}")


# ----------------------
# CLI entrypoint (keeps previous behavior)
# ----------------------
if __name__ == "__main__":
    mapping_file = "Saas_Legacy_Migration.xlsx"
    input_folder = "Input File"
    output_file = "Source_File_Analysis.xlsx"
    start_time = datetime.now()
    analyze_required_columns(mapping_file, input_folder, output_file)
    end_time = datetime.now()
    print(f"Time taken: {end_time - start_time}")

# original code which is from file.

