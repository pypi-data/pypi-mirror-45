"""
This module is responsible for creating, drawing, displaying, saving
and connecting all independent windows of interactive diagrams.

"""
from numpy import array_equal
from matplotlib import pyplot as plt
from matplotlib.widgets import Button
from idgrms.data import (list_iterator, get_specific_data, get_marked_points,
                         get_colored_points, get_color_data, get_data,
                         mark_points, read_file_content, feedback)


image_number = 0
marked_data_indexes = None


def get_figures(columns_argument, talk_argument, all_data):
    """
    Generate a tuple with figures.

    Parameters
    ----------
    columns_argument : list
        A nested list which contains sublists. Each sublist is made of
        two integers. The numbers are indexes of columns to be used.
    talk_argument : bool
        This value is resposible for displaying the feedback button.
    all_data : ndarray
        An array which stores all information about data taken from
        an input file.

    Returns
    -------
    tuple
        A tuple which contains figures for all displayed windows. Each figure
        is an object of matplotlib.figure.Figure class.
    """
    figures = ()
    global marked_data_indexes

    for _ in list_iterator(columns_argument):
        figure = plt.figure()
        axis = figure.add_subplot(111)
        plt.subplots_adjust(bottom=0.15)
        axis.save = plt.axes([0.125, 0.05, 0.15, 0.05])
        axis.save_button = Button(axis.save, 'Snapshot')

        if not talk_argument:
            axis.info = plt.axes([0.75, 0.05, 0.15, 0.05])
            axis.info_button = Button(axis.info, 'Feedback')
            axis.info_button.on_clicked(
                lambda event: feedback(all_data, marked_data_indexes))

        figures += figure,

    return figures


def draw_all_figures(filename, figures, data, columns_argument,
                     groups_argument, marked_data=(), colored_data=(),
                     save_images=False):
    """
    This function triggers displaying or saving to files all diagrams.

    Parameters
    ----------
    filename : str
        The name of the file which contains columns with integers and floats
        separated by spaces. The first column should contain integers, the
        rest of them - floats.
    figures : tuple
        A tuple with figures returned by the get_figures() function.
    data : tuple
        A nested tuple contains subtuples. Each subtuple is made of the column
        index, the label of the column and the column's data stored in the
        masked_array.
    columns_argument : list
        A nested list which contains sublists. Each sublist is made of
        two integers. The numbers are indexes of columns to be used.
    groups_argument : list
        A list which contains sublists. Each sublist is made of two
        strings. The first one points the name of another file with
        integers. The second is a color name.
    marked_data : tuple
        A tuple which can contain subtuples or be empty. Each subtuple
        represents a set of points coming from a data column.
    colored_data : tuple
        A tuple which can contain subtuples or be empty. Each subtuple
        contains masked_arrays with data only for colored points and a string
        which represents a color name.
    save_images : bool
        A switch between displaying windows and saving images to PNG files.
    """
    for figure, columns in zip(figures, columns_argument):
        points, axes_labels, axes_orientation = (
            get_specific_data(data, columns))
        marked_points = get_marked_points(data, marked_data, columns)
        colored_points = get_colored_points(data, colored_data, columns,
                                            groups_argument)

        figure.axes[0].cla()
        set_axes_labels(figure, axes_labels, len(data[-1][-1]))
        set_axes_orientation(figure, axes_orientation)

        if save_images:
            save_diagram(filename, figure, points, axes_labels,
                         marked_points, colored_points)
        else:
            plot_diagram(figure, points, marked_points, colored_points)


def set_axes_labels(figure, axes_labels, points_number):
    """
    Set labels of axes for a single diagram.

    Parameters
    ----------
    figure : matplotlib.figure.Figure
        A single figure.
    axes_labels : tuple
        A tuple with two elements. Each one is a string which describes
        a single axis of a diagram.
    points_number : int
        A number of points used to construct one diagram.
    """
    figure.axes[0].set_title("Diagram for " + str(points_number) + " points",
                             fontsize=20)
    figure.axes[0].set_xlabel(axes_labels[0], fontsize=15)
    figure.axes[0].set_ylabel(axes_labels[1], fontsize=15)


