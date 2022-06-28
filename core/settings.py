import json
import sys

import PySimpleGUI as GUI


class Settings:
    def __init__(self):
        with open('./settings.json', 'r') as data:
            self.SETTINGS = json.load(data)
        GUI.theme('Gray Gray Gray')
        GUI.set_options(font='Franklin 10',)
        layout = [
            [GUI.Text(text='Resolution', size=12), GUI.Spin(values=['800x640', '1024x768', '1280x1024'], readonly=True, initial_value=f"{self.SETTINGS['HEIGHT']}x{self.SETTINGS['WIDTH']}", size=8, key='-RESOLUTION-')],
            [GUI.Text(text='Frame Rate', size=12), GUI.Spin(values=['30', '60'], readonly=True, initial_value=self.SETTINGS['FPS'], size=8, key='-FPS-')],
            [GUI.Text(text='Sound Volume', size=12), GUI.Spin(values=[x for x in range(0, 100, 5)], readonly=True, initial_value=int(self.SETTINGS['SOUNDTRACK_VOLUME']*100), size=8, key='-VOLUME-')],
            [GUI.Text(text='', visible=False, expand_x=True, enable_events=True, key='-MESSAGE-')],
            [GUI.VPush()],
            [GUI.Button('Set', size=(7, 1), key='-SAVE-'), GUI.Button('Recover', size=(7, 1), key='-RECOVER-'), GUI.Push()],
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

            if event == '-SAVE-':
                self.SETTINGS['HEIGHT'] = int(values['-RESOLUTION-'].split('x')[1])
                self.SETTINGS['WIDTH'] = int(values['-RESOLUTION-'].split('x')[0])
                self.SETTINGS['FPS'] = int(values['-FPS-'])
                self.SETTINGS['SOUNDTRACK_VOLUME'] = float(values['-VOLUME-'])/100
                
                with open('./settings.json', 'w') as data:
                    json.dump(self.SETTINGS, data, indent=4)

                self.window['-MESSAGE-'].update('Settings have been applied successfully', visible=True)

            if event == '-RECOVER-':
                with open('./settings_default.json', 'r') as data:
                    self.SETTINGS = json.load(data)
                
                self.window['-RESOLUTION-'].update(f"{self.SETTINGS['WIDTH']}x{self.SETTINGS['HEIGHT']}")
                self.window['-FPS-'].update(self.SETTINGS['FPS'])
                self.window['-VOLUME-'].update(int(self.SETTINGS['SOUNDTRACK_VOLUME']*100))

                with open('./settings.json', 'w') as data:
                    json.dump(self.SETTINGS, data, indent=4)

                self.window['-MESSAGE-'].update('Settings have been reset', visible=True)

            if event == '-CLOSE-':
                break

            if event == '-RUN-':
                self.window.close()
                return True
        
        self.window.close()


if __name__ == '__main__':
    '''
    Only for debugging.
    '''
    Settings().run()