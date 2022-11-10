import streamlit as st
import chess
from chess import svg as csvg
import base64
import pandas as pd

if 'count' not in st.session_state:
    st.session_state.count = 0

if 'board' not in st.session_state:
    st.session_state.board = chess.Board()

if 'last_move' not in st.session_state:
    st.session_state.last_move = ""

if 'orientation' not in st.session_state:
    st.session_state.orientation = chess.WHITE

dict_files = {
      "Variation 1": "config/sg_variation_1.csv"
    , "Variation 2": "config/sg_variation_2.csv"
    , "Variation 3": "config/sg_variation_3.csv"
    , "Variation 4": "config/sg_variation_4.csv"
    , "Variation 5": "config/sg_variation_5.csv"
    , "Variation 6": "config/sg_variation_6.csv"
    , "Variation 7": "config/sg_variation_7.csv"
    , "Fishing Pole Trap": "config/fishing_pole_trap.csv"
}

dict_moves = dict()
for k, v in dict_files.items():
    df_config = pd.read_csv(v)
    df_config.columns = [x.strip() for x in df_config.columns]
    variation = [x.strip() for xs in df_config.values.tolist() for x in xs]
    dict_moves[k] = variation


def reset_counter():
    st.session_state.count = 0
    st.session_state.board = chess.Board()
    st.session_state.last_move = ""

def increment_counter():
    moves = dict_moves[st.session_state.variation]
    if st.session_state.count < len(moves):
        st.session_state.last_move = st.session_state.board.push_san(moves[st.session_state.count])
        st.session_state.count += 1

def decrement_counter():
    if st.session_state.count > 0:
        st.session_state.last_move = st.session_state.board.pop()
        st.session_state.count -= 1

def render_svg(col1):
    """Renders the given svg string."""
    if st.session_state.last_move == "":
        svg = csvg.board(st.session_state.board,
                         orientation=st.session_state.orientation,
                         size=350)
    else:
        if st.session_state.board.is_check():
            svg = csvg.board(st.session_state.board,
                             orientation=st.session_state.orientation,
                             check=chess.Square(st.session_state.board.king(chess.WHITE)),
                             lastmove=st.session_state.last_move,
                             size=350)
        else:
            svg = csvg.board(st.session_state.board,
                             orientation=st.session_state.orientation,
                             lastmove=st.session_state.last_move,
                             size=350)

    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
    #with display_area.container():
    col1.write(html, unsafe_allow_html=True)

st.session_state.variation = st.sidebar.selectbox(
    "Select Variation", dict_files.keys(), on_change=reset_counter)

# st.write('Count = ', st.session_state.count)
st.markdown("""### Stafford Gambit""")
#st.markdown("""---""")
st.write(st.session_state.variation)
vv, xx, yy, aa = st.columns([2, 1, 1, 4])
but_prev = xx.button('<<', on_click=decrement_counter)
but_next = yy.button('>>', on_click=increment_counter)
orientation = vv.radio("Orient", ('White', 'Black'), horizontal=True)
col1, col2 = st.columns(2)
st.session_state.orientation = chess.WHITE if orientation == 'White' else chess.BLACK
render_svg(col1)
if st.session_state.board.is_check():
    if st.session_state.board.is_checkmate():
        col1.write('CHECK MATE!')
    else:
        col1.write('CHECK!')
df_config = pd.read_csv(dict_files[st.session_state.variation])
df_config.index += 1
col2.table(df_config)

# display_area = st.empty()
