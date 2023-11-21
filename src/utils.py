from typing import BinaryIO
from datetime import datetime
import numpy as np
import pandas as pd
import streamlit as st
from jinja2 import Environment, select_autoescape, FileSystemLoader
import pdfkit


def generate_quotation_invoice(file_name: str,
                               project_name: str,
                               client_contact_person: str,
                               client_company_name: str,
                               client_email: str,
                               reference_num: str,
                               category: str,
                               type_: str,
                               df_items: pd.DataFrame,
                               total_price: float,
                                ) -> BinaryIO:
    """Input user inputs to the html template and generate a pdf

    Args:
        file_name (str): file name of quotation pdf
        project_name (str): name of project
        client_contact_person (str): name of contact person
        client_company_name (str): company name of client
        client_email (str): email address of client
        quotation_num (str): quotation number
        df_items (pd.DataFrame): quotation items details
        total_quotation_price (float): total price

    Returns:
        BinaryIO: pdf binary from wkhtmltopdf
    """
    
    env = Environment(loader=FileSystemLoader("."), autoescape=select_autoescape())

    template = env.get_template("assets/quotation_template.html")
    html_body = template.render(PROJECT_NAME = project_name,
                                CONTACT_PERSON = client_contact_person,
                                CLIENT_NAME = client_company_name,
                                CLIENT_EMAIL = client_email,
                                CATEGORY = category,
                                TYPE = type_,
                                REFERENCE_NUM = reference_num,
                                ITEMS = df_items,
                                TOTAL_PRICE = total_price,
                                DATE_TODAY = datetime.now().date().strftime(format="%d %B %Y"))



    #path_wkhtmltopdf = r'C:\Users\Joanna\Desktop\Projects\tabistudios-webapp\web_app\wkhtmltopdf.exe'
    #config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    options = {
        'page-size': 'A4',
        'dpi': 800,
        'enable-local-file-access': ''}
    
    
    pdf_remote = pdfkit.from_string(html_body, 
                                    options=options)

    # pdf_local = pdfkit.from_string(html_body,
    #                                 output_path=file_path,
    #                                 configuration=config,
    #                                 options=options)
                    
    # pdf_remote = pdfkit.from_string(html_body,
    #                                 configuration=config,
    #                                 options=options)
    return pdf_remote



def item_save_to_dataframe(list_item: list,
                           list_quantity: list,
                           list_rate: list,
                           list_amount: list) -> pd.DataFrame:
    df = pd.DataFrame()
    df['Item'] = list_item
    df['Quantity'] = list_quantity
    df['Rate'] = list_rate
    df['Amount'] = list_amount

    df.Rate = df.Rate.apply(lambda x: np.where(len(str(x).split(".")[1]) == 1,
                                                str(x) + '0', 
                                                x)) 
    df.Amount = df.Amount.apply(lambda x: np.where(len(str(x).split(".")[1]) == 1,
                                                str(x) + '0', 
                                                x)) 
    return df


def format_total_price(price: float):
    final_price = np.where(len(str(price).split(".")[1]) == 1,
                               str(price) + '0', 
                               price)
    return final_price