def set_axes_orientation(figure, axes_orientation):
    """
    Set orientation of axes for a single diagram.

    Parameters
    ----------
    figure : matplotlib.figure.Figure
        A single figure.
    axes_orientation : tuple
        A tuple made of two integers indicating which columns of data to use
        to construct a single diagram. If a number is negative it means to
        revert an axis.
    """
    if axes_orientation[0] < 0:
        figure.axes[0].invert_xaxis()
    if axes_orientation[1] < 0:
        figure.axes[0].invert_yaxis()


def plot_diagram(figure, points=(), marked_points=(), colored_points=()):
    """
    Plot a single diagram.

    Parameters
    ----------
    figure : matplotlib.figure.Figure
        A single figure.
    points : tuple
        A tuple made of two masked_arrays. The arrays store x, y coordinates
        of each point which is plotted on a diagram.
    marked_points : tuple
        A tuple made of two subtuples. Each subtuple stores x, y coordinates
        of each marked point, respectively.
    colored_points : tuple
        A tuple made of three subtuples. Each subtuple stores x, y coordinates
        and a string with color name, respectively. A single coordinate is
        stored in a masked_array.
    """
    ax = figure.axes[0]
    ax.scatter(points[0], points[1], 60, c='gray', alpha=0.4, zorder=1)

    if marked_points != ():
        ax.scatter(marked_points[0], marked_points[1], 100, c='red',
                   alpha=1.0, zorder=3)
    if colored_points != ():
        for cp in colored_points:
            ax.scatter(cp[0], cp[1], 60, c=cp[2], alpha=0.6, zorder=2)

    ax.scatter(points[0], points[1], 50, alpha=0.0, picker=3)
    figure.canvas.draw_idle()


def save_all_figures(filename, data, columns_argument, groups_argument,
                     marked_data=(), colored_data=(), save_images=True):
    """
    Save all diagrams to image files.

    Parameters
    ----------
    filename : str
        The name of the file which contains columns with integers and floats
        separated by spaces. The first column should contain integers, the
        rest of them - floats.
    data : tuple
        A nested tuple contains subtuples. Each subtuple is made of the column
        index, the label of the column and the column's data stored in the
        masked_array.
    columns_argument : list
        A nested list which contains sublists. Each sublist is made of
        two integers. The numbers are indexes of columns to be used.
    groups_argument : list
        A list which contains sublists. Each sublist is made of two
        strings. The first one points the name of another file with
        integers. The second is a color name.
    marked_data : tuple
        A tuple which can contain subtuples or be empty. Each subtuple
        represents a set of points coming from a data column.
    colored_data : tuple
        A tuple which can contain subtuples or be empty. Each subtuple
        contains masked_arrays with data only for colored points and a string
        which represents a color name.
    save_images : bool
        A switch between displaying windows and saving images to PNG files.
        Default is True.
    """
    figures = ()
    global image_number
    image_number += 1

    for _ in list_iterator(columns_argument):
        figure = plt.figure()
        axis = figure.add_subplot(111)
        figures += figure,

    draw_all_figures(filename, figures, data, columns_argument,
                     groups_argument, marked_data, colored_data, save_images)


