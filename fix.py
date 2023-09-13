import pandas as pd

empresas_df = pd.read_csv('empresas.csv', encoding='utf-8-sig')
empresas_df['Nome Provável da Empresa'] = empresas_df['Nome Provável da Empresa'].apply(lambda x: str(x).strip().strip('.').replace('/', '_'))
cnpj_df = pd.read_csv('valorPRO_empresas.csv', index_col=0, encoding='utf-8-sig')
cnpj_df.index = cnpj_df.index.map(lambda x: str(x).strip().strip('.').replace('/', '_').lower())

def cnpj(x):
    try:
        cnpj_values = cnpj_df.loc[x.lower(), 'cnpj']
        if isinstance(cnpj_values, pd.Series):
            unique_cnpjs = cnpj_values.dropna().unique()
            if unique_cnpjs.size > 0:
                return ' ou '.join(unique_cnpjs.astype(str))
            else:
                return None
        else:
            return cnpj_values
    except:
        return None

unique_names = empresas_df['Nome Provável da Empresa'].unique()
cnpj_mapping = {name: cnpj(name) for name in unique_names}
empresas_df['cnpj_empresa'] = empresas_df['Nome Provável da Empresa'].map(cnpj_mapping)
empresas_df.to_csv('empresas.csv', index=False, encoding='utf-8-sig')

if __name__ == '__main__':
    print(len(empresas_df['cnpj_empresa']) - empresas_df['cnpj_empresa'].isna().sum())
    print(empresas_df['cnpj_empresa'].isna().sum())