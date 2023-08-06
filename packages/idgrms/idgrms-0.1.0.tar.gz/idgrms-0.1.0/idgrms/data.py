"""
Read data from files, storage and cooperate with them.

"""
import numpy as np


def _read_file(filename, max_lines_number=None,
               comment_mark="#", data_type=float):
    try:
        with open(filename, 'r') as file_descriptor:
            file_content = np.genfromtxt(
                file_descriptor, max_rows=max_lines_number,
                comments=comment_mark, dtype=data_type, encoding="utf-8")
    except FileNotFoundError:
        print("File {} doesn't exist!".format(filename))
        exit(1)

    return file_content


def read_file_header(filename):
    """
    Read a one-line file header.

    Parameters
    ----------
    filename : str
        The name of the file which contains columns with integers and floats
        separated by spaces. The file must begin with a one-line header.
        The header should describe each column and begin with a single '#'
        sign then a space and the rest of columns labels.

    Returns
    -------
    file_header : ndarray
        A 1D array which elements are labels of each column.
    """
    file_header = _read_file(filename, max_lines_number=1,
                             comment_mark="//", data_type=None)

    return file_header[1:]


def read_file_content(filename):
    """
    Read a content of a file without a header.

    Parameters
    ----------
    filename : str
        The name of the file which contains columns with integers and floats
        separated by spaces. The first column should contain integers, the
        rest of them - floats. The file must begin with a one-line header.

    Returns
    -------
    file_content : ndarray
        A 2D array which elements are floats.
    """
    file_content = _read_file(filename)

    return file_content


def read_group_file(filename):
    """
    Read a content of a file.

    Parameters
    ----------
    filename : str
        The name of the file which contains one column with integers.

    Returns
    -------
    file_content : tuple
        A tuple which contains integers.
    """
    file_content = tuple(_read_file(filename, data_type=int))

    return file_content


def unique_columns_list(nested_lists):
    """
    Flatten the nested list (two levels) and leave unique elements.

    Parameters
    ----------
    nested_lists : list
        A list which contains sublists.

    Returns
    -------
    list
        A list with unique elements from sublists.
    """
    return list(set([item for sublist in nested_lists for item in sublist]))


def get_necessary_data_column(file_content, file_header, column_index):
    """
    Get a specific column from the ndarray object.

    Parameters
    ----------
    file_content : ndarray
        An array with floats values. The data should be read from a file.
    file_header : ndarray
        An array which stores a header from the file where file_content
        comes from.
    column_index : int
        Indicates which column to use.

    Returns
    -------
    tuple
        A tuple is made of the column index, the label of the column
        and the column's data stored in the masked_array.
    """
    index = abs(column_index) - 1
    column_data = np.ma.array([])
    column_data = np.append(column_data, file_content[:, index:index+1])

    return column_index, file_header[index], column_data


def get_data(filename, columns_argument):
    """
    Get specific columns with data.

    Parameters
    ----------
    filename : str
        The name of the file which contains columns with integers and floats
        separated by spaces. The first column should contain integers, the
        rest of them - floats. The file must begin with a one-line header.
    columns_argument : list
        A nested list which contains sublists. Each sublist is made of
        two integers. The numbers are indexes of columns to be used.

    Returns
    -------
    tuple
        A nested tuple contains subtuples. Each subtuple is made of
        the returned value by the get_necessary_data_column() function.
    """
    data = ()
    file_header = read_file_header(filename)
    file_content = read_file_content(filename)
    unique_columns = unique_columns_list(columns_argument)

    for column_index in unique_columns:
        data += (get_necessary_data_column(file_content, file_header,
                                           column_index),)

    return data


def list_iterator(list_argument):
    """
    Iterate over a number of list elements.

    Parameters
    ----------
    list_argument : list
        A list with elements.

    Returns
    -------
    range
        A range which iterates as many times as the number of elements.
    """
    return range(len(list_argument))


def current_data_indexes(data, two_columns_argument):
    """
    Transform the columns argument to the indexes of data tuple.

    Parameters
    ----------
    data : tuple
        A value returned by the get_data() function.
    two_columns_argument : list
        A list which contains two indexes of used columns - columns argument.

    Returns
    -------
    tuple
        A tuple which contains two indexes.
    """
    first_index = -1
    second_index = -1

    for index, column_data in enumerate(data):
        if two_columns_argument[0] == column_data[0]:
            first_index = index
        if two_columns_argument[1] == column_data[0]:
            second_index = index

    return first_index, second_index


def get_specific_data(data, columns):
    """
    Get specific information from data tuple.

    Parameters
    ----------
    data : tuple
        A value returned by the get_data() function.
    two_columns_argument : list
        A list which contains two indexes of used columns - columns argument.

    Returns
    -------
    tuple
        A tuple which is made of subtuples. Each subtuple contains information
        about values for X and Y axes. There are:
         - points
         - axes labels
         - axes orientation (negative value means reverted axis)
    """
    first_index, second_index = current_data_indexes(data, columns)
    axes_orientation = data[first_index][0], data[second_index][0]
    axes_labels = data[first_index][1], data[second_index][1]
    points_position = data[first_index][2], data[second_index][2]

    return (points_position, axes_labels, axes_orientation)


