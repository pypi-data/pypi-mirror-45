from lxml import etree
from io import StringIO

#
# Function that validates an xml file and aborts with 1 if it is not valid
#
def validateXML(filename_xml: str, filename_xsd: str, debug:bool = False) -> None:
    isValid:bool = validateXML_internal(filename_xml, filename_xsd)
    if not isValid:
        print("ELAN file does not validate. Aborting")
        quit(1)

#
# Function that does the actual validation
#
def validateXML_internal(filename_xml: str, filename_xsd: str, debug:bool = False) -> bool:
    # open and read schema file
    with open(filename_xsd, 'r') as schema_file:
        schema_to_check = schema_file.read()

    # print(schema_to_check)

    # open and read xml file
    with open(filename_xml, 'r') as xml_file:
        xml_to_check = xml_file.read()

    # print(xml_to_check)

    xmlschema_doc = etree.parse(StringIO(schema_to_check))
    xmlschema = etree.XMLSchema(xmlschema_doc)

    # parse xml
    try:
        #doc = etree.parse(StringIO(xml_to_check))
        doc = etree.parse(filename_xml)
        if(debug):
            print('XML well formed, syntax ok.')

    # check for file IO error
    except IOError:
        print('Invalid File')
        return(False)

    # check for XML syntax errors
    except etree.XMLSyntaxError as err:
        print('XML Syntax Error, see error_syntax.log')
        with open('error_syntax.log', 'w') as error_log_file:
            error_log_file.write(str(err.error_log))
        return(False)

    except:
        print('Unknown error, exiting.')
        return(False)

    # validate against schema
    try:
        xmlschema.assertValid(doc)
        if(debug):
            print('XML valid, schema validation ok.')

    except etree.DocumentInvalid as err:
        print('Schema validation error, see error_schema.log')
        with open('error_schema.log', 'w') as error_log_file:
            error_log_file.write(str(err.error_log))

        return(False)

    except:
        print('Unknown error, exiting.')
        return(False)

    return(True)
