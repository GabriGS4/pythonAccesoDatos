# https://apuntes.de/python/expresiones-regulares-y-busqueda-de-patrones-en-python-poder-y-flexibilidad/#gsc.tab=0
# https://rico-schmidt.name/pymotw-3/pickle/index.html
# https://stackoverflow.com/questions/55809976/seek-on-pickled-data
# https://www.reddit.com/r/learnpython/comments/pgfj63/sorting_a_table_with_pysimplegui/
# https://www.geeksforgeeks.org/python-sorted-function/
# https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Table_Element_Header_or_Cell_Clicks.py
# https://github.com/PySimpleGUI/PySimpleGUI/issues/5646
# https://docs.python.org/3/howto/sorting.html


from SerializeFile import *
from Customer import *
import PySimpleGUI as sg
import re
import operator

fCustomer = 'Customer.json'
# fCustomer = open('Customer.dat', 'rb+')
lCustomer = []
pattern_email = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
pattern_ID = r"\d{3}"
pattern_phone = r"\d{3}-\d{6}"


def addCustomer(l_Customer, t_CustomerInterfaz, oCustomer, fCustomer):
    # Obtener la posFile del último cliente en la lista
    last_pos = l_Customer[-1].posFile if l_Customer else 0

    # Sumarle uno para la nueva posición del cliente
    new_pos = last_pos + 1

    # Actualizar la posFile del cliente antes de agregarlo a la lista
    oCustomer.posFile = new_pos
    l_Customer.append(oCustomer)
    saveCustomer(fCustomer, oCustomer)
    t_CustomerInterfaz.append(
        [oCustomer.ID, oCustomer.name, oCustomer.bill, oCustomer.phone, oCustomer.email, oCustomer.posFile])
    pass


def delCustomer(l_Customer, t_CustomerInterfaz, posinTable):
    if 0 <= posinTable < len(t_CustomerInterfaz):
        # Hacer algo con cdel si es necesario
        l_Customer.pop(posinTable)
        t_CustomerInterfaz.pop(posinTable)
        deleteCustomer(fCustomer, posinTable)
    pass


def updateCustomer(l_Customer, t_row_CustomerInterfaz, posinFile):
    cdel = next((customer for customer in l_Customer if customer.customerinPos(posinFile)), None)
    if cdel is not None:
        cdel.setCustomer(t_row_CustomerInterfaz[1], t_row_CustomerInterfaz[2], t_row_CustomerInterfaz[3],
                         t_row_CustomerInterfaz[4])
        modifyCustomer(fCustomer, cdel.posFile, cdel)
    pass


def sort_table(table, cols):
    """ sort a table by multiple columns
        table: a list of lists (or tuple of tuples) where each inner list
               represents a row
        cols:  a list (or tuple) specifying the column numbers to sort by
               e.g. (1,0) would sort by column 1, then by column 0
    """
    for col in reversed(cols):
        try:
            table = sorted(table, key=operator.itemgetter(col))
        except Exception as e:
            sg.popup_error('Error in sort_table', 'Exception in sort_table', e)
    return table


def interfaz():
    font1, font2 = ('Arial', 14), ('Arial', 16)
    sg.theme('DarkGrey4')
    sg.set_options(font=font1)
    table_data = []
    rowToUpdate = []
    readCustomer(fCustomer, lCustomer)
    for o in lCustomer:
        if (not o.erased):
            table_data.append([o.ID, o.name, o.bill, o.email, o.phone, o.posFile])

    layout = [
                 [sg.Push(), sg.Text('Game CRUD'), sg.Push()]] + [
                 [sg.Text(text), sg.Push(), sg.Input(key=key)] for key, text in Customer.fields.items()] + [
                 [sg.Push()] +
                 [sg.Button(button) for button in ('Add', 'Delete', 'Modify', 'Clear')] +
                 [sg.Push()],
                 [sg.Table(values=table_data, headings=Customer.headings, max_col_width=50, num_rows=10,
                           display_row_numbers=False, justification='center', enable_events=True,
                           enable_click_events=True,
                           vertical_scroll_only=False, select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                           expand_x=True, bind_return_key=True, key='-Table-')],
                 [sg.Button('Purge'), sg.Push(), sg.Button('Sort File')],
             ]
    sg.theme('Reddit')
    window = sg.Window('Customer Management with Files', layout, finalize=True)
    window['-PosFile-'].update(disabled=True)
    window['-Table-'].bind("<Double-Button-1>", " Double")
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == 'Add':
            valida = False
            if re.match(pattern_email, values['-Email-']):
                if re.match(pattern_ID, values['-ID-']):
                    if re.match(pattern_phone, values['-Phone-']):
                        valida = True
            if (valida):
                addCustomer(lCustomer, table_data,
                            Customer(values['-ID-'], values['-Name-'], values['-Bill-'], values['-Phone-'],
                                     values['-Email-'], -1), fCustomer)
                window['-Table-'].update(table_data)
        if event == 'Delete':
            if len(values['-Table-']) > 0:
                selected_index = int(values['-Table-'][0])
                delCustomer(lCustomer, table_data, selected_index)
                window['-Table-'].update(table_data)

        if (event == '-Table- Double'):
            if len(values['-Table-']) > 0:
                row = values['-Table-'][0]
                window['-ID-'].update(disabled=True)
                window['-ID-'].update(str(table_data[row][0]))
                window['-Name-'].update(str(table_data[row][1]))
                window['-Bill-'].update(str(table_data[row][2]))
                window['-Phone-'].update(str(table_data[row][3]))
                window['-Email-'].update(str(table_data[row][4]))
                window['-PosFile-'].update(str(table_data[row][5]))
            pass
        if event == 'Clear':
            window['-ID-'].update(disabled=False)
            window['-ID-'].update('')
            window['-Name-'].update('')
            window['-Bill-'].update('')
            window['-Phone-'].update('')
            window['-Email-'].update('')
            window['-PosFile-'].update('')
        if event == 'Modify':
            valida = False
            if re.match(pattern_email, values['-Email-']):
                if re.match(pattern_ID, values['-ID-']):
                    if re.match(pattern_phone, values['-Phone-']):
                        valida = True
            if valida:
                for t in table_data:
                    if t[-1] == int(values['-PosFile-']):
                        rowToUpdate = t
                        t[1], t[2], t[3], t[4] = values['-Name-'], values['-Bill-'], values['-Phone-'], values[
                            '-Email-']
                        break
                updateCustomer(lCustomer, rowToUpdate, int(values['-PosFile-']))
                window['-Table-'].update(table_data)
                window['-ID-'].update(disabled=False)
        if isinstance(event, tuple):
            # TABLE CLICKED Event has value in format ('-TABLE=', '+CLICKED+', (row,col))
            # You can also call Table.get_last_clicked_position to get the cell clicked
            if event[0] == '-Table-':
                if event[2][0] == -1:  # Header was clicked
                    col_num_clicked = event[2][1]
                    table_data = sort_table(table_data, (col_num_clicked, 0))
                    window['-Table-'].update(table_data)

    window.close()


interfaz()
