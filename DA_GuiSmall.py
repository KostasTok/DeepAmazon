'''
Collection of small widgets used within a window.
Most are identical to the ones imported from 
PyQt5.QtWidgets in all apart from the StyleSheet.
'''

from PyQt5.QtWidgets import (QWidget, QPushButton, QLabel,
                             QDesktopWidget, QLineEdit,
                             QToolButton, QMenu, QAction,
                             QComboBox, QTableWidget,
                             QTableWidgetItem, QAbstractItemView)
from PyQt5.QtGui import (QFont, QIcon)
from PyQt5.QtCore import QSize
import PyQt5.QtCore as QtCore

class CenterWidget(QWidget):
    '''
    Simple adds the center function
    '''
    def __init__(self):
        super().__init__()
        self.center()
        
    def center(self):
        # Centers the window on the screen
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

class ComboBoxWithUpdate(QComboBox):
    '''
    QComboBox with an update attribute, which updates its 
    entries using the connected backend list.
    '''
    def __init__(self, parent, _list = None,
                 showEntry = None):
        '''
        _list --> list that is put in the ComboBox
        showEntry --> str with the entry of the list
                        that will be checked.
        '''
        super().__init__(parent)
        if _list is not None:
            self.updateList(_list)
            if showEntry is not None:
                self.setIndexWithText(showEntry)
    def updateList(self, _list, showEntry = None):
        self.clear()
        for i in _list:
            self.addItem(i)
        if showEntry is not None:
            self.setIndexWithText(showEntry)
        self.update()
    def setIndexWithText(self, text):
        '''
        text --> str in self._list
        Attempts to find 'text' in the loaded keys.
        If it does, it sets this as the checked one.
        '''
        i = self.findText(text)
        if i != -1:
            self.setCurrentIndex(i)
        
class LabelOfButton(QLabel):
    '''
    QLabel class with custom StyleSheet
    '''
    def __init__(self, text, parent = None):
        super().__init__()
        self.setText(text)
        self.setParent(parent)
        self.setStyleSheet("""
                QLabel{
                    border-style: none;
                    font-family: SansSerif;
                    font-size: 12px;
                    color: rgb(34, 39, 65);
                }""")

class ButtonIcon(QPushButton):
    '''
    Button of fixed size with icon. If icon
    is '-' or '+', then uses corresponding icons.
    Otherwise, give name of icon in 'resources/icons/'
    Size has first the size of the button, then that
    of the Icon.
    '''
    def __init__(self, icon, parent, size = [30, 15, 30, 15]):
        super().__init__('', parent)
        self.setStyleSheet("""
                QPushButton{
                    background-color: rgb(247, 247, 247);
                    border-width: 0px;
                    border-radius: 5px;
                }
                QPushButton:pressed{
                    background-color: rgb(180, 180, 180);
                    border-width: 0px;
                    border-radius: 5px;
                }
                QPushButton:disabled{
                    background-color: rgb(180, 180, 180);
                    border-width: 0px;
                    border-radius: 5px;  
                }""")
        if icon is '+':
            self.resize(35, 20)
            self.setIcon(QIcon('resources/icons/add.png'))
            self.setIconSize(QSize(30, 15))
        elif icon is '-':
            self.resize(35, 20)
            self.setIcon(QIcon('resources/icons/minus.png'))
            self.setIconSize(QSize(30, 15))
        else:
            try:
                self.resize(size[0], size[1])
                i = 'resources/icons/' + icon
                self.setIcon(QIcon(i))
                self.setIconSize(QSize(size[2], size[3]))
            except:
                self.resize(35, 20)
                self.setText('!')
                
