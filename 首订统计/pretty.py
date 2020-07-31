import pandas as pd
import sys

def strB2Q(ustring):
    """半角转全角"""
    rstring = ""
    for uchar in ustring:
        inside_code=ord(uchar)
        if inside_code == 32:                                 #半角空格直接转化                  
            inside_code = 12288
        elif inside_code >= 32 and inside_code <= 126:        #半角字符（除空格）根据关系转化
            inside_code += 65248

        rstring += chr(inside_code)
    return rstring

def show(name):
    #pd.set_option('display.unicode.ambiguous_as_wide',True)
    #pd.set_option('display.unicode.east_asian_width',True)
    df=pd.read_csv(name,sep='\t')[['分类','书名','作者','首日总订']]
    #formatters={'分类':lambda x:x+' '*(3-len(x))},index=False,justify='left'
    print(strB2Q(df.sort_values('首日总订',ascending=False).to_string(formatters={'分类':'{:3s}'.format,'首日总订':'{:.0f}'.format},index=False)))

show(sys.argv[1])