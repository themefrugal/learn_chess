import streamlit as st
import chess
from chess import svg as csvg
import base64
import pandas as pd

if 'count' not in st.session_state:
    st.session_state.count = 0

if 'board' not in st.session_state:
    st.session_state.board = chess.Board()

variation_1 = [
    "e4",  "e5",
    "Nf3", "Nf6"
]

variation_2 = [
    "e4",  "e5",
    "Nf3", "Nf6",
    "Ne5", "Nc6",
    "Nc6", "d7c6"
]

v3 = pd.read_csv('sg_variation_3.csv')
v3.columns = [x.strip() for x in v3.columns]
variation_3 = [x.strip() for xs in v3.values.tolist() for x in xs]

dict_moves = {
      "Variation 1": variation_1
    , "Variation 2": variation_2
    , "Variation 3": variation_3
}

def reset_counter():
    st.session_state.count = 0
    st.session_state.board = chess.Board()

def increment_counter():
    moves = dict_moves[st.session_state.variation]
    if st.session_state.count < len(moves):
        st.session_state.board.push_san(moves[st.session_state.count])
        st.session_state.count += 1

def decrement_counter():
    if st.session_state.count > 0:
        st.session_state.board.pop()
        st.session_state.count -= 1

def render_svg(col1):
    """Renders the given svg string."""
    svg = csvg.board(st.session_state.board, size=350)
    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
    #with display_area.container():
    col1.write(html, unsafe_allow_html=True)

st.session_state.variation = st.sidebar.selectbox(
    "Stafford Gambit:",["Variation " + str(x) for x in range(1, 7)], on_change=reset_counter)

left, right = st.sidebar.columns(2)
but_prev = left.button('Prev', on_click=decrement_counter)
but_next = right.button('Next', on_click=increment_counter)
# st.write('Count = ', st.session_state.count)
st.markdown("""### Stafford Gambit""")
#st.markdown("""---""")
st.write(st.session_state.variation)
col1, col2 = st.columns(2)
render_svg(col1)
col2.table(v3)

# display_area = st.empty()

