import streamlit as st
from google.cloud import firestore
import json
key_dict = json.loads(st.secrets["textkey"])
# creds = service_account.Credentials.from_service_account_info(key_dict)


from google.oauth2 import service_account
creds = service_account.Credentials.from_service_account_info(key_dict)




db = firestore.Client(credentials=creds, project="streamlit-98234")

# Streamlit widgets to let a user create a new post
title = st.text_input("Post title")
url = st.text_input("Post url")
email = st.text_input("Post e-mail")
submit = st.button("Submit new post")

# Once the user has submitted, upload it to the database
if title and url and submit:
    doc_ref = db.collection("onln").document(title)
    doc_ref.set({
        "title": title,
        "url": url,
        "email": email,
    })

# And then render each post, using some light Markdown
users_ref = db.collection("onln")
for doc in users_ref.stream():
    post = doc.to_dict()
    try:
        title = post["title"]
        url = post["url"]
        email = post["email"]

        st.subheader(f"Post: {title}")
        st.write(f":link: [{url}]({url})")

    except:
        st.write(f"[post with no title:] {post}")

# Now let's make a reference to ALL of the users
users_ref = db.collection("onln")

# For a reference to a collection, we use .stream() instead of .get()
for doc in users_ref.stream():
    st.write("The id is: ", doc.id)
    st.write("The contents are: ", doc.to_dict())