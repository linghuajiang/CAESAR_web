import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from hirespy.attr.attribution import attribution as attr

try:
    import plotly.express as px
except:
    px = None


def interactive_scatter(data, out_file, sizes, names,
                        label=None, title=None, alpha=1, aes_label=None):
    """
    This function is to generate an interactive scatter plot of embedded single cell data.

    Parameters
    ----------
    data : numpy.array
        A numpy array which has 2 or 3 columns, every row represent a point.
    out_file : str
        Output file path.
    point_size : float, optional
        Set the size of the points in scatter plot.
        The default is 3.
    label : list or None, optional
        Specifiy the label of each point. The default is None.
    title : str, optional
        Title of the plot. The default is None.
    alpha : float, optional
        The alpha blending value. The default is 1.
    aes_label : list, optional
        Set the label of every axis. The default is None.
    """

    # Error messages.
    if px is None:
        raise ImportError('Need `plotly` installed to use function `interactive_scatter`.')
    if (label is not None) and len(data) != len(label):
        raise ValueError('Number of rows in data must equal to length of label!')

    # 2D scatter plot
    if aes_label is None:
        aes_label = ['x1', 'x2']

    # Plot with label
    if label is not None:
        df = pd.DataFrame({'position': names,
                           aes_label[0]: data[:, 0],
                           aes_label[1]: data[:, 1],
                           'label': label,
                           'size': sizes})
        df = df.astype({'label': 'category'})
        fig = px.scatter(df, x=aes_label[0], y=aes_label[1],
                         color="label", hover_data=['position'],
                         size="size",
                         opacity=alpha)
    # Plot without label
    else:
        df = pd.DataFrame({'position': names,
                           aes_label[0]: data[:, 0],
                           aes_label[1]: data[:, 1]})
        fig = px.scatter(df, x=aes_label[0], y=aes_label[1],
                         hover_data=['position'], opacity=alpha)

    fig.update_traces(selector=dict(mode='markers'))

    fig.update_layout(title=title)

    fig.write_html(out_file)


def plot_new_stripe(coordinate=[0, 0], output='interactive.html'):
    """
    Args:
        coordinate(list or numpy array): the 2-D embedding of the stripe's attribution result

    Return:
        No return. Generate a .html file.
    """
    names = [line.strip() for line in open('emb_names.txt')] + ['Your chosen stripe']

    label = np.loadtxt('emb_labels.txt', dtype=int)
    label = np.concatenate([label, np.array([1 + np.max(label)])])

    data = np.loadtxt('emb_TSNE.txt')
    data = np.concatenate([data, np.array([coordinate])], axis=0)

    sizes = [3] * len(data)
    sizes[-1] = 15

    interactive_scatter(data, output, label=label, sizes=sizes, names=names)


def embed_attributions(attributions=None):
    """
    Calculate the embedding results for a region's attribution results

    Args:
        attributions

    Return:
        embedding results (a 2-D vector)

    """
    # To be implemented
    return [0, 0]


plot_new_stripe(embed_attributions(a))


