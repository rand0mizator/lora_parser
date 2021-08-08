from datetime import datetime
import PySimpleGUI as sg


class Packet:

    def __init__(self, pckt):
        self.unix_time = int(pckt[:8], 16)
        self.battery_charge = int(pckt[8:10], 16)
        self.alarm_state = pckt[11]
        self.fault_state = pckt[13]
        self.tamper_state = pckt[15]
        self.smoke_level = int(pckt[16:18], 16)
        self.dirty_level = int(pckt[18:20], 16)
        self.main_battery_voltage = int(pckt[20:22], 16)
        self.temperature = int(pckt[22:24], 16)
        self.human_time = datetime.utcfromtimestamp(self.unix_time).strftime('%d-%m-%Y %H:%M:%S')

    def __str__(self):
        return f"""
Time: {self.human_time}
Unix Time: {self.unix_time}
Battery Charge:{self.battery_charge}
Alarm State: {self.alarm_state}
Fault State: {self.fault_state}
Tamper State: {self.tamper_state}     
Smoke Level: {self.smoke_level}
Dirty Level: {self.dirty_level}
Main Battery Voltage: {self.main_battery_voltage}
Temperature: {self.temperature}
        """


layout = [[sg.Text('Пакет:', size=(8,1)), sg.Input(key='-NAME-', do_not_clear=True, size=(31,1))],
          [sg.Text('Результат', size=(8,1)), sg.Multiline(size=(31,17), key='-LINE-OUTPUT-', do_not_clear=True)],
          [sg.Button('Конвертировать')]]

window = sg.Window('LoRa Parser', layout)

while True:             # Event Loop
    event, values = window.read()
    if event in (None, 'Exit'):
        break
    elif event == 'Конвертировать':
        try:
            packet = Packet(values['-NAME-'])
            window['-LINE-OUTPUT-'].update(packet)
        except ValueError:
            window['-LINE-OUTPUT-'].update('Неправильный пакет')
            continue
    else:
        window['-LINE-OUTPUT-'].update('Что-то пошло не так')
window.close()

