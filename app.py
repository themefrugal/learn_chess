import streamlit as st
import chess
from chess import svg as csvg
import base64

board = chess.Board()

def render_svg(svg):
    """Renders the given svg string."""
    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
    st.write(html, unsafe_allow_html=True)

render_svg(csvg.board(board, size=350))

board.push_san("e4")

render_svg(csvg.board(board, size=350))
