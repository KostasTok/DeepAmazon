'''
Collection of classes used to handle backend processing.
'''
import pickle
import boto3
import os
from botocore.exceptions import ClientError

class Backend():
    '''
    Class that handles all the backend processing
    '''
    def __init__(self):
        # Attempts to retrive user_data. If not possible,
        # it initialises them with empty/default values.
        self.user_data = User_Data()
        # Attemps to update list of AWS regions that
        # support EC2 instances.
        self.user_data.update_regions()
        
        # placeholder for the AWS session/client which will
        # connect the backend instance with the AWS server.
        self.sess = None
        self.client = None
        
        # placeholders for the name of the profile (i.e. cre-
        # dentials) that is used to create self.sess and
        # the regions on which the session will run.
        self.used_profile = None
        self.used_region = None
        
        # placeholders for arrays which will store the
        # names of available key-pairs and security groups.
        # key_pairs_files stores all the key pair, so that
        # it can be exported as a file.
        self.key_pairs = []
        self.key_pairs_local = []
        self.security_groups = []
        self.Vpcs = []
        
        # placehorders for instancesData as returned by boto3
        # describe_instances and a smaller version of it
        # that is used to build the corresponding GUI table.
        self.instancesDataBig = []
        self.instancesData = [self.emptyInstanceData()]
        
    def connect(self, profile, region):
        '''
        profile -> str with the name of the profile which will
                   be used to connect with the AWS server.
        1.  Finds credentials corresponding to profile
        2.  Validates credentials by requesting list of regions
            that support EC2 instances.
        3.  If profile exists and credentials are valid, then 
            sets self.sess = boto3.Session(), and similarly
            for the self.client. It also returns 'NoError'
        4.  Otherwise, returns error from AWS.
        '''
        # Attempts to find credentials. If it fails
        # returns errors.
        if profile != '':
            credentials = self.user_data.pass_credentials(profile)
            if credentials is not None:
                # Defines session with retrived credentials
                self.sess = boto3.Session(
                    aws_access_key_id = credentials[0], 
                    aws_secret_access_key = credentials[1],
                    region_name = region
                )
                self.client = self.sess.client('ec2')
                self.get_instances()
                try:
                    # Requests list of regions. If it fails
                    # moves to 'ConnectionError'.
                    self.client.describe_regions()
                    try:
                        # Attempts to update attributes. If it
                        # fails move to 'DescribeError'
                        self.user_data.save()
                        self.get_key_pairs()
                        self.get_security_groups()
                        self.get_Vpcs()
                        
                        # If successful updates self.used_
                        # and returns 'NoError'
                        self.used_profile = profile
                        self.used_region = region
                        self.user_data.default_region = region
                        return 'NoError'
                    except:
                        self.sess = None
                        self.client = None
                        return 'DescribeError'
                except:
                    self.sess = None
                    self.client = None
                    return 'ConnectionError'
            else:
                return 'WrongCredentials'
        else:
            return 'NoAccessKey'
    
    def disconnect(self):
        '''
        Sets all sesssion related variables but to
        the logged out state.
        '''
        self.sess = None
        self.client = None
        self.used_profile = None
        self.used_region = None
        self.key_pairs = []
        self.security_groups = []
        self.Vpcs = []
        self.instancesDataBig = []
        self.instancesData = [self.emptyInstanceData()]
    
    def get_key_pairs(self):
        '''
        Obtains list of key pairs on AWS server.
        '''
        KeyPairNames = []
        response = self.client.describe_key_pairs()
        for i in response['KeyPairs']:
            KeyPairNames.append(i['KeyName'])
        self.key_pairs = KeyPairNames
    
    def get_key_pairs_local(self):
        '''
        Obtains list of local key pairs associated with used
        credentials and regions. Then it checks if
        corresponding file exists in /resources/key_pairs,
        and if those are valid. Finally, it saves list
        of key pairs that satisfay all the above.
        '''
        KeyPairNames = []
        response = self.client.describe_key_pairs()
        for i in response['KeyPairs']:
            try: # this will only append if file is found
                i_path = 'resources/key_pairs/' \
                         + i['KeyName'] + '.pem'
                with open(i_path, 'r') as i_file:
                    KeyPairNames.append(i['KeyName'])
            except:
                pass
            self.key_pairs_local = KeyPairNames
            
    def get_security_groups(self):
        '''
        Obtains list of security groups associated with used
        credentials and regions.
        '''
        SecurityGroups = []
        response = self.client.describe_security_groups()
        for i in response['SecurityGroups']:
            SecurityGroups.append(i['GroupName'])
        self.security_groups = SecurityGroups
    
    def get_Vpcs(self):
        '''
        Obtains list of Vpcs associated with used
        credentials and regions.
        '''
        Vpcs = []
        response = self.client.describe_vpcs()
        for i in response['Vpcs']:
            Vpcs.append(i['VpcId'])
        self.Vpcs = Vpcs
    
    def create_key_pair(self, name):
        '''
        Takes name of file as 'example' or example.pem
        and creates a KeyPair, which is stored both on
        AWS and on the correspondning local folder.
        '''
        name = name.replace('.pem', '')
        name = name.replace(' ', '')
        if name == '':
            return 'NoName'
        elif name in self.key_pairs: 
            return 'NameDuplicate'
        else:
            #try:
            KeyPair = self.client.create_key_pair(KeyName = name)
            self.user_data.key_pairs_files.append(KeyPair)
            self.user_data.save()
            self.key_pairs.append(name)
            self.export_key_pair(name)
            return 'NoError'
            #except:
                #return 'Error'
            
    def delete_key_pair(self, name, dir_path = 'resources/key_pairs'):
        '''
        Deletes Key pair from all local sources
        and from the AWS server.
        '''
        name = name.replace('.pem', '')
        try:
            i = self.key_pairs.index(name)
            del self.key_pairs[i]
            self.client.delete_key_pair(KeyName = name)
        except:
            pass
        for i in self.user_data.key_pairs_files:
            if i['KeyName'] == name:
                del i
        name = name + '.pem'
        dir_path = os.path.abspath(dir_path)
        if name in os.listdir(dir_path):
            path = os.path.join(dir_path, name)
            os.remove(path)
    
    def export_key_pair(self, name, dir_path = 'resources/key_pairs'):
        '''
        Export key pair if it is stored on user_data object.
        '''
        dir_path = os.path.abspath(dir_path)
        found = False
        for i in self.user_data.key_pairs_files:
            if i['KeyName'] == name:
                path = os.path.join(dir_path, name+'.pem')
                with open(path, 'w') as file:
                    file.write(i['KeyMaterial'])
                found = True
        if found:
            return 'Found'
        else:
            return 'NotFound'
        
    def create_security_group(self, Description, name, VpcId):
        '''
        Creates security group with the given name
        and also stores the name in self.security_groups.
        '''
        name = name.replace(' ', '')
        if name == '':
            return 'NoName'
        elif name in self.security_groups:
            return 'NameDuplicate'
        else:
            try:
                if VpcId == '':
                    self.client.create_security_group(
                        Description=Description,
                        GroupName=name) 
                else:
                    self.client.create_security_group(
                        Description=Description,
                        GroupName=name,
                        VpcId=VpcId)  
                self.security_groups.append(name)
                return 'NoError'
            except:
                return 'Error'
            
    def delete_security_group(self, name):
        '''
        Deletes Security Group from all local sources
        and from the AWS server.
        '''
        if name == 'default':
            return 'DefaultError'
        else:
            try:
                i = self.security_groups.index(name)
                del self.security_groups[i]
                self.client.delete_security_group(GroupName = name)
                return 'NoError'
            except:
                return 'Error'
    
    def emptyInstanceData(self):
        '''
        Returns a dictionary with the elements found in self.instancesData
        all set to ''
        '''
        d ={'InstanceName': '',
            'InstanceId' : '',
            'InstanceState' : '',
            'InstanceType' : '',
            'StatusCheck' : '',
            'AvailabilityZone' : '',
            'SecurityGroupId' : '',
            'SecurityGroupName': '',
            'ImageId' : '',
            'KeyName' : '',
            'PublicDns' : '',
            'PublicIp' : '',
            'PrivateDns' : '',
            'PrivateIp' : '',
            'VpcId' : '',
            'SubnetId' : ''}
        return d
    
    def get_instances(self, client = None):
        '''
        Saves the response of boto3 --> describe_instances,
        and it also creates a smaller verion of it that is
        used to build the GUI instance table.
        
        If client is given, it uses this client to obtain
        the list with the Instances Attributes and returns it.
        
        If client is not given, but self.sess exists (logged in)
        the uses self.client to get the list, and saves it in
        self.instancesData.
        
        If neither, then it return 'NoClient'
        
        If InstanceIds are different from the
        previous update, then return 'InstanceChange'.
        If InstanceIds are the same, but other entries
        changed, then returns 'AttributeChange'.
        If neither, then returns 'NoChange'.
        '''
        old_instancesData = self.instancesData
        error = False
        instancesDataBig = None
        if client is not None:
            try:
                # Saves response as given by AWS
                instancesDataBig = client.describe_instances()
            except:
                error = True
        elif self.sess is not None:
            try:
                # Saves response as given by AWS
                self.instancesDataBig = self.client.describe_instances()
                instancesBig = self.instancesDataBig
            except:
                error = True
        
        if error:
            return 'Error'
        elif instancesBig is None:
            return 'NoClient'
        else:
            instancesData = []
            # Loops through the entry for each instance
            for y in self.instancesDataBig['Reservations']:
                # Defines dict which temporarily stores the values as
                # they are extracted from instancesBig
                d = self.emptyInstanceData()
                # Defines i to shorten notation
                i = y['Instances'][0]
                # 'Tags' only exists if a tag has been
                # created. If not InstanceName = ''
                try:
                    # If Tags exist, loops until it finds
                    # Tag with Key = 'Name'. If not uses
                    # the first Tag for InstanceName.
                    k = 0
                    while k < len(i['Tags']):
                        if i['Tags'][k]['Key'] == 'Name':
                            d['InstanceName'] = i['Tags'][k]['Value']
                            k = len(i['Tags']) + 1
                        else:
                            k += 1 
                    if k == len(i['Tags']):
                        d['InstanceName'] = i['Tags'][k]['Value']
                except:
                    d['InstanceName'] = ''
                # Fills the rest of the entries
                d['InstanceId'] = i['InstanceId']
                d['InstanceState'] = i['State']['Name']
                d['InstanceType'] = i['InstanceType']
                d['AvailabilityZone'] = i['Placement']['AvailabilityZone']
                if i['SecurityGroups'] != []:
                    d['SecurityGroupId'] = i['SecurityGroups'][0]['GroupId']
                    d['SecurityGroupName'] = i['SecurityGroups'][0]['GroupName']
                d['ImageId'] = i['ImageId']
                if 'KeyName' in i.keys():
                    d['KeyName'] = i['KeyName']
                d['PublicDns'] = i['PublicDnsName']
                # Some keys do not always exist
                if 'PublicIpAddress' in i.keys():
                    d['PublicIp'] = i['PublicIpAddress']
                if 'PrivateIpAddress' in i.keys():
                    d['PrivateIp'] = i['PrivateIpAddress']
                if 'VpcId' in i.keys():
                    d['VpcId'] = i['VpcId']
                if 'SubnetId' in i.keys():
                    d['SubnetId'] = i['SubnetId']
                # Gets status report
                if d['InstanceState'] == 'running':
                    if client is not None:
                        r = client.describe_instance_status(
                            InstanceIds=[d['InstanceId']])
                    elif self.sess is not None:
                        r = self.client.describe_instance_status(
                            InstanceIds=[d['InstanceId']])
                    InstanceTest = \
                    r['InstanceStatuses'][0]['InstanceStatus']['Status']=='ok' 
                    SystemTest = \
                    r['InstanceStatuses'][0]['SystemStatus']['Status']=='ok'
                    if InstanceTest and SystemTest:
                        d['StatusCheck'] = '2/2 checks passed'
                    else:
                        d['StatusCheck'] = 'Initializing'  
                # Appends self.instancesData with the dictionary
                # as one entry.
                instancesData.append(d.copy())
            
            # Onces instances is ready it returns it, and 
            # ponetrially saves it as self.instancesData
            if client is None:
                self.instancesData = instancesData
                if self.instancesData == old_instancesData:
                    return 'NoChange'
                elif len(self.instancesData)==len(old_instancesData):
                    sameIDs = 0
                    for i in range(len(self.instancesData)):
                        if self.instancesData[i]['InstanceId'] \
                             == old_instancesData[i]['InstanceId']:
                            sameIDs += 1
                    if sameIDs == len(self.instancesData):
                        return 'AttributeChange'
                    else:
                        return 'InstanceChange'
    
    def act_instances(self, indexes, act):
        '''
        indexes --> list with indexes of instance which
                        will act upon.
        act --> 'start', 'stop', 'reboot', 'terminate'
        '''
        try:
            ids = []
            for i in indexes:
                ids.append(self.instancesData[i]['InstanceId'])
            try:
                if act == 'start':
                    self.client.start_instances(InstanceIds = ids)
                elif act == 'stop':
                    self.client.stop_instances(InstanceIds = ids)
                elif act == 'reboot':
                    self.client.reboot_instances(InstanceIds = ids)
                elif act == 'terminate':
                    self.client.terminate_instances(InstanceIds = ids)
                return 'NoError'
            except:
                return 'ConnectionError'
        except:
            return 'IndexDoesNotExist'
    
    def launch_instance(self, name, imageId, instanceType,
                           keyPair, secGroup):
        '''
        Launches AWS instance.
        '''
        if imageId == '':
            return 'NoAmiIdError'
        elif instanceType == '':
            return 'NoTypeError'
        elif keyPair == '':
            return 'NoKeyError'
        else:
            if secGroup == 'Recommended':
                secGroup = []
            else:
                secGroup = [secGroup]
            try:
                response = self.client.run_instances(
                    MaxCount       = 1,
                    MinCount       = 1,
                    ImageId        = imageId,
                    InstanceType   = instanceType,
                    KeyName        = keyPair,
                    SecurityGroups = secGroup)
                InstanceId = response['Instances'][0]['InstanceId']
                self.client.create_tags(
                            Resources=[InstanceId],
                            Tags=[{
                                'Key': 'Name',
                                'Value': name}]
                                        )
                return 'NoError'
            except ClientError as e:
                return e.response['Error']['Code']
    
    def get_more_info(self, idx):
        '''
        Return Text with information on how to Log In to the 
        chosen instance through:
        1) the terminal
        2) an FTP client
        3) the Jupyter Notebook
        '''
        user = 'ubuntu@'
        KeyName  = self.instancesData[idx]['KeyName']
        rel_path = 'resources/key_pairs/' + KeyName + '.pem'
        abs_path = os.path.abspath(rel_path)
        UserPublicIp = user  + self.instancesData[idx]['PublicIp']
        UserDNS = user + self.instancesData[idx]['PublicDns']
        
        t1 = '1) To ensure that Key Pair is accessible write on local terminal:\n' \
              + 'chmod 400 ' + abs_path
        
        t2 = '2) To log in though the Terminal press:\n' \
              + 'ssh -oStrictHostKeyChecking=no -i ' \
              + abs_path + ' ' + UserPublicIp
                
        t3 = '3) To log in through an FTP client provide:\n' \
                + 'server: ' + self.instancesData[idx]['PublicIp'] \
                + '\nusername: ' + 'ubuntu' \
                + '\nSSH Pr. Key: ' + abs_path
        
        t4 = '4) To log in through the Jupyter Notebook:' \
                + '\na) Open terminal connection and press:' \
                + '\njupyter notebook --ip=0.0.0.0 --no-browser --port=8888' \
                + '\nb) On new local terminal window press:' \
                + '\nssh -i ' + abs_path + ' -L 8000:localhost:8888 ' + UserDNS \
                + '\nc) Open browser and press localhost:8000. Use the token' \
                + 'provided on step (a)'
                
        return t1 + '\n\n' + t2 + '\n\n' + t3 + '\n\n' + t4

