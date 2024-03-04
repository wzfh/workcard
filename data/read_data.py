from configparser import ConfigParser





class ReadFile():
    def read_ini(self,file_path):
        config=ConfigParser()
        config.read(file_path,encoding='utf-8')
        data=dict(config._sections)
        return data






read=ReadFile()