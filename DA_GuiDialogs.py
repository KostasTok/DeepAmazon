'''
Collection of GUI classes used to build the Dialog
Windows with which the MainWindow interacts.
'''

from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from DA_GuiSmall import *

class AccessKeyAddWindow(QDialog):
    '''
    Small window used to add new Access Key
    '''
    def __init__(self, mainX, mainY, backend):
        '''
        Takes instance of backend in order to create an
        internal reference to it and manipulate it.
        '''
        super().__init__()
        
        self.backend = backend
        self.Added = False
        
        self.create_Gui(mainX, mainY)
        self.GuiAdd.clicked.connect(self.ActAdd)
        self.GuiCancel.clicked.connect(self.close)
        
        # disables parrent window until ok or cancel from
        # this window has been clicked.
        self.setWindowModality(Qt.ApplicationModal)
        self.exec_()
        
    def create_Gui(self, mainX, mainY):
        '''
        Sets up the GUI of AccessKeyAddWindow.
        '''
        self.setGeometry(mainX+100, mainY+100,
                         320, 170) # X, Y, width , height             
        self.setWindowTitle('AWS Credentials')
        
        # Access Key Name and label
        self.GuiProfileLabel = LabelOfButton('Name', self)
        self.GuiProfileLabel.move(10, 20)
        self.GuiProfile = InputLine('', self)
        self.GuiProfile.move(120, 20)
        self.GuiProfile.resize(QSize(190, 20))
        self.GuiProfile.setToolTip('Choose a Name for the Access Key')
        
        # Access Key Id and label
        self.GuiAccessKeyIdLabel = LabelOfButton('Access Key Id', self)
        self.GuiAccessKeyIdLabel.move(10, 50)
        self.GuiAccessKeyId = InputLine('', self)
        self.GuiAccessKeyId.move(120, 50)
        self.GuiAccessKeyId.resize(QSize(190, 20))
        self.GuiAccessKeyId.setToolTip('Provide Access Key Id as given by AWS.')
        
        # Secret Access Key and label
        self.GuiSecretAccessKeyLabel = LabelOfButton('Secret Access Key', self)
        self.GuiSecretAccessKeyLabel.move(10, 80)
        self.GuiSecretAccessKey = InputLine('', self)
        self.GuiSecretAccessKey.move(120, 80)
        self.GuiSecretAccessKey.resize(QSize(190, 20))
        self.GuiSecretAccessKey.setToolTip(
            'Provide Secret Access Key as given by AWS.')
        
        # Cancel Key
        self.GuiCancel = RectButton('Cancel', self)
        self.GuiCancel.move(190, 120)
        self.GuiCancel.resize(QSize(50, 30))
        
        # Add Key
        self.GuiAdd = RectButton('Add', self)
        self.GuiAdd.move(255, 120)
        self.GuiAdd.resize(QSize(50, 30))
        
    def ActAdd(self):
        '''
        Calls backend functions to check if profile does not
        already exists, and if it is valid. If everything ok
        it updates the corresponding backend list and ComboBox.
        '''
        error = self.backend.user_data.add_profile(
                    self.GuiProfile.text(),
                    self.GuiAccessKeyId.text(),
                    self.GuiSecretAccessKey.text())
        # Error reporting
        if error is 'NoName':
            error_msg = 'Choose a Name for the Access Key' 
        elif error is 'ProfileExists':
            error_msg = 'Name given already exists.' 
        elif error is 'KeyIdExists':
            error_msg = 'Access Key Id given already exists.'
        elif error is 'InvalidCredentials':
            error_msg = 'Credentials were not validated by AWS.'
        
        # In NoError, then the backend has been updated
        # and after returning to main loop it will also 
        # update the corresponding GuiCombobox.
        if error is 'NoError':
            self.close()
            self.Added = True
        else:
            QMessageBox.information(self, 'Error', 
                                    error_msg, QMessageBox.Ok)
        
