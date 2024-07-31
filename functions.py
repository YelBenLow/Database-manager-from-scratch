import os
import shutil
import subprocess
import time
from datetime import datetime

def get_current_databases():
    path_to_dir = os.getcwd() + '\\' + 'Databases'
    return os.listdir(path_to_dir)

def get_current_database_tables(dbase):
    path = os.getcwd() + '\\' + 'Databases' + '\\' + dbase

    txtfiles = []
    for txtfinder in os.listdir(path):
        if '.txt' in txtfinder:
            txtfiles.append(txtfinder)

    return txtfiles

def get_saved_queries():
    path = os.getcwd() + '\\' + 'Queries'
    queries = []
    for querifinder in os.listdir(path):
        if '.query' in querifinder:
            queries.append(querifinder[:-6])

    return queries

def create_database(database_name):
    database_path = os.getcwd() + '\\' + 'Databases' + '\\' + database_name
    if os.path.exists(database_path):
        return 'Hiba: Ez az adatbázis már létezik.'
    else:
        os.mkdir(database_path)
        return 'Siker'


def delete_database(database_name):
    database_path = os.getcwd() + '\\' + 'Databases' + '\\' + database_name
    if os.path.exists(database_path):
        shutil.rmtree(database_path) # shutil azokat a mappákat is törli, amiben vannak fájlok is.
        return 'Siker'
    else:
        return 'Hiba: Ez az adatbázis nem létezik.'


def create_table(database_name, table_name):
    table_path = os.getcwd() + '\\' + 'Databases' + '\\' + database_name + '\\' + table_name + '.txt'
    if os.path.exists(table_path):
        return 'Hiba: Ez a tábla már létezik'
    else:
        table_file = open(table_path, 'w', encoding = 'utf-8')
        table_file.close()

        return 'Siker'


def delete_table(database_name, table_name):
    table_path = os.getcwd() + '\\' + 'Databases' + '\\' + database_name + '\\' + table_name + '.txt'
    if os.path.exists(table_path):
        os.remove(table_path)
        return 'Siker'

    else:
        return 'Hiba: Ez a tábla nem létezik'

def get_table_content(database_name, table_name):
    if database_name == '__nagyonegyedikülönckecreatedQuery':
        table_path = os.getcwd() + '\\' + '_query.query'

    elif database_name == '__nagyonegyedikülönckesavedQuery':
        table_path = os.getcwd() + '\\' + 'Queries' + '\\' + table_name

    else:
        table_path = os.getcwd() + '\\' + 'Databases' + '\\' + database_name + '\\' + table_name + '.txt'


    if os.path.exists(table_path):
        return_data = {'Columns': [], 'Content': []}
        helper = 0

        with open(table_path, 'r', encoding = 'utf-8', buffering = 1) as file:
            for content in file:
                if helper == 0:
                    return_data['Columns'] = content.split()
                    helper += 1

                else:
                    return_data['Content'].append(content.split())

        return return_data

    else:
        return f'Hiba: Ez az elérési út nem létezik!\n({table_path})'

def tablecontent_record_manipulation(database_name, table_name, input_line, operation):
    table_path = os.getcwd() + '\\' + 'Databases' + '\\' + database_name + '\\' + table_name + '.txt'
    tablecontent = get_table_content(database_name, table_name)
    line = input_line

    if tablecontent['Columns']:
        if operation == 'add':
            if len(line.split()) < len(tablecontent['Columns']):
                if line[-1] != ' ':
                    line += ' '+' '.join(['None' for _ in range(abs(len(line.split()) - len(tablecontent['Columns'])))])
                else:
                    line +=' '.join(['None' for _ in range(abs(len(line.split()) - len(tablecontent['Columns'])))])

            with open(table_path, 'a', encoding = 'utf-8', buffering = 1) as f:
                f.write(line+'\n')

            return 'Siker'

        elif operation == 'del':
            index = int(input_line) - 1
            my_content = tablecontent['Content']
            my_content.remove(my_content[index])

            with open(table_path, 'w', encoding='utf-8', buffering = 1) as f:
                f.write(' '.join(tablecontent['Columns'])+'\n')
                for content in my_content:
                    f.write(' '.join(content)+'\n')

            return 'Siker'
    else:
        return 'Nincs oszlop!'

def tablecontent_column_manipulation(database_name, table_name, column_name, operation):
    table_path = os.getcwd() + '\\' + 'Databases' + '\\' + database_name + '\\' + table_name + '.txt'
    tablecontent = get_table_content(database_name, table_name)
    columns = tablecontent['Columns']
    content = tablecontent['Content']

    if operation == 'add':
        if column_name not in columns:
            columns.append(column_name)
            if content:
                for line in content:
                    line.append('None')  # we ignore this shit warning

            with open(table_path, 'w', encoding='utf-8', buffering = 1) as f:
                f.write(' '.join(columns)+'\n')
                if content:
                    for record in content:
                        f.write(' '.join(record)+'\n')
            return 'Siker'
        else:
            return 'Ez az oszlop már létezik'

    elif operation == 'del':
        if column_name in columns:
            columnindex = columns.index(column_name)
            columns.remove(column_name)
            if content:
                for line in content:
                    line.remove(line[columnindex])  # we ignore this shit warning again

            with open(table_path, 'w', encoding='utf-8', buffering = 1) as f:
                f.write(' '.join(columns)+'\n')
                if content:
                    for record in content:
                        f.write(' '.join(record)+'\n')
            return 'Siker'
        else:
            return 'Ez az oszlop nem létezik'

