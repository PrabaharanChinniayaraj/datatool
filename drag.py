from math import nan
from pickletools import uint2
import pandas as pd
from datetime  import datetime
import streamlit as st
from streamlit_option_menu import option_menu
import warnings
from datetime import timedelta, date
from pandas.tseries.offsets import DateOffset
# from fpdf import FPDF
from st_aggrid import AgGrid
import numpy as np
from st_aggrid.grid_options_builder import GridOptionsBuilder
from collections import Counter
import re
import os
import openpyxl
import requests
import json
import csv
from decimal import Decimal
from sqlalchemy.types import String
import pyodbc
# import xlsxwriter
import hydralit_components as hc
import io
from decimal import Decimal
# import resultcheck as rt
import cv2
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb



st.header("")
hide_st_style= """
            <style>
            footer{visibility:hidden;}
            footer{visibility:hidden;}
            </style>
            """
st.markdown(hide_st_style,unsafe_allow_html=True)





st.markdown(
    """
    <style>
    /* Set the sidebar background color */
    .css-1d391kg {
        background-color: #4CAF50; /* Change this to your desired color */
    }
    </style>
    """,
    unsafe_allow_html=True
)





def apend():
    DF2.to_excel('Source File.xlsx',sheet_name='Sheet1',index=False)









uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx", "xls"])

