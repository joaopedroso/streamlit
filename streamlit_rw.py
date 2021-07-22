import streamlit as st
from google.cloud import firestore

# Authenticate to Firestore with the JSON account key.
db = firestore.Client.from_service_account_json("firestore-key.json")

# Create a reference to the Google post.
doc_ref = db.collection("users").document("jpp9374")

# This time, we're creating a NEW post reference for Apple
doc_ref = db.collection("users").document("jpp0123")

# And then uploading some data to that reference
doc_ref.set({
    "title": "JPP title",
    "url": "www.joaopedroso.org"
})





# Streamlit widgets to let a user create a new post
title = st.text_input("Post title")
url = st.text_input("Post url")
submit = st.button("Submit new post")

# Once the user has submitted, upload it to the database
if title and url and submit:
    doc_ref = db.collection("users").document(title)
    doc_ref.set({
        "title": title,
        "url": url
    })

# And then render each post, using some light Markdown
users_ref = db.collection("users")
for doc in users_ref.stream():
    post = doc.to_dict()
    try:
        title = post["title"]
        url = post["url"]

        st.subheader(f"Post: {title}")
        st.write(f":link: [{url}]({url})")

    except:
        st.write(f"[post with no title:] {post}")

# Now let's make a reference to ALL of the users
users_ref = db.collection("users")

# For a reference to a collection, we use .stream() instead of .get()
for doc in users_ref.stream():
    st.write("The id is: ", doc.id)
    st.write("The contents are: ", doc.to_dict())