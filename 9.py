import datetime
import xml.sax.saxutils

COPYRIGHT_TEMPLE="Copyright (c) {0} {1}.All rights reserved."
STYLESHEET_TEMPLE=('<link rel="stylesheet" type="text/css" '
                   'media="all" href="{0}" />\n')
HTML_TEMPLE="""<?xml version="1.0"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Scrict//EN"\
"http://www.w3.org.org/TR/xhtml1/DTD/xhtml -strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
<head>
<title>{title}</title>
<!--{copy_right}-->
<meta name="Description" content="{description}" />
<meta name="Keywords" content="{keywords}" />
<meta equiv="content-type" content="text/html;charset=utf-8" />
{stylesheet}\
</head>
<body>

</body>
</html>
"""

class CancelledError(Exception):pass

def get_string(message,name="string",default=None,minimum_length=0,maximum_length=80):
    message+=":" if default is None else "[{}]:".format(default)
    while True:
        try:
            line=input(message)
            if not line:
                if default is not None:
                    return default
                if minimum_length==0:
                    return ""
                else:
                    raise ValueError("{} may not be empty.".format(name))
            if not (minimum_length<=len(line)<=maximum_length):
                raise ValueError("{name} must have at least "
                                 "{minimum_length} and at most"
                                 "{maximum_length} characters".format(**locals()))
            return line
        except ValueError as err:
            print("Error",err)

def get_integer(message,name="integer",default=None,minimum=0,maximum=100,allow_zero=True):
    message+=":" if default is None else "[{}]:".format(default)
    while True:
        try:
            line=input(message)
            if not line:
                if default is not None:
                    return default
                if allow_zero:
                    return 0
                else:
                    raise ValueError("{} may not be empty.".format(name))
            if not (minimum<=int(line)<=maximum):
                raise ValueError("{name} must have at least "
                                 "{minimum} and at most"
                                 "{maximum} characters".format(**locals()))
            return int(line)
        except ValueError as err:
            print("Error",err)

def populate_information(information):
    name=get_string("Enter your name(for copyright)","name",information["name"])
    if not name:
        raise CancelledError()
    year=get_integer("Enter copyright year","year",information["year"],2000,datetime.date.today().year+1,True)
    if year==0:
        raise CancelledError()
    filename=get_string("Enter filename","filename")
    if not filename:
        raise CancelledError()
    if not filename.endswith((".htm","html")):
        filename+=".html"
    title=get_string("Enter title","title")
    description=get_string("Enter description","description")
    keywords=get_string("Enter keywords","keywords").split()
    stylesheet=get_string("Enter stylesheet","stylesheet")
    
    information.update(name=name,year=year,filename=filename,title=title,
                       description=description,keywords=keywords,
                       stylesheet=stylesheet)

def make_html_skeleton(year,name,title,description,keywords,stylesheet,filename):
    copy_right=COPYRIGHT_TEMPLE.format(year,name)
    title=xml.sax.saxutils.escape(description)
    description=xml.sax.saxutils.escape(description)
    keywords=",".join([xml.sax.saxutils.escape(k) for k in keywords]) if keywords else ""
    stylesheet=(STYLESHEET_TEMPLE.format(stylesheet)) if stylesheet else ""
    html=HTML_TEMPLE.format(**locals())
    fh=None
    try:
        fh=open(filename,"w",encoding="utf-8")
        fh.write(html)
    except EnvironmentError as err:
        print("Error",err)
    else:
        print("Saved skeleton",filename)
    finally:
        if fh is not None:
            fh.close()

def main():
    information=dict(name=None,year=datetime.date.today().year,
                     filename=None,title=None,description=None,
                     keywords=None,stylesheet=None)
    while True:
        try:
            print("\nMake HTML Skeleton\n")
            populate_information(information)
            make_html_skeleton(**information)
        except CancelledError:
            print("Cancelled")
        if(get_string("\nCreate another(y/n),default=\"y\"\n")).lower() not in {"y","yes"}:
            break

main()
