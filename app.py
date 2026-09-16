### app.py
```python
import pandas as pd
import streamlit as st

# 2. Set page title and icon
st.set_page_config(page_title="Gospel Bot", page_icon="🎵")

# 3. Show title with music note emoji
st.title("Gospel Bot 🎵")

# 4. Show descriptive text
st.write("Find your favorite gospel songs")

# 5. Read the CSV file
# Make sure 'songs.csv' is in the same folder as app.py in your GitHub repo
df = pd.read_csv("songs.csv")

# 6. Text input box for searching
search_query = st.text_input("Search song or artist")

# 7 & 9. Filter table if user types something, otherwise show all
if search_query:
  # Filter rows where search matches Title or Artist, ignoring case
  filtered_df = df[
      df["Title"].str.contains(search_query, case=False, na=False)
      | df["Artist"].str.contains(search_query, case=False, na=False)
  ]

  # 8. Show how many songs found
  st.write(f"Found **{len(filtered_df)}** song(s)")
  st.dataframe(filtered_df, hide_index=True, use_container_width=True)
else:
  st.dataframe(df, hide_index=True, use_container_width=True)

# 10. Show total songs count at the bottom
st.markdown("---")
st.write(f"Total songs: {len(df)}")
