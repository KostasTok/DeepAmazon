'''
Collection of classes used to build the GUI.
'''

from PyQt5.QtWidgets import (QWidget, QToolTip, QMessageBox,
                             QFrame, QDesktopWidget, QComboBox,
                             QGridLayout, QTableWidget, QDialog)
from PyQt5.QtWidgets import (QToolButton, QMenu)
from PyQt5.QtGui import (QFont, QIcon)
from PyQt5.QtCore import QSize
from DA_GuiSmall import *
from DA_GuiDialogs import *

class Main(CenterWidget):
    '''
    Class of first windon that appears.
    '''
    def __init__(self, app, backend):
        super().__init__()
        
        self.app = app
        self.backend = backend
        self.refresher = None
        
        # Creates GUI of main Window
        self.setGeometry(300, 300, 550, 450) # X, Y, width , height             
        self.setWindowTitle('DeepAmazom')
        self.create_GuiButtonGrid()
        self.create_GuiTop()
        self.create_GuiMid()
        self.create_GuiBottom()
                
        # Creates the Actions that connect the backend with
        # the frontend, and binds them to GUI elements
        self.connect_Actions()
        self.setEnabledStates(False)
        
        self.show()
    
    # ========  Below the four functions that  ========
    # ========  create the GUI are defined     ========  
    def create_GuiButtonGrid(self):
        '''
        Sets distances of elements that appear in GuiTop and GuiMid
        '''
        # vertical distance from top for:
        self.v_lab = 15  # label
        self.v_btn = 35  # buttons
        self.v_com = 31  # Comboboxes
        
        # hor. distance from left beginning for:
        self.h_btn1 = 15              # 1st button
        self.h_com1 = self.h_btn1+90  # 1st combobox
        self.h_btn2 = self.h_com1+150 # 2nd button
        self.h_com2 = self.h_btn2+80  # 2nd combobox
        self.h_btn3 = self.h_com2+150 # 3rd button
        
    def create_GuiTop(self):
        '''
        Creates top container that contains the buttons and options
        necessary to log in to AWS account with AWS credentials. It
        also creates the corresponding buttons, labels, etc...
        '''
        # Container on top
        self.GuiTop = QFrame(self)
        self.GuiTop.resize(550, 75)
        self.GuiTop.setStyleSheet("""
                QFrame{
                    background-color: rgb(219, 219, 219);
                    border: 0px solid rgb(100, 100, 100);
                    border-bottom-width: 0.5px;
                }""")
        
        # Connect button and label
        self.GuiConnectLabel = LabelOfButton('Connect', self.GuiTop)
        self.GuiConnectLabel.move(self.h_btn1, self.v_lab)
        self.GuiConnect = ButtonIcon('aws-connect.png', self.GuiTop,
                                      [55, 18, 50, 13])
        self.GuiConnect.move(self.h_btn1, self.v_btn)
        self.GuiConnect.setToolTip('Connect with AWS Credentials')
        
        # Access Key, label, drop down menu, and actions button
        self.GuiAccessKeyLabel = LabelOfButton('Access Keys', self.GuiTop)
        self.GuiAccessKeyLabel.move(self.h_com1+15, self.v_lab)
        self.GuiAccessKey = ComboBoxWithUpdate(
                                    self.GuiTop,
                                    self.backend.user_data.profile)
        self.GuiAccessKey.move(self.h_com1, self.v_com)
        self.GuiAccessKey.resize(130, 30)
        self.GuiAccessKey.setToolTip('Access Key used to connect with AWS')
        self.GuiAccessKeyBtn = ButtonIconMenu('gear.png', self.GuiTop)
        self.GuiAccessKeyBtn.setBtnIconSize(40, 20, 35, 16)
        self.GuiAccessKeyBtn.move(self.h_btn2, self.v_btn)
        self.GuiAccessKeyBtn.setToolTip('Add or delete Access Key Pairs.') 
        
        # Region drop down menu and label
        self.GuiRegionsLabel = LabelOfButton('Regions', self.GuiTop)
        self.GuiRegionsLabel.move(self.h_com2+15, self.v_lab)
        self.GuiRegions = ComboBoxWithUpdate(
                            self.GuiTop,
                            self.backend.user_data.ec2_regions,
                            self.backend.user_data.default_region)
        self.GuiRegions.move(self.h_com2, self.v_com)
        self.GuiRegions.resize(130, 30)
        self.GuiRegions.setToolTip('Region with which the connection opens.')
            
        # Help button and label
        self.GuiHelp = ButtonIcon('questionmark.png', self.GuiTop,
                                      [35, 20, 30, 15])
        self.GuiHelp.move(self.h_btn3, self.v_btn)
        self.GuiHelp.setToolTip('Help Menu')
    
    def create_GuiMid(self):
        '''
        Creates container with information on existing
        key pairs and security groups.
        '''
        self.GuiMid = QFrame(self)
        self.GuiMid.move(0, 75)
        self.GuiMid.resize(550, 75)
        self.GuiMid.setStyleSheet("""
                QFrame{
                    background-color: rgba(235, 240, 243, 1);
                    border: 0px solid rgb(100, 100, 100);
                }""")
        
        # Disconnect button and label
        self.GuiDisconnectLabel = LabelOfButton('Disconnect', self.GuiMid)
        self.GuiDisconnectLabel.move(self.h_btn1, self.v_lab)
        self.GuiDisconnect = ButtonIcon('aws-connect.png', self.GuiMid,
                                      [55, 18, 50, 13])
        self.GuiDisconnect.move(self.h_btn1, self.v_btn)
        self.GuiDisconnect.setToolTip('Disconnect from session.')
        
        
        # Key Pairs drop down menu and label
        self.GuiKeyPairLabel = LabelOfButton('Key Pairs', self.GuiMid)
        self.GuiKeyPairLabel.move(self.h_com1+15, self.v_lab)
        self.GuiKeyPair = ComboBoxWithUpdate(
                                self.GuiMid,
                                self.backend.key_pairs)
        self.GuiKeyPair.move(self.h_com1, self.v_com)
        self.GuiKeyPair.resize(130, 30)
        self.GuiKeyPair.setToolTip('Key Pairs used with AWS instances')
        self.GuiKeyPairBtn = ButtonIconMenu('gear.png', self.GuiMid)
        self.GuiKeyPairBtn.setBtnIconSize(40, 20, 35, 16)
        self.GuiKeyPairBtn.move(self.h_btn2, self.v_btn)
        self.GuiKeyPairBtn.setToolTip(
            'Create or delete a Key Pair to connect with an instance') 
        
        # Security Groups drop down menu and label
        self.GuiSecurityLabel = LabelOfButton('Security Groups', self.GuiMid)
        self.GuiSecurityLabel.move(self.h_com2+15, self.v_lab)
        self.GuiSecurity = ComboBoxWithUpdate(
                                self.GuiMid,
                                self.backend.security_groups)
        self.GuiSecurity.move(self.h_com2, self.v_com)
        self.GuiSecurity.resize(130, 30)
        self.GuiSecurity.setToolTip('Access Key used to connect with AWS')
        self.GuiSecurityBtn = ButtonIconMenu('gear.png', self.GuiMid)
        self.GuiSecurityBtn.setBtnIconSize(40, 20, 35, 16)
        self.GuiSecurityBtn.move(self.h_btn3, self.v_btn)
        self.GuiSecurityBtn.setToolTip('Create or delete a Security Group')
        
    def create_GuiBottom(self):
        '''
        Creates container with options to launch, stop instance, ..,
        list of instances running, and information on each instances
        '''
        self.GuiBottom = QFrame(self)
        self.GuiBottom.move(0, 150)
        self.GuiBottom.resize(550, 280)
        self.GuiBottom.setStyleSheet("""
                QFrame{
                    background-color: rgba(235, 240, 243, 1);
                    border: 0.5px solid rgb(100, 100, 100);
                }""")
        
        v_dist_btn = 25 # vert dist of btns from top of frame
        
        # Launch Instance button
        self.GuiInstanceLaunch = RectButton('Launch Instance', self.GuiBottom)
        self.GuiInstanceLaunch.move(15, v_dist_btn)
        self.GuiInstanceLaunch.resize(110, 30)
        self.GuiInstanceLaunch.setToolTip('Launch new instance')
        
        # Stop, terminate button
        self.GuiInstanceActions = ButtonMenu('Actions',
                                                    self.GuiBottom)
        self.GuiInstanceActions.move(145, v_dist_btn)
        self.GuiInstanceActions.resize(110, 30)
        self.GuiInstanceActions.setToolTip(
                        'Start, stop, or terminate an instance')
        # Drop down menu which can be used to choose what info
        # appear for the running instances.
        self.GuiInstanceView = ButtonMenu('View Options', 
                                                    self.GuiBottom)
        self.GuiInstanceView.move(275, v_dist_btn)
        self.GuiInstanceView.resize(110, 30)
        self.GuiInstanceView.setToolTip(
            'Choose columns that appear on the table of the running instances')
        
        # Connection Report Label with icon
        self.GuiStateReport = StateReport(self.GuiBottom)
        self.GuiStateReport.move(430, v_dist_btn-17)
        
        # Instances Table
        labels = list(self.backend.user_data.InstanceView.keys())
        self.GuiInstances = InstanceTable(self.GuiBottom, labels)
        self.GuiInstances.setStyleSheet("""
                    QTableWidget{
                        background-color: rgb(250, 250, 250);
                    }""")
        self.GuiInstances.move(0, 80)
        self.GuiInstances.resize(550,200)
        
    # ========  Below Actions are defined and binded  ========
    # ========  to the GUI objects of main window     ========    
    def connect_Actions(self):
        '''
        Here the action that are defined in the next
        def's are connected to the GUI.
        '''
        # Actions of GuiTop:
        #    GuiConnect Button
        self.GuiConnect.clicked.connect(self.ActConnect)
        #    GuiAccessKey Button
        self.ActAccessKeyBtnAdd = QAction('Add', self)
        self.ActAccessKeyBtnAdd.triggered.connect(
                                    self.ActAccessKeyWinAdd)
        self.ActAccessKeyBtnDelete = QAction('Delete', self)
        self.ActAccessKeyBtnDelete.triggered.connect(
                                    self.ActAccessKeyWinDelete)
        self.GuiAccessKeyBtn.bindMenu([self.ActAccessKeyBtnAdd,
                                       self.ActAccessKeyBtnDelete])
        #    GuiHelp Button
        self.GuiHelp.clicked.connect(self.ActHelp)
        
        # Actions of GuiMid:
        #    GuiDisconnect Button 
        self.GuiDisconnect.clicked.connect(self.ActDisconnect)
        #    GuiKeyPair Button
        self.ActKeyPairBtnAdd = QAction('Add', self)
        self.ActKeyPairBtnAdd.triggered.connect(
                                    self.ActKeyPairCreate)
        self.ActKeyPairBtnDelete = QAction('Delete', self)
        self.ActKeyPairBtnDelete.triggered.connect(
                                    self.ActKeyPairDelete)
        self.GuiKeyPairBtn.bindMenu([self.ActKeyPairBtnAdd,
                                     self.ActKeyPairBtnDelete])
        #    GuiSecurity Button
        self.ActSecurityBtnCreate = QAction('Create', self)
        self.ActSecurityBtnCreate.triggered.connect(
                                    self.ActSecurityCreate)
        self.ActSecurityBtnDelete = QAction('Delete', self)
        self.ActSecurityBtnDelete.triggered.connect(
                                    self.ActSecurityDelete)
        self.GuiSecurityBtn.bindMenu([self.ActSecurityBtnCreate,
                                      self.ActSecurityBtnDelete])
        
        # Actions of GuiBottom:
        #    GuiInstanceView Button
        self.ActInstanceViewCreateMenu()
        self.GuiInstanceView.bindMenu(self.ActInstanceView)
        #    GuiInstanceActions Button
        self.ActInstanceActionsCreateMenu()
        self.GuiInstanceActions.bindMenu(self.ActInstanceActions)
        #    GuiInstanceLaunch Button
        self.GuiInstanceLaunch.clicked.connect(self.ActInstanceLaunch)
        
        # Defines Refresher that periodically updates GuiInstances
        # and the corresponding backend object.
        self.refresher = MainRefresher(1, self)
        
    # ==================== GuiTop Actions ====================
    # ========================================================  
    def ActConnect(self):
        '''
        Triggered by: GuiConnect
        1) Checks using the backend if connection is possible
        2) Reports error, and resets enabled states of buttons
        '''
        error = self.backend.connect(self.GuiAccessKey.currentText(),
                                           self.GuiRegions.currentText())
        if error == 'NoAccessKey':
            error_msg = 'Access Key has not been provided.'
            QMessageBox.information(self, 'Error', error_msg, QMessageBox.Ok)
        elif error == 'WrongCredentials':
            error_msg = 'Could not match name with credentials. Possible bug.'
            QMessageBox.information(self, 'Error', error_msg, QMessageBox.Ok)
        elif error == 'ConnectionError':
            error_msg = 'Not able to establish connection.'
            QMessageBox.information(self, 'Error', error_msg, QMessageBox.Ok)
        elif error == 'DescribeError':
            msg1 = 'A connection was successfully established, but'
            msg2 = ' there was an error while requesting data from AWS.'
            msg3 = '\n\nPossible bug because of an update on'
            msg4 = ' a describe_someitem() method.'
            error_msg = msg1+msg2+msg3+msg4
            QMessageBox.information(self, 'Error', error_msg, QMessageBox.Ok)
        else:
            self.backend.user_data.default_region = self.GuiRegions.currentText()
            self.setEnabledStates(True)
            self.GuiKeyPair.updateList(self.backend.key_pairs)
            self.GuiSecurity.updateList(self.backend.security_groups)
            self.backend.user_data.get_AmiNames(self.backend.client)
            self.refresher.on()
            
    def ActHelp(self):
        '''
        Triggered by: GuiHelp
        1) Popups a window with some basic instructions on
            how to use the Main window.
        '''
        a1 = 'This application provides a Graphic Interface in order to'
        a2 = ' use some common features of boto3. Some knowledge of'
        a3 = ' boto3 is necessary in order to understand what each'
        a4 = ' of the GUI is doing.'
        A = a1+a2+a3+a4+'\n\n'
        b1 = 'Access Keys: Those can be obtained from AWS once you logged'
        b2 = ' in. When adding a Key you are also requested to select a'
        b3 = ' name for it.'
        B = b1+b2+b3+'\n\n'
        C = '...To be written.'
        text = A+B+C
        QMessageBox.information(self, 'Help', text, QMessageBox.Ok)
        
    def ActAccessKeyWinAdd(self):
        '''
        Triggered by: GuiAccessKey --> Add
        1) Opens Window that allows user to Add new Access Key. 
        2) Using Backend it ensures that this is valid.
        '''
        x = self.mapToGlobal(QPoint(0,0)).x()
        y = self.mapToGlobal(QPoint(0,0)).y()
        GuiAccessKeyWinAdd = AccessKeyAddWindow(x, y, self.backend)
        if GuiAccessKeyWinAdd.Added:
            self.GuiAccessKey.updateList(self.backend.user_data.profile)
        del GuiAccessKeyWinAdd
        
    def ActAccessKeyWinDelete(self):
        '''
        Triggered by: GuiAccessKey --> Delete
        1) Opens message box to confirm delete of Access Key selected
            on GuiAccessKey (QCombobox).
        2) Deletes it from both GuiAccessKey and Backend.
        '''
        if len(self.backend.user_data.profile) == 0:
            error_msg = 'There is no Access Key to Delete.'
            QMessageBox.information(self, 'Error', error_msg, QMessageBox.Ok)
        else:
            msg = 'Are you sure you want to delete the selected Access Key?'
            buttonReply = QMessageBox.question(self, 'Warning',
                            msg, QMessageBox.Yes|QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                self.backend.user_data.delete_profile(
                    self.GuiAccessKey.currentText())
                self.GuiAccessKey.updateList(self.backend.user_data.profile)
    
    # ==================== GuiMid Actions ====================
    # ======================================================== 
    def ActDisconnect(self):
        '''
        Triggered by: GuiDisconnect
        1) Pops up window for the user to confirm she wants to log out.
        1) In the backend it deletes the session used to communicate
            with AWS.
        2) In the frontend it disable and empties GuiMid and GuiBottom.
        3) ATTENTION: It leaves any AWS instances running as they are.
        '''
        msg1 = 'This will log you out, but it will not'
        msg2 = ' affect any AWS instances currently running.'
        msg3 = '\n\nAre you sure you want to log out?'
        msg = msg1+msg2+msg3
        buttonReply = QMessageBox.question(self, 'Warning',
                            msg, QMessageBox.Yes|QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            self.refresher.off()
            self.backend.disconnect()
            self.GuiKeyPair.clear()
            self.GuiSecurity.clear() 
            self.GuiInstances.totalClear()
            self.setEnabledStates(False)      
    
    def ActKeyPairCreate(self):
        '''
        Triggered by: GuiKeyPair --> Create
        1) Popups window to take name of new key pair
        2) If no repetition, creates it, stores it in corresponding
            directory defined in Backend, and updates GuiKeyPair.
        '''
        name, okPressed = QInputDialog.getText(self, '',
                                    'Key Pair Name (without .pem):', 
                                    QLineEdit.Normal, '')
        if okPressed:
            response = self.backend.create_key_pair(name)
            if response == 'NoName':
                error_msg = 'Provide name for the new Key Pair.'
                QMessageBox.information(self, 'Error', error_msg, QMessageBox.Ok)
            elif response == 'NameDuplicate':
                error_msg = 'A Key Pair with the same name already exists.'
                QMessageBox.information(self, 'Error', error_msg, QMessageBox.Ok)
            elif response == 'Error':
                error_msg = 'Unexpected Error. Possible bug.'
                QMessageBox.information(self, 'Error', error_msg, QMessageBox.Ok)
            else:
                self.GuiKeyPair.updateList(self.backend.key_pairs)
    
    def ActKeyPairDelete(self):
        '''
        Triggered by: GuiKeyPair --> Delete
        1) Opens message box to confirm delete of Access Key selected
            on GuiKeyPair (QCombobox).
        2) Deletes it from both GuiAccessKey and Backend.
        '''
        if len(self.backend.key_pairs) == 0:
            error_msg = 'There is no Key Pair to Delete.'
            QMessageBox.information(self, 'Error', error_msg, QMessageBox.Ok)
        else:
            msg1 = 'This will delete the Key Pair from both your computer'
            msg2 = ' and the AWS server.'
            msg3 = 'Are you sure you want to proceed?'
            msg = msg1 + msg2 + msg3
            buttonReply = QMessageBox.question(self, 'Warning',
                            msg, QMessageBox.Yes|QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                self.backend.delete_key_pair(
                    self.GuiKeyPair.currentText())
                self.GuiKeyPair.updateList(self.backend.key_pairs)
    
    def ActSecurityCreate(self):
        '''
        Triggered by: GuiSecurity --> Create
        1) Popups window to take Description, Name, and VPC of new
            security group.
        2) If inputs are valid creates it, and updates both
            GuiSecurity and the Backend.
        '''
        x = self.mapToGlobal(QPoint(0,0)).x()
        y = self.mapToGlobal(QPoint(0,0)).y()
        GuiSecurityGroupCreate = SecurityGroupCreateWindow(x, y, self.backend)
        if GuiSecurityGroupCreate.Created:
            self.GuiSecurity.updateList(self.backend.security_groups)
        del GuiSecurityGroupCreate
    
    def ActSecurityDelete(self):
        '''
        Triggered by: GuiSecurity --> Delete
        1) Opens message box to confirm delete of Security Group
            selected on GuiSecurity (QCombobox).
        2) Deletes it from both GuiSecurity and Backend.
        '''
        if len(self.backend.security_groups) == 0:
            error_msg = 'There is no Security Group to Delete.'
            QMessageBox.information(self, 'Error', error_msg, QMessageBox.Ok)
        elif self.GuiSecurity.currentText() == 'default':
            error_msg = 'Default Group cannot be deleted.'
            QMessageBox.information(self, 'Error', error_msg, QMessageBox.Ok)
        elif self.GuiSecurity.currentText() == 'Recommended':
            error_msg = 'Recommended option cannot be deleted.'
            QMessageBox.information(self, 'Error', error_msg, QMessageBox.Ok)
        else:
            msg1 = 'This will delete the Security Group from'
            msg2 = ' the AWS server. Are you sure you want to proceed?'
            msg = msg1 + msg2
            buttonReply = QMessageBox.question(self, 'Warning',
                            msg, QMessageBox.Yes|QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                self.backend.delete_security_group(
                    self.GuiSecurity.currentText())
                self.GuiSecurity.updateList(self.backend.security_groups)
    
    # ================= GuiBottom Actions ====================
    # ========================================================
    
    def ActInstanceViewCreateMenu(self):
        '''
        Used by: GuiInstanceView, GuiInstance
        1) Creates a Menu with the actions that will go
            into GuiInstanceView
        2) 'SelectAll' and 'DeselectAll' are used to perform
            the two actions on both the frontend Menu (defined
            here), and the corresponding Beckend list.
        3) All other actions of the menu correspond to an
            element of Backend.user_data.InstanceView.
        4) Those (un)check the element of the frontend menu,
            update backend list, and call ActInstanceViewUpdate 
            to update GuiInstance (QTableWidget)
        '''
        backendDict = self.backend.user_data.InstanceView
        Keys = list(backendDict.keys())
        self.ActInstanceView = {}
        # Adds special buttons to select or deselect all
        self.ActInstanceView['SelectAll'] = QAction('(Select All)',
                                                     self, checkable=False)
        self.ActInstanceView['SelectAll'].triggered.connect(
                                    self.ActInstanceViewSelectAll)
        self.ActInstanceView['DeselectAll'] = QAction('(Deselect All)',
                                                       self, checkable=False)
        self.ActInstanceView['DeselectAll'].triggered.connect(
                                    self.ActInstanceViewDeselectAll)
        for i in Keys:
            # Defines the action
            self.ActInstanceView[i] = QAction(i, self, checkable=True)
            # Sets initial check of the action using backend.user_data
            self.ActInstanceView[i].setChecked(
                    self.backend.user_data.InstanceView[i])
            # Connects the action so that when clicked it updates
            # backend.user_data.InstanceView and the collumns shown in
            # GuiInstaces
            self.ActInstanceView[i].triggered.connect(
                                    self.ActInstanceViewUpdate)
    
    def ActInstanceViewUpdate(self):
        '''
        Triggered by: GuiInstanceView --> AttributeAction
        1) Updates the Backend Attribute to be on the same
            state (True, False) with that of the fronend menu.
        2) Refreshes GuiInstance (QTableWidget). 
        '''
        backendDict = self.backend.user_data.InstanceView
        Keys = list(backendDict.keys())
        for i in Keys:
            self.backend.user_data.InstanceView[i] \
            = self.ActInstanceView[i].isChecked()
        self.backend.user_data.save()
        self.GuiInstances.refresh(
                self.backend.user_data.InstanceView,
                self.backend.instancesData)
    
    def ActInstanceViewSelectAll(self):
        '''
        Triggered by: GuiInstanceView --> SelectAll
        1) Selects all Action in the menu of GuiInstanceView
            end updates the corresponding Backend list.
        '''
        backendDict = self.backend.user_data.InstanceView
        Keys = list(backendDict.keys())
        for i in Keys:
            self.backend.user_data.InstanceView[i] = True
            self.ActInstanceView[i].setChecked(True)
        self.backend.user_data.save()
        self.GuiInstances.refresh(
                self.backend.user_data.InstanceView,
                self.backend.instancesData)
    
    def ActInstanceViewDeselectAll(self):
        '''
        Triggered by: GuiInstanceView --> DeselectAll
        1) Deselects all Action in the menu of GuiInstanceView
            end updates the corresponding Backend list.
        '''
        backendDict = self.backend.user_data.InstanceView
        Keys = list(backendDict.keys())
        for i in Keys:
            self.backend.user_data.InstanceView[i] = False
            self.ActInstanceView[i].setChecked(False)
        self.backend.user_data.save()
        self.GuiInstances.refresh(
                self.backend.user_data.InstanceView,
                self.backend.instancesData)
    
    def ActInstanceActionsCreateMenu(self):
        '''
        Used by: GuiInstanceActions
        1) Creates a Menu with the actions that will go
            into GuiInstanceView.
        2) Those, stop, reboot, and terminate an instances
            if it is selected from GuiInstances (QTableWidget).
        '''
        self.ActInstanceActions = {}
        self.ActInstanceActions['Start'] = QAction('Start',
                                            self, checkable=False)
        self.ActInstanceActions['Start'].triggered.connect(
                                            self.ActInstanceStart)
        self.ActInstanceActions['Stop'] = QAction('Stop',
                                            self, checkable=False)
        self.ActInstanceActions['Stop'].triggered.connect(
                                            self.ActInstanceStop)
        self.ActInstanceActions['Reboot'] = QAction('Reboot',
                                            self, checkable=False)
        self.ActInstanceActions['Reboot'].triggered.connect(
                                            self.ActInstanceReboot)
        self.ActInstanceActions['Terminate'] = QAction('Terminate',
                                            self, checkable=False)
        self.ActInstanceActions['Terminate'].triggered.connect(
                                            self.ActInstanceTerminate)
        self.ActInstanceActions['More'] = QAction('More',
                                            self, checkable=False)
        self.ActInstanceActions['More'].triggered.connect(
                                            self.ActInstanceMore)
   
    def ActInstanceMore(self):
        '''
        Triggered by: GuiInstanceActions --> More
        1) If a row with a running instance is selected on GuiInstances
            (QTableWidget), then it pops up a box with information on
            how to connect to this instance through the terminal, or
            other.
        2) Otherwise, provides appropriate messages to user.
        '''
        # Obtains indexes of the subset of selected rows that are running 
        sr  = self.GuiInstances.selectedRows()
        srd = self.GuiInstances.RowsFilter('InstanceState','running', sr)
        # First checks if instance is selected. 
        if srd == []:
            msg = 'No running AWS Instance selected.'
            QMessageBox.information(self, 'Error', msg, QMessageBox.Ok)
        # Then if more than one running instance has been selected
        elif len(srd) > 1:
            msg = 'Select a single AWS Instance.'
            QMessageBox.information(self, 'Error', msg, QMessageBox.Ok)
        else:
            msg = self.backend.get_more_info(srd[0])
            QMessageBox.information(self, 'More Information', msg, QMessageBox.Ok)
    
    def ActInstanceStart(self):
        '''
        Triggered by: GuiInstanceActions --> Start
        1) If a row with a stopped instance is selected on GuiInstances
            (QTableWidget), then it requests from AWS to start it.
        2) If successful, updates backend list and GuiInstances.
        3) Otherwise, provides appropriate messages to user.
        '''
        # Obtains indexes of selected rows and the subset of those
        # that are stopped.
        sr  = self.GuiInstances.selectedRows()
        srd = self.GuiInstances.RowsFilter('InstanceState','stopped', sr)
        # First checks if instance is selected. 
        if sr == []:
            msg = 'No AWS Instance selected.'
            QMessageBox.information(self, 'Error', msg, QMessageBox.Ok)
        # Then if the two groups are the same
        elif sr != srd:
            if len(sr) == 1:
                msg = 'Only a stopped AWS Instance can be started.'
            else:
                msg1 = 'Your selection includes AWS Instances that are not'
                msg2 = ' stopped.\n\nOnly a stopped AWS Instance can be started.'
                msg = msg1+msg2
            QMessageBox.information(self, 'Error', msg, QMessageBox.Ok)
        else:
            error = self.backend.act_instances(sr, 'start')
            if error == 'IndexDoesNotExist':
                msg1 = 'Could not match frontend and backend indexes.'
                msg2 = ' Potential bug.'
                msg = msg1+msg2
            elif error == 'ConnectionError':
                self.get_instances()
                self.GuiInstances.refresh(self.backend.user_data.InstanceView)
                msg1 = 'Error while communicating with AWS. An attempt'
                msg2 = ' to update Table with AWS Instances was made.'
                msg3 = ' To be on the safe side also check using the'
                msg4 = ' AWS website.'
                msg = msg1+msg2+msg3+msg4
                QMessageBox.information(self, 'Error', msg, QMessageBox.Ok)
            else:
                self.backend.get_instances()
                self.GuiInstances.refresh(
                    self.backend.user_data.InstanceView,
                    self.backend.instancesData)
                
    def ActInstanceStop(self):
        '''
        Triggered by: GuiInstanceActions --> Stop
        1) If a row with a running instance is selected on GuiInstances
            (QTableWidget), then it requests from AWS to stop it.
        2) If successful, updates backend list and GuiInstances.
        3) Otherwise, provides appropriate messages to user.
        '''
        # Obtains indexes of selected rows and the subset of those
        # that are running.
        sr  = self.GuiInstances.selectedRows()
        srd = self.GuiInstances.RowsFilter('InstanceState', 'running', sr)
        
        # First checks if instance is selected. 
        if sr == []:
            msg = 'No AWS Instance selected.'
            QMessageBox.information(self, 'Error', msg, QMessageBox.Ok)
        # Then if the two groups are the same
        elif sr != srd:
            if len(sr) == 1:
                msg = 'Only a running AWS Instance can be stopped.'
            else:
                msg1 = 'Your selection includes AWS Instances that are not'
                msg2 = ' running.\n\nOnly a running AWS Instance can be stopped.'
                msg = msg1+msg2
            QMessageBox.information(self, 'Error', msg, QMessageBox.Ok)
        else:
            error = self.backend.act_instances(sr, 'stop')
            if error == 'IndexDoesNotExist':
                msg1 = 'Could not match frontend and backend indexes.'
                msg2 = ' Potential bug.'
                msg = msg1+msg2
            elif error == 'ConnectionError':
                self.get_instances()
                self.GuiInstances.refresh(self.backend.user_data.InstanceView)
                msg1 = 'Error while communicating with AWS. An attempt'
                msg2 = ' to update Table with AWS Instances was made.'
                msg3 = ' To be on the safe side also check using the'
                msg4 = ' AWS website.'
                msg = msg1+msg2+msg3+msg4
                QMessageBox.information(self, 'Error', msg, QMessageBox.Ok)
            else:
                self.backend.get_instances()
                self.GuiInstances.refresh(
                    self.backend.user_data.InstanceView,
                    self.backend.instancesData)
    
    def ActInstanceReboot(self):
        '''
        Triggered by: GuiInstanceActions --> Reboot
        1) If a row with a running instance is selected on GuiInstances
            (QTableWidget), then it requests from AWS to reboot it.
        2) If successful, updates backend list and GuiInstances.
        3) Otherwise, provides appropriate messages to user.
        '''
        # Obtains indexes of selected rows and the subset of those
        # that are stopped.
        sr  = self.GuiInstances.selectedRows()
        srd = self.GuiInstances.RowsFilter('InstanceState', 'running', sr)
        # First checks if instance is selected. 
        if sr == []:
            msg = 'No AWS Instance selected.'
            QMessageBox.information(self, 'Error', msg, QMessageBox.Ok)
        # Then if the two groups are the same
        elif sr != srd:
            if len(sr) == 1:
                msg = 'Only a running AWS Instance can be rebooted.'
            else:
                msg1 = 'Your selection includes AWS Instances that are not'
                msg2 = ' running.\n\nOnly a running AWS Instance can be rebooted.'
                msg = msg1+msg2
            QMessageBox.information(self, 'Error', msg, QMessageBox.Ok)
        else:
            error = self.backend.act_instances(sr, 'reboot')
            if error == 'IndexDoesNotExist':
                msg1 = 'Could not match frontend and backend indexes.'
                msg2 = ' Potential bug.'
                msg = msg1+msg2
            elif error == 'ConnectionError':
                self.get_instances()
                self.GuiInstances.refresh(self.backend.user_data.InstanceView)
                msg1 = 'Error while communicating with AWS. An attempt'
                msg2 = ' to update Table with AWS Instances was made.'
                msg3 = ' To be on the safe side also check using the'
                msg4 = ' AWS website.'
                msg = msg1+msg2+msg3+msg4
                QMessageBox.information(self, 'Error', msg, QMessageBox.Ok)
            else:
                self.backend.get_instances()
                self.GuiInstances.refresh(
                    self.backend.user_data.InstanceView,
                    self.backend.instancesData)
        
    def ActInstanceTerminate(self):
        '''
        Triggered by: GuiInstanceActions --> Terminate
        1) If a row with a running or stopped instance is selected
            on GuiInstances (QTableWidget), then it requests from 
            AWS to terminate it.
        2) If successful, updates backend list and GuiInstances.
        3) Otherwise, provides appropriate messages to user.
        '''
        # Obtains indexes of selected rows and the subset of those
        # that are stopped or running.
        sr  = self.GuiInstances.selectedRows()
        srd = self.GuiInstances.RowsFilter('InstanceState',
                                           ['running','stopped'], sr)
        # First checks if instance is selected. 
        if sr == []:
            msg = 'No AWS Instance selected.'
            QMessageBox.information(self, 'Error', msg, QMessageBox.Ok)
        # Then if the two groups are the same
        elif sr != srd:
            if len(sr) == 1:
                msg = 'Only a running or stopped AWS Instance can be terminated.'
            else:
                msg1 = 'Your selection includes AWS Instances that are either'
                msg2 = ' not running, or are not stopped.'
                msg3 = '\n\nOnly a running or stopped AWS Instance can be'
                msg4 = ' terminated.'
                msg = msg1+msg2+msg3+msg4
            QMessageBox.information(self, 'Error', msg, QMessageBox.Ok)
        else:
            error = self.backend.act_instances(sr, 'terminate')
            if error == 'IndexDoesNotExist':
                msg1 = 'Could not match frontend and backend indexes.'
                msg2 = ' Potential bug.'
                msg = msg1+msg2
            elif error == 'ConnectionError':
                self.get_instances()
                self.GuiInstances.refresh(self.backend.user_data.InstanceView)
                msg1 = 'Error while communicating with AWS. An attempt'
                msg2 = ' to update Table with AWS Instances was made.'
                msg3 = ' To be on the safe side also check using the'
                msg4 = ' AWS website.'
                msg = msg1+msg2+msg3+msg4
                QMessageBox.information(self, 'Error', msg, QMessageBox.Ok)
            else:
                self.backend.get_instances()
                self.GuiInstances.refresh(
                    self.backend.user_data.InstanceView,
                    self.backend.instancesData)
    
    def ActInstanceLaunch(self):
        '''
        Triggered by: GuiInstanceLaunch
        1) Pops up window for the user to provide details
            on the AWS instance she want to start.
        2) Launches the AWS instance and updates
            Instances (QTableWidget).
        '''
        GuiInstanceLaunchWindow = InstanceLaunchWindow(self)
    
    def setEnabledStates(self, logged_in):
        '''
        Part of ActConnect: triggered by: GuiConnect
        1) Takes logged_in (True, False)
        2) If False allows only the buttons of GuiTop to 
            be manipulated. Otherwise, it disable those 
            and enables the remaining ones.
        '''
        # GuiTop
        self.GuiConnect.setEnabled(not logged_in)
        self.GuiAccessKey.setEnabled(not logged_in)
        self.GuiAccessKeyBtn.setEnabled(not logged_in)
        self.GuiRegions.setEnabled(not logged_in)
        # GuiMid and GuiBottom
        self.GuiMid.setEnabled(logged_in)
        self.GuiBottom.setEnabled(logged_in)    

    # ========================================================              
    # ========================================================
        
    def closeEvent(self, event):
        '''
        triggered by: 'x button on titlebar'
        1) Asks user to confirm she want to close the app and
            if yes, then it closes it.
        '''
        msg1 = 'This will not stop any AWS instances currently running.'
        msg2 = '\n\nDo you still want to close the application?'
        msg = msg1 + msg2
        reply = QMessageBox.question(self, 'Warning', msg,
            QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.refresher.off()
            event.accept()
        else:
            event.ignore()
        
# =============  Used to setup a timer  ======================              
# ==========  to refresh the main window  ====================

from threading import Timer
class MainRefresher():
    def __init__(self, interval, main):
        '''
        Used to refresh the content of GuiInstances of
        the main window.
        interval --> interval between refreshing
        main --> Instance of Main Window as defined above
        '''
        self._timer   = None
        self.interval = interval
        self.main     = main
    
    def on(self):
        '''Call to set the timer running'''
        # Does a big update that unselects all rows
        self.main.GuiInstances.refresh(
            self.main.backend.user_data.InstanceView,
            self.main.backend.instancesData)
        # Switch to run, which allows for inplace
        # update to GuiInstances.
        self._timer = Timer(self.interval, self.run)
        self._timer.start()
        # Updates GuiStateReport
        self.main.GuiStateReport.isOnOff('on')
    
    def run(self):
        '''Call to set the timer running'''
        # Takes backend report on update on instances
        change = self.main.backend.get_instances()
        # Calls refresh or inplaceRefresh
        if change == 'InstanceChange':
            print('Big')
            # Does a big update that unselects all rows
            self.main.GuiInstances.refresh(
                self.main.backend.user_data.InstanceView,
                self.main.backend.instancesData)
        elif change == 'AttributeChange':
            # Only updates items, does not affect selection
            self.main.GuiInstances.inplaceRefresh(
                self.main.backend.instancesData)
        # Continues calling run().
        self._timer = Timer(self.interval, self.run)
        self._timer.start()
        # Updates GuiStateReport
        self.main.GuiStateReport.isOnOff('on')
    
    def off(self):
        '''Call to set the timer off'''
        if self._timer is not None:
            self._timer.cancel()
            self._timer = None
            self.main.GuiInstances.totalClear()
        # Updates GuiStateReport
        self.main.GuiStateReport.isOnOff('off')
            
            
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
class StateReport(QFrame):
    '''
    Frame with two QLabels. Top displays 'Connected'
    or 'Disconnected', bottom displays four
    corresponding icons.
    '''
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setStyleSheet("""
                QFrame{
                    background-color: rgb(235, 240, 243);
                    border: 0px solid rgb(100, 100, 100);
                }""")
        # Change comments below to use the Top label
        self.resize(90, 50)
        self.TopLabel = QLabel(self)
        self.TopLabel.resize(90,15)
        self.TopLabel.setText('')
        self.BotLabel = QLabel(self)
        self.BotLabel.resize(60,30)
        self.BotLabel.setScaledContents(True)
        self.isOnOff('off')
    def isOnOff(self, OnOff):
        if OnOff == 'off':
            self.state = 0
            #self.BotLabel.move(23,18)
            self.BotLabel.move(0,18)
        elif OnOff == 'on':
            #self.BotLabel.move(5,18)
            self.BotLabel.move(0,18)
            if self.state == 3:
                self.state = 1
            else:
                self.state += 1
        self.setState()
    def setState(self):
        if self.state == 0:
            #self.TopLabel.setText('Disconnected')
            self.BotLabel.setPixmap(
                QPixmap('resources/icons/disconnected.png'))
        elif self.state == 1:
            #self.TopLabel.setText('Connected')
            self.BotLabel.setPixmap(
                QPixmap('resources/icons/connected1.png'))
        elif self.state == 2:
            #self.TopLabel.setText('Connected')
            self.BotLabel.setPixmap(
                QPixmap('resources/icons/connected2.png'))
        elif self.state == 3:
            #self.TopLabel.setText('Connected')
            self.BotLabel.setPixmap(
                QPixmap('resources/icons/connected3.png'))
        