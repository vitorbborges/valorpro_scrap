import pdfplumber
import re
import pandas as pd
import numpy as np
from itertools import chain
from multiprocessing import Pool, cpu_count
import os
from tqdm import tqdm

def extract_pdf(path):
    try:
        date_pattern = re.compile(r'\d{2}/\d{2}/\d{4}')
        company_name_pattern = re.compile(r'Empresa:\s*(.*?)\s*Situação')
        with pdfplumber.open(path) as pdf_file:
            first_page_text = pdf_file.pages[0].extract_text()
            date = path.split('__')[1].split('.')[0].replace('_', '/')
            company_name_match = company_name_pattern.search(first_page_text)
            company_name_found = company_name_match.group(1) if company_name_match else None
            tabelas = []
            for page in pdf_file.pages:
                tables = page.extract_tables()
                for table in tables:
                    tabelas.append(table)
            tabelas = list(chain.from_iterable(tabelas))
            tabelas = pd.DataFrame(np.array(tabelas[2:]), columns=tabelas[1])
            tabelas['Data'] = date
            tabelas['Empresa'] = company_name_found
            tabelas = tabelas.apply(lambda x: x.str.replace('\n', ' '))
            return tabelas[['Data', 'Empresa', 'Nome:', 'CNPJ/CPF:', 'Cargo:']]
    except Exception as e:
        print(f"Error processing {path}: {e}")
        return None
    
# def process_pdfs_in_parallel_imap(pdf_paths):
#     with Pool(cpu_count()) as pool:
#         results = list(pool.imap_unordered(extract_pdf, pdf_paths))
#     return pd.concat(results, ignore_index=True)

def process_pdfs_in_parallel_imap(pdf_paths):
    with Pool(cpu_count()) as pool:
        results = list(tqdm(pool.imap_unordered(extract_pdf, pdf_paths), total=len(pdf_paths)))
    return pd.concat(results, ignore_index=True)



# if __name__ == '__main__':
#     directories = [root for root, dirs, files in os.walk('empresas')][1:]
#     for path in tqdm(directories):
#         pdfs = os.listdir(path)
#         pdf_paths = [os.path.join(path, pdf) for pdf in pdfs if pdf.endswith('.pdf')]
#         df_parallel_imap = process_pdfs_in_parallel_imap(pdf_paths)
#         filename = '\\'+path.split('\\')[1]
#         df_parallel_imap.to_csv(f"csvs{filename}.csv", index=False)

if __name__ == '__main__':
    files = [os.path.join(root, name)
            for root, dirs, files in os.walk('empresas')
            for name in files
            if name.endswith((".pdf"))]
    df_parallel_imap = process_pdfs_in_parallel_imap(files)
    df_parallel_imap.to_csv(f"empresas.csv", index=False)




