#!/usr/bin/env python

'''
Weather Data Analysis v0.1
Author : Vasista Polali
Date : 10/12/2016
'''


import sys
import os
import csv
import glob
import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import logging




#Calculate Average Max, Min temperatures and total Precipitation
def avgTmps(output_file):
    l=[]
    averages_out_file= open(output_file, 'w')
    for file in os.listdir('.'):
        df = pd.read_csv(file,sep='\t', header=None )
        df.columns = ['TimeStamp', 'MaxTmp','MinTmp','Prcp']

        df['TimeStamp']=  pd.to_datetime(df['TimeStamp'],format='%Y%m%d').dt.year
        df['MaxTmp'],df['MinTmp'],df['Prcp'] = df['MaxTmp'].replace('-9999', np.nan),df['MinTmp'].replace('-9999', np.nan),df['Prcp'].replace('-9999', np.nan)

        df = df.groupby(df['TimeStamp'])
        for k,v in df:
            d= file.replace(".txt",""),k,"{0:.2f}".format(v['MaxTmp'].mean()/10), "{0:.2f}".format(v['MinTmp'].mean()/10),"{0:.2f}".format(v['Prcp'].sum()/100)
            l.append(d)
            logger.info("Finished calculating average temparatures and Total precipitaion for station code" + str(file.replace(".txt","")))


    df_avg = pd.DataFrame(l,columns=['Station_Code', 'Year','Avg_Max_Tmp','Avg_Min_Tmp','Total_Prcp'])
    df_avg.to_csv(averages_out_file,sep='\t',index=False)
    averages_out_file.close()
    logger.info("Finished calculating average temparatures and Total precipitaion for all weather stations")



#Calculate Pearsons correlation between tthe total corn yield and the Average Max and Min tempertaures and Total precipitation
def pearsonsCorr(input_file,df_yield,corr_output_file):
    l_corr = []
    corr_out_file= open(corr_output_file, 'w')
    df_avg = pd.read_csv(input_file, sep='\t').sort_values(by='Station_Code')
    for k,v in df_avg.groupby('Station_Code'):
        df_c = v.merge(df_yield, on='Year', how='outer')
        df_corr = df_c.corr(method='pearson')
        c = k,"{0:.2f}".format(df_corr.iloc[4]['Avg_Max_Tmp']),"{0:.2f}".format(df_corr.iloc[4]['Avg_Min_Tmp']),"{0:.2f}".format(df_corr.iloc[4]['Total_Prcp'])
        l_corr.append(c)
        logger.info("Finished calculating Pearsons correlation between the total corn yield and the Average Max and Min tempertaures and Total precipitation for station code" + str(k))

    df_avg = pd.DataFrame(l_corr,columns=['Station_Code','Max_Tmp_Corr','Min_Tmp_Corr','Total_Prcp_Corr'])
    df_avg.to_csv(corr_out_file,sep='\t',index=False)
    corr_out_file.close()
    logger.info("Finished calculating Pearsons correlation between the total corn yield and the Average Max and Min tempertaures and Total precipitation for all weather stations")

#Plot the linear regression between Max or Min temperatures or Total preciption under a weather station and the Corn yield
def plot(averages_file,station_code,xLabel,yLabel,correlation_file):
    df_plot= pd.read_csv(averages_file, sep='\t')
    df_corr= pd.read_csv(correlation_file, sep='\t')
    for k,v in df_plot.groupby('Station_Code'):
        if k == station_code:
            df = v.merge(df_yield)
            x = df[xLabel]
            y= df[yLabel]
            if 'Max' in xLabel:
                corr_coef = df_corr.loc[df_corr['Station_Code'] == k].iloc[0][1]
            elif 'Min' in xLabel:
                corr_coef = df_corr.loc[df_corr['Station_Code'] == k].iloc[0][2]
            elif 'Prcp' in xLabel:
                corr_coef = df_corr.loc[df_corr['Station_Code'] == k].iloc[0][3]
            plt.scatter(x,y,color='green')
            if xLabel == 'Avg_Min_Tmp':
                plt.xlabel('Average Minimum Temperature in Celsius')
            elif xLabel == 'Avg_Max_Tmp':
                plt.xlabel('Average Maximum Temperature in Celsius')
            elif xLabel == 'Total_Prcp':
                plt.xlabel('Total Precipitation in Centimeters')

            plt.ylabel('Corn Yield in Thousands of Megatons')
            ax = plt.subplot(111)
            ax.set_title('r = ' + str(corr_coef))

            A = np.vstack([x,np.ones(len(x))]).T
            m,c = np.linalg.lstsq(A,np.array(y))[0]
            plt.plot(x,x*m+c,color='red',)
            logger.info("Plotting linear regression for" + str(xLabel) + " and " + str(yLabel))
            plt.show()





if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    __name__ = "Weather-Analysis"
    logger = logging.getLogger(__name__)


    if sys.argv[1] == 'avg-corr':
        if len(sys.argv) < 6:
            logger.info('Invalid arguments,for average and correlation the args are <operation> <input dir> <averages output file>' \
                   ' <corn Yield file> <correlation output file>')
            sys.exit(2)
        filelist = os.chdir(sys.argv[2]) #wx_data
        averages_output_file = sys.argv[3] #averages output file
        corn_yield_file = open(sys.argv[4], 'r')
        corr_output_file = sys.argv[5]
        df_yield = pd.read_csv(corn_yield_file, sep='\t',header=None)
        df_yield.columns = ['Year', 'Yield']
        avgTmps(averages_output_file)
        pearsonsCorr(averages_output_file,df_yield,corr_output_file)

    elif sys.argv[1]=='plot-weather-data':
        if len(sys.argv) < 9:
            logger.info('Invalid arguments,for average and correlation the args are <operation> <input dir> <averages output file>' \
                  '<corn Yield file> <correlation output file> <station code> <X Label> <Y Label>')
            sys.exit(2)

        filelist = os.chdir(sys.argv[2]) #wx_data
        averages_output_file = sys.argv[3] #averages output file
        corn_yield_file = open(sys.argv[4], 'r')
        corr_output_file = sys.argv[5]
        df_yield = pd.read_csv(corn_yield_file, sep='\t',header=None)
        df_yield.columns = ['Year', 'Yield']
        avgTmps(averages_output_file)
        pearsonsCorr(averages_output_file,df_yield,corr_output_file)
        station_code=sys.argv[6]
        xLabel=sys.argv[7]
        yLabel=sys.argv[8]
        plot(averages_output_file,station_code,xLabel,yLabel,corr_output_file)






