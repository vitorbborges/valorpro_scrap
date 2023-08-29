# valorpro_scrap

## Overview
The "valorpro_scrap" repository is designed to automate the extraction and organization of economic data from VALORPRO, a premium service by the Brazilian company Valor Econômico. VALORPRO offers real-time information on various economic aspects, combining market speed with the credibility of Valor Econômico. This repository specifically focuses on collecting data related to the composition of company boards.

## Purpose
The primary goal of this repository is to simplify and streamline the process of gathering and analyzing board composition data of companies from VALORPRO. By leveraging the scripts and tools provided, users can efficiently extract, organize, and analyze board composition data, ensuring timely and accurate economic insights.

## Main Components

### 1. automation.py
Automates the process of accessing VALORPRO, reading a list of companies, and downloading board composition data for each company.

### 2. count.py
Provides a count of the total number of companies, the number of companies that have been collected, and other related metrics.

### 3. functions.py
Contains a collection of functions used in the automation process, facilitating interactions with VALORPRO and data extraction.

### 4. pdf_to_csv.py
Extracts board composition data from PDF files and saves it to a CSV format for easier analysis and storage.

## Additional Resources
- **descritivas.html**: Potential descriptive statistics or visualizations.
- **empresas.csv**: List of companies and related data.
- **empresas_faltantes.csv**: Companies missing from the main dataset.
- **valorPRO_empresas.csv**: Data related to VALORPRO companies.
- **valorPRO_empresas.xlsx**: Excel data related to VALORPRO companies.
- **wait_for_this/**: Directory containing images, possibly used for image recognition during automation.

## About VALORPRO
VALORPRO is a comprehensive platform offering exclusive news, real-time quotations from major stock exchanges, a vast database of over 8,000 Brazilian companies, and a suite of tools to support investment decisions. For more details on VALORPRO, visit [VALORPRO's official website](https://valorpro.globo.com/#/).

---

For more details or to contribute, please refer to the individual script files or raise an issue on the repository.

