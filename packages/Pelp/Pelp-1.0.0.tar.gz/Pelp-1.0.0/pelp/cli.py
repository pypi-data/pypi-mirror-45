import argparse
from .utils import * 
from .jsutils import * 

def getPythonInfo(ds):
    if ds == "string":
        getStringDocs()
    elif ds == "dict":
        getDictDocs()
    elif ds == "list":
        getListDocs()
    elif ds == "set":
        getSetDocs()
    elif ds == "all":
        getStringDocs()
        getDictDocs()
        getListDocs()
        getSetDocs() 
    else:
        print("\nThat isn't something we have support for right now :(")

def getJSInfo(ds):
    if ds == "string":
        getJSStringDocs()
    elif ds == "map":
        getJSMapDocs()
    elif ds == "array":
        getJSArrayDocs()
    elif ds == "all":
        getJSStringDocs()
        getJSMapDocs()
        getJSArrayDocs()
    else:
        print("\nThat isn't something we have support for right now :(")

def main():
    parser = argparse.ArgumentParser(description = "Language Options\n Python,JavaScript\n\nStructure Options\n Python: (string,list,dict,set,all)\n JavaScript: (string,array,map,all)", 
                                    usage='use "%(prog)s [language] [structure] --help" for more information',
                                    formatter_class = argparse.RawTextHelpFormatter)

    parser.add_argument("language", help = "The language you want information for", type = str)
    parser.add_argument("structure", help = "The datastructure you want documentation for", type = str)
    
    args = parser.parse_args()

    ds = args.structure.lower()
    lang = args.language.lower()
    
    if lang == "python":
        getPythonInfo(ds)
    elif lang == "javascript":
        getJSInfo(ds)
    else:
        print("\nThat isn't something we have support for right now :(")

if __name__ == "__main__":
	main()