import streamlit as st
import pickle
import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings("ignore")  # Suppress warnings

@st.cache_data
def load_cached_data():
    books = pickle.load(open('books_dict.pkl', 'rb'))
    pt = pickle.load(open('pt.pkl', 'rb'))
    similarity_score = pickle.load(open('similarity_score.pkl', 'rb'))
    famous_books=pickle.load(open('famous_books.pkl','rb'))
    popular_df=pickle.load(open('popular_df.pkl','rb'))
    return pd.DataFrame(famous_books),books, pt, similarity_score, popular_df

famous_books, books, pt, similarity_score, popular_df = load_cached_data()


def recommend(book_name):
    index=np.where(pt.index==book_name)[0][0]
    similar_items=sorted(list(enumerate(similarity_score[index])),key=lambda x:x[1],reverse=True)[1:6]
    
    data=[]
    for i in similar_items:
        item=[]
        temp_df=books[books['Book-Title']==pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title']))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author']))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M']))

        data.append(item)

    return data
    

st.title('Book Recommender System')
st.markdown("""
    <div style="position: fixed; bottom: 10px; right: 10px; color: #d3d3d3; font-size: 12px; background-color: transparent;">
        Made by Kashika
    </div>
""", unsafe_allow_html=True)

st.sidebar.title("Top 50 Books")
book_name=list(popular_df['Book-Title'])
author=list(popular_df['Book-Author'])
image=list(popular_df['Image-URL-M'])
num_rating=list(popular_df['num_ratings'])
avg_rating=list(popular_df['avg_rating'])

for i in range(len(popular_df)):
    with st.sidebar:
        st.image(image[i], width=100)  
        st.markdown(f"**{book_name[i]}**")  
        st.write(f"Author: {author[i]}")  
        st.write(f"⭐ {avg_rating[i]:.2f} ({num_rating[i]} ratings)")  
        st.markdown("---")  


selected_book_name=st.selectbox(
    'Enter book name',
    famous_books
)

if st.button('Recommend'):
    recommendations = recommend(selected_book_name)
    cols = st.columns(len(recommendations))  
    for idx, i in enumerate(recommendations):
        with cols[idx]:
            st.image(i[2], use_container_width=True)  
            st.markdown(f"<h4>{i[0]}</h4>", unsafe_allow_html=True)
            st.write(f"**Author:** {i[1]}")  
            st.markdown("<br><br><br><br>", unsafe_allow_html=True)