class ButtonIconMenu(QToolButton):
    '''
    Define ToolButton with Icon, with two additional
    attributes, which can be used to add a popup menu,
    and to resize the button and its icon.
    '''
    def __init__(self, icon, parent):
        super().__init__(parent)
        
        self.setStyleSheet("""
                QToolButton{
                    background-color: rgb(247, 247, 247);
                    border-width: 0px;
                    border-radius: 5px;
                }
                QToolButton:pressed{
                    background-color: rgb(180, 180, 180);
                    border-width: 0px;
                    border-radius: 5px;
                }
                QToolButton:disabled{
                    background-color: rgb(180, 180, 180);
                    border-width: 0px;
                    border-radius: 5px;  
                }""")
        try:
            i = 'resources/icons/' + icon
            self.setIcon(QIcon(i))    
        except:
            self.setText('!')         
    def bindMenu(self, menu):
        '''
        Give Menu as a list of QActions. This will
        bind those action to QIconButtonMenu as a
        pop up menu.
        '''
        toolmenu = QMenu(self)
        for i in menu:
            toolmenu.addAction(i)
        self.setMenu(toolmenu)
        self.setPopupMode(QToolButton.InstantPopup)
    def setBtnIconSize(self, ButtonWidth, ButtonHeight, 
                       IconWidth, IconHeight):
        '''Sets the Size of the Button and its Icon'''
        self.resize(ButtonWidth, ButtonHeight)
        self.setIconSize(QSize(IconWidth, IconHeight))

class RectButton(QPushButton):
    '''
    QPushButton class with custom StyleSheet,
    used with text inside.
    '''
    def __init__(self, text, parent = None):
        super().__init__()
        
        self.setText(text)
        self.setParent(parent)
        self.setStyleSheet("""
                QPushButton{
                    background-color: rgb(231, 234, 235);
                    border: 0.5px solid rgb(34, 39, 65);
                    border-radius: 5px;
                    font-family: SansSerif;
                    font-size: 12px;
                    color: rgb(34, 39, 65);
                }
                QPushButton:pressed{
                    background-color: rgb(173, 173, 173);
                    border: 0.5px solid rgb(34, 39, 65);
                    border-radius: 5px;
                    font-family: SansSerif;
                    font-size: 12px;
                    color: rgb(34, 39, 65);
                }
                QPushButton:disabled{
                    background-color: rgb(173, 173, 173);
                    border: 0.5px solid rgb(34, 39, 65);
                    border-radius: 5px;
                    font-family: SansSerif;
                    font-size: 12px;
                    color: rgb(34, 39, 65);
                }""")

class InputLine(QLineEdit):
    '''
    QLineEdit with custom StyleSheet
    '''
    def __init__(self, text, parent = None):
        super().__init__()
        self.setText(text)
        self.setParent(parent)
        self.resize(QSize(60, 20))
        
class ButtonMenu(QToolButton):
    '''
    Same with QButtonMenu, but drop down menu allows
    for choice to remain there and multiple choices.
    options -> backend dictionary with boolean entries.
    Each key is used to define an action, and this is 
    checked or unchecked depending on the corresponding
    entry.
    '''
    def __init__(self, text, parent = None):
        super().__init__(parent)
        self.setText(text)
        self.setPopupMode(QToolButton.InstantPopup)
        self.setStyleSheet("""
                QToolButton{
                    background-color: rgb(231, 234, 235);
                    border: 0.5px solid rgb(34, 39, 65);
                    border-radius: 5px;
                    font-family: SansSerif;
                    font-size: 12px;
                    color: rgb(34, 39, 65);
                }
                QToolButton:pressed{
                    background-color: rgb(173, 173, 173);
                    border: 0.5px solid rgb(34, 39, 65);
                    border-radius: 5px;
                    font-family: SansSerif;
                    font-size: 12px;
                    color: rgb(34, 39, 65);
                }
                QToolButton:disabled{
                    background-color: rgb(173, 173, 173);
                    border: 0.5px solid rgb(34, 39, 65);
                    border-radius: 5px;
                    font-family: SansSerif;
                    font-size: 12px;
                    color: rgb(34, 39, 65);
                }""")
        
    def bindMenu(self, menu):
        '''
        Give Menu as a list or dict of QActions. This
        will bind those action to QIconButtonMenu as a
        pop up menu.
        '''
        # If dict was given, turns it into list
        menu2 = []
        toolmenu = QMenu(self)
        if isinstance(menu, list):
            menu2 = menu
        elif isinstance(menu, dict):
            for i in menu.keys():
                menu2.append(menu[i])
        # Creates toolmenu and binds it
        for i in menu2:
            toolmenu.addAction(i)
        self.setMenu(toolmenu)
        self.setPopupMode(QToolButton.InstantPopup)