def sorszerkeszto(database_name, table_name, sor, column_name, data):
    table_path = os.getcwd() + '\\' + 'Databases' + '\\' + database_name + '\\' + table_name + '.txt'
    tablecontent = get_table_content(database_name, table_name)
    columns = tablecontent['Columns']
    content = tablecontent['Content']

    if content:
        columnindex = columns.index(column_name)
        content[sor-1][columnindex] = data

        with open(table_path, 'w', encoding='utf-8', buffering = 1) as f:
            f.write(' '.join(columns) + '\n')
            for sorok in content:
                f.write(' '.join(sorok)+'\n')

        return 'Siker'


    elif not columns:
        return 'Nincs oszlop!'

    elif not content:
        return 'Nincs sor!'

def doQueryStuff(database_name, sql):
    database_path = os.getcwd() + '\\' + 'Databases' + '\\' + database_name

    csak_ezeket = ['select', 'from', 'where']

    sqlHentesFeldolgozo = [tyuk.lower() if tyuk.lower() in csak_ezeket else tyuk for tyuk in sql.split()]

    select_table = sqlHentesFeldolgozo[sqlHentesFeldolgozo.index('from') + 1:sqlHentesFeldolgozo.index('from') + 2]
    select_columns = sqlHentesFeldolgozo[sqlHentesFeldolgozo.index('select')+1:sqlHentesFeldolgozo.index('from')]

    operators = ['==', '!=', '<', '>', '<=', '>=', 'and', 'or']
    condition_dict = None
    content = get_table_content(database_name, select_table[0].strip())

    if ';' in select_table[0]:
        select_table[0] = select_table[0].replace(';','')


    try:
        select_conditions = sqlHentesFeldolgozo[sqlHentesFeldolgozo.index('where')+1:]
    except:
        select_conditions = None


    if select_columns != '*':
        for tisztitas in select_columns:
            if ',' in tisztitas:
                copyindex = select_columns.index(tisztitas)
                for kosz in range(tisztitas.count(',')):
                    select_columns[copyindex] = select_columns[copyindex].replace(',', '')

    if select_conditions:
        for kiegeszites in select_conditions:
            if kiegeszites == '=':
                select_conditions[select_conditions.index(kiegeszites)] = '=='
            elif kiegeszites.lower() in operators:
                select_conditions[select_conditions.index(kiegeszites)] = kiegeszites.lower()

        if ';' in select_conditions[-1]:
            select_conditions[-1] = select_conditions[-1][:-1]

    if select_conditions and (select_conditions.count('and') >= 1 or select_conditions.count('or') >= 1):
        condition_dict = {'and': [],
                          'or': []}

        statements = select_conditions.count('and')+select_conditions.count('or')
        left, right = 0, 0
        last_operator = ''
        for cond in range(1, statements+1):
            left, right = right, cond*4

            if right == 4:
                condition_dict[select_conditions[right-1]].append(select_conditions[left:right-1])
                last_operator = select_conditions[right-1]

            else:
                condition_dict[select_conditions[left-1]].append(select_conditions[left:right-1])
                last_operator = select_conditions[right-1]


        condition_dict[last_operator].append(select_conditions[-3:])

    #  pass code to an outer helper .py file

    skip_id = 0
    with open('query.py', 'w', encoding = 'utf-8') as f:
        ids = {}
        if select_columns[0] != '*':
            for id in select_columns:
                ids[id] = content['Columns'].index(id)

            if select_conditions:
                for check in select_conditions:
                    if check in content['Columns'] and check not in ids:
                        ids[check] = content['Columns'].index(check)
                        skip_id += 1
        else:
            for id in content['Columns']:
                ids[id] = content['Columns'].index(id)

        skip_ids = len(ids)-skip_id
        f.write(f'indexes = {list(ids.values())}\n')
        f.write(f'selected_items = [{[content["Columns"][x] for x in ids.values()]}]\n')
        f.write(f'selected_items = [selected_items[0][:{skip_ids}]]\n\n')

        f.write(f'for row in {content["Content"]}:\n')
        f.write(f'{" "*4}sel_row = []\n')
        f.write(f'{" "*4}for index in indexes[:{skip_ids}]:\n')
        f.write(f'{" "*8}try:\n')
        if select_conditions:
            condi_row = 'if '

            if condition_dict:
                print('ez')
                ors = '('
                ands = 'and '

                if condition_dict['or']:
                    for vagy in condition_dict['or']:
                        for elem in condition_dict['or'][condition_dict['or'].index(vagy)]:
                            if elem not in content['Columns']:
                                if elem not in operators:
                                    if elem.isnumeric() or (elem[0] == '-' and elem[1:].isnumeric()):
                                        ors += elem
                                    else:
                                        ors += f'"{elem}"'
                                else:
                                    ors += elem
                            else:
                                if content['Content'][0][ids[elem]].isnumeric():
                                    ors += f'int(row[{ids[elem]}])'

                                else:
                                    ors += f'row[{ids[elem]}]'

                        ors += ' or ' if condition_dict['or'].index(vagy) != len(condition_dict['or'])-1 else ''

                    ors += ')'

                else:
                    ors = None

                ands = ands if ors else ''

                if condition_dict['and']:
                    for es in condition_dict['and']:
                        for elem in condition_dict['and'][condition_dict['and'].index(es)]:
                            if elem not in content['Columns']:
                                if elem not in operators:
                                    if elem.isnumeric() or (elem[0] == '-' and elem[1:].isnumeric()):
                                        ands += elem
                                    else:
                                        ands += f'"{elem}"'
                                else:
                                    ands += elem
                            else:
                                if content['Content'][0][ids[elem]].isnumeric():
                                    ands += f'int(row[{ids[elem]}])'

                                else:
                                    ands += f'row[{ids[elem]}]'

                        ands += ' and ' if condition_dict['and'].index(es) != len(condition_dict['and']) - 1 else ''
                else:
                    ands = None


                final_condition = f'if{ors if ors else ""}{" " if ands else ""}{ands if ands else ""}:'

                f.write(f'{" " * 12}{final_condition}\n')
                f.write(f'{" " * 16}sel_row.append(row[index])\n')

                f.write(f'{" " * 8}except:\n')
                f.write(f'{" " * 12}pass\n')

                f.write(f'{" " * 4}if sel_row:\n')
                f.write(f'{" " * 8}selected_items.append(sel_row)\n\n')


            else:
                for condi in select_conditions:
                    condi = condi.strip()
                    if condi not in content['Columns']:
                        if condi not in operators:
                            if (condi.isnumeric() or (condi[0] == '-' and condi[1:].isnumeric())) and condi != None:
                                condi_row += condi + ' ' if select_conditions.index(condi) != len(select_conditions)-1 else condi + ':'
                            else:
                                condi_row += '"' + condi + '"' + ' ' if select_conditions.index(condi) != len(select_conditions) - 1 else '"' + condi + '"' + ':'
                        else:
                            condi_row += condi + ' ' if select_conditions.index(condi) != len(select_conditions) - 1 else condi + ':'
                    else:
                        if content['Content'][0][ids[condi]].isnumeric() or content['Content'][0][ids[condi]][1:].isnumeric():
                            condi_row += f'int(row[{ids[condi]}])' + ' ' if select_conditions.index(condi) != len(select_conditions)-1 else f'int(row[{ids[condi]}])' + ':'
                        else:
                            condi_row += f'row[{ids[condi]}]' + ' ' if select_conditions.index(condi) != len(select_conditions) - 1 else f'row[{ids[condi]}]' + ':'

                f.write(f'{" "*12}{condi_row}\n')
                f.write(f'{" "*16}sel_row.append(row[index])\n')

                f.write(f'{" "*8}except:\n')
                f.write(f'{" "*12}pass\n')

                f.write(f'{" "*4}if sel_row:\n')
                f.write(f'{" "*8}selected_items.append(sel_row)\n\n')


        else:
            f.write(f'{" " * 12}sel_row.append(row[index])\n')
            f.write(f'{" " * 8}except:\n')
            f.write(f'{" " * 12}pass\n')
            f.write(f'{" " * 4}if sel_row:\n')
            f.write(f'{" " * 8}selected_items.append(sel_row)\n\n')

        f.write(f'if selected_items:')
        f.write(f'\n{" "*4}with open("_query.query", "w", encoding="utf-8", buffering=1) as q:\n')
        f.write(f'{" "*8}for write in selected_items:\n')
        f.write(f'{" "*12}q.write(" ".join(write)+"\\n")\n')

    time.sleep(0.05)
    subprocess.Popen(["python", "query.py"], shell=False)

    time.sleep(0.05)
    return get_table_content(database_name='__nagyonegyedikülönckecreatedQuery', table_name='')


def delete_query(query_name):
    query_path = os.getcwd() + '\\' + 'Queries' + '\\' + f'{query_name}.query'
    if os.path.exists(query_path):
        os.remove(query_path)
        return 'Siker'

    else:
        return 'Hiba: Ez a lekérdezés nem létezik'

def makeEverythingOk():
    feelings = ['Databases', 'Queries']
    for feeling in feelings:
        if not os.path.exists(os.getcwd()+'\\'+feeling):
            os.mkdir(feeling)

    if not os.path.exists(os.getcwd()+'\\'+'_query.query'):
        with open(os.getcwd()+'\\'+'_query.query', 'w', encoding = 'utf-8') as f:
            f.write('nye')