class SecurityGroupCreateWindow(QDialog):
    '''
    Small window used to add new Security Group
    '''
    def __init__(self, mainX, mainY, backend):
        '''
        Takes instance of backend in order to create an
        internal reference to it and manipulate it.
        '''
        super().__init__()
        
        self.backend = backend
        self.Created = False
        
        self.create_Gui(mainX, mainY)
        self.GuiAdd.clicked.connect(self.ActAdd)
        self.GuiCancel.clicked.connect(self.close)
        
        # disables parrent window until ok or cancel from
        # this window has been clicked.
        self.setWindowModality(Qt.ApplicationModal)
        self.exec_()
        
    def create_Gui(self, mainX, mainY):
        '''
        Sets up the GUI of SecurityGroupAddWindow.
        '''
        self.setGeometry(mainX+100, mainY+100,
                         320, 170) # X, Y, width , height             
        self.setWindowTitle('AWS Credentials')
        
        # Security Group Description
        self.GuiDescriptionLabel = LabelOfButton('Description', self)
        self.GuiDescriptionLabel.move(10, 23)
        self.GuiDescription = InputLine('', self)
        self.GuiDescription.move(100, 20)
        self.GuiDescription.resize(QSize(190, 20))
        self.GuiDescription.setToolTip('Choose Description of the New Security Group.')
        
        # Security Group Name and label
        self.GuiNameLabel = LabelOfButton('Name', self)
        self.GuiNameLabel.move(10, 53)
        self.GuiName = InputLine('', self)
        self.GuiName.move(100, 50)
        self.GuiName.resize(QSize(190, 20))
        self.GuiName.setToolTip('Choose Name of the New Security Group.')
        
        # Security Group VPC and label
        self.GuiVpcLabel = LabelOfButton('VPC', self)
        self.GuiVpcLabel.move(10, 83)
        self.GuiVpc = ComboBoxWithUpdate(self, ['']+self.backend.Vpcs)
        self.GuiVpc.move(98, 80)
        self.GuiVpc.resize(QSize(200, 30))
        self.GuiVpc.setToolTip('Choose a Vpc or leave empty.')
        
        # Cancel Key
        self.GuiCancel = RectButton('Cancel', self)
        self.GuiCancel.move(170, 120)
        self.GuiCancel.resize(QSize(50, 30))
        
        # Add Key
        self.GuiAdd = RectButton('Add', self)
        self.GuiAdd.move(235, 120)
        self.GuiAdd.resize(QSize(50, 30))
        
    def ActAdd(self):
        '''
        Calls backend functions to check if name does not
        already exists, and if it is valid. If everything ok
        it updates the corresponding backend list and ComboBox.
        '''
        VpcToPass = self.GuiVpc.currentText()
        VpcToPass = VpcToPass.replace(' ', '')
        error = self.backend.create_security_group(
                    self.GuiDescription.text(),
                    self.GuiName.text(),
                    VpcToPass)
        # Error reporting
        if error is 'NoName':
            error_msg = 'Choose a Name for the Security Group.' 
        elif error is 'ProfileExists':
            error_msg = 'A Security Group with the given Name already exists.' 
        elif error is 'Error':
            error_msg = 'Unexpected Error. Potential Bug.'
        
        # In NoError, then the backend has been updated
        # and after returning to main loop it will also 
        # update the corresponding GuiCombobox.
        if error is 'NoError':
            self.close()
            self.Created = True
        else:
            QMessageBox.information(self, 'Error', 
                                    error_msg, QMessageBox.Ok)
            
