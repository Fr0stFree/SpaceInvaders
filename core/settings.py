import json
import sys

import PySimpleGUI as GUI


class Settings:
    GUI.theme('Gray Gray Gray')
    WINDOW_SIZE = (300, 200)
    
    def __init__(self, SETTINGS):
        self.SETTINGS = SETTINGS
    
        GUI.theme('Gray Gray Gray')
        GUI.set_options(font='Franklin 10')
        
        TEXT_RESOLUTION = GUI.Text(text='Resolution', size=12)
        SPIN_RESOLUTION = GUI.Spin(
            values=['800x640', '1024x768', '1280x1024'],
            readonly=True,
            initial_value=f"{SETTINGS['WIDTH']}x{SETTINGS['HEIGHT']}",
            size=8,
            enable_events=True,
            key='-RESOLUTION-',
        )
        TEXT_FPS = GUI.Text(text='Frame Rate', size=12)
        SPIN_FPS = GUI.Spin(
            values=['30', '60'],
            readonly=True,
            initial_value=SETTINGS['FPS'],
            size=8,
            enable_events=True,
            key='-FPS-',
        )
        TEXT_VOLUME = GUI.Text(text='Sound Volume', size=12)
        SPIN_VOLUME = GUI.Spin(
            values=[x for x in range(0, 100, 5)],
            readonly=True,
            initial_value=int(SETTINGS['SOUNDTRACK_VOLUME']*100),
            size=8,
            enable_events=True,
            key='-VOLUME-',
        )
        TEXT_MESSAGE = GUI.Text(text='', visible=False, expand_x=True, enable_events=True, key='-MESSAGE-')
        BUTTON_SET = GUI.Button('Set', size=(7, 1), key='-SET-')
        BUTTON_RUN = GUI.Button('Run', size=(7, 1), key='-RUN-')
        BUTTON_RESET = GUI.Button('Reset', size=(7, 1), key='-RESET-')
        BUTTON_CLOSE = GUI.Button('Close', size=(7, 1), key='-CLOSE-')
        layout = [
            [TEXT_RESOLUTION,       SPIN_RESOLUTION,                      ],
            [TEXT_FPS,              SPIN_FPS,                             ],
            [TEXT_VOLUME,           SPIN_VOLUME,                          ],
            [TEXT_MESSAGE                                                 ],
            [GUI.VPush()                                                  ],
            [BUTTON_SET,            BUTTON_RESET,          GUI.Push()     ],
            [BUTTON_RUN,            GUI.Push(),            BUTTON_CLOSE   ],
        ]
        self.window = GUI.Window(
            title='Settings',
            layout=layout,
            size=self.WINDOW_SIZE,
            no_titlebar=True,
        )


    def open(self):
        while True:
            event, values = self.window.read()

            if event == '-SET-':
                self.SETTINGS['HEIGHT'] = int(values['-RESOLUTION-'].split('x')[1])
                self.SETTINGS['WIDTH'] = int(values['-RESOLUTION-'].split('x')[0])
                self.SETTINGS['FPS'] = int(values['-FPS-'])
                self.SETTINGS['SOUNDTRACK_VOLUME'] = float(values['-VOLUME-'])/100
                
                with open('./settings.json', 'w') as data:
                    json.dump(self.SETTINGS, data, indent=4)

                self.window['-MESSAGE-'].update('Settings have been applied successfully', visible=True)

            if event == '-RESET-':
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
                return
            
            # Обновление окна вывода сообщений при изменении настроек
            if event in ['-FPS-', '-RESOLUTION-', '-VOLUME-']:
                self.window['-MESSAGE-'].update('')

        self.window.close()


if __name__ == '__main__':
    '''
    Запуск для отладки.
    '''
    with open('./settings.json', 'r') as data:
        settings = json.load(data)
    Settings(settings).open()