if uploaded_file is not None:
  
    xls = pd.ExcelFile(uploaded_file)
    

    sheet_names = xls.sheet_names
    sheet_choice = st.selectbox("Select a sheet", sheet_names)
    
    # Input box to enter the number of rows to skip
    skip_rows = st.number_input("Number of rows to skip", min_value=0, value=0, step=1)
    
    # Load the selected sheet with the specified number of rows to skip
    if sheet_choice:
        DF2 = pd.read_excel(xls, sheet_name=sheet_choice, skiprows=skip_rows)
        DF2.to_excel('Source File.xlsx',index=False)
        COLUM=DF2.columns.tolist()
        

    menu_data = [
    {'icon': "fa fa-table", 'label': "Add New Column"},
    {'icon': "fa fa-network-wired", 'label': "Conditional Column"},
    {'icon': "fa fa-shapes", 'label': "Concatenate Columns"},
    {'icon': "fa fa-link", 'label': "Source Mapping"},
    {'icon': "fa fa-calculator", 'label': "Arithmetic Columns"},
    {'icon': "fa fa-fax", 'label': "Reordered Columns"},
    {'icon': "fa fa-credit-card", 'label': "Rename Columns"},
    {'icon': "fa fa-handshake", 'label': "DF-Join"},
    {'icon': "fa fa-filter", 'label': "Filter Row"},
    {'icon': "fa fa-sort", 'label': "Sort Row"},
    {'icon': "fa fa-trash", 'label': "Delete Columns"},
    {'icon': "fas fa-list-alt", 'label': "Aggregate Row"},
    {'icon': "far fa-copy", 'label': "Dataframe Merge"},
    {'icon': "fas fa-theater-masks", 'label': "Remove Duplicates"},
    {'icon': "fa fa-magic", 'label': "Substring"},
    {'icon': "fa fa-bars", 'label': "Formatting"},
    {'icon': "fa fa-calendar", 'label': "Date Function"},
    {'icon': "fa fa-table", 'label': "Split Column"},
    {'icon': "fa fa-fill", 'label': "Fill & Replace"},
    {'icon': "fab fa-first-order", 'label': "Explode"}
]

    
    over_theme = {'txc_inactive': 'white','menu_background':"dodgerblue",'txc_active':'white','option_active':'#1ee94d'}
    font_fmt = {'font-class':'h8','font-size':'100%'}

    menu_id = hc.option_bar(option_definition=menu_data,key='PrimaryOption1',override_theme=over_theme,font_styling=font_fmt,horizontal_orientation=True)









    def newcolumn():
        cols=st.columns(3)
        FCN=cols[0].text_input('Enter Column Name:')
        cols[1].selectbox('OPP:','=')
        F_val=cols[2].selectbox('Value type',["",'Fixed Value','Mapping'])

        if F_val=='Fixed Value':
            F_DTY=cols[2].selectbox('Data type',['string','Date'])
            if F_DTY =='string':
                F_T=cols[2].text_input('Enter the text')
            elif F_DTY == 'Date':
                F_DAT=cols[2].date_input('Enter the Fdate value')
                F_T=F_DAT.strftime('%Y-%m-%d')
                
        elif F_val=='Mapping':
            FDST=cols[2].selectbox('Choose  F-DST- Name',options=['DF2'])
            FCOL=cols[2].selectbox('Choose  F-COL- Name',COLUM)
        Z=st.radio("",options=["Cancel","Preview"])
        if Z=="Preview": 
            if F_val=='Fixed Value':
                DF2[FCN]=F_T
                DF2
                if st.button('SUBMIT'):
                    apend()
                    
            if F_val=='Mapping':
                DF2[FCN]=DF2[FCOL]
                DF2
                if st.button('SUBMIT'):
                    apend()
                    
    if menu_id=='AddNew column':        
        newcolumn() 

    def dropduplicate():
        DF2=pd.read_excel('Source File.xlsx')
        D=st.text_input("Enter The Data Frame Name:")
        DF2=DF2.drop_duplicates()
        a1=st.radio("Do you want Submit:",options=['Cancel','Preview'])
        if a1=='Preview':
            DF2
            if st.button('SUBMIT'):
                apend()
                
    if menu_id=='Remove Duplicates':
        dropduplicate()

    def concatenatecol():
        st.header("Concatenate Columns")
        col1,col2,col3,col4=st.columns(4)
        with col1:
            AD=st.text_input('ENTER THE  CONCATENATE COLUMN NAME:')
        

        with col2:
            AC2=st.selectbox('SELECT COLUMN1 TO CONCATENATE:',COLUM)
            if AC2.isnumeric():
                DF2[AC2]=DF2[AC2].astype(int)
            else:
                pass
        with col3:
            AD2=st.text_input('ENTER THE  STRINGS B/W CONCATINATED COLUMN:')

        with col4:
            AC3=st.selectbox('SELECT COLUMN2 TO CONCATENATE:',COLUM)
            if AC3.isnumeric():
                DF2[AC3]=DF2[AC3].astype(int)
            else:
                pass
            
            ks="DF2['"+AD+"']=DF2['"+AC2+"']+'"+AD2+"'+DF2['"+AC3+"']"

        
        a1=st.radio("Do you want a Preview:",options=['Cancel','Preview'])
        if a1=='Preview':
            DF2[AD]=DF2[AC2].astype(str)+AD2+DF2[AC3].astype(str)
            DF2
        
        if st.button('SUBMIT'):
            apend()
            
        
    if menu_id=="Concatenate Columns":
        concatenatecol()
        
    if menu_id=='Delete Columns':
        st.write("Delete Columns")
        LC=st.multiselect('SELECT COLUMNS TO DELETE:',COLUM)
        
        
        cd1=st.radio('Do you want to delete columns:',['Preview','Cancel'])
        if cd1=='Preview':
            DF2 = DF2.drop(LC, axis=1)
            DF2
        if st.button('SUBMIT'):
            apend()
            


    elif menu_id=="Rename Columns":
        st.write("Columns  Rename")
        C1,C2=st.columns(2)
        with C1:
            C11=st.selectbox("Select Column to Rename:",COLUM)
        with C2:
            C22=st.text_input("Enter the  column name:")
        Z=st.radio("",options=['Preview','Cancel'])
        if Z=='Preview':
            DF2 = DF2.rename(columns={C11:C22})
            DF2
            A="DF2.rename(columns={'"+C11+"':'"+C22+"'})"
        if st.button('SUBMIT'):
            
            apend()
            
    if menu_id=='Arithmetic Columns':
        st.write('Arithmetic Operations')
        C1,C2,C3,C4=st.columns([3,3,1,3])
        with C1:
            C11=st.text_input("Enter the column name:")
        with C2:
            F_val=st.selectbox('Value type',["",'Fixed Value','Mapping'])
            if F_val=='Fixed Value':
                F_DTY1=st.number_input("Enter Value:",step=1.0)
            elif F_val=='Mapping':
                FDST=st.selectbox('Choose  F-DST- Name',options=['DF2'])
                FCOL=st.selectbox('Choose  F-COL- Name',COLUM)
        with C3:
            C22=st.selectbox("operator:",options=['+','-','x','/'])
        with C4:
            F_val2=st.selectbox('Value Type',["",'Fixed Value','Mapping'])

            if F_val2=='Fixed Value':
                F_DTY2=st.number_input("Enter value:")
                
            elif F_val2=='Mapping':
                FDST=st.selectbox('Choose  DST- Name',options=['DF2'])
                FCOL1=st.selectbox('Choose  COL- Name',COLUM)
        Z=st.radio("",options=["Cancel","Preview"])
        if Z=="Preview":
            if F_val=='Fixed Value' and F_val2=='Fixed Value'and C22=='+':
                DF2[C11]=F_DTY1+F_DTY2
                A="DF2['"+C11+"']="+str(F_DTY1)+"+"+str(F_DTY2)
                
                DF2
            if F_val=='Fixed Value' and F_val2=='Fixed Value'and C22=='-':
                DF2[C11]=F_DTY1-F_DTY2
                A="DF2['"+C11+"']="+str(F_DTY1)+"-"+str(F_DTY2)
                DF2
            if F_val=='Fixed Value' and F_val2=='Fixed Value'and C22=='/':
                DF2[C11]=F_DTY1/F_DTY2
                A="DF2['"+C11+"']="+str(F_DTY1)+"/"+str(F_DTY2)
                DF2
            if F_val=='Fixed Value' and F_val2=='Fixed Value'and C22=='x':
                DF2[C11]=F_DTY1*F_DTY2
                A="DF2['"+C11+"']="+str(F_DTY1)+"*"+str(F_DTY2)
                DF2

            if F_val=='Fixed Value' and F_val2=='Mapping'and C22=='+':
                DF2[C11]=F_DTY1+pd.to_numeric(DF2[FCOL1], errors='coerce')
                A="DF2['"+C11+"']="+str(F_DTY1)+"+pd.to_numeric(DF2["+FCOL1+"], errors='coerce')"
                DF2
            if F_val=='Fixed Value' and F_val2=='Mapping'and C22=='-':
                DF2[C11]=F_DTY1-pd.to_numeric(DF2[FCOL1], errors='coerce')
                A="DF2['"+C11+"']="+str(F_DTY1)+"-pd.to_numeric(DF2["+FCOL1+"], errors='coerce')"
                DF2
            if F_val=='Fixed Value' and F_val2=='Mapping'and C22=='/':
                DF2[C11]=F_DTY1/pd.to_numeric(DF2[FCOL1], errors='coerce')
                A="DF2['"+C11+"']="+str(F_DTY1)+"/pd.to_numeric(DF2["+FCOL1+"], errors='coerce')"
                DF2
            if F_val=='Fixed Value' and F_val2=='Mapping'and C22=='x':
                DF2[C11]=F_DTY1*pd.to_numeric(DF2[FCOL1], errors='coerce')
                A="DF2['"+C11+"']="+str(F_DTY1)+"*pd.to_numeric(DF2['"+FCOL1+"'], errors='coerce')"
                DF2


            if F_val=='Mapping' and F_val2=='Fixed Value'and C22=='+':
                DF2[C11]=pd.to_numeric(DF2[FCOL], errors='coerce')+F_DTY2
                A="DF2['"+C11+"']=pd.to_numeric(DF2['"+FCOL+"'], errors='coerce')"+"+"+str(F_DTY2)
                DF2
            if F_val=='Mapping' and F_val2=='Fixed Value'and C22=='-':
                DF2[C11]=pd.to_numeric(DF2[FCOL], errors='coerce')-F_DTY2
                A="DF2['"+C11+"']=pd.to_numeric(DF2['"+FCOL+"'], errors='coerce')"+"-"+str(F_DTY2)
                DF2
            if F_val=='Mapping' and F_val2=='Fixed Value'and C22=='/':
                DF2[C11]=pd.to_numeric(DF2[FCOL], errors='coerce')/F_DTY2
                A="DF2['"+C11+"']=pd.to_numeric(DF2['"+FCOL+"'], errors='coerce')"+"/"+str(F_DTY2)
                DF2
            if F_val=='Mapping' and F_val2=='Fixed Value'and C22=='x':
                DF2[C11]=pd.to_numeric(DF2[FCOL], errors='coerce')*F_DTY2
                A="DF2['"+C11+"']=pd.to_numeric(DF2['"+FCOL+"'], errors='coerce')"+"*"+str(F_DTY2)
                DF2

            if F_val=='Mapping' and F_val2=='Mapping'and C22=='+':
                DF2[C11]=pd.to_numeric(DF2[FCOL], errors='coerce')+pd.to_numeric(DF2[FCOL1], errors='coerce')
                A="DF2['"+C11+"']=pd.to_numeric(DF2['"+FCOL+"'], errors='coerce')+pd.to_numeric(DF2['"+FCOL1+"'], errors='coerce')"
                DF2
            if F_val=='Mapping' and F_val2=='Mapping'and C22=='-':
                DF2[C11]=pd.to_numeric(DF2[FCOL], errors='coerce')-pd.to_numeric(DF2[FCOL1], errors='coerce')
                A="DF2['"+C11+"']=pd.to_numeric(DF2['"+FCOL+"'], errors='coerce')-pd.to_numeric(DF2['"+FCOL1+"'], errors='coerce')"
                DF2
            if F_val=='Mapping' and F_val2=='Mapping'and C22=='/':
                DF2[C11]=pd.to_numeric(DF2[FCOL], errors='coerce')/pd.to_numeric(DF2[FCOL1], errors='coerce')
                A="DF2['"+C11+"']=pd.to_numeric(DF2['"+FCOL+"'], errors='coerce')/pd.to_numeric(DF2['"+FCOL1+"'], errors='coerce')"
                DF2
            if F_val=='Mapping' and F_val2=='Mapping'and C22=='x':
                DF2[C11]=pd.to_numeric(DF2[FCOL], errors='coerce')*pd.to_numeric(DF2[FCOL1], errors='coerce')
                A="DF2['"+C11+"']=pd.to_numeric(DF2['"+FCOL+"'], errors='coerce')*pd.to_numeric(DF2['"+FCOL1+"'], errors='coerce')"
                DF2
            if st.button('SUBMIT'):
                apend()
                
            
    if menu_id=='Reordered Columns':

        column_order=st.multiselect('select columns  to  reorder',COLUM)
        a1=st.radio(" ",options=['Cancel','Preview'],horizontal=True)
        
        if a1=='Preview':
            DF2 = DF2[column_order]
            DF2
            if st.button('SUBMIT'):
                apend()
                


    # if A=='Fixed Value':
        st.write("")
        
        
        def logic(i=0):
            
            
            cols1,cols2,cols3,cols4,cols5=st.columns([2,4,2,4,4]) 
            with cols1:
                
                a5=st.selectbox('DF'+str(i),options=['DF2'])
            with cols2:
                a6=st.selectbox('SELECT  COLUMN'+str(i),COLUM)
            with cols3:
                a7=st.selectbox(""+str(i),["="])
            with cols4:
                a8=st.text_input('ENTER THE VALUE'+str(i))
                
            with cols5:
                
                a1=st.radio("Do you want Continue"+str(i),options=['No','Preview','Yes'],horizontal=True)
            if a1=='Yes':
                
            
                i=i+1
                logic(i)
            if a1=='Preview':
                
                a67="'"+a6+"'"
                DF2[a6]=a8
                DF2
                if st.button('SUBMIT'):
                    apend()
                    
                    
                    

    elif menu_id == 'Source Mapping':
        def source(i=0):
            
            cols1,cols2,cols3,cols4,cols5,cols6=st.columns([1,3,1,1,3,1]) 
            with cols1:
                dst=st.selectbox('DST OP'+str(i),options=['DF2'])
            with cols2:
                col=st.selectbox('COLUMN NAME'+str(i),COLUM)
            with cols3:
                opp=st.selectbox(""+str(i),["="])
            with cols4:
                dstin=st.selectbox('DST IN'+str(i),options=['DF2'])
            with cols5:
                colin=st.selectbox('MAPPING COLUMN'+str(i),COLUM)
            with cols6:
                
                a1=st.radio("Do you want Continue"+str(i),options=['No','Yes','Preview'])
                
            if a1=='Yes':
                i=i+1
                source(i)
            elif a1=='Preview':
                DF2[col]=DF2[colin]
                DF2
                if st.button('SUBMIT'):
                    apend()
                    
    elif menu_id == 'Blank Value':
        def Blank(i=0):
            
                cols1,cols2,cols3,cols4,cols5=st.columns(5) 
                with cols1:
                    DSTOP=st.selectbox('SELECT YOUR DST'+str(i),['DF2'])
                with cols2:
                    DSTOPC=st.selectbox('SELECT THE COLUMN NAME'+str(i),COLUM)
                with cols3:
                    OPP=st.selectbox(""+str(i),["="])
                with cols4:
                    VAL=st.text_input("ENTER "+str(i))
                with cols5:
                        
                        a1=st.radio("Do you want Continue"+str(i),options=['No','Yes','Apply'])
                if a1=='Yes':
                    i=i+1
                    Blank(i)
                elif a1=='Apply':
                    AQ=DSTOP+"="+DSTOP+"['"+DSTOPC+"']"+OPP+"'"+VAL+"'"
                    


        
    ############################################################ SORT ROW #######################################################
        

    if menu_id=='Sort Row':
        DFS=""
        FIELDS=""
        CATEGORYS=""
        ASSIGNS=""
        st.header('SORT ROW')
        def sort1(i=0):
            global DFS
            global FIELDS
            global CATEGORYS
            global ASSIGNS
            global DF2
                
            c1,c2,c3,c4=st.columns([1,3,3,1])
            with c1:
                DST=st.selectbox(' DF:'+str(i),options=['DF2'])
                
            with c2:
                column=st.multiselect('select column  to  Sort'+str(i),COLUM)
                
                sort_string="ASCEND,DESCEND,"*len(column)
            with c3:
                cas=st.multiselect('SORT BY'+str(i),sort_string[:-1].split(","))
                delimiter = ', '

                cas = delimiter.join(cas)
                # st.write(cas)
                
            with c4:
                
                a1=st.radio("Do you want Continue"+str(i),options=['No','Yes','Preview'])
            if a1=='Yes':
                i=i+1
                sort1(i)
            elif a1=='Preview':
                DF2=pd.read_excel('D:/HiSmart/Source File.xlsx')
                
                cas=cas.replace('ASCEND',"True").replace('DESCEND',"False")
                
                
                s1=DST+"=" +DST+".sort_values(by=["+','.join('\'' + str(elem) + '\'' for elem in column)+"],ascending = ["+cas+"])"
                s2="sort_values by("+','.join('\'' + str(elem) + '\'' for elem in column)+") = ["+cas+"])"
                s2=s2.replace("True",'ASCEND').replace("False",'DESCEND')
                
                DF2=DF2.sort_values(by=column,ascending = [eval(x) for x in cas.split(",")])
                DF2
                if st.button('SUBMIT'):
                    apend()
                
                    
                
        sort1()
    ############################################################## FILTER ROW ###################################################################
    if menu_id=='Filter Row':
        A11=""
        B11=""
        C11=""
        D11=""
        F11=""
        E=""
        
        def FILTER(i=0):
            global A11
            global B11
            global C11
            global D11
            global F11
            global E
            
            cols=st.columns([1,1,1,3,1,2,2])
            if i==0:
            
                Fcondition=cols[0].selectbox ("condition"+str(i),["if"])
            else:
                F_Select=cols[1].selectbox('opperator'+str(i),["","and","or"])
                D11=F_Select
            F_DST=cols[2].selectbox('DST'+str(i),options=['DF2'])
            F_COL=cols[3].selectbox('Column'+str(i),COLUM)
            F_OP= cols[4].selectbox('Operator '+str(i),["",'==','>=','<','>','!=',".is",'.not','!','<='])
            F_val=cols[5].selectbox('Value type'+str(i),["",'Fixed Value','Mapping'])

            if F_val=='Fixed Value':
                F_DTY=cols[5].selectbox('Data type'+str(i),['string','Date'])
                if F_DTY =='string':
                    F_T=cols[5].text_input('Enter the text'+str(i))
                elif F_DTY == 'Date':
                    F_DAT=cols[5].date_input('Enter the Fdate value'+str(i))
                    F_T=F_DAT.strftime('%Y-%m-%d')
                    F_T="'"+F_T+"'"
                
            elif F_val=='Mapping':
                FDST=cols[5].selectbox('Choose  F-DST- Name'+str(i),options=['DF2'])
                FCOL=cols[5].selectbox('Choose  F-COL- Name'+str(i),COLUM)
            F_cont=cols[6].radio("Wish to add logic"+str(i),["","-","+",],horizontal=True)
            

            DF2=pd.read_excel('Source File.xlsx')
        
            if i==0 and F_cont=="-" and  F_val=="Fixed Value":
                A11=C11+F_DST+".loc"+"[("+F_DST+"['"+F_COL+"']"+F_OP+F_T+")"
            
                C11=A11
            ######################ok###############
            elif i==0 and F_cont=="-" and F_val=='Mapping':
                A11=C11+F_DST+".loc"+"[("+F_DST+"['"+F_COL+"']"+F_OP+FDST+"['"+FCOL+"'])"
                C11=A11
            #####################ok#####################################
            
            if i==0 and F_cont=="+" and  F_val=="Fixed Value":
                A11=C11+F_DST+".loc"+"[("+F_DST+"['"+F_COL+"']"+F_OP+F_T+")"
                C11=A11
            ######################ok###############
            elif i==0 and F_cont=="+" and F_val=='Mapping':
                A11=C11+F_DST+".loc"+"[("+F_DST+"['"+F_COL+"']"+F_OP+FDST+"['"+FCOL+"'])"
                C11=A11   
            elif D11=="or"and F_val=='Mapping':
                B11=C11+" | "+"("+F_DST+"['"+F_COL+"']"+F_OP+FDST+"['"+FCOL+"'])"
                C11=B11
            elif D11=="and"and F_val=='Mapping':
                B11=C11+" & "+"("+F_DST+"['"+F_COL+"']"+F_OP+FDST+"['"+FCOL+"'])"
                C11=B11
            
            elif D11=="or"and F_val=='Fixed Value':
                B11=C11+" | "+"("+F_DST+"['"+F_COL+"']"+F_OP+F_T+")"
                C11=B11
            elif D11=="and"and F_val=='Fixed Value':
                B11=C11+" & "+"("+F_DST+"['"+F_COL+"']"+F_OP+F_T+")"
                C11=B11
            #######################ok
            if i>=0  and D11=="and"and F_val=='Fixed Value':
                A11=C11
                C11=A11
            elif i>0  and D11=="or"and F_val=='Fixed Value' :
                A11=C11
                C11=A11
            elif i>0  and D11=="or"and F_val=='Fixed Value':
                A11=C11
                C11=A11
            elif i>0  and D11=="and"and F_val=='Fixed Value' :
                A11=C11
                C11=A11

            if i>=0 and D11=="or" and F_val=='Mapping' :
                A11=C11
                C11=A11

            if i>=0 and D11=="and" and F_val=='Mapping' :
                A11=C11
        
        
        
            if i>=0 and D11=="and"and F_cont=="-" and F_val=='Mapping' :
                A11=C11
            if i>=0 and D11=="or"and F_cont=="-" and F_val=='Mapping' :
                A11=C11
                C11=A11

            
                
        
        
        
            
            if F_cont=="+":
                i=i+1
                FILTER(i)
            if F_cont=="-":

                
                if st.button("Preview"):
                    C12=C11+"]"
                    DF2=eval(C12)
                    DF2
                if st.button("Submit"):
                    C12=C11+"]"
                    DF2=eval(C12)
                    DF2.to_excel('D:/HiSmart/Source File.xlsx',sheet_name='Sheet1',index=False)
                    
        FILTER()

    ############################################################ LOOK UP ##################################################################
    
            
    ############################################################### logic ############################################################
    if menu_id == 'Conditional column':
        st.header('LOGIC BUILDER')
        A3=""
        B3=""
        C3=""
        def else4(i=0):
            global A3
            global B3
            # global C3
            cols=st.columns(5)
            if i==0:
                Fcondition=cols[0].selectbox ("select condition"+str(i),["else"])
            
                F1DST=cols[1].selectbox(' DST Name'+str(i),options=['DF2'])

                FOPCV=cols[2].text_input("ColName1"+str(i))
                F_OP= cols[3].selectbox('operator1'+str(i),["","=",'==','>=','<','>','!=',"is",'not','!','<=',""])
                F_val=cols[4].selectbox('value type1'+str(i),["",'Fixed Value',' Mapping'])
                if F_val=='Fixed Value':
                    F_DTY=cols[4].selectbox('data type1'+str(i),['string','Date'])
                    if F_DTY =='string':
                        F_T=cols[4].text_input('enter text1'+str(i))
                    elif F_DTY == 'Date':
                        F_DAT=cols[4].date_input('enter date value1'+str(i))
                        F_T=F_DAT.strftime('%Y-%m-%d')
                        F_T="'"+F_T+"'"
                elif F_val==' Mapping':
                    FDST=cols[4].selectbox('choose DST Name'+str(i),options=['DF2'])
                    FCOL=cols[4].selectbox('choose COL Name'+str(i),COLUM)
            if i== 0 and F_val == "Fixed Value":
                C3=F1DST +"['" +FOPCV +"']"+ F_OP + F_T
            if i== 0 and F_val == ' Mapping':
                C3=F1DST +"['" +FOPCV +"']"+ F_OP + FDST+"['"+FCOL+"']"
            # st.write(C3)

            
            if st.button("Preview"):
                DF2=pd.read_excel('D:/HiSmart/Source File.xlsx')
                exec(C3)
                DF2
            if st.button("Submit"):
                exec(C3)
                apend()
                
                




        A22=""
        B22=""
        C22=""
        D22=""
        F22=""
        G=""
        def elseif(i=0):
            global A22
            global B22
            global C22
            global D22
            global F22
            global G
        
            cols=st.columns(10)
            if i==0:
                Fcondition=cols[0].selectbox ("Condition"+str(i),["else if",""])
            else:
                F_Select=cols[1].selectbox('Opperator'+str(i),["","and","or"])
                D22=F_Select
            F_DST=cols[2].selectbox('DST '+str(i),options=['DF2'])
            F_COL=cols[3].selectbox('Column '+str(i),COLUM)
            F_OP= cols[4].selectbox('Operator '+str(i),["",'==','>=','<','>','!=',"is",'not',' !','<='])
            F_val=cols[5].selectbox('Value type'+str(i),[" ",'Fixed Value','Mapping'])

            if F_val=='Fixed Value':
                F_DTY=cols[5].selectbox('Datatype'+str(i),['string','Date'])
                if F_DTY =='string':
                    F_T=cols[5].text_input('Enter the Text'+str(i))
                elif F_DTY == 'Date':
                    F_DAT=cols[5].date_input('Enter the Fdate Value'+str(i))
                    F_T=F_DAT.strftime('%Y-%m-%d')
                    F_T="'"+F_T+"'"
            elif F_val=='Mapping':
                FDST=cols[5].selectbox('Choose  FDST- Name'+str(i),options=['DF2'])
                FCOL=cols[5].selectbox('Choose  FCOL- Name'+str(i),COLUM)
            F_cont=cols[6].radio(" add logic"+str(i),["-","","+",],horizontal=True)
            if F_cont=="-":

            
            
                FOPCV=cols[8].text_input("Col Name"+str(i))
                F_val1=cols[9].selectbox('Data type '+str(i),["",'Fixed value','Mapping'])
                if F_val1=='Fixed value':
                    F_DTY=cols[9].selectbox(' Data type'+str(i),['String','Date'])
                    if F_DTY =='String': 
                        F_T1=cols[9].text_input('Enter  Text'+str(i))
                    elif F_DTY == 'Date':
                        F_DAT=cols[9].date_input('Enter the Date value'+str(i))
                        F_T1=F_DAT.strftime('%Y-%m-%d')
                elif F_val1=='Mapping':
                    FDS1=cols[9].selectbox('Choose-  FDST- Name'+str(i),options=['DF2'])
                    FCOL1=cols[9].selectbox('Choose-  FCOL- Name'+str(i),COLUM)
            
            

            if i==0 and Fcondition=="else if" and F_val=='Fixed Value' and F_cont== "-" and F_val1 == 'Fixed value':
                A22=F_DST+".loc"+"[("+F_DST+"['"+F_COL+"']"+F_OP+""+F_T+"), "+"'"+FOPCV+"']="+F_T1
                C22=A22
            #####ok######
            if i==0 and Fcondition=="else if" and F_val=='Fixed Value' and F_cont== "-" and F_val1 == 'Mapping':
                A22=F_DST+".loc"+"[("+F_DST+"['"+F_COL+"']"+F_OP+""+F_T+"), "+"'"+FOPCV+"']="+FDS1+"['"+FCOL1+"']"
                C22=A22


            if i==0 and Fcondition=="else if" and F_val=='Mapping' and F_cont== "-" and F_val1 == 'Mapping':
                A22=F_DST+".loc"+"[("+F_DST+"['"+F_COL+"']"+F_OP+"'"+F_OP+FDST+"['"+FCOL+"']"+"'), "+"'"+FOPCV+"']="+FDS1+"['"+FCOL1+"']"
                C22=A22

            if i==0 and Fcondition=="else if" and F_val=='Mapping' and F_cont== "-" and F_val1 == 'Fixed value':
                A22=F_DST+".loc"+"[("+F_DST+"['"+F_COL+"']"+F_OP+"'"+F_OP+FDST+"['"+FCOL+"']"+"'), "+"'"+FOPCV+"']="+F_T1
                C22=A22
            ###############ok#########################################3
        
            elif i>=0 and F_cont=="+" and  F_val=="Fixed Value":
                A22=F_DST+".loc"+"[("+F_DST+"['"+F_COL+"']"+F_OP+""+F_T+")"
                C22=A22
            ######################ok###############
            elif i>=0 and F_cont=="+" and F_val=='Mapping':
                A22=F_DST+".loc"+"[("+F_DST+"['"+F_COL+"']"+F_OP+FDST+"['"+FCOL+"'])"
                C22=A22
            #####################ok#####################################
            elif D22=="or"and F_val=='Mapping':
                B22=C22+" | "+"("+F_DST+"['"+F_COL+"']"+F_OP+FDST+"['"+FCOL+"'])"
                C22=B22
            elif D22=="and"and F_val=='Mapping':
                B22=C22+" & "+"("+F_DST+"['"+F_COL+"']"+F_OP+FDST+"['"+FCOL+"'])"
                C22=B22
            
            elif D22=="or"and F_val=='Fixed Value':
                B22=C22+" | "+"("+F_DST+"['"+F_COL+"']"+F_OP+""+F_T+")"
                C22=B22
            elif D22=="and"and F_val=='Fixed Value':
                B22=C22+" & "+"("+F_DST+"['"+F_COL+"']"+F_OP+""+F_T+")"
                C22=B22
            #######################ok
            if i>=0  and D22=="and"and F_val=='Fixed Value' and F_cont== "-" and F_val1 == 'Fixed value':
                A22=C22+",'"+FOPCV+"']="+F_T1
                C22=A22
            elif i>0  and D22=="or"and F_val=='Fixed Value' and F_cont== "-" and F_val1 == 'Fixed value':
                A22=C22+",'"+FOPCV+"']="+F_T1
                C22=A22
            elif i>0  and D22=="or"and F_val=='Fixed Value' and F_cont== "-" and F_val1 == 'Mapping':
                A22=C22+",'"+FOPCV+"']="+FDS1+"['"+FCOL1+"']"
                C22=A22
            elif i>0  and D22=="and"and F_val=='Fixed Value' and F_cont== "-" and F_val1 == 'Mapping':
                A22=C22+",'"+FOPCV+"']="+FDS1+"['"+FCOL1+"']"
                C22=A22

            if i>=0 and D22=="or"and F_cont=="-" and F_val=='Mapping' and F_val1 == 'Fixed value':
                A22=C22+",'"+FOPCV+"']="+F_T1
                C22=A22

            if i>=0 and D22=="and"and F_cont=="-" and F_val=='Mapping' and F_val1 == 'Fixed value':
                A22=C22+",'"+FOPCV+"']="+F_T1
                C22=A22
        
        
        
            if i>=0 and D22=="and"and F_cont=="-" and F_val=='Mapping' and F_val1 == 'Mapping':
                A22=C22+",'"+FOPCV+"']="+FDS1+"['"+FCOL1+"']"
                C22=A22
            if i>=0 and D22=="or"and F_cont=="-" and F_val=='Mapping' and F_val1 == 'Mapping':
                A22=C22+",'"+FOPCV+"']="+FDS1+"['"+FCOL1+"']"
                C22=A22
            
            
            if F_cont=="+":
                i=i+1
                elseif(i)
            if F_cont=="-":
                c1,C3=st.columns(2)
                with c1:
                    if st.button("Preview"):
                        exec(C22)
                        DF2
                with C3:
                    if st.button("Submit"):
                        exec(C22)
                        apend()
                        
            
        A11=""
        B11=""
        C11=""
        D11=""
        F11=""
        E=""
        def IF1(i=0):
            global A11
            global B11
            global C11
            global D11
            global F11
            global E
        
            cols=st.columns(10)
            if i==0:
            
                Fcondition=cols[0].selectbox ("condition"+str(i),["if"])
            else:
                F_Select=cols[1].selectbox('opperator'+str(i),["","and","or"])
                D11=F_Select
            F_DST=cols[2].selectbox('DST'+str(i),options=["DF2"])
            F_COL=cols[3].selectbox('Column'+str(i),COLUM)
            F_OP= cols[4].selectbox('Operator '+str(i),["",'==','>=','<','>','!=',".is",'.not','!','<='])
            F_val=cols[5].selectbox('Value type'+str(i),["",'Fixed Value','Mapping'])

            if F_val=='Fixed Value':
                F_DTY=cols[5].selectbox('Data type'+str(i),['string','Date'])
                if F_DTY =='string':
                    F_T=cols[5].text_input('Enter the text'+str(i))
                elif F_DTY == 'Date':
                    F_DAT=cols[5].date_input('Enter the Fdate value'+str(i))
                    F_T=F_DAT.strftime('%Y-%m-%d')
                    F_T="'"+F_T+"'"
            elif F_val=='Mapping':
                FDST=cols[5].selectbox('Choose  F-DST- Name'+str(i),options=['DF2'])
                FCOL=cols[5].selectbox('Choose  F-COL- Name'+str(i),COLUM)
            F_cont=cols[6].radio("Wish to add logic"+str(i),["","-","+",],horizontal=True)
            if F_cont=="-":

            
            
                FOPCV=cols[8].text_input("ColName"+str(i))
                F_val1=cols[9].selectbox('Data type'+str(i),["",'Fixed value','Mapping'])
                if F_val1=='Fixed value':
                    F_DTY=cols[9].selectbox('Data type'+str(i),['String','Date'])
                    if F_DTY =='String':
                        F_T1=cols[9].text_input('Enter  text'+str(i))
                    elif F_DTY == 'Date':
                        F_DAT=cols[9].date_input('Enter the date value'+str(i))
                        F_T1=F_DAT.strftime('%Y-%m-%d')
                elif F_val1=='Mapping':
                    FDS1=cols[9].selectbox('Choose  FDST- Name'+str(i),options=['DF2'])
                    FCOL1=cols[9].selectbox('Choose  FCOL- Name'+str(i),COLUM)
            

            if i==0 and Fcondition=="if" and F_val=='Fixed Value' and F_cont== "-" and F_val1 == 'Fixed value':
                A11=F_DST+".loc"+"[("+F_DST+"['"+F_COL+"']"+F_OP+F_T+"), "+"'"+FOPCV+"']="+F_T1
                C11=A11
            #####ok######
            if i==0 and Fcondition=="if" and F_val=='Fixed Value' and F_cont== "-" and F_val1 == 'Mapping':
                A11=F_DST+".loc"+"[("+F_DST+"['"+F_COL+"']"+F_OP+F_T+"), "+"'"+FOPCV+"']="+FDS1+"['"+FCOL1+"']"
                C11=A11


            if i==0 and Fcondition=="if" and F_val=='Mapping' and F_cont== "-" and F_val1 == 'Mapping':
                A11=F_DST+".loc"+"[("+F_DST+"['"+F_COL+"']"+F_OP+"'"+F_OP+FDST+"['"+FCOL+"']"+"'), "+"'"+FOPCV+"']="+FDS1+"['"+FCOL1+"']"
                C11=A11

            if i==0 and Fcondition=="if" and F_val=='Mapping' and F_cont== "-" and F_val1 == 'Fixed value':
                A11=F_DST+".loc"+"[("+F_DST+"['"+F_COL+"']"+F_OP+"'"+F_OP+FDST+"['"+FCOL+"']"+"'), "+"'"+FOPCV+"']="+F_T1
                C11=A11
            ###############ok#########################################3
        
            elif i==0 and F_cont=="+" and  F_val=="Fixed Value":
                A11=C11+F_DST+".loc"+"[("+F_DST+"['"+F_COL+"']"+F_OP+F_T+")"
                C11=A11
            ######################ok###############
            elif i==0 and F_cont=="+" and F_val=='Mapping':
                A11=C11+F_DST+".loc"+"[("+F_DST+"['"+F_COL+"']"+F_OP+FDST+"['"+FCOL+"'])"
                C11=A11
            #####################ok#####################################
            elif D11=="or"and F_val=='Mapping':
                B11=C11+" | "+"("+F_DST+"['"+F_COL+"']"+F_OP+FDST+"['"+FCOL+"'])"
                C11=B11
            elif D11=="and"and F_val=='Mapping':
                B11=C11+" & "+"("+F_DST+"['"+F_COL+"']"+F_OP+FDST+"['"+FCOL+"'])"
                C11=B11
            
            elif D11=="or"and F_val=='Fixed Value':
                B11=C11+" | "+"("+F_DST+"['"+F_COL+"']"+F_OP+F_T+")"
                C11=B11
            elif D11=="and"and F_val=='Fixed Value':
                B11=C11+" & "+"("+F_DST+"['"+F_COL+"']"+F_OP+F_T+")"
                C11=B11
            #######################ok
            if i>=0  and D11=="and"and F_val=='Fixed Value' and F_cont== "-" and F_val1 == 'Fixed value':
                A11=C11+",'"+FOPCV+"']="+F_T1
                C11=A11
            elif i>0  and D11=="or"and F_val=='Fixed Value' and F_cont== "-" and F_val1 == 'Fixed value':
                A11=C11+",'"+FOPCV+"']="+F_T1
                C11=A11
            elif i>0  and D11=="or"and F_val=='Fixed Value' and F_cont== "-" and F_val1 == 'Mapping':
                A11=C11+",'"+FOPCV+"']="+FDS1+"['"+FCOL1+"']"
                C11=A11
            elif i>0  and D11=="and"and F_val=='Fixed Value' and F_cont== "-" and F_val1 == 'Mapping':
                A11=C11+",'"+FOPCV+"']="+FDS1+"['"+FCOL1+"']"
                C11=A11

            if i>=0 and D11=="or"and F_cont=="-" and F_val=='Mapping' and F_val1 == 'Fixed value':
                A11=C11+",'"+FOPCV+"']="+F_T1
                C11=A11

            if i>=0 and D11=="and"and F_cont=="-" and F_val=='Mapping' and F_val1 == 'Fixed value':
                A11=C11+",'"+FOPCV+"']="+F_T1
                C11=A11
        
            if i>=0 and D11=="and"and F_cont=="-" and F_val=='Mapping' and F_val1 == 'Mapping':
                A11=C11+",'"+FOPCV+"']="+FDS1+"['"+FCOL1+"']"
                C11=A11
            if i>=0 and D11=="or"and F_cont=="-" and F_val=='Mapping' and F_val1 == 'Mapping':
                A11=C11+",'"+FOPCV+"']="+FDS1+"['"+FCOL1+"']"
                C11=A11
            
            if F_cont=="+":
                i=i+1
                IF1(i)
            if F_cont=="-":
                
                c1,C3=st.columns(2)
                with c1:
                    if st.button("Preview"):
                        
                        exec(C11)
                        st.write(C11)
                        DF2
                        
                with C3:
                    if st.button("Submit"):
                        exec(C11)
                        apend()
        a=st.radio('Select:',options=['if','elseif','else'],horizontal=True)          
        if a=='if':
            IF1()
            
        if a=='elseif':
            elseif()
        if a== 'else':
            else4()
    ########################################## aggregate    ##################################################################
    elif menu_id== "Aggregate Row":
        
        B66=""
        C66=""
        D66=""
        F66=""
        E=""
        def AGG(i=0):

            global B66
            global C66
            global D66
            global F66
            global E

            cols=st.columns(4)
            if i==0:
            
                Fcondition=cols[0].multiselect ("select columns to Group by"+str(i),COLUM)
                Fcondition1=','.join('\'' + str(elem) + '\'' for elem in Fcondition)
                F66=Fcondition1

            else:
                F_Select=cols[1].selectbox('Select Aggregate Function'+str(i),["","sum","min",'max','first','last','count','unique count'])
                D66=F_Select
                result1 = list((Counter(COLUM) - Counter(F66)).elements())
                result = [*set(result1)]
                    
                AGGC=cols[2].multiselect ("select columns to Aggregate"+D66+"FN"+str(i),result)
                AGGC=','.join('\'' + str(elem) + '\'' for elem in AGGC)
            
            
            F_cont=cols[3].radio("Wish to add another aggregate function"+str(i),["","-","+",],horizontal=True)
            
            ###############ok#########################################3
            
            if i==0:
                C66="DF2.groupby(["+F66+"]).agg({"
            
            
            #####################ok#####################################
            elif i>=0 and D66=="sum":
                if i==1:
                    B66=C66+AGGC+":sum"
                else:
                    B66=C66+" , "+AGGC+":sum"
                C66=B66
            elif i>=0 and D66=="max":
                if i==1:
                    B66=C66+AGGC+":'max'"
                else:
                    B66=C66+" , "+AGGC+":'max'"
                C66=B66
            elif i>=0 and D66=="min":
                if i==1:
                    B66=C66+AGGC+":'min'"
                else:
                    B66=C66+" , "+AGGC+":'min'"
                C66=B66
            elif i>=0 and D66=="first":
                if i==1:
                    B66=C66+AGGC+":'"+"first'"
                else:
                    B66=C66+" , "+AGGC+":'first'"
                C66=B66
            elif i>=0 and D66=="last":
                if i==1:
                    B66=C66+AGGC+":'last'"
                else:
                    B66=C66+" , "+AGGC+":'last'"
                C66=B66
            elif i>=0 and D66=="count":
                if i==1:
                    B66=C66+AGGC+":'count'"
                else:
                    B66=C66+" , "+AGGC+":'count'"
                C66=B66
            elif i>=0 and D66=='unique count':
                if i==1:
                    B66=C66+AGGC+":'nunique'"
                else:
                    B66=C66+" , "+AGGC+":'nunique'"
                C66=B66
            
            


            
            if F_cont=="+":
                i=i+1
                AGG(i)
            if F_cont=="-":
                
                
                if st.button("Preview"):
                    DF2=pd.read_excel('Source File.xlsx')
                    DF2.fillna(0, inplace=True)
                    DF2=eval(C66+"},skipna=False)")
                    DF2
                    
                    
                if st.button("Submit"):
                    DF2=pd.read_excel('D:/HiSmart/Source File.xlsx')
                    DF2.fillna(0, inplace=True)
                    DF2=eval(C66+"},skipna=False)")
                    
                    DF2.to_excel('Source File.xlsx',sheet_name='Sheet1')
                    


        AGG()

    #########################################  DATAFRAME MERGE ########################################################
    

