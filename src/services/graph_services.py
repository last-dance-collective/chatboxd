import plotly.express as px
import streamlit as st
from enum import Enum

COLORS = {
  "GREEN": "#00D271",
  "BLUE": "#46C2F5",
  "ORANGE": "#323947"
}

class GRAPH_TYPES(Enum):
    RATING_DISTRIBUTION = "rating_distribution"

def display_rating_graph(ratings):
  if not ratings:
      st.write("No ratings to display.")
      return

  bins = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]

  fig = px.histogram(
      x=ratings,
      nbins=len(bins)-1,
      range_x=[0, 5],
      title='Histogram of Movie Ratings',
      labels={'x': 'Rating (0 - 5)', 'y': 'Cantidad de películas'},
      color_discrete_sequence=[COLORS["GREEN"]]
  )
  fig.update_layout(
      xaxis=dict(
          tickmode='array',
          tickvals=bins,
          title='Rating (0 to 5)'
      ),
      bargap=0.1
  )

  st.plotly_chart(fig)

GRAPHS_TYPES_DICT = {
    GRAPH_TYPES.RATING_DISTRIBUTION: display_rating_graph,
    
}
