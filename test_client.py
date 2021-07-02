from ftplib import FTP
import json

class FTP_client():

    def setdefaultvalue(self,ip= "127.0.0.1",user= "xxxxx",psw= "00000"):
        self.FTP_HOST = ip
        self.FTP_USER = user
        self.FTP_PASS = psw
        
    def connect(self):
        self.client_FTP = FTP(self.FTP_HOST,self.FTP_USER,self.FTP_PASS)

    def disconnect(self):
        self.client_FTP.quit()

    def list_all_file(self):
        #list file name ***output list type
        return self.client_FTP.nlst()

    def check_file(self,check_word):
        for listword in self.list_all_file():
            #print(listword)
            if(listword.find(check_word) == -1):
                print("file not exist")
                return False
            else :
                print("file exist")
                return True

    def search_file(self,check_word):
        if(self.check_file(check_word)):
            for FTPfilename in self.list_all_file():
                #print(FTPfilename)
                if(FTPfilename.find(check_word) > -1):
                    print ("return value: "+FTPfilename)
            return FTPfilename

    def check_path(self):
        print(self.client_FTP.pwd())

    def change_type_object(self,type="utf-8"):
        self.encoding = type

    def path_folder_server(self,path_server):
        path = str(path_server).split('/')
        for i in path:
            if(i ==''):
                pass
            else:
                self.client_FTP.cwd(i)
        #print(path)
        print(self.client_FTP.pwd())
    
    def read_file(self,namefile):
        with open(self.Path_Download+namefile,'rb') as file:
            print("open "+namefile)
            return file.read()

    def back_to_root(self):
        self.client_FTP.cwd("/")

    def download_file(self,filename,path):
        write_file = path+filename
        with open(write_file, "wb") as file:
            # use FTP's RETR command to download the file
            self.client_FTP.retrbinary(f"RETR {filename}", file.write)
        print("download "+filename+" done")

    def check_firmware_ver_server(self):
        self.back_to_root() #reset path server
        self.Path_Download = "Test_server_client/transfer_file_log/"
        detail_name = "detail.txt"
        self.path_folder_server("/"+device_name+"/fw")
        if(self.check_file(detail_name)):
            self.download_file(detail_name,self.Path_Download)
            detail = self.read_file(detail_name)
            detail = json.loads(detail) #search info in detail.txt 
            least_version = detail["fw-ver"]
            return str(least_version)

    def check_log(self,device_name):
        self.back_to_root()
        mac = []
        date = []
        self.check_path()
        self.path_folder_server("/"+device_name+"/fw/log")
        self.check_path()
        #use for check new version firmware 
        #if(self.check_file(self.check_firmware_ver_server())):
            #list_log = self.search_file("_v"+self.check_firmware_ver_server())
        list_log = self.search_file("v0123")
        
        for i in range(len(list_log)):
            print(len(list_log))
            detail_log = list_log.split("_")
            print("current list = "+list_log)
            print("detail0 = "+detail_log[0])
            print("detail1 = "+detail_log[1])
            mac.insert(i,detail_log[0])
            date.insert(i,detail_log[1])
            
        return mac,date
        
if __name__ == "__main__":

    #default setting
    ip = '******'
    user = '*****'
    pws = '******'
    device_name = "EMU-B20MC"
    Path_Download = "../transfer_file_log/"
    Path_server = "/"+device_name+"/fw/log"
    filename = "detail.txt" #test search
    
    #test class
    client_FTP = FTP_client()
    client_FTP.setdefaultvalue(ip,user,pws)
    client_FTP.connect()
    client_FTP.change_type_object()
    #firmware_ver = client_FTP.check_firmware_ver_server()
    #print(firmware_ver)
    #client_FTP.check_path()

    mac,date = client_FTP.check_log(device_name)
    for y in range(len(mac)):
        
        print("log mac "+ str(y+1) +": ",mac[y])
        print("log date "+ str(y+1) +": ",date[y])
        print("////////////////////////\n")
    
    client_FTP.check_path()
    client_FTP.disconnect()
    

    


