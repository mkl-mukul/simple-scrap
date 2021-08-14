import pandas as pd
import numpy as np
from pandas import ExcelWriter
from pandas import ExcelFile
from bs4 import BeautifulSoup

import requests

class scrap:

    def __init__(self,link):
        self.link=link
        self.r = requests.get(self.link)
        self.soup = BeautifulSoup (self.r.content,'lxml') 

    def url_list(self):

        self.link_list=[]
        self.links = self.soup.find('tbody') 
    
    def title_year(self):
        self.title=self.soup.find_all('td',attrs = {'class':'titleColumn'})
        self.ratings=self.links.find_all('td',attrs={'class':'ratingColumn imdbRating'})

        for i in range(len(self.title)):
            self.link_list.append(self.title[i].a.get('href'))

        self.data1={'title':[],'ratings':[],year':[]}
        # # data={'title':[],'year':[],'duration':[],'Description':[]}


        for r in range(6):
            self.data1['title'].append(self.title[r].a.text)
            self.data1['year'].append(self.title[r].span.text)
            self.data1['ratings'].append(self.ratings.strong.text)

        # self.df=pd.DataFrame(self.data1)
        # print(self.df)
        # self.writer = pd.ExcelWriter('scrapsheet.xlsx')  
        # self.df.to_excel(self.writer)  
        # self.writer.save()

        print("successfully scrapped title year detail")

    def duration_desc(self):
        self.data2={'duration':[],'Description':[]}


        # checking every link 

        for i in range(6):
            self.r2=requests.get("https://www.imdb.com/{0}".format(self.link_list[i]))
            self.soup2 = BeautifulSoup (self.r2.content,'lxml')
            self.duration= self.soup2.find_all('li',attrs={'class':'ipc-inline-list__item'})
            self.data2['duration'].append(self.duration[2].text)
            self.description= self.soup2.find('span',attrs={'class':'GenresAndPlot__TextContainerBreakpointXS_TO_M-cum89p-0 dcFkRD'})
            self.data2['Description'].append(self.description.text)
        print("successfully scrapped duration and description detail")


    def final(self):
        self.data1.update(self.data2)
        self.df=pd.DataFrame(self.data1)
        print(self.df)
        self.writer = pd.ExcelWriter('scrapsheet.xlsx')  
        self.df.to_excel(self.writer)  
        self.writer.save()
        print("successfully scrapped and made excel sheet")

f=scrap('https://www.imdb.com/chart/top?ref_=nv_mv_250')
f.url_list()
f.title_year()
f.duration_desc()
f.final()
















