import  numpy as np
import pandas as pd
import logging.handlers
import argparse


LOG_FILENAME = 'data/log/prouct_catalog.log'

# Logger with desired output level
logging.basicConfig(level=1)
log = logging.getLogger("Product_Catalogue")


# Add the log message handler to the logger
handler = logging.handlers.RotatingFileHandler(
    LOG_FILENAME, maxBytes=5000, backupCount=2)

log.addHandler(handler)

#Implement ArgParser
parser = argparse.ArgumentParser(description='Product Catalogue')

parser.add_argument('-i','--input',help='Input file Path')
parser.add_argument('-o','--output',help='Output file Path')
args = parser.parse_args()

log.info("Loading Input Data")
#Load input data into DataFrame
df_articles = pd.read_csv(args.input,header=0,sep="|")

log.info("Pivoting on PART_NO ")
#Pivot on PART_NO
df_articles_pivot = df_articles.pivot(columns="PART_NO",values="COLOR")

df_articles_pivot_frame = df_articles["ARTICLE_CD"].to_frame("ARTICLE_CD")

log.info("Concatenating ARTICLE_CD data with Pivoted PART_NO ")
#Concat ARTICLE_CD data with Pivoted PART_NO
df_result = pd.concat([df_articles_pivot_frame,df_articles_pivot],axis=1)

log.info("Performing Groupby on ARTICLE_CD and max on PART_X")
#Groupby on ARTICLE_CD and max on PART_X
df_groupby = df_result.groupby(by=["ARTICLE_CD"]).max().replace(to_replace=np.NaN,value="")
df_groupby.columns = ['PART_' + str(col) for col in df_groupby.columns if col != "ARTICLE_CD"]

log.info("Writing result to " + args.output)
#Write to csv out
df_groupby.to_csv(args.output)

