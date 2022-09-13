import streamlit as st
from matplotlib.backends.backend_agg import RendererAgg
import numpy as np
import pandas as pd
import xmltodict
from pandas import json_normalize
import urllib.request
import seaborn as sns
import matplotlib
from matplotlib.figure import Figure
from PIL import Image
import requests
import re
from streamlit_lottie import st_lottie
st.set_page_config(
	page_title="Books data",
	initial_sidebar_state="expanded",
	page_icon="smiley",
	layout="wide",
	 menu_items={
		 'Get Help': 'https://www.extremelycoolapp.com/help',
		 'Report a bug': "https://www.extremelycoolapp.com/bug",
		 'About': "# This is a header. This is an *extremely* cool app!"})


def load_lottieurl(url: str):
	r = requests.get(url)
	if r.status_code != 200:
		return None
	return r.json()

lottie_book = load_lottieurl('https://assets6.lottiefiles.com/packages/lf20_WHZwmw.json')
st_lottie(lottie_book, speed=1, height=200, key="initial")

row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns(
	(.1, 2, .2, 1, .1))

row0_1.title("Book read data 🎈")
st.sidebar.markdown("# Book read data 🎈")


row2_spacer1, row2_1, row2_spacer2 = st.columns((.1, 3.2, .1))
with row2_1:
	#default_username = st.selectbox("Select one of our sample Goodreads profiles", (
	   # "89659767-tyler-richards", "7128368-amanda", "17864196-adrien-treuille", "133664988-jordan-pierre"))
	default_username=f"https://www.goodreads.com/user/show/139340318-khanh-hua"
 
	user_input = st.text_input(
		"Input your own Goodreads Link (e.g. https://www.goodreads.com/user/show/139340318-khanh-hua)")
	need_help = st.expander('Need help? 👉')
	with need_help:
		st.markdown(
			"Having trouble finding your Goodreads profile? Head to the [Goodreads website](https://www.goodreads.com/) and click profile in the top right corner.")

	if not user_input:
		user_input = f"https://www.goodreads.com/user/show/{default_username}"

user_id = ''.join(filter(lambda i: i.isdigit(), user_input))
user_name = user_input.split(user_id, 1)[1].split('-', 1)[1].replace('-', ' ')



@st.cache
def get_user_data(user_id, key='ZRnySx6awjQuExO9tKEJXw', v='2', shelf='read', per_page='200'):
	api_url_base = 'https://www.goodreads.com/review/list/'
	final_url = api_url_base + user_id + '.xml?key=' + key + \
		'&v=' + v + '&shelf=' + shelf + '&per_page=' + per_page
	contents = urllib.request.urlopen(final_url).read()
	return(contents)


user_input = str(user_input)
contents = get_user_data(user_id=user_id, v='2', shelf='read', per_page='200')
contents = xmltodict.parse(contents)




Goodread_profile = f"https://www.goodreads.com/user/show/{user_input}"
user_id = ''.join(filter(lambda i: i.isdigit(), Goodread_profile))
user_name = re.findall(r'(?:\d[-.]|[^-.])*(?:[-.]|$)', Goodread_profile.split(user_id, 1)[1])[1]
user_id_name = user_id+'-'+user_name

apiKey = "ZRnySx6awjQuExO9tKEJXw"
version = "2"
shelf = "read"
per_page = "200"

@st.cache
def get_user_data(user_id, apiKey, version, shelf, per_page):
	api_url_base = "https://www.goodreads.com/review/list/"
	final_url = (
		api_url_base
		+ user_id
		+ ".xml?key="
		+ apiKey
		+ "&v="
		+ version
		+ "&shelf="
		+ shelf
		+ "&per_page="
		+ per_page
	)
	contents = urllib.request.urlopen(final_url).read()
	return contents

contents = get_user_data(user_id_name,apiKey,version, shelf, per_page)
contents_json = xmltodict.parse(contents)
df = pd.json_normalize(contents_json["GoodreadsResponse"]["reviews"]["review"])
df = df[df["date_updated"].notnull()]
final_df = df[
	[
		"rating",
		"started_at",
		"read_at",
		"date_added",
		"book.title",
		"book.average_rating",
		'book.ratings_count',
		"book.publication_year",
		"book.authors.author.name"
	]
]
final_df.style.highlight_max(axis=0)
with row2_1:
	st.write('Data Dimension: ' + str(final_df.shape[0])+ ' rows and ' + str(final_df.shape[1]) + ' columns')
	#slider3 = st.slider('Average_Ratings:',0,5,0.5)
	options = st.multiselect('Choose rating',['Must-read','Recommendation','Boring','Unworth reading'])
	#filtered_df = final_df[final_df["book.average_rating"].isin(filter1)]
	filtered_df = final_df[final_df["book.average_rating"].isin(options)]
	st.dataframe(final_df)
