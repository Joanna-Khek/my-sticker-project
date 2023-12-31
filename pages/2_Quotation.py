import numpy as np
import pandas as pd
import streamlit as st
from src import ui
from src import utils


st.title("Quotation")

type_ = st.selectbox(label="Is this quotation/invoice?", 
                     options=['Quotation', 'Invoice'])

st.subheader("Project Information")
if type_ == "Quotation":
    category = 'QUOTATION'
elif type_ == "Invoice":
    category = 'INVOICE'

dict_project_info = ui.display_project_info_inputs(category)

reference_num = dict_project_info['reference_num']
project_name = dict_project_info['project_name']
client_contact_person = dict_project_info['client_contact_person']
client_company_name = dict_project_info['client_company_name']
client_email = dict_project_info['client_email']



st.subheader('Details')
list_item, list_quantity, list_rate, list_amount, total_quotation_price = ui.display_project_details()

# Save to dataframe
df_items = utils.item_save_to_dataframe(list_item, list_quantity, list_rate, list_amount)
total_quotation_price = np.where(len(str(total_quotation_price).split(".")[1]) == 1,
                                            str(total_quotation_price) + '0', 
                                            total_quotation_price)

st.markdown(f"Total Price: <span style='color:#ff6854;'>${total_quotation_price}</span>", 
            unsafe_allow_html=True)

file_name=f"{reference_num}_({project_name}).pdf".replace(" ", "_")

if st.button("Generate Quotation"):
    with st.status("Generating Quotation...",expanded=True):
        pdf_remote = utils.generate_quotation_invoice(file_name=file_name,
                                                      project_name=project_name,
                                                      client_contact_person=client_contact_person,
                                                      client_company_name=client_company_name,
                                                      client_email=client_email,
                                                      reference_num=reference_num,
                                                      category=category,
                                                      type_=type_,
                                                      df_items=df_items,
                                                      total_price=total_quotation_price,
                                                      )
        

        st.success(f"Quotation Generated for {file_name}")
        
        # Preview Invoice
        st.download_button(
            label="Preview Quotation",
            data=pdf_remote,
            file_name=file_name,
            mime="application/octet-stream")
        
        






            

