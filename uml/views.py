from django.shortcuts import render
from django.conf import settings
import os
import re
import ast
import collections

def services_list(request):
    service_list = []
    for file in os.listdir(settings.FILES_DIR):
        if "." not in file:
            service_list.append(file)
    context = {'service_list':service_list}
    return render(request, 'uml/service_list.html', context)


def service_detail(request , service):
    service_path = os.path.join(settings.FILES_DIR, service)
    controller_file = ""
    class_names = []
    method_names = []
    class_details = collections.defaultdict(list)
    endpoints_list = []

    for service_file in os.listdir(service_path):
        if service_file.endswith('Controller.py'):
            controller_file = service_file
            break

    #to get the controller path
    controller_file = os.path.join(service_path, controller_file)

    #to search through the controller file for finding methods related to it ex: GET, PUT etc
    with open(controller_file , 'r') as f:
        lines= f.read()

        tree = ast.parse(lines)
        for i in tree.body:
            if isinstance(i, ast.ClassDef):
                for j in i.body:
                    if isinstance(j, ast.FunctionDef):
                        if j.name != '__init__':
                            class_details[i.name].append(j.name)


    #to search through the controller file for finding endpoints and class names
    with open(controller_file) as f:
        lines= f.readlines()

        #to print all the endpoints
        for line in lines:
            if '.add_resource' in line:
                endpoint_name = str(re.findall(r"'(.*?)'", line, re.DOTALL)[0])
                class_name = str(re.findall(r"\((.*?)\,", line)[0])
                class_details[class_name].append(endpoint_name)

    print(">>>>>>>>>>>")
    print(class_details)
    print(">>>>>>>>>>>")
    context = {'class_details':dict(class_details),'service':service}

    return render(request, 'uml/service_detail.html', context)

def look_for_any_import_class_keyword(import_details):
    return


def diagrams(request ,service, controller_name , method_name):
    class_diagrams = []
    component_diagram = []
    sequence_diagram = []
    entity_diagram = []
    block_diagram = []

    '''
    component Diagram - static view of components in the system and their relationship,
    Node              - consists of set of well defined interfaces(classes)
    Edges             - relationships between components
    
    Symbols
    o-   =represnts a provider interface(interface that is provided by interface)
    (o-   = represents required interface
    dotted lines (------) -relationship between components
    '''


    service_path = os.path.join(settings.FILES_DIR, service)
    controller_file = ""
    import_details = collections.defaultdict(list)

    for service_file in os.listdir(service_path):
        if service_file.endswith('Controller.py'):
            controller_file = service_file
            break

    #to get the controller path
    controller_file = os.path.join(service_path, controller_file)

    #to search through the controller file for finding methods related to it ex: GET, PUT etc
    with open(controller_file , 'r') as f:
        lines= f.readlines()

        #to get the list of imports and map it to correct dict key
        for line in lines:
            if 'middleware' in line and  "import" in line:
                import_details['middleware'].append(line.split('import')[1])
            if 'config' in line and "import" in line:
                import_details['config'].append(line.split('import')[1])
            if 'lib' in line and  "import" in line:
                import_details['lib'].append(line.split('import')[1])
            if 'xception' in line and  "import" in line:
                import_details['exception'].append(line.split('import')[1])
            if 'models' in line and  "import" in line:
                import_details['models'].append(line.split('import')[1])

        #so the lines to go through should correspond only to the particular method(GET ,PUT)
        starting_line = "class " + controller_name + "(BaseController):"
        end_line = "add_resource("+ controller_name
        class_line_count = 0
        method_code = []
        class_code = []
        started = False
        for line in lines:
            if starting_line in line:
                started = True
            if started and 'add_resource' in line:
                break
            if started:
                class_line_count +=1
                class_code.append(line)

        method_starting_line = "def " + method_name
        method_line_count = 0
        started = False
        for line in class_code:
            if method_starting_line in line:
                started = True
            if "def __init__" in line:
                continue
            if "def " in line and method_starting_line not in line:
                break
            if started:
                method_line_count +=1
                method_code.append(line)

        #look_for_any_import_class_keyword(dict(import_details))
        for key,value in import_details.items():
            for v in value:
                for line in method_code:
                    #print(v,line)
                    if v.lower() in line.lower():
                        print(key,v +"in the class")

        #we should find list of  classes and the methods used in there

        #we should again parse for the particular method in that file

        #see whether it is an entity or model or middleware file


        #we should


    context = {}
    return render(request, 'uml/diagrams.html', context)