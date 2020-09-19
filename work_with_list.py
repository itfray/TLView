def lists_are_diff(list1: list, list2: list, *indices)-> bool:
    """ The function checks the differences
        elements of lists at the specified indices.
        * indices - a tuple of indices of the elements to check; """
    if len(list1) != len(list2):
        raise ValueError("Lists should have same length!!!")
    for index in indices:
        if list1[index] != list2[index]:
            return True
    return False

def tables_difference(table1: list, table2: list, *columns) -> list:
    """ The function searches for rows of the first
        table that are not in the second table.
        * columns - a tuple of columns of the table to check rows;"""
    answer = []                         # a list of the rows first table that haven't in second table
    for i in range(len(table1)):
                                        # count of the rows table2 that different from table1 row
        count = 0
        for j in range(len(table2)):
            if lists_are_diff(table1[i], table2[j], *columns):
                count += 1
        # if all rows table2 diferent from table1 row
        if count == len(table2):
            answer.append(table1[i])
    return answer


def updated_rows(old_table: list, new_table: list, indexes_id: tuple, indexes_cmp: tuple) -> list:
    """ The function сhecks the rows of the old table that are updated in the new table.
        * indexes_id - indexes identifying a row in a table;
        * indexes_cmp - data indexes in which to compare. These are the indices of the elements
          for which the data could be updated; """
    answer = []
    for i in range(len(old_table)):
        for j in range(len(new_table)):
            if not lists_are_diff(old_table[i], new_table[j], *indexes_id) and \
                    lists_are_diff(old_table[i], new_table[j], *indexes_cmp):
                answer.append(old_table[i])
    return answer