############################################################################################################
    def Explode():
        SELECTCOL= st.selectbox("SELECT THE COLUMN TO EXPLODE",COLUM)
        
        S=st.text_input("ENTER DELIMITER")
        # DF2=DF2.assign(SELECTCOL=DF2.Units.str.split(','))
        DF2[SELECTCOL]=DF2[SELECTCOL].str.strip('[]').str.split(S)
        C="DF2['"+SELECTCOL+"']="+"DF2['"+SELECTCOL+"'].str.strip('[]').str.split("+S+")"
        DF3=DF2.explode(SELECTCOL)
    
        
        Z=st.radio("",options=['','Preview'])
        if Z=='Preview':
            DF3.to_excel('D:/HiSmart/Source File.xlsx',sheet_name='Sheet1',index=False)
            DF3
        if st.button('SUBMIT'):
            DF3.to_excel('D:/HiSmart/Source File.xlsx',sheet_name='Sheet1',index=False)
        else:
            st.write('Press Submit to Complete the Process')
        
        
    ### FILL COLUMN ###
    def FILL():
        y=st.select_slider('SELECT',options=["Replae Entire String","Replace Matching character","Fill"])
        if y=="Replae Entire String":
            col1, col2, col3 = st.columns(3)
            with col1:
                SELECTCOL= st.selectbox("SELECT THE COLUMN TO REPLACE",COLUM)
            with col2:
                N=st.text_input('Find the value to replace')
            with col3:
                O=st.text_input('Enter the replace value')
            grade_mapping = {N: O}
            DF2[SELECTCOL] = DF2[SELECTCOL].replace(grade_mapping)
            A="DF2['"+SELECTCOL+"'] = DF2['"+SELECTCOL+"'].replace(grade_mapping)"
            
            
            Z=st.radio("",options=['','Preview'])
            if Z=='Preview':
                
                AgGrid(DF2)
            if st.button('SUBMIT'):
            
                apend()
            else:
                st.write('Press Submit to Complete the Process')
            
                
        if y=="Replace Matching character":
            col1, col2, col3 = st.columns(3)
            with col1:
                SELECTCOL= st.selectbox("SELECT THE COLUMN TO REPLACE",COLUM)
            with col2:
                N=st.text_input('Find the value to replace')
            with col3:
                O=st.text_input('Enter the replace value')
            
            DF2[SELECTCOL] = DF2[SELECTCOL].str.replace(N, O)
            
            
            Z=st.radio("",options=['','Preview'])
            if Z=='Preview':
            
                AgGrid(DF2)
            if st.button('SUBMIT'):
                
                apend()
            
            
            

        if y=="Fill":
            col1, col2, col3,col4 = st.columns(4)
            with col1:
                st.write('')
            with col2:
                st.header('FILL')
            with col3:
                SELECTCOL= st.selectbox("SELECT THE COLUMN TO FILL",COLUM)
            with col4:
                FILLTYPE=st.selectbox("Select Fill Method:",options=['ffill','bfill','pad'])
    
            
            
            Z=st.radio("",options=['','Preview'])
            if Z=='Preview':
                DF2[SELECTCOL] = DF2[SELECTCOL].fillna(method=FILLTYPE)
                DF2
            if st.button('SUBMIT'):
                
                apend()
                DF='DF2'
                
    #################################################################################################################################
    # SPLIT COLUMN FUNCTION #
    def splitcolumn():
        st.header("Split Columns")  
        col1, col2, col3 = st.columns(3)
        with col1:
            SELECTCOL= st.selectbox("SELECT THE COLUMN TO SPLIT",COLUM)
        with col2:
            B=st.text_input("ENTER THE DELIMITER:")
        with col3:
            D=(st.text_input("ENTER THE COLUMN NAME:"))
        
            result = D.split(",")
            
            DF2[result] = DF2[SELECTCOL].str.split(B,expand=True)
            
            
            
            Z=st.radio("",options=['','Preview'])
            if Z=='Preview':
                apend()
                AgGrid(DF2.head(5))
            if st.button('SUBMIT'):
                apend()
                
    #########################################################################################################################################
    # FORMATTING FUNCTION #
    def formatting():
        A=""
        st.header("Formatting")  
        SELECTCOL= st.selectbox("SELECT  COLUMN TO CHANGE CASE",COLUM)
        CASE=st.selectbox("Select case to convert:",options=["upper","lower","Capitalize Each Word"])
    
        if CASE=="upper":
            DF2[SELECTCOL] = DF2[SELECTCOL].str.upper()
            
            
        if CASE=="Capitalize Each Word":
            DF2[SELECTCOL] = DF2[SELECTCOL].str.title() 
        
        
        if CASE=="lower":
            DF2[SELECTCOL] = DF2[SELECTCOL].str.lower() 
            
    
        
    
        Z=st.radio("",options=['','Preview'])
        if Z=='Preview':
        
            AgGrid(DF2)
        if st.button('SUBMIT'):
            apend()
            #########################################################################
    # SUBSTRING FUNCTION #
    def Substring(): 
        A=""   
        st.header("Substring")
        condition=st.radio("SELECT:",options=[" ",'Substring Between the  Delimiter','Substring By Delimiter',"Substring By Start and End Indexing","Length of Substring","Find the index of character","Cell count by Column"],horizontal=True)
        if condition=='Substring Between the  Delimiter':
            st.header("Substring Between the  Delimiter")
            cols1,cols2,cols3=st.columns(3)
            with cols1:
                SELECTCOL= st.selectbox("SELECT COLUM ",COLUM)
            with cols2:
                start_delim=st.text_input("Enter starting the Delimiter:")
            with cols3:
                end_delim=st.text_input("Enter endinging the Delimiter:")
            
    
            
            Z=st.radio("",options=['','Preview'])
            if Z=='Preview':
                DF2[SELECTCOL]=DF2[SELECTCOL].str.split(start_delim).str.get(0).str.split(end_delim).str.get(0)
                AgGrid(DF2)
            
            if st.button('SUBMIT1'):
                apend()
                
            
        if condition=="Length of Substring":
            cols1,cols2,cols3=st.columns(3)
            with cols2:
                SELECTCOL= st.selectbox("SELECT COLUM TO FIND THE LENGTH OF STRING",COLUM)
    
            Z=st.radio("",options=['','Preview'])
            if Z=='Preview':
                DF2[SELECTCOL+" String Length"]= DF2[SELECTCOL].str.len()
                
                DF2
            if st.button('SUBMIT LENGTH OF SUBSTRING'):
                apend()
                
        if condition=="Find the index of character":
            cols1,cols2,cols3=st.columns(3)
            with cols1:
                SELECTCOL= st.selectbox("SELECT COLUM TO SUBSTRING BY DELIMITER",COLUM)
            with cols3:
                sub=st.text_input("Enter the character to find index:")
            DF2["Index of "+sub+" "+SELECTCOL]= DF2[SELECTCOL].str.find(sub)
            
            
        
            Z=st.radio("",options=['','Preview'])
            if Z=='Preview':
                apend()
                AgGrid(DF2.head(5))
                if st.button('SUBMIT'):
                    apend()
                else:
                    st.write('Press Submit to Complete the Process')
        
                
                
            
        if condition=='Substring By Delimiter':
            A=" "
            cols1,cols2,cols3=st.columns(3)
            with cols1:
                SELECTCOL= st.selectbox("SELECT COLUM TO SUBSTRING BY DELIMITER",COLUM)
            with cols2:
                Delimiter=st.text_input("Enter the Delimiter:")
            with cols3:
                F=st.selectbox("Select the Side",options=['Left','Right'])
            
            
            
    
            Z=st.radio("",options=['','Preview'])
            if Z=='Preview':
                if F=="Left":
                    DF2[SELECTCOL]=DF2[SELECTCOL].str.split(Delimiter).str[0]
                    A="DF2['"+SELECTCOL+"'] = DF2['"+SELECTCOL+"'].str.split('"+Delimiter+"').str[0]"
                if F=="Right":
                    DF2[SELECTCOL]=DF2[SELECTCOL].str.split(Delimiter).str[1]
                    A="DF2['"+SELECTCOL+"'] = DF2['"+SELECTCOL+"'].str.split('"+Delimiter+"').str[1]"
                
                AgGrid(DF2.head(5))
            if st.button(' SUBMIT'):
                apend()
                
                
            else:
                st.write('Press Submit to Complete the Process')
        
            
            
            
            
        if condition=="Substring By Start and End Indexing":
            cols1,cols2,cols3=st.columns(3)
            with cols1:
                SELECTCOL= st.selectbox("SELECT COLUM TO SUBSTRING BY START AND END INDEX",COLUM)
            with cols2:
                sta=(st.text_input("Enter the start index:"))
            with cols3:
                end=(st.text_input("Enter the end index:"))
            sta1=str(sta)
            end1=str(end)
            try:
                sta=int(sta)
                end=int(end)
                DF2[SELECTCOL]=DF2[SELECTCOL].str[sta:end]
            
            except:
                st.warning("Enter the Numeric value")
            
            Z=st.radio("",options=['','Preview'])
            if Z=='Preview':
                apend()
                AgGrid(DF2.head(5))
                
                if st.button('SUBMIT'):
                    apend()
                    
                
        if condition=="Cell count by Column":
            cols1,cols2=st.columns(2)
            with cols1:
                SELECTCOL= st.selectbox("SELECT COLUM TO CELL COUNT BY DELIMITER",COLUM)
            with cols2:
                Del=(st.text_input("Enter the start Delimiter:"))
        
            
            try:
                DF2[SELECTCOL+' Word Count'] = DF2[SELECTCOL].str.split(Del).apply(len)
                
            
                
            except:
                st.warning("Enter the Delimiter")
            
            Z=st.radio("",options=['','Preview'])
            if Z=='Preview':
                apend()
                AgGrid(DF2.head(5))
                
                if st.button('SUBMIT'):
                    apend()
                    
                else:
                    st.write('Press Submit to Complete the Process')
            
                
                
                
    #########################################################################################################################################################################
    
    def datefunction():
        global B
        import numpy as np
        h=st.radio("Choose Function",options=['Date Format Function','Date Difference and Date Comparison'],horizontal=True)
        
        if h=='Date Format Function':
            st.header("Date Format Function")
            date_cols = [col for col in DF2.columns if DF2[col].dtypes == 'datetime64[ns]']
            my_string = ', '.join(date_cols)
            st.write("The following columns are in date format: "+my_string)
            # DATE PARSING
            try:
                cols1,cols2=st.columns(2)
                with cols1:
                    SELECTCOL= st.selectbox("SELECT DATE COLUMN TO PARSE",COLUM)
                
                    DF2[SELECTCOL]= pd.to_datetime(DF2[SELECTCOL])
                    
                    
            
                    
                with cols2:
                    F=st.select_slider("SELECT:",options=["FormatDate",'Year','Month','Day','weekday','Name of the Day'])
            
                if F=='Year':
                    
                    st.write("YEAR")
                    
                    DF2[SELECTCOL+'- Year']= DF2[SELECTCOL].dt.year
                    
                    if st.button('preview'):
                        
                        DF2
                        
                    if st.button('SUBMIT-YEAR'):
                        st.write(B)
                        apend()
                        
                if F=='Month':
                    DF2[SELECTCOL+'- Month']= DF2[SELECTCOL].dt.month
                    
                    
                    if st.button('Preview of Month'):
                        
                        AgGrid(DF2.head(5))
                    if st.button('SUBMIT MONTH'):
                        apend()
                        
                    else:
                        st.write('Press Submit to Complete the Process')
                        
                if F=='Day':
                    DF2[SELECTCOL+'-'+' Day']= DF2[SELECTCOL].dt.day
                    A="DF2['"+SELECTCOL+'- Day'+"']= DF2['"+SELECTCOL+"'].dt.day"
                    
                    if st.button('PREVIEW-DAY'):
                        
                        AgGrid(DF2.head(5))
                    if st.button('SUBMIT-DAY'):
                        
                        
                        apend()
                        
                if F=='weekday':
                    DF2[SELECTCOL+'- '+'Weekday']= DF2[SELECTCOL].dt.weekday
                    A="DF2['"+SELECTCOL+'- Weekday'+"']= DF2['"+SELECTCOL+"'].dt.weekday"
                    
                    if st.button('PREVIEW'):
                        
                        AgGrid(DF2.head(5))
                    if st.button('SUBMIT'):
                        apend()
                        
                    else:
                        st.write('Press Submit to Complete the Process')
                        
                if F=='Name of the Day':
                    DF2[SELECTCOL+'-'+'Name of the Day']= DF2[SELECTCOL].dt.day_name()
                    A="DF2['"+SELECTCOL+'- Name of the Day'+"']= DF2['"+SELECTCOL+"'].dt.day_name()"
                    Z=st.radio("",options=['','Preview'])
                    if Z=='Preview':
                        
                        AgGrid(DF2.head(5))
                        
                    if st.button('SUBMIT'):
                        apend()
                        
                        
                if F=="FormatDate":
                    Dateformat=st.text_input("Enter the Date format of the Column:")
                    try:
                        DF2[SELECTCOL] = DF2[SELECTCOL].dt.strftime(Dateformat)
                        A="DF2['"+SELECTCOL+"']= DF2['"+SELECTCOL+"'].dt.strftime('"+Dateformat+"')"
                    except:
                        st.info("Select Date Column")
                    Z=st.radio("",options=['','Preview'])
                    if Z=='Preview':
                        
                        AgGrid(DF2.head(5))
                    if st.button('SUBMIT'):
                        apend()
                        
                    else:
                        st.write('Press Submit to Complete the Process')
            except:
                st.info("Select Date column")

            

        if h=='Date Difference and Date Comparison':
            st.header("Date Difference and Date Comparison")
            j=st.radio("SELECT",options=['Date Difference','Date Comparison'])
            if j=='Date Difference':
                date_cols = [col for col in DF2.columns if DF2[col].dtypes == 'datetime64[ns]']
                my_string = ', '.join(date_cols)
                st.write("The following columns are in date format: "+my_string)
                cols1,cols2=st.columns(2)
                with cols1:
                    Date1 = st.selectbox("SELECT DATE 1",COLUM)
                with cols2:
                    Date2 = st.selectbox("SELECT DATE 2",COLUM)
                try:
                    DF2[Date1]= pd.to_datetime(DF2[Date1])
                    
                    DF2[Date2]= pd.to_datetime(DF2[Date2])
                    
            
                    G=str(" Diff B/W "+Date1+"&"+Date2)
                    G1="str( Diff B/W "+Date1+"&"+Date2+")"
                    diff=st.select_slider("SELECT DIFFERENCE IN",options=['Days','Months','Years'],)
            
                    if diff=='Days':
                        Z=st.radio("",options=['','Preview'])
                        if Z=='Preview':
                            DF2[G+" in Days"]=(DF2[Date1]-DF2[Date2])/ np.timedelta64(1, 'D')
                            
                            AgGrid(DF2.head(5))
                        
                            if st.button('SUBMIT'):
                                apend()
                            else:
                                st.write('Press Submit to Complete the Process')
                            
                            
                        
                    if diff=='Months':
                        Z=st.radio("",options=['','Preview '])
                        if Z=='Preview ':
                            DF2[G+" in Months"]=(DF2[Date1]-DF2[Date2])/ np.timedelta64(1, 'M')
                            
                            AgGrid(DF2.head(5))
                        
                            if st.button('SUBMIT'):
                                apend()
                                
                            else:
                                st.write('Press Submit to Complete the Process')
                            
                            
                    if diff=='Years':
                        Z=st.radio("",options=['','Preview'])
                        if Z=='Preview':
                            DF2[G+"in Years"]=(DF2[Date1]-DF2[Date2])/ np.timedelta64(1, 'Y')
                            
                            AgGrid(DF2.head(5))
                            
                            if st.button('SUBMIT'):
                                apend()
                                
                            else:
                                st.write('Press Submit to Complete the Process')
                            
                            
                        
                            
                except:
                    st.info("Selected colums Must contains Date")

            
            if j=='Date Comparison':
                date_cols = [col for col in DF2.columns if DF2[col].dtypes == 'datetime64[ns]']
                my_string = ', '.join(date_cols)
                st.write("The following columns are in date format: "+my_string)
                cols1,cols2,cols3=st.columns(3)
                with cols1:
                    Date1 = st.selectbox("SELECT DATE 1",COLUM)
                with cols2:
                    Date2 = st.selectbox("SELECT DATE 2",COLUM)
                with cols3:
                    v=st.selectbox("Select ",options=['Date1 is Grater Then Date2','Date1 is Less Then Date2','Date1 is Grater Then or Equal To Date2','Date1 is Less Then or Equal To Date2','Date1 is  Equal To Date2']) 
                try:
                    DF2[Date1]= pd.to_datetime(DF2[Date1])
                    
                    DF2[Date2]= pd.to_datetime(DF2[Date2])
                    
                    if v=='Date1 is Grater Then Date2':
                        DF2[Date1+" > "+ Date2] = DF2[Date1] > DF2[Date2]
                        
                    
                    if v=='Date1 is Less Then Date2':
                        DF2[Date1+" < "+ Date2] = DF2[Date1] < DF2[Date2]
                        
                        
                    if v=='Date1 is Grater Then or Equal To Date2':
                        DF2[Date1+" >= "+Date2] = DF2[Date1] >= DF2[Date2]
                        
                        
                    if v=='Date1 is Less Then or Equal To Date2':
                        DF2[Date1+" <= "+ Date2] = DF2[Date1] <= DF2[Date2]   
                        
                    
                    if v=='Date1 is  Equal To Date2':
                        DF2[Date1+" = "+ Date2] = DF2[Date1] == DF2[Date2]   
                        
                
                    
                    Z=st.radio("",options=['','Preview'])
                    if Z=='Preview':
                        apend()
                        AgGrid(DF2.head(5))
                        
                        if st.button(' SUBMIT'):
                            apend()
                
                        else:
                            st.write('Press Submit to Complete the Process')
                except:
                    st.info("Selected colums Must contains Date")


        
        
    
    if menu_id=="Explode":
        Explode()
    if menu_id== "Fill & Replace":
        FILL()

    if menu_id=="Substring":
        Substring()

    if menu_id== "Date Function":
    
        datefunction()
        

    if menu_id== "Split Column": 
        splitcolumn()
    
            
    if menu_id== "Formatting":   
        formatting()
    
    

DF2=pd.read_excel('Source File.xlsx')

with st.expander("DATA"):

    DF2=pd.read_excel('Source File.xlsx')
    DF2
    


    
    
    