def get_marked_points(data, marked_data, columns):
    """
    Get specific points from data.

    Parameters
    ----------
    data : tuple
        A value returned by the get_data() function.
    marked_data : tuple
        A tuple which can contain subtuples or be empty. Each subtuple
        represents a set of points coming from a data column. The column is
        pointed by an index included in the columns variable.
    columns : list
        A list which contains two indexes of used columns - columns argument.

    Returns
    -------
    tuple
        A tuple which can contain subtuples. Each subtuple represents a set
        of points coming from a data column. The column is pointed by an index
        included in the columns variable.
    """
    if marked_data != ():
        first_index, second_index = current_data_indexes(data, columns)
        return marked_data[first_index], marked_data[second_index]
    else:
        return marked_data


def get_colored_points(data, colored_data, columns, groups_argument):
    """
    Get colored points from data.

    Parameters
    ----------
    data : tuple
        A value returned by the get_data() function.
    colored_data : tuple
        A tuple which can contain subtuples or be empty. Each subtuple
        contains masked_arrays with data only for colored points and a string
        which represents a color name.
    columns : list
        A list which contains two indexes of used columns - columns argument.
    group_argument : list
        A list which contains another lists, each one with two elements, a file
        name and a string with a color name.

    Returns
    -------
    tuple
        The same as colored_data but masks in the masked_arrays can be changed.
    """
    colored_points = ()

    if colored_data != ():
        first_index, second_index = current_data_indexes(data, columns)
        for i in list_iterator(groups_argument):
            single_group = ()
            single_group += (colored_data[i][first_index],
                             colored_data[i][second_index],
                             colored_data[i][-1])
            colored_points += (single_group,)

    return colored_points


def mark_points(data, marked_data_indexes):
    """
    Mark specific points.

    Parameters
    ----------
    data : tuple
        A value returned by the get_data() function.
    marked_data_indexes : ndarray
        An array containing indexes of points from data variable. The indexes
        come from marked points.

    Returns
    -------
    tuple
        A tuple with subtuples. Each subtuple contains points from data
        and is related to one index.
    """
    marked_data = ()

    if len(marked_data_indexes) == 0:
        return marked_data

    for single_data in data:
        dat = single_data[-1]
        marked_points = ()
        for index in marked_data_indexes:
            marked_points += (dat[index],)
        marked_data += (marked_points,)

    return marked_data


def feedback(all_data, marked_data_indexes):
    """
    Print information about marked point(s).

    Parameters
    ----------
    all_data : ndarray
        The whole data coming from the main input file without a header.
    marked_data_indexes : ndarray
        A list containing indexes of points from data variable. The indexes
        come from marked points.
    """
    for object_index, index in enumerate(marked_data_indexes):
        print("# object {}".format(object_index + 1))
        print(int(all_data[index][0]))
        for parameter in all_data[index][1:]:
            print(parameter)


# If the --grp option is switched on, use these functions.
def get_points_numbers(filename):
    """
    Get integers from the first column of a file.

    Parameters
    ----------
    filename : str
        The name of the file which contains columns with integers and floats
        separated by spaces. The first column should contain integers, the
        rest of them - floats. The file must begin with a one-line header.

    Returns
    -------
    tuple
        A tuple which contains integers from the first column.
    """
    file_content = read_file_content(filename)

    return tuple(file_content[:, 0:1].flatten().astype(int))


def get_single_group_data(points_numbers, filename, color_argument):
    """
    Transform integers from a file to indexes of points_numbers.

    Parameters
    ----------
    points_numbers : tuple
        Contains integers.
    filename : str
        The name of the file which contains column with integers.
    color_argument : str
        Define a color which marks particular integers from the file.

    Returns
    -------
    tuple
        A tuple which contains a tuple of points indexes and the color
        name at the end.
    """
    indexes = ()
    file_content = read_group_file(filename)

    for number in file_content:
        indexes += (points_numbers.index(number),)

    return (indexes, color_argument)


def get_group_data(data_filename, group_arguments):
    """
    Make a tuple which elements are returned values
    by the get_single_group_data() function.

    Parameters
    ----------
    data_filename : str
        The name of the file which contains columns with integers and floats
        separated by spaces. The first column should contain integers, the
        rest of them - floats. The file must begin with a one-line header.
     group_arguments : list
        A list which contains sublists. Each sublist is made of two
        strings. The first one points the name of another file with
        integers. The second is a color name.

    Returns
    -------
    tuple
        A tuple which contains subtuples. Each subtuple is made of
        the returned value by the get_single_group_data() function.
    """
    group_data = ()
    points_numbers = get_points_numbers(data_filename)

    for group_argument in group_arguments:
        group_data += (get_single_group_data(points_numbers, *group_argument),)

    return group_data


def get_color_data(data_filename, group_arguments, data):
    """
    Mark specific points.

    Parameters
    ----------
    data_filename : string
        The name of the file which contains columns with integers and floats
        separated by spaces. The file must begin with a one-line header.
        The header should describe each column and begin with a single '#'
        sign then a space and the rest of columns labels.
     group_arguments : list
        A list which contains another lists, each one with two elements, a file
        name and a string with a color name.
    data : tuple
        A value returned by the get_data() function.

    Returns
    -------
    tuple
        A tuple with subtuples. Each subtuple contains points from data
        in masked_arrays and the color name.
    """
    group_data = get_group_data(data_filename, group_arguments)
    color_data = ()

    for one_group_data in group_data:
        group = ()
        for one_column_data in data:
            group += np.take(one_column_data[-1], one_group_data[0]),
        group += one_group_data[-1],
        color_data += group,

    return color_data
