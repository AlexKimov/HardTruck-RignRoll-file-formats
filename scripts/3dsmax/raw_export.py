import toml
import sys


class maxscript_joiner:
    def __init__(self):
        self.filename = ""
        self.includes = []
    
    def get_file_data(self, filename):
        with open(filename, "r") as ms_file:
            file_data = ""
            comments = ""
            comments_is_on = True
            for line in ms_file:
                if line.find('/*') != -1:
                    comments_is_on = True
                    
                if line.find('filein') == -1 and not comments_is_on:
                    file_data += line 
                elif comments_is_on:
                    comments += line 
                    
                if line.find('*/') != -1:
                    comments_is_on = False                    
        return file_data
                   
    def join_maxscript_files(self):
        ms_file = self.get_file_data(self.filename)               
        
        included_ms_files = ""
        for file in self.includes:
            included_ms_files += "-- {}\n".format(file)
            included_ms_files += self.get_file_data(file)
            included_ms_files += "\n\n"            
        
        ms_file = included_ms_files + ms_file
        
        with open("builds/" + self.filename, "w") as file:
            file.writelines(ms_file)
        
        return 1

    def parse_toml_file(self, toml_filename):
        try:
            build_file = open(toml_filename, "r").read()
            build_config = toml.loads(build_file)
        except:
            raise Exception('Error parsing file {}'.format(toml_filename))    
    
        for section, params in build_config.items():
            self.filename = params.get("filename")
            self.includes = params.get("includes")
     
    def join(self, toml_filename):
        self.parse_toml_file(toml_filename)
        self.join_maxscript_files()        
    
    
if __name__ == "__main__":
    msj = maxscript_joiner()
    msj.join("build.toml")