class InstanceLaunchWindow(QDialog):
    '''
    Window used to launch a new AWS instance
    '''
    def __init__(self, main):
        '''
        Takes instance of backend in order to create an
        internal reference to it and manipulate it.
        '''
        super().__init__()
        
        mainX = main.mapToGlobal(QPoint(0,0)).x()
        mainY = main.mapToGlobal(QPoint(0,0)).y()
        self.main = main
        self.backend = main.backend
        self.Ok = False
        
        self.create_Gui(mainX, mainY)
        self.create_GuiGrid()
        self.connect_Actions()
        
        # disables parrent window until ok or cancel from
        # this window has been clicked.
        self.setWindowModality(Qt.ApplicationModal)
        self.exec_()
    
    # ========  Below the four functions that  ========
    # ========  create the GUI are defined     ========  
    def create_GuiGrid(self):
        '''Sets position of elements'''
        # 1) AMI elements
        self.GuiAmiTagLabel.move(10, 10)
        self.GuiAmiTag.move(120, 10)
        self.GuiAmiNameLabel.move(10, 46)
        self.GuiAmiNames.move(120, 40)
        self.GuiAmiIdLabel.move(10, 76)
        self.GuiAmiIds.move(120, 70)
        self.GuiAmiBtn.move(260, 75)
        # 2) Instance Types
        self.GuiInstanceTypeLabel.move(10, 106)
        self.GuiInstanceType.move(120, 100)
        self.GuiInstanceTypeBtn.move(260, 105)
        # 3) Key Pairs
        self.GuiKeyPairLabel.move(10, 136)
        self.GuiKeyPair.move(120, 130)
        self.GuiKeyPairBtn.move(260, 105+30)
        # 4) Security Groups
        self.GuiSecurityLabel.move(10, 166)
        self.GuiSecurity.move(120, 160)
        self.GuiSecurityBtn.move(260, 165)
        # 5) Cancel and Ok
        self.GuiCancel.move(180, 205)
        self.GuiLaunch.move(245, 205)
        
    def create_Gui(self, mainX, mainY):
        '''
        Sets up the GUI of LaunchInstanceWindow
        '''
        self.setGeometry(mainX+100, mainY+100,
                         320, 250) # X, Y, width , height             
        self.setWindowTitle('Instance Launch')
        
        # AMI Comboboxes and label and button
        self.GuiAmiTagLabel = LabelOfButton('Image Name Tag', self)
        self.GuiAmiTag = InputLine('', self)
        self.GuiAmiTag.resize(130, 20)
        self.GuiAmiTag.setToolTip('Creates a Tag with key=Name.')
        self.GuiAmiNameLabel = LabelOfButton('Image AWS Name', self)
        self.GuiAmiNames = ComboBoxWithUpdate(self,
                                self.backend.user_data.ImageNames)
        self.GuiAmiNames.resize(130, 30)
        self.GuiAmiNames.setToolTip('Choose an AMI by Name')
        self.GuiAmiIdLabel =   LabelOfButton('Image Id', self)
        self.GuiAmiIds = ComboBoxWithUpdate(self,
                                self.backend.user_data.ImageIds)
        self.GuiAmiIds.resize(130, 30)
        self.GuiAmiIds.setToolTip('Choose an AMI by Id')     
        self.GuiAmiBtn = ButtonIconMenu('gear.png', self)
        self.GuiAmiBtn.setBtnIconSize(40, 20, 35, 16)
        self.GuiAmiBtn.setToolTip('Add or delete an AMI')
        
        # Access Instance Types and label
        self.GuiInstanceTypeLabel = LabelOfButton('Instance Type', self)
        self.GuiInstanceType = ComboBoxWithUpdate(self,
                                self.backend.user_data.InstanceTypes)
        self.GuiInstanceType.resize(130, 30)
        self.GuiInstanceType.setToolTip('Choose an AMI by Id') 
        self.GuiInstanceTypeBtn = ButtonIconMenu('gear.png', self)
        self.GuiInstanceTypeBtn.setBtnIconSize(40, 20, 35, 16)
        self.GuiInstanceTypeBtn.setToolTip('Add or delete an Instance Type')
        
        # Key Pairs drop down menu and label
        self.GuiKeyPairLabel = LabelOfButton('Key Pairs', self)
        self.GuiKeyPair = ComboBoxWithUpdate(self,
                                self.backend.key_pairs)
        self.GuiKeyPair.resize(130, 30)
        self.GuiKeyPair.setToolTip('Key Pairs used with AWS instances')
        self.GuiKeyPairBtn = ButtonIconMenu('gear.png', self)
        self.GuiKeyPairBtn.setBtnIconSize(40, 20, 35, 16)
        self.GuiKeyPairBtn.setToolTip(
            'Create or delete a Key Pair to connect with an instance')
        
        # Security Groups drop down menu and label
        self.GuiSecurityLabel = LabelOfButton('Security Groups', self)
        SecurityList = ['Recommended'] + self.backend.security_groups
        self.GuiSecurity = ComboBoxWithUpdate(self, SecurityList)
        self.GuiSecurity.resize(130, 30)
        self.GuiSecurity.setToolTip('Access Key used to connect with AWS')
        self.GuiSecurityBtn = ButtonIconMenu('gear.png', self)
        self.GuiSecurityBtn.setBtnIconSize(40, 20, 35, 16)
        self.GuiSecurityBtn.setToolTip('Create or delete a Security Group')
        
        # Cancel Key
        self.GuiCancel = RectButton('Cancel', self)
        self.GuiCancel.resize(QSize(50, 30))
        # Launch Key
        self.GuiLaunch = RectButton('Launch', self)
        self.GuiLaunch.resize(QSize(50, 30))
        
    # ========  Below Actions are defined and binded  ========
    # ========  to the GUI objects of main window     ========    
    def connect_Actions(self):
        '''
        Here the action that are defined in the next
        def's and in the main Gui are connected to the
        GUI elements of the window.
        '''
        self.GuiAmiIds.currentIndexChanged.connect(
                self.ActAmiNamesChange)
        self.GuiAmiNames.currentIndexChanged.connect(
                self.ActAmiIdsChange)
        
        #    GuiAmiBtn Button
        self.ActAmiBtnAdd = QAction('Add', self)
        self.ActAmiBtnAdd.triggered.connect(
                                    self.ActImageAdd)
        self.ActAmiBtnDelete = QAction('Delete', self)
        self.ActAmiBtnDelete.triggered.connect(
                                    self.ActImageDelete)
        self.GuiAmiBtn.bindMenu([
                    self.ActAmiBtnAdd,
                    self.ActAmiBtnDelete])
        
        #    GuiInstanceType Button
        self.ActInstanceTypeBtnAdd = QAction('Add', self)
        self.ActInstanceTypeBtnAdd.triggered.connect(
                                    self.ActInstanceTypeAdd)
        self.ActInstanceTypeBtnDelete = QAction('Delete', self)
        self.ActInstanceTypeBtnDelete.triggered.connect(
                                    self.ActInstanceTypeDelete)
        self.GuiInstanceTypeBtn.bindMenu([
                    self.ActInstanceTypeBtnAdd,
                    self.ActInstanceTypeBtnDelete])
        
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
        
        # GuiCancel and GuiLaunch Buttons
        self.GuiCancel.clicked.connect(self.close)
        self.GuiLaunch.clicked.connect(self.ActLaunch)
    
    def ActLaunch(self):
        '''
        Attemps to Launch the new AWS instance as
        specified, otherwise returns error in msgbox.
        '''
        error = self.backend.launch_instance(
                    self.GuiAmiTag.text(),
                    self.GuiAmiIds.currentText(), 
                    self.GuiInstanceType.currentText(),
                    self.GuiKeyPair.currentText(),
                    self.GuiSecurity.currentText())
        if error == 'NoAmiIdError':
            msg = 'No Image Id was given.'
            QMessageBox.information(self, 'Error', msg, QMessageBox.Ok)
        elif error == 'NoTypeError':
            msg = 'No Instance Type was given.'
            QMessageBox.information(self, 'Error', msg, QMessageBox.Ok)
        elif error == 'NoKeyError':
            msg = 'No Key Pair was given.'
            QMessageBox.information(self, 'Error', msg, QMessageBox.Ok)
        elif error == 'NoError':
            msg = 'AWS Instance is starting up.'
            QMessageBox.information(self, 'Report', msg, QMessageBox.Ok)
            # Updates Gui of main window
            self.main.GuiKeyPair.updateList(self.backend.key_pairs)
            self.main.GuiSecurity.updateList(self.backend.security_groups)
            self.main.refresher.on()
            self.close()
        else:
            msg = 'AWS reported error: ' + error
            QMessageBox.information(self, 'Error', msg, QMessageBox.Ok)
    
    def ActAmiNamesChange(self):
        '''
        Synchronize current text of GuiAmiIds with
        that of GuiAmiNames.
        '''
        i = self.GuiAmiIds.currentIndex()
        self.GuiAmiNames.setCurrentIndex(i)
        
    def ActAmiIdsChange(self):
        '''
        Synchronize current text of GuiAmiNames with
        that of GuiAmiIds.
        '''
        i = self.GuiAmiNames.currentIndex()
        self.GuiAmiIds.setCurrentIndex(i)
        
    def ActImageAdd(self):
        '''
        Triggered by: GuiAmiBtn --> Add
        1) Popups window to take new Image Id
        2) If no repetition, creates it, stores it in corresponding
            directory defined in Backend, and updates InstanceType.
        '''
        id, okPressed = QInputDialog.getText(self, '',
                                            'Give valid Image Id:', 
                                            QLineEdit.Normal, '')
        if okPressed:
            if id == '':
                msg = 'No Image Id was given.'
                QMessageBox.information(self, 'Error', msg, QMessageBox.Ok)
            else:
                error = self.backend.user_data.add_AMI(id, self.backend.client)
                if error == 'Error':
                    msg1 = 'It was not possible to complete the process.'
                    msg2 = '\n\mEither wrong Image Id was given, or some other'
                    msg3 = 'connection error.'
                    msg = msg1+msg2+msg3
                    QMessageBox.information(self, 'Error', msg, QMessageBox.Ok)
                else:
                    self.GuiAmiIds.updateList(self.backend.user_data.ImageIds)
                    self.GuiAmiNames.updateList(self.backend.user_data.ImageNames)
                    
    def ActImageDelete(self):
        '''
        Triggered by: GuiAmiBtn --> Delete
        1) Opens message box to confirm delete of Image
            selected on GuiImageIds (QCombobox).
        2) Deletes it from both Frontend and Backend.
        '''
        if len(self.backend.user_data.ImageIds) == 0:
            msg = 'There is no Image to Delete.'
            QMessageBox.information(self, 'Error', msg, QMessageBox.Ok)
        else:
            msg1 = 'This will delete the Image.'
            msg2 = ' Are you sure you want to proceed?'
            msg = msg1 + msg2
            buttonReply = QMessageBox.question(self, 'Warning',
                            msg, QMessageBox.Yes|QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                self.backend.user_data.delete_AMI(self.GuiAmiIds.currentText())
                self.GuiAmiIds.updateList(self.backend.user_data.ImageIds)
                self.GuiAmiNames.updateList(self.backend.user_data.ImageNames)
        
    def ActInstanceTypeAdd(self):
        '''
        Triggered by: GuiInstanceType --> Add
        1) Popups window to take new Instance Type
        2) If no repetition, creates it, stores it in corresponding
            directory defined in Backend, and updates InstanceType.
        '''
        InstanceType, okPressed = QInputDialog.getText(self, '',
                                    'Give valid Instance Type:', 
                                    QLineEdit.Normal, '')
        if okPressed:
            error = self.backend.user_data.add_InstanceType(InstanceType)
            if error == 'EmptyError':
                msg = 'No Instance Type was given.'
                QMessageBox.information(self, 'Error', msg, QMessageBox.Ok)
            elif error == 'DuplicateError':
                msg = 'This Instance Type has already been added.'
                QMessageBox.information(self, 'Error', msg, QMessageBox.Ok)
            else:
                self.GuiInstanceType.updateList(
                        self.backend.user_data.InstanceTypes)
    
    def ActInstanceTypeDelete(self):
        '''
        Triggered by: GuiInstanceType  --> Delete
        1) Opens message box to confirm delete of Instance Type
            selected on GuiInstanceType (QCombobox).
        2) Deletes it from both GuiInstanceType and Backend.
        '''
        if len(self.backend.user_data.InstanceTypes) == 0:
            msg = 'There is no Instance Type to Delete.'
            QMessageBox.information(self, 'Error', msg, QMessageBox.Ok)
        else:
            msg1 = 'This will delete the Instance Type.'
            msg2 = ' Are you sure you want to proceed?'
            msg = msg1 + msg2
            buttonReply = QMessageBox.question(self, 'Warning',
                            msg, QMessageBox.Yes|QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                error = self.backend.user_data.delete_InstanceType(
                                self.GuiInstanceType.currentText())
                if error == 'Error':
                    msg1 = 'Could not find the selected Instance Type in the'
                    msg2 = ' backend list. Potential bug.'
                    msg  = ms1 + msg2
                    QMessageBox.information(self, 'Error', msg, QMessageBox.Ok)
                elif error == 'NoError':
                    self.GuiInstanceType.updateList(
                        self.backend.user_data.InstanceTypes)
        
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
        

        
                