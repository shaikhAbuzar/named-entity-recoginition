import wikipediaapi
import spacy
import streamlit as st
import pandas as pd
import altair as alt
from spacy import displacy
from collections import Counter
import en_core_web_sm

# loading the english language for nlp
# nlp = spacy.load("en_core_web_sm")
nlp = en_core_web_sm.load()


# creating the wikipedia api object
wiki_wiki = wikipediaapi.Wikipedia(
	language='en',
	extract_format=wikipediaapi.ExtractFormat.WIKI
)


# the function to plot the bar graph
def draw_bar_graph(sentence_list):
	doc_sent = nlp(str(sentence_list))
	# creating the dataframe for the bar graph
	# and then plotting the bar graph
	data_points = {'Entity': [], 'Count': []}
	d = dict(Counter([x.label_ for x in doc_sent.ents]))
	for key, value in d.items():
		data_points['Entity'] += [key]
		data_points['Count'] += [value]
	data_points_DF = pd.DataFrame(data_points)
	# plotting of graph happens here
	bar_chart = alt.Chart(data_points_DF).mark_bar().encode(
		x='Entity', y='Count'
	)
	return bar_chart, data_points_DF


# Title of the page:
st.title("Wikipedia _NER_")

# Topic to search
st.write("**Name of the topic:**")
topic = st.text_input("[Press Enter to Search]", "Wikipedia")

if topic != '':
	# get the page using the wikipedia api
	page = wiki_wiki.page(topic)

	if page.exists():
		text = page.text
		# print(text)
		# Process the text using the nlp object
		doc = nlp(text)
		# generate all the sentences from the provided object
		sentences = [sentence for sentence in doc.sents]

		# Adding the slider for selecting the number of sentence to display
		sentence_length = len(sentences)
		st.markdown("<br> **Select the indexes of the statements**", unsafe_allow_html=True)
		sentence_start = st.slider("Start Index: ", min_value=0, max_value=sentence_length, value=0)
		sentence_end = st.slider("End index: ", min_value=sentence_start, max_value=sentence_length, value=1)

		if sentence_end > sentence_start:
			# plot the chart for the selected sentences and
			# display the dataframe with all the values
			graph, table = draw_bar_graph(sentences[sentence_start: sentence_end])
			column_1, column_2 = st.beta_columns([3, 1])

			with column_1:
				st.write('**Below is the chart:**')
				st.altair_chart(graph, use_container_width=True)

			with column_2:
				with st.beta_expander("See the table of the values:"):
					st.write(table)

			# display the output of the provided statements
			with st.beta_expander("See the Statements"):
				# st.write("**Below are the statement(s)**")
				st.markdown(
					displacy.render(
						nlp(str(
								' '.join([str(stmt) for stmt in sentences[sentence_start: sentence_end]])
							)), style='ent'),
					unsafe_allow_html=True
				)
		elif sentence_end <= sentence_start:
			msg = f"Start Index {sentence_start} > End Index {sentence_end}....!!"
			st.write(msg)
	else:
		st.write(f"Page for {topic} Not Found...!! :-(")
