import json
import sys

import PySimpleGUI as GUI


with open('./settings.json', 'r') as data:
    SETTINGS = json.load(data)


class Settings:
    def __init__(self):
        GUI.theme('Gray Gray Gray')
        GUI.set_options(
            font='Franklin 10',
        )
        layout = [
            [GUI.Text('Resolution'), GUI.Spin(['800x640', '1280x1024', '1024x768'], key='-RESOLUTION-')],
            [GUI.Text('Frame Rate'), GUI.Spin(['30', '60'], key='-FPS-')],
            [GUI.Text('Sound Volume'), GUI.Spin([x for x in range(0, 100, 5)], key='-VOLUME-')],
            [GUI.VPush()],
            [GUI.Button('Read', size=(7, 1), key='-READ-'), GUI.Button('Save', size=(7, 1), key='-SAVE-'), GUI.Button('Recover', size=(6, 1), key='-RECOVER-'), GUI.Push()],
            [GUI.Button('Run', size=(7, 1), key='-RUN-'), GUI.Push(), GUI.Button('Close', size=(7, 1), key='-CLOSE-')]
        ]
        self.window = GUI.Window(
            title='Settings',
            layout=layout,
            size=(300, 200),
            no_titlebar=True,
            element_justification='left',
        )


    def run(self):
        while True:
            event, values = self.window.read()

            if event == '-READ-':
                with open('./settings.json', 'r') as data:
                    SETTINGS = json.load(data)
                print(f'settings: {SETTINGS}')

            if event == '-SAVE-':
                # SETTINGS['WIDTH'] = values['']
                print(f'values: {values}')

            if event == '-CLOSE-':
                break
        
        self.window.close()
        sys.exit()

    def __str__(self):
        return 'settings'

st = Settings()
st.run()