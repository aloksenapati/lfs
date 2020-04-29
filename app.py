# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 16:39:58 2020

@author: Administrator
"""

import pandas as pd  
import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)
data= pickle.load(open('data_pickle.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
     #qustine no : 1
    def qes1(op1,op2,op3): #for query type 'discounted_products_list'  this function is written
        if op1=='discount':
            if op2=='>':   #return the id which are discounting as per given condition
                try:
                    z=list(pd.DataFrame(list(data[data['discount%']>float(op3)]['_id']))['$oid'])
                    return z
                except:
                    z=['invalid input op3']
                    return z
            elif op2=='<':
                try:
                    z=list(pd.DataFrame(list(data[data['discount%']<float(op3)]['_id']))['$oid'])
                    return z
                except:
                    z=['invalid input op3']
                    return z
            elif op2=='==':
                try:
                    z=list(pd.DataFrame(list(data[data['discount%']==float(op3)]['_id']))['$oid'])
                    return z
                except:
                    z=['invalid input op3']
                    return z
            else:
                z=['invalid input op2']
                return z
        elif op1=='brand.name': #return the id's of given codition brand
            if op2 in ['>','<']:
                z=['invalid input op2']
                return z
            elif op2=='==':
                try:
                    z=list(pd.DataFrame(list(data[data['brand'].map(lambda x:x['name']==op3)]['_id']))['$oid'])
                    return z
                except:
                    z=['invalid input op3']
                    return z
            
            else:
                z=['invalid input op2']
                return z
        else:
            z=['invalid input op1']
            return z
            
            
            
   #question : 2
    def qes2(op1,op2,op3): #this function is written for 'discounted_products_count' & 'avg_discount' return in dict format
        d={}
        if op1=='discount': #for operand1 type 1 thses are the test case
            if op2=='>':
                d['discounted_products_count']=len(data[data['discount%']>float(op3)])
                d['avg_dicount']=data[data['discount%']>float(op3)]['discount%'].sum()/len(data[data['discount%']>float(op3)])
                z=d
                return z
            elif op2=='<':
                d['discounted_products_count']=len(data[data['discount%']<float(op3)])
                d['avg_dicount']=data[data['discount%']<float(op3)]['discount%'].sum()/len(data[data['discount%']<float(op3)])
                z=d
                return z
            elif op2=='==':
                d['discounted_products_count']=len(data[data['discount%']==float(op3)])
                d['avg_discount']=data[data['discount%']==float(op3)]['discount%'].sum()/len(data[data['discount%']==float(op3)])
                z=d
                return z
            else:
                z=['invalid input op2']
                return z
        elif op1=='brand.name': #for operand1 type 2 thses are the test case
            if op2 in ['>','<']:
                z=['invalid input op2']
                return z
                    
            elif op3 in list(set(pd.DataFrame(list(data['brand']))['name'])):
                df=pd.DataFrame(data[data['brand'].map(lambda x:x['name']==op3)]['discount%'])
                d['discounted_products_count']=len(df)
                d['avg_dicount']=df.sum()/len(df)
                z=d
                return z
            else:
                z=['invalid input op3']
                return z
        else:
            z=['invalid input']
            return z
        
    
#question : 3
    def qes3(op1,op2,op3): #this function for 'expensive_list' return id's
        if op1=='brand.name':
            if op2=='==':
                if op3 in list(set(pd.DataFrame(list(data['brand']))['name'])):
                    ls=[]
                    for i in range(len(data)):
                        if data['brand'][i]['name']==op3:
                            if data['price_positioning_text'][i]=='expensive':
                                ls.append(data.iloc[i]['_id']['$oid'])
                    z=ls
                    return z
                else:
                    z=['invalid input op3']
                    return z
            else:
                z=['invalid input op2']
                return z
        else:
            z=['invalid input op1']
            return z
    
    
#question no : 4
    def qes4(op1,op2,op3): #this function written for 'competition_discount_diff_list' & return id's
        if op1=='discount_diff': #type 1 case study
            ls3=[]
            for i in range(len(data)):
                for j in range(4):
                    df=pd.DataFrame(pd.DataFrame(data['similar_products'][1768]['website_results']).iloc[1][2],columns=['total_results','min_price','max_price','avg_price','avg_discount'])
                    
                    if df.iloc[0][0] !=0:
                        fd=pd.DataFrame(pd.DataFrame(data['similar_products'][i]['website_results']).iloc[1][j])
                        lt=fd.loc['basket']['avg_price']
                        x=pd.DataFrame(data.iloc[:,10][i])
                        bp=x.basket_price[1]
                        dd=(bp-lt)*100/bp
                        if op2=='>':
                            if dd>float(op3):
                                ls3.append(data.iloc[i]['_id']['$oid'])
                                
                        elif op2=='<':
                            if dd<float(op3):
                                ls3.append(data.iloc[i]['_id']['$oid'])
                        elif op2=='==':
                             if dd==float(op3):
                                ls3.append(data.iloc[i]['_id']['$oid'])
                        else:
                            z=['invalid op2 input']
                            return z
            z=ls3
            return z
        elif op1=='competition': #type 2 case study
            if op2=='==':
                ls2=[]
                for i in range(len(data)):
                    n=pd.DataFrame(data['similar_products'][i]['website_results']).iloc[1,:][op3]['total_results']
                    if n!=0:
                        ls2.append(data.iloc[i]['_id']['$oid'])
                z=ls2
                return z
            else:
                z=['invalid input op2']
                return z
        

        else:
            z=['invalid input op1']
            return z
    
    int_features = [k for k in request.form.values()]
    query = int_features[0]
    op1 = int_features[1]
    op2 = int_features[2]
    op3 = int_features[3]
    if query=='discounted_products_list':
        pred=qes1(op1,op2,op3)
    elif query in ['discounted_products_count','avg_discount']:
        pred=qes2(op1,op2,op3)
    elif query=='expensive_list':
        pred=qes3(op1,op2,op3)
    elif query=='competition_discount_diff_list':
        pred=qes4(op1,op2,op3)       

    return render_template('index.html', prediction_text=pred)
    
    #For rendering results on HTML GUI
    

if __name__ == "__main__":
    app.run(debug=True)
