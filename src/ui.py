import os
from typing import List, Optional, Literal
import pandas as pd
import streamlit as st

def set_page_config():
    st.set_page_config(
        page_title="My Sticker Project Form",
        layout="wide",
        initial_sidebar_state="expanded",
    )



def set_page_container_style() -> None:
    """Set report container style."""

    margins_css = """
    <style>
        /* Configuration of paddings of containers inside main area */
        .main > div {
            max-width: 100%;
            padding-left: 5%;
        }
        /*Font size in tabs */
        button[data-baseweb="tab"] div p {
            font-size: 18px;
            font-weight: bold;
        }
    </style>
    """
    st.markdown(margins_css, unsafe_allow_html=True)

def show_logo() -> None:
    logo_url = "https://raw.githubusercontent.com/Joanna-Khek/my-sticker-project/main/assets/logo.jpg"
    st.image(logo_url, use_column_width=True)
    st.header("")  # add space between logo and selectors



def display_project_details() -> List:
    """Show quotation details fields

    Returns:
        item (str): description of item
        quantity (int): quantity amount of item
        rate (float): rate of item
        amount (float): quantiy * rate
        total_quotation_price (float): total accumulated amount across all items
    """
    
    total_quotation_price = 0

    list_item = []
    list_quantity = []
    list_rate = []
    list_amount = []

        
    num_items = st.number_input(label="Number of items",
                                min_value=1,
                                key='num_items')


    for i in range(num_items):
        row = st.columns([0.6, 0.1, 0.15, 0.15])
        item = row[0].text_input("Item Description",
                                key=f'item_{i+1}_desc')
        
        quantity = row[1].number_input(label="Qty", 
                                        min_value=1, 
                                        step=1,
                                        key=f'item_{i+1}_quantity')
        
        rate = row[2].number_input(label="Rate ($)",
                                    min_value=1.00,
                                    step=1.00,
                                    format="%.2f",
                                    key=f'item_{i+1}_rate')
        
        amount = row[3].number_input(label="Amount ($)",
                                        value=round(quantity*rate, 2),
                                        disabled=True,
                                        min_value=1.00,
                                        step=1.00,
                                        format="%.2f",
                                        key=f'item_{i+1}_amount',)
        
        total_quotation_price += amount

        list_item.append(item)
        list_quantity.append(quantity)
        list_rate.append(rate)
        list_amount.append(amount)

    return list_item, list_quantity, list_rate, list_amount, total_quotation_price

def display_project_info_inputs(category):
    """Show project information inputs for quotation and invoice tab

    Args:
        project_info (pd.DataFrame): project information of selected quotation number
        reference (bool, optional): Option to refer to past quotation number details. Defaults to False.
    """
   
    # Blank quotation
    category = st.text_input(label="Category", value=category, disabled=True)
    reference_num = st.text_input(label="Reference Number")
    project_name = st.text_input(label="Project Name")
    client_contact_person = st.text_input(label="Client Contact Person")
    client_company_name = st.text_input(label="Client Company Name")
    client_email = st.text_input(label="Client Email")
    
    # Save all the information
    dict_project_info = {'reference_num': reference_num,
                         'category': category,
                         'project_name': project_name,
                         'client_contact_person': client_contact_person,
                         'client_company_name': client_company_name,
                         'client_email': client_email
                         }
    
    return dict_project_info