class InstanceTable(QTableWidget):
    '''
    QTableWidget that also:
    1) takes list of labels in order to sets 
        HorizontalHearerLabels and ColumnCount.
    2) Defines refresh(), which uses given labels
        along with two dictionaries (inputs) to 
        contol what it shows.
    3) Defines selectedRows(), which returns list of
        selectedRows.
    4) Defines totalClear(), which clears not only
        labels and content, but also sets columns and
        rows to zero.
    '''
    def __init__(self, parent, labels, 
                 view = None, data = None):
        super().__init__(parent)
        
        # Stores labels and passes them to Headers
        self.labels = labels
        self.labelsCount = len(labels)
        self.setColumnCount(self.labelsCount)
        self.setHorizontalHeaderLabels(labels)
        
        # Uses refresh to pass to the table the
        # content it is initialised with.
        self.refresh(view, data)
        
        # Ensures that rows (not items) are selected, and that
        # the table is not editable directly from the user.
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
    def refresh(self, view = None, data = None):
        '''
        view --> dict of which the keys match those
        of self.labels. Set a key to False if you want
        the corresponding collumn to be hidden.
                 If None, then no column is shown.
        
        data --> list of which each entry is a dict with
        the same keys as self.labels. Each dict is used
        to populated one row.
        
        If data is not given, then it only changes which
        collumns are hidden.
        '''
        # If views has not given Hides all columns
        if view is None:
            for x in range(self.labelsCount):
                self.setColumnHidden(x, True)
        # Otherwise, sets columns according to view.
        else:
            for x in range(self.labelsCount):
                self.setColumnHidden(
                    x, not view[self.labels[x]]) 
        # Clears the table and loops through dictionaries
        # contains in data to update the entries of the table.
        if data is not None:
            self.clearContents()
            self.setRowCount(len(data))
            y = 0
            # loops through instances
            for d in data:
                # loops through labels
                for x in range(self.labelsCount):
                    item = QTableWidgetItem( 
                            d[self.labels[x]] )
                    self.setItem(y, x, item)
                y += 1
        else:
             self.setRowCount(0)
        # Ensures that GUI is updated.
        self.update()
    
    def inplaceRefresh(self, data):
        '''
        Same with refresh but it updates the table items
        instead of redefining the whole table. This does
        not affect the rows that are currently selected.
        '''
        # If data does not match row count, then inplace
        # Refresh was wrongly called and instead calls
        # the refresh function.
        if len(data) != self.rowCount():
            self.refresh(self, view = None, data = data)
        else:
            y = 0
            # loops through instances
            for d in data:
                # loops through labels
                for x in range(self.labelsCount):
                    self.item(y,x).setText(d[self.labels[x]])
                y += 1
            # Ensures that GUI is updated.
            self.update()
        
    def selectedRows(self):
        '''
        Returns list of rows that are selected. For example
        [0,1] for first and second row, or [] if not row is
        selected.
        '''
        # Obtains QObjects with the indexes of all selected
        # items.
        selectedItems = self.selectedIndexes()
        # Uses .row on each item of selectedIndexes to get
        # the row on which this item is.
        selectedRows = []
        for item in selectedItems:
            if item.row() not in selectedRows:
                selectedRows.append(item.row())
        return selectedRows
    
    def RowsFilter(self, label, values, sr = None):
        '''
        Returns list of the rows in 'sr' that 
        have value equal to one of the entries 
        of 'values' in the column with the given
        label.
        
        label --> str with the label of the column
        value --> str or list of str with the values
                    for which a match occurs
        sr --> list of indexes of rows to be filtered.
                If None, selectedRows is used.

        Any non existing label is ignored.
        '''
        # rows to filter is not given, then it
        # uses the ones currently selected.
        if sr is None:
            sr = self.selectedRows()
        # If str were given, turns them to lists
        if isinstance(values, str):
            values = [values]
        # Loops through rows. If the coresponding value
        # of a column matches one of values, then it
        # adds it to out.
        if label not in self.labels:
            return 'Error'
        else:
            out = []
            x = self.labels.index(label)
            # Loops through rows
            for y in sr:
                if self.item(y,x).text() in values:
                    out.append(y)
            return out
        
    def totalClear(self):
        '''
        Clears content, sets all rows to zero, and
        hides all columns.
        '''
        self.clearContents()
        self.setRowCount(0)
        for x in range(self.labelsCount):
            self.setColumnHidden(x, True)
        
            