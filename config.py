from ConfigParser import ConfigParser

def readconfig(filename, section='postgresql'):
   """Read database configuration file (similar to INI files in Windows).
   Args:
      - filename: the name of configuration file which follow format of:
          [section_name]
          key = value or key : value
      - section: the name of the section in the file to fetch
          (default to prosgresql) 

   Returns:
      dictionary object with key,value pair read from input file
   """
   parser = ConfigParser()
   parser.read(filename)
   if parser.has_section(section):
       return dict(parser.items(section))
   else:
       raise Exception('Section %s not found in file %s.',
                       format(section,filename)) 
