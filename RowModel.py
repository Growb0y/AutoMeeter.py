import json
import os.path


class RowModel:

    def __init__(self):
        if not os.path.isfile('row_model.json'):
            self.writeRowModel()
        self.readRowModel()

    def writeRowModel(self, my_name='', conf_id='', conf_pass='', date='01.01.01', time='00:00', iterance='', platform=''):

        row_model = {
                    'my_name': f'{my_name}',
                    'conf_id': f'{conf_id}',
                    'conf_pass': f'{conf_pass}',
                    'date': f'{date}',
                    'time': f'{time}',
                    'iterance': f'{iterance}',
                    'platform': f'{platform}',
        }

        with open('row_model.json', 'w') as outfile:
            json.dump(row_model, outfile)

    def readRowModel(self):

        with open('row_model.json') as model:
            row_model = json.load(model)

            string = ''
            string += row_model['my_name'] + '~@~'
            string += row_model['conf_id'] + '~@~'
            string += row_model['conf_pass'] + '~@~'
            string += row_model['date'] + '~@~'
            string += row_model['time'] + '~@~'
            string += row_model['iterance'] + '~@~'
            string += row_model['platform']
            return string