class User_Data():
    '''
    Class that saves and retrives used data from the disk
    '''
    def __init__(self):
        '''
        Attemps to load pickle object with user data. If it
        does not exist, it initialises it empty.
        '''
        try:
            with open('resources/user_data.pkl', 'rb') as input:
                imported_data = pickle.load(input)
            # Copies data from the imported object
            self.profile = imported_data.profile
            self.access_key_id = imported_data.access_key_id
            self.secret_access_key = imported_data.secret_access_key
            self.ec2_regions = imported_data.ec2_regions
            self.default_region = imported_data.default_region
            self.key_pairs_files = imported_data.key_pairs_files
            self.InstanceView = imported_data.InstanceView
            self.ImageIds = imported_data.ImageIds
            self.ImageNames = imported_data.ImageNames
            self.InstanceTypes = imported_data.InstanceTypes
            del imported_data
        except:
            # Initialises all attributes empty
            self.profile = []
            self.access_key_id = []
            self.secret_access_key = []
            # Initialises list of regions that support EC2, below
            # list a given on 20-Jun-2018
            self.ec2_regions = ['ap-south-1', 'eu-west-3', 'eu-west-2',
                                'eu-west-1','ap-northeast-2',
                                'ap-northeast-1', 'sa-east-1',
                                'ca-central-1', 'ap-southeast-1',
                                'ap-southeast-2', 'eu-central-1', 
                                'us-east-1', 'us-east-2', 
                                'us-west-1', 'us-west-2']
            self.default_region = 'ap-south-1'
            self.key_pairs_files = []
            
            # List of attributes that appear on the running
            # instance table.
            self.InstanceView = {
                                'InstanceName': True,
                                'InstanceId' : True,
                                'InstanceState' : True,
                                'InstanceType' : True,
                                'StatusCheck' : True,
                                'AvailabilityZone' : True,
                                'SecurityGroupId' : True,
                                'SecurityGroupName' : True,
                                'ImageId' : True,
                                'KeyName' : True,
                                'PublicDns' : True,
                                'PublicIp' : True,
                                'PrivateDns' : True,
                                'PrivateIp' : True,
                                'VpcId' : True,
                                'SubnetId' : True}
            # List of AMIs Ids. Names are taken by AWS
            # after a successful log in.
            self.ImageIds = ['ami-1a8c8a63', 'ami-31cbc748',
                             'ami-958d8bec', 'ami-6babae12',
                             'ami-66abae1f', 'ami-2fb0c956']
            self.ImageNames = ['', '', '', '', '', '']
            # List of Instance Types
            self.InstanceTypes = ['p2.xlarge', 'p2.8xlarge',
                                 'p2.16xlarge', 'p3.2xlarge',
                                 'p3.8xlarge', 'p3.16xlarge']
    
    def save(self):
        with open('resources/user_data.pkl', 'wb') as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)
            
    def add_profile(self, profile, access_key_id, secret_access_key):
        '''
        Adds profile and returns error if not possible, otherwise
        it returns 'NoError'.
        '''
        # Deletes white spaces
        profile = profile.replace(' ', '')
        access_key_id = access_key_id.replace(' ', '')
        secret_access_key = secret_access_key.replace(' ', '')
        
        # Checks if profile already exists, and if it is valid.
        if profile == '':
            return 'NoName'
        elif profile in self.profile:
            return 'ProfileExists'
        elif access_key_id in self.access_key_id:
            return 'KeyIdExists'
        else:
            try:
                # The instance is defined even with invalid credentials
                ec2 = boto3.client('ec2',
                    aws_access_key_id = access_key_id, 
                    aws_secret_access_key = secret_access_key
                                  )
                # This is where invalid credentials return error
                responce = ec2.describe_regions()
                # If no error, then profile is added.
                self.profile.append(profile)
                self.access_key_id.append(access_key_id)
                self.secret_access_key.append(secret_access_key)
                self.save()
                return 'NoError'
            except:
                return 'InvalidCredentials'
            del ec2
                
    def delete_profile(self, profile):
        '''Deletes profile using its name'''
        try:
            i = self.profile.index(profile)
            del self.profile[i]
            del self.access_key_id[i]
            del self.secret_access_key[i]
            self.save()
        except:
            return 'Error'
    
    def pass_credentials(self, profile):
        '''
        Returns list [access_key_id, secret_access_key]
        with the key that corresponds to the profile with
        the given name. Returns None if name doesn't exist
        '''
        try:
            i = self.profile.index(profile)
            return [self.access_key_id[i], self.secret_access_key[i] ]
        except:
            return None
    
    def update_regions(self):
        '''
        If a profile that can log in to AWS exists, then it
        uses it to request list of regions that support EC2
        instances.
        '''
        # Loops through profiles until it finds a valid one.
        i = 0
        stop = False
        while stop == False and i<len(self.profile):
            # The instance is defined even with invalid credentials
            ec2 = boto3.client('ec2',
                    aws_access_key_id = self.access_key_id[i], 
                    aws_secret_access_key = self.secret_access_key[i]
                              )
            try:
                # This is where invalid credentials return error
                responce = ec2.describe_regions()
                updated_list = []
                for i in responce['Regions']:
                    updated_list.append(i['RegionName'])
                # If regions successfully retrived signals to stop
                stop = True
                # Updates list of regions of the User Data instance
                self.ec2_regions = updated_list
            except:
                i += 1
            del ec2
            
    def add_AMI(self, imageId, client):
        '''
        imageId --> str with the Id of a new AWS Image
            to be added. Can only be used if an activate
            client is provided, so that the imageId can
            be validated.
        '''
        try:
            responce = client.describe_images(ImageIds=[imageId])
            self.ImageIds.append(imageId)
            self.ImageNames.append(responce['Images'][0]['Name'])
            self.save()
            return 'NoError'
        except:
            return 'Error'
        
    def delete_AMI(self, imageId):
        '''
        imageId --> str with the Id of the image to be deleted.
        '''
        try:
            i = self.ImageIds.index(imageId)
            del self.ImageIds[i]
            del self.ImageNames[i]
            self.save()
            return 'NoError'
        except:
            return 'Error'
    
    def get_AmiNames(self, client = None):
        '''
        For each amiId that doesn't have a corresponding name
        attempts to get it from AWS using client.
        
        If client is not given, then loops through saved
        profiles.
        '''
        
        if '' in self.ImageNames:
            # If no client, loops through profiles to find a valid one.
            if client is None:    
                i = 0
                stop = False
                while stop == False and i<len(self.profile):
                    # The instance is defined even with invalid credentials
                    client = boto3.client('ec2',
                        aws_access_key_id = self.access_key_id[i], 
                        aws_secret_access_key = self.secret_access_key[i]
                                             )
                    # If this fails because of DryRun, the valid client
                    try:
                        client.describe_regions(DryRun=True)
                    except ClientError as e:
                        error = e.response['Error']['Code']
                        if error == 'DryRunOperation':
                            stop = True
                        else:
                            client = None
                            i += 1
            # If client is given, checks if a valid one.
            else:
                try:
                    client.describe_regions(DryRun=True)
                except ClientError as e:
                    error = e.response['Error']['Code']
                    if error != 'DryRunOperation':
                        client = None
            # If above produces a valid client, retrieve names
            if client is not None:
                for i in range(len(self.ImageNames)):
                    if self.ImageNames[i] == '':
                        try:
                            r =  client.describe_images(
                                ImageIds=[self.ImageIds[i]])
                            self.ImageNames[i] = r['Images'][0]['Name']
                        except ClientError as e:
                            # Depending on the region some AMIs may
                            # not exist.
                            pass
                self.save()

    def add_InstanceType(self, InstanceType):
        '''
        InstanceType --> str with the type, only added if no
                            repetition.
        '''
        if InstanceType == '':
            return 'EmptyError'
        elif InstanceType in self.InstanceTypes:
            return 'DuplicateError'
        else:
            self.InstanceTypes.append(InstanceType )
            self.save()
            return 'NoError'
        
    def delete_InstanceType(self, InstanceType):
        '''
        InstanceType --> str with the Id of the image to be deleted.
        '''
        try:
            i = self.InstanceTypes.index(InstanceType)
            del self.InstanceTypes[i]
            self.save()
            return 'NoError'
        except:
            return 'Error'