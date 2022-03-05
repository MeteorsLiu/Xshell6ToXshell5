import configparser

import os
import codecs
import io
from os import listdir
from os.path import isfile, join
xshellpath = r"C:\Users\HaoLan\Desktop\xsh"
onlyfiles = [os.path.join(xshellpath, f) for f in listdir(xshellpath) if isfile(join(xshellpath, f)) and ".xsh" in f]
outputdir = r"C:\Users\HaoLan\Desktop\xsh\out"
for of in onlyfiles:
        with open(of, 'rb') as f:
            encoded_text = f.read()
            thefilename = os.path.basename(f.name)
        if encoded_text.startswith(codecs.BOM_UTF16_LE):
            encoded_text = encoded_text[len(codecs.BOM_UTF16_LE):]
            buf = io.StringIO(encoded_text.decode('utf-16le'))
        elif encoded_text.startswith(codecs.BOM_UTF8):
            encoded_text = encoded_text[len(codecs.BOM_UTF8):]
            buf = io.StringIO(encoded_text.decode('utf-8'))
        else:
            buf = io.StringIO(encoded_text.decode('utf-8'))

        config = configparser.RawConfigParser(allow_no_value=True)
        config.optionxform = str
        config.readfp(buf)
        buf.close()
        config.remove_section('BELL')
        config.remove_section('HIGHLIGHT')
        config.remove_section('ADVANCED')
        config.remove_option("SessionInfo", "Version")
        config.set('SessionInfo', 'Version', '5.3')
        config.remove_option('CONNECTION:SSH', 'SSHCiphers')
        config.remove_option('CONNECTION:SSH', 'SSHMACs')
        config.remove_option('CONNECTION:SSH', 'SSHKeyExchanges')
        config.remove_option('TERMINAL', 'FixedCols')
        buf = io.StringIO()
        config.write(buf, space_around_delimiters=False)

        with open(os.path.join(outputdir, thefilename), "wb") as f :
            f.write(buf.getvalue().encode('utf-8'))
        buf.close()
