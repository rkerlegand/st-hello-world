import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import nfl_data_py as nfl
import os
import urllib.request
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
###
import plotly.express as px
import plotly.graph_objects as go
import adjustText

pbp = nfl.import_pbp_data([2023])
pbp = pd.DataFrame(pbp)

# Define the color palette
ggpalette = ["#F8766D", "#00BFC4", "#00BA38", "#9F8CFF", "#9DA700", "#00B4F0", "#F564E3", "#DE8C00"]
chosen_color = "#F8766D"  # Default color if not specified or invalid

#ggplot style
plt.style.use('ggplot')

# Set default plotting parameters
plt.rcParams['font.family'] = 'DejaVu Serif'
plt.rcParams['figure.figsize'] = (10, 10)
plt.rcParams['figure.dpi'] = 300

def ggscatter(x, y, data, title=None, xlabel=None, ylabel=None, label_col=None, color=None, hue=None, reference=None):

    # Set custom color palette
    sns.set_palette(ggpalette)

    # Set default labels if xlabel or ylabel is not provided
    xlabel = xlabel if xlabel is not None else x
    ylabel = ylabel if ylabel is not None else y

    if hue is not None:
      ax = sns.scatterplot(x=x, y=y, hue=hue, data=data, palette=ggpalette)
    else:

      # Choose a color from the palette based on the color index
      if color is not None and 1 <= color <= len(ggpalette):
          chosen_color = ggpalette[color - 1]
      else:
          chosen_color = "#F8766D"  # Default color if not specified or invalid

      # Create a scatter plot using Seaborn
      ax = sns.scatterplot(x=x, y=y, data=data, color=chosen_color)

    # Add data labels to the points if label_col is provided
    if label_col is not None:
        # Create a list of text objects
        texts = [plt.text(value, data[y].iloc[i], label, va='center', fontweight='bold', color='black')
                 for i, (value, label) in enumerate(zip(data[x], data[label_col]))]

        # Use adjust_text to automatically adjust text labels
        adjustText.adjust_text(texts, arrowprops=dict(arrowstyle='-', color='gray'), expand_text=(1.05, 1.2))

    # Show reference lines based on the reference option
    if reference == 'Fit':
        # Linear regression line with a confidence interval
        sns.regplot(x=x, y=y, data=data, scatter=False, color='black', ci=95, line_kws={'linestyle': '--'},
                    label=f'Best Fit ({xlabel} vs. {ylabel})')
    elif reference == 'Avgs':
        # Vertical reference line at the average of x
        ax.axvline(data[x].mean(), color='black', linestyle='--', linewidth=1, label=f'Average {xlabel}')
        # Horizontal reference line at the average of y
        ax.axhline(data[y].mean(), color='black', linestyle='--', linewidth=1, label=f'Average {ylabel}')

    # Set default title if title is not provided
    title = title if title is not None else f'{xlabel} vs {ylabel}'

    # Customize the axes and title
    ax.set_title(title, fontweight='bold')
    ax.set_xlabel(xlabel, fontweight='bold')
    ax.set_ylabel(ylabel, fontweight='bold')

    # Remove top and right borders
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Show the legend if reference lines are included
    if reference is not None:
        ax.legend()

    # Show the plot
    plt.show()
