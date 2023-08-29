import time
import os
import pandas as pd
from unidecode import unidecode
import functions
import numpy as np

def main():

    # open VALORPRO
    functions.open_application()

    # time for the user to put VALORPRO in full screen 
    time.sleep(1)

    try:
        # companies csv
        empresas_df = pd.read_csv('valorPRO_empresas.csv', index_col=0)

        # missing companies list
        empresas = empresas_df.iloc[np.where(np.logical_and(empresas_df['collected'] != 'X', empresas_df['collected'] != 'unavailable'))]
        empresas = empresas.index.to_list()
        empresas = [unidecode(x) for x in empresas]

        # channel directory
        full_path = os.path.abspath('automation.py').split('automation.py')[0].replace('\\', '/') + 'empresas/'

        # loop through the companies and available dates
        for empresa in empresas:

            # create the company directory
            path = f"{full_path}{empresa.strip().strip('.').replace('/', '_')}/"
            if not os.path.exists(path):
                os.mkdir(path.strip())

            # lookup the company and select 'Dados Cadastrais'
            if not functions.lookup_company(empresas_df.loc[empresa,'cnpj']):
                # mark the company as unavailable
                empresas_df.loc[empresa, 'collected'] = 'unavailable'
                empresas_df.to_csv('valorPRO_empresas.csv')
                continue
            
            # select the fields
            functions.select_fields()

            # download the first date
            if not functions.download(path):
                continue

            # loop the available dates
            time.sleep(1)
            last_date = True
            start_time = time.time()
            while last_date:
                time.sleep(1)
                functions.my_click(400, 160)
                time.sleep(0.5)
                # check if the date is the last one
                last_date = functions.read_screen(335, 525, 110, 20).replace('/', '').isdigit()
                functions.my_click(380, 245)
                if not functions.download(path):
                    continue

            for i in range(2, 10):
                time.sleep(1)
                functions.my_click(400, 160)
                time.sleep(0.5)
                functions.my_click(380, (210 + 33*i))
                if not functions.download(path):
                    continue

            # mark the company as collected
            empresas_df.loc[empresa, 'collected'] = 'X'
            empresas_df.to_csv('valorPRO_empresas.csv')

    except Exception as e:
        print(e)
        import count
        # run again
        functions.reset_program()
        main()

if __name__ == '__main__':
    main()