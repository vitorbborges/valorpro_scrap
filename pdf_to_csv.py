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
        company_name_pattern = re.compile(r'Empresa:\s*(.*)\s*Situação', re.DOTALL)
        with pdfplumber.open(path) as pdf_file:
            first_page_text = pdf_file.pages[0].extract_text()
            date = path.split('__')[1].split('.')[0].replace('_', '/')
            assumed_name = path.split('__')[0].split('\\')[-1]
            company_name_match = company_name_pattern.search(first_page_text)
            company_name_found = company_name_match.group(1).replace('\n', '') if company_name_match else None
            tabelas = []
            for page in pdf_file.pages:
                tables = page.extract_tables()
                for table in tables:
                    tabelas.append(table)
            tabelas = list(chain.from_iterable(tabelas))
            tabelas = pd.DataFrame(np.array(tabelas[2:]), columns=tabelas[1])
            tabelas['Data'] = date
            tabelas['Empresa'] = company_name_found
            tabelas['Nome Provável da Empresa'] = assumed_name
            tabelas = tabelas.apply(lambda x: x.str.replace('\n', ' '))
            return tabelas[['Data', 'Empresa', 'Nome Provável da Empresa', 'Nome:', 'CNPJ/CPF:', 'Cargo:']]
    except Exception as e:
        print(f"Error processing {path}: {e}")
        return None

def process_pdfs_in_parallel_imap(pdf_paths):
    with Pool(cpu_count()) as pool:
        results = list(tqdm(pool.imap_unordered(extract_pdf, pdf_paths), total=len(pdf_paths)))
    return pd.concat(results, ignore_index=True)


if __name__ == '__main__':
    files = [os.path.join(root, name)
            for root, dirs, files in os.walk('empresas')
            for name in files
            if name.endswith((".pdf"))]
    df_parallel_imap = process_pdfs_in_parallel_imap(files)
    df_parallel_imap.to_csv(f"empresas.csv", index=False, encoding='utf-8-sig')

    import fix