def save_diagram(filename, figure, points, axes_labels, marked_points=(),
                 colored_points=()):
    """
    Save current diagrams to the PNG images.

    Parameters
    ----------
    filename : str
        The name of the file which contains columns with integers and floats
        separated by spaces. The first column should contain integers, the
        rest of them - floats.
    figure : matplotlib.figure.Figure
        A single figure.
    points : tuple
        A tuple made of two masked_arrays. The arrays store x, y coordinates
        of each point which is plotted on a diagram.
    marked_data : tuple
        A tuple which can contain subtuples or be empty. Each subtuple
        represents a set of points coming from a data column.
    colored_data : tuple
        A tuple which can contain subtuples or be empty. Each subtuple
        contains masked_arrays with data only for colored points and a string
        which represents a color name.
    """
    ax = figure.axes[0]
    ax.scatter(points[0], points[1], 60, c='gray', alpha=0.4, zorder=1)

    if marked_points != ():
        ax.scatter(marked_points[0], marked_points[1], 100, c='red',
                   alpha=1.0, zorder=3)
    if colored_points != ():
        for cp in colored_points:
            ax.scatter(cp[0], cp[1], 60, c=cp[2], alpha=0.6, zorder=2)

    ax.scatter(points[0], points[1], 50, alpha=0.0, picker=3)
    filename = saved_filename(filename, axes_labels)
    figure.set_size_inches(10.0, 10.0, forward=True)
    figure.savefig(filename)
    plt.close(figure)


def saved_filename(filename, axes_labels):
    """
    Generate a filename of the PNG image.

    Parameters
    ----------
    filename : str
        The name of the file which contains columns with integers and floats
        separated by spaces. The first column should contain integers, the
        rest of them - floats.
    axes_labels : tuple
        A tuple with two elements. Each one is a string which describes
        a single axis of a diagram.

    Returns
    -------
    save_filename : string
        A name of a file to save as a PNG image.
    """
    global image_number
    save_filename = (filename + "_" + axes_labels[1] + "_" + axes_labels[0]
                     + "_" + str(image_number) + ".png")

    return save_filename


def connect_figures(filename, figures, all_data, data,
                    columns_argument, groups_argument, talk_argument,
                    marked_data=(), colored_data=()):
    """
    Create a connection between all figures.
    """
    def pick_point(event):
        global marked_data_indexes

        if array_equal(marked_data_indexes, event.ind):
            marked_data_indexes = ()
        else:
            marked_data_indexes = event.ind
        marked_data = mark_points(data, marked_data_indexes)
        draw_all_figures(filename, figures, data,
                         columns_argument, groups_argument,
                         marked_data, colored_data)

        if talk_argument:
            feedback(all_data, marked_data_indexes)

    for figure in figures:
        figure.axes[0].save_button.on_clicked(
            lambda event: save_all_figures(
                filename, data, columns_argument, groups_argument,
                mark_points(data, marked_data_indexes), colored_data))
        figure.canvas.mpl_connect('pick_event', pick_point)


def trigger_windows(filename, columns_argument, groups_argument,
                    talk_argument):
    """
    Generate a tuple with figures, i.e. diagrams.

    Parameters
    ----------
    filename : str
        The name of the file which contains columns with integers and floats
        separated by spaces. The first column should contain integers, the
        rest of them - floats.
    columns_argument : list
        A nested list which contains sublists. Each sublist is made of
        two integers. The numbers are indexes of columns to be used.
    groups_argument : list
        A list which contains sublists. Each sublist is made of two
        strings. The first one points the name of another file with
        integers. The second is a color name.
    talk_argument : bool
        This value is resposible for displaying the feedback button.
    """
    all_data = read_file_content(filename)
    figures = get_figures(columns_argument, talk_argument, all_data)
    data = get_data(filename, columns_argument)

    if groups_argument:
        colors = get_color_data(filename, groups_argument, data)
        draw_all_figures(filename, figures, data, columns_argument,
                         groups_argument, colored_data=colors)
        connect_figures(filename, figures, all_data, data, columns_argument,
                        groups_argument, talk_argument, colored_data=colors)
    else:
        draw_all_figures(filename, figures, data, columns_argument,
                         groups_argument)
        connect_figures(filename, figures, all_data, data, columns_argument,
                        groups_argument, talk_argument)

    plt.show()
