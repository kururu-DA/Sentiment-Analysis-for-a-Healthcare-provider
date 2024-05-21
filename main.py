import serpapi
import os
import pandas as pd
from dotenv import load_dotenv
from dateutil import parser
from review import Review

#load env
load_dotenv()

api_key = os.getenv("SERVICE_KEY")
client = serpapi.Client(api_key=api_key)
#"place_id": "ChIJAWHqLdZZfxURRfYEe1Yy_zs"

def get_results(token):
    results=''
    if token is None or token=="":
         results = client.search({
    'engine':'google_maps_reviews' , 
    'type':'search',
    "place_id": "ChIJAWHqLdZZfxURRfYEe1Yy_zs",
    "sort_by":"ratingHigh",
    # 'q':'Endocrine and Diabetes Center, Naziyah، An Naziyah, Buraydah 52366',
#   'll':'@24.6746995,46.8337699'
    })
    else:
        results = client.search({
    'engine':'google_maps_reviews' , 
    'type':'search',
    "place_id": "ChIJAWHqLdZZfxURRfYEe1Yy_zs",
    "sort_by":"ratingHigh",
    "next_page_token":next_page_token
    # 'q':'Endocrine and Diabetes Center, Naziyah، An Naziyah, Buraydah 52366',
#   'll':'@24.6746995,46.8337699'
      })
    print(results)    
    return results
#info@wafyapp.com
    
# print(results.data['serpapi_pagination']['next_page_token'])
#esults.data['reviews']
next_page_token=""
reviews =[]
page=0
df=pd.DataFrame({"id":[],"rating":[],"date":[],"source":[],"reviews":[],"snippet":[]})

while True:
     results =get_results(next_page_token)
     if "serpapi_pagination" in results.data:
         next_page_token =results.data['serpapi_pagination']['next_page_token']
     else:
         next_page_token=""

     
     page=page+1
     data=results.data['reviews']

     for i in range(len(data)):
         

         if "snippet" in data[i]:
             reviews.append(Review(i*page,data[i]['rating'],
                                   parser.parse( data[i]['iso_date_of_last_edit']), 
                                    data[i]['source'],  
                               data[i]['user']['reviews'],
                               str(data[i]['snippet'])
                               ))
         else:
             reviews.append(Review(i*page,data[i]['rating'],
                                    parser.parse( data[i]['iso_date_of_last_edit']), 
                                    data[i]['source'],  
                               data[i]['user']['reviews'],
                               str("")
                               ))

     if next_page_token == None or next_page_token =='':
        
        break
for i in range(len(reviews)):
        df=pd.concat([df,pd.DataFrame({"id":[reviews[i].id],"rating":[reviews[i].rating],"date":[reviews[i].date],"source":[reviews[i].source],"reviews":[reviews[i].review],"snippet":reviews[i].snippets})])

        # print(i.id)
        df.to_csv("results.csv")

