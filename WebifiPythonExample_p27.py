#!/usr/bin/python

import Webifi_p27
import Tkinter
import tkMessageBox
import logging
import sys
import ConfigParser
import os


class GuiControls():
    def __init__(self, webifi_connect_name, webifi_password, webifi_enable_logging, webifi_network_names):
        gui = Tkinter.Tk()
        self.webifi = Webifi_p27.Webifi()
        if webifi_enable_logging:
            self.webifi.enable_logging('log.txt', logging.DEBUG, True)
        self.webifi.log_application_message(logging.INFO, "Webifi Python Example started")
        pad_x = 5
        pad_y = 3
        self.gui = gui
        self.gui_row_number = 0
        self.checkbutton_add_send_count_state = Tkinter.IntVar()
        self.checkbutton_use_encryption_state = Tkinter.IntVar()
        self.checkbutton_discoverable_state = Tkinter.IntVar()
        self.checkbutton_use_websocket_state = Tkinter.IntVar()

        gui.iconbitmap('images/favicon.ico')
        gui.title('Webifi Example')

        # connect name, connect password, set network names and start button (column 1)
        Tkinter.Label(gui, text='Connect name:').grid(row=self.get_row_num(False), column=0, padx=pad_x-2, pady=pad_y, sticky='W')
        self.entry_connect_name = Tkinter.Entry(gui, width=25)
        self.entry_connect_name.insert(0, webifi_connect_name)
        self.entry_connect_name.grid(row=self.get_row_num(True), column=0, padx=pad_x, pady=0, sticky='W')
        Tkinter.Label(gui, text='Connect password:').grid(row=self.get_row_num(True), column=0, padx=pad_x-2, pady=pad_y, sticky='W')
        self.entry_connect_password = Tkinter.Entry(gui, width=25)
        self.entry_connect_password.grid(row=self.get_row_num(True), column=0, padx=pad_x, pady=0, sticky='W')
        self.entry_connect_password.insert(0, webifi_password)
        Tkinter.Label(gui, text='Network names:').grid(row=self.get_row_num(True), column=0, padx=pad_x-2, pady=pad_y, sticky='W')
        self.text_network_names = Tkinter.Text(gui, wrap=Tkinter.WORD, undo=True, height=5, width=15)
        self.text_network_names.grid(row=self.get_row_num(True), column=0, columnspan=1, padx=pad_x-2, pady=0, sticky='WE')
        self.scroll_network_names = Tkinter.Scrollbar(gui, command=self.text_network_names.yview)
        self.scroll_network_names.grid(row=self.get_row_num(False), column=0, sticky='nsew')
        self.text_network_names['yscrollcommand'] = self.scroll_network_names.set
        self.text_network_names.insert(Tkinter.INSERT, webifi_network_names)
        self.button_set_network_names = Tkinter.Button(gui, text='Set network names', width=16, command=self.click_button_set_network_names)
        self.button_set_network_names.grid(row=self.get_row_num(True), column=0, padx=pad_x, pady=pad_y, sticky='W')
        self.image_stop = Tkinter.PhotoImage(file='images/webifiStop.gif')
        self.image_running = Tkinter.PhotoImage(file='images/webifiRunning.gif')
        self.label_status_image = Tkinter.Label(gui, image=self.image_stop)
        self.label_status_image.grid(row=self.get_row_num(False), column=0, padx=pad_x, pady=pad_y, sticky='E')
        self.button_start = Tkinter.Button(gui, text='Start', width=12, command=self.click_button_start)
        self.button_start.grid(row=self.get_row_num(True), column=0, padx=pad_x, pady=pad_y, sticky='W')

        # labels showing Session ID and Counts (column 2)
        status_pad_x = 3
        status_pad_y = 0
        self.gui_row_number = 0
        self.frame_status = Tkinter.Frame(self.gui, borderwidth=2, relief=Tkinter.RAISED)
        self.frame_status.grid(row=self.get_row_num(False), column=1, padx=pad_x, pady=pad_y, sticky='W', rowspan=8)
        Tkinter.Label(self.frame_status, text='Session ID:').grid(row=0, column=0, padx=status_pad_x-2, pady=status_pad_y, sticky='W')
        self.label_session_id = Tkinter.Label(self.frame_status, text='-1')
        self.label_session_id.grid(row=self.get_row_num(False), column=1, padx=status_pad_x-2, pady=status_pad_y, sticky='W')
        Tkinter.Label(self.frame_status, text='Request count:').grid(row=self.get_row_num(True), column=0, padx=status_pad_x-2, pady=status_pad_y, sticky='W')
        self.label_request_count = Tkinter.Label(self.frame_status, text='-1')
        self.label_request_count.grid(row=self.get_row_num(False), column=1, padx=status_pad_x-2, pady=status_pad_y, sticky='W')
        Tkinter.Label(self.frame_status, text='Send count:').grid(row=self.get_row_num(True), column=0, padx=status_pad_x-2, pady=status_pad_y, sticky='W')
        self.label_send_count = Tkinter.Label(self.frame_status, text='-1')
        self.label_send_count.grid(row=self.get_row_num(False), column=1, padx=status_pad_x-2, pady=status_pad_y, sticky='W')
        Tkinter.Label(self.frame_status, text='Buffered amount:').grid(row=self.get_row_num(True), column=0, padx=status_pad_x-2, pady=status_pad_y, sticky='W')
        self.label_buffered_amount = Tkinter.Label(self.frame_status, text='-1')
        self.label_buffered_amount.grid(row=self.get_row_num(False), column=1, padx=status_pad_x - 2, pady=status_pad_y, sticky='W')

        # use encryption, discoverable check boxes, set instance name
        self.checkbutton_use_encryption = Tkinter.Checkbutton(self.frame_status, text='Use encryption', variable=self.checkbutton_use_encryption_state, command=self.checkbutton_use_encryption_callback)
        self.checkbutton_use_encryption.grid(row=self.get_row_num(True), column=0, padx=pad_x, pady=pad_y, sticky='W')
        self.checkbutton_discoverable = Tkinter.Checkbutton(self.frame_status, text='Discoverable', variable=self.checkbutton_discoverable_state, command=self.checkbutton_discoverable_callback)
        self.checkbutton_discoverable.grid(row=self.get_row_num(True), column=0, padx=pad_x, pady=pad_y, sticky='W')
        self.checkbutton_discoverable.select()
        self.checkbutton_use_websocket = Tkinter.Checkbutton(self.frame_status, text='Use WebSocket', variable=self.checkbutton_use_websocket_state, command=self.checkbutton_use_websocket_callback)
        self.checkbutton_use_websocket.grid(row=self.get_row_num(True), column=0, padx=pad_x, pady=pad_y, sticky='W')
        self.checkbutton_use_websocket.select()
        Tkinter.Label(self.frame_status, text='Instance name:').grid(row=self.get_row_num(True), column=0, padx=pad_x-2, pady=pad_y, sticky='W')
        self.entry_instance_name = Tkinter.Entry(self.frame_status, width=25)
        self.entry_instance_name.grid(row=self.get_row_num(True), column=0, padx=pad_x, pady=0, sticky='W')
        self.entry_instance_name.insert(0, 'Webifi Python Example')
        self.button_set_network_names = Tkinter.Button(self.frame_status, text='Set instance name', width=16, command=self.click_button_set_instance_name)
        self.button_set_network_names.grid(row=self.get_row_num(True), column=0, padx=pad_x, pady=pad_y, sticky='W')

        # send data widgets
        self.gui_row_number = 0
        self.frame_send_data = Tkinter.Frame(self.gui, borderwidth=2, relief=Tkinter.RAISED)
        self.frame_send_data.grid(row=0, column=2, padx=pad_x, pady=pad_y, sticky='W', rowspan=8)
        Tkinter.Label(self.frame_send_data, text='Send Data Controls').grid(row=self.get_row_num(False), column=0, padx=pad_x-2, pady=pad_y, sticky='W')
        Tkinter.Label(self.frame_send_data, text='Data type:').grid(row=self.get_row_num(True), column=0, padx=pad_x-2, pady=pad_y, sticky='W')
        self.entry_data_type = Tkinter.Entry(self.frame_send_data, width=25)
        self.entry_data_type.grid(row=self.get_row_num(True), column=0, padx=pad_x, pady=0, sticky='W')
        self.entry_data_type.insert(0, 'data type')
        Tkinter.Label(self.frame_send_data, text='To session IDs:').grid(row=self.get_row_num(True), column=0, padx=pad_x-2, pady=pad_y, sticky='W')
        self.entry_to_session_ids = Tkinter.Entry(self.frame_send_data, width=25)
        self.entry_to_session_ids.grid(row=self.get_row_num(True), column=0, padx=pad_x, pady=0, sticky='W')
        Tkinter.Label(self.frame_send_data, text='Text to send:').grid(row=self.get_row_num(True), column=0, padx=pad_x-2, pady=pad_y, sticky='W')
        self.entry_send_data = Tkinter.Entry(self.frame_send_data, width=56)
        self.entry_send_data.grid(row=self.get_row_num(True), column=0, columnspan=2, padx=pad_x, pady=pad_y, sticky='W')
        self.entry_send_data.insert(0, 'test message')
        self.button_send = Tkinter.Button(self.frame_send_data, text='Send', width=12, command=self.click_send_data)
        self.button_send.grid(row=self.get_row_num(True), column=0, padx=pad_x, pady=pad_y, sticky='W')
        self.button_send_discovery = Tkinter.Button(self.frame_send_data, text='Send discovery', width=12, command=self.click_send_discovery)
        self.button_send_discovery.grid(row=self.get_row_num(False), column=1, padx=pad_x, pady=pad_y, sticky='W')
        self.checkbutton_add_send_count = Tkinter.Checkbutton(self.frame_send_data, text='Add send count to string', variable=self.checkbutton_add_send_count_state)
        self.checkbutton_add_send_count.grid(row=self.get_row_num(True), column=0, padx=pad_x, pady=pad_y, sticky='W')
        self.checkbutton_add_send_count.select()
        Tkinter.Label(self.frame_send_data, text='To networks:').grid(row=1, column=1, padx=pad_x-2, pady=pad_y, sticky='W')
        self.text_to_networks = Tkinter.Text(self.frame_send_data, wrap=Tkinter.WORD, undo=True, height=4, width=15)
        self.text_to_networks.grid(row=2, column=1, columnspan=1, rowspan=3, padx=pad_x-2, pady=0, sticky='WE')
        self.scroll_to_networks = Tkinter.Scrollbar(self.frame_send_data, command=self.text_to_networks.yview)
        self.scroll_to_networks.grid(row=2, column=2, rowspan=3, sticky='nsew')
        self.text_to_networks['yscrollcommand'] = self.scroll_to_networks.set

        # received data
        self.gui_row_number = 8
        Tkinter.Label(gui, text='Text received:').grid(row=self.get_row_num(True), column=0, padx=pad_x-2, pady=pad_y, sticky='W')
        self.text_rec_data = Tkinter.Text(gui, wrap=Tkinter.WORD, undo=True, height=5, width=40)
        self.text_rec_data.grid(row=self.get_row_num(True), column=0, columnspan=3, padx=pad_x-2, pady=0, sticky='WE')
        self.scroll_rec_data = Tkinter.Scrollbar(gui, command=self.text_rec_data.yview)
        self.scroll_rec_data.grid(row=self.get_row_num(False), column=3, sticky='nsew')
        self.text_rec_data['yscrollcommand'] = self.scroll_rec_data.set
        self.button_clear_rec_data = Tkinter.Button(gui, text='Clear', width=12, command=self.click_clear_rec_data)
        self.button_clear_rec_data.grid(row=self.get_row_num(True), column=0, padx=pad_x, pady=pad_y, sticky='W')

        # messages
        Tkinter.Label(gui, text='Messages:').grid(row=self.get_row_num(True), column=0, padx=pad_x-2, pady=pad_y, sticky='W')
        self.text_messages = Tkinter.Text(gui, wrap=Tkinter.WORD, undo=True, height=5, width=40)
        self.text_messages.grid(row=self.get_row_num(True), column=0, columnspan=3, padx=pad_x-2, pady=0, sticky='WE')
        self.scroll_messages = Tkinter.Scrollbar(gui, command=self.text_messages.yview)
        self.scroll_messages.grid(row=self.get_row_num(False), column=3, sticky='nsew')
        self.text_messages['yscrollcommand'] = self.scroll_messages.set
        self.button_clear_messages = Tkinter.Button(gui, text='Clear', width=12, command=self.click_clear_messages)
        self.button_clear_messages.grid(row=self.get_row_num(True), column=0, padx=pad_x, pady=pad_y, sticky='W')
        self.gui.protocol("WM_DELETE_WINDOW", self.form_closing)

        gui.mainloop()

    def get_row_num(self, new_row):
        if new_row:
            self.gui_row_number += 1
        return  self.gui_row_number

    def add_message(self, message):
        self.text_messages.insert(Tkinter.END, message + '\n')
        self.text_messages.see(Tkinter.END)

    def data_received_callback(self, data, data_type, from_who):
        if data_type == 'Discovery Response':
            # valid discovery response received
            self.add_message('Device Discovered: ' + data + ', ID: ' + str(from_who))
        else:
            message = data + ', ' + data_type + ', ' + str(from_who)
            self.text_rec_data.insert(Tkinter.END, message + '\n')
            self.text_rec_data.see(Tkinter.END)

    def connection_status_callback(self, connected):
        if connected:  # connection was successful
            self.add_message('Connection successful')
            session_id = self.webifi.get_session_id()
            self.label_session_id.config(text=session_id)
            self.label_status_image.config(image=self.image_running)
            self.button_start['text'] = 'Stop'
        else:
            # there was an error
            self.add_message('Connection failed')
            self.label_status_image.config(image=self.image_stop)
            self.button_start['text'] = 'Start'

    def message_callback(self, message):
        self.add_message(message)

    def error_callback(self, error_code):
        self.add_message('Error: ' + error_code + ' - ' + self.webifi.convert_error_code_to_string(error_code))

    def click_button_set_network_names(self):
        if self.webifi is not None:
            network_names = self.text_network_names.get("1.0", Tkinter.END).split('\n')
            self.webifi.set_network_names(network_names)

    def click_send_discovery(self):
        if self.webifi is not None:
            self.webifi.send_discovery()

    def click_button_start(self):
        if not self.webifi.connected:
            connect_name = self.entry_connect_name.get()
            connect_password = self.entry_connect_password.get()
            network_names = self.text_network_names.get("1.0", Tkinter.END).split('\n')
            input_error = False
            if connect_name is '':
                tkMessageBox.showerror('Connect name error', 'Please enter a valid connect name')
                input_error = True
            if connect_password is '':
                tkMessageBox.showerror('Connect password error', 'Please enter a valid connect password')
                input_error = True
            if not input_error:
                # start webifi service
                self.webifi.set_connect_name(connect_name)
                self.webifi.set_connect_password(connect_password)
                self.webifi.set_network_names(network_names)
                self.webifi.set_connection_status_callback(self.connection_status_callback)
                self.webifi.set_error_callback(self.error_callback)
                self.webifi.set_data_received_callback(self.data_received_callback)
                self.checkbutton_use_encryption_callback()   # turn encryption on or off
                checkbutton_state = self.checkbutton_discoverable_state.get()
                self.webifi.set_discoverable(checkbutton_state)
                instance_name = self.entry_instance_name.get()
                self.webifi.name = instance_name
                self.webifi.start()
                self.update_counters()
            self.button_start['text'] = 'Stop'
        else:
            self.webifi.close_connection()
            self.button_start['text'] = 'Start'

    def click_send_data(self):
        if self.webifi is not None:
            send_data = Webifi_p27.CreateSendData()
            send_data.data = self.entry_send_data.get()
            send_data.data_type = self.entry_data_type.get()
            send_data.to_session_ids = self.entry_to_session_ids.get().split(',')
            send_data.to_networks = self.text_to_networks.get("1.0", Tkinter.END).split('\n')
            checkbutton_state = self.checkbutton_add_send_count_state.get()
            if checkbutton_state == 1:
                counters = self.webifi.get_counters()
                send_data.data += str(counters.upload)
            if self.webifi.connected:
                self.webifi.send_data(send_data)
        else:
            tkMessageBox.showerror('Please start service', 'The service needs to be started before this action can be performed')

    def checkbutton_discoverable_callback(self):
        if self.webifi is not None:
            checkbutton_state = self.checkbutton_discoverable_state.get()
            self.webifi.set_discoverable(checkbutton_state)

    def checkbutton_use_websocket_callback(self):
        if self.webifi is not None:
            checkbutton_state = self.checkbutton_use_websocket_state.get()
            self.webifi.set_use_websocket(checkbutton_state)

    def click_button_set_instance_name(self):
        instance_name = self.entry_instance_name.get()
        self.webifi.name = instance_name

    def click_clear_rec_data(self):
        self.text_rec_data.delete(1.0, Tkinter.END)

    def click_clear_messages(self):
        self.text_messages.delete(1.0, Tkinter.END)

    def checkbutton_use_encryption_callback(self):
        checkbutton_state = self.checkbutton_use_encryption_state.get()
        if self.webifi is not None:
            if checkbutton_state == 1:
                self.webifi.set_use_encryption(True)
            else:
                self.webifi.set_use_encryption(False)

    def update_counters(self):
        if self.webifi is not None:
            counters = self.webifi.get_counters()
            self.label_request_count.config(text=str(counters.download))
            self.label_send_count.config(text=str(counters.upload))
            self.gui.after(1000, self.update_counters)

    def form_closing(self):
        if self.webifi is not None:
            self.webifi.close_connection(True)
        self.webifi = None
        self.gui.destroy()


if __name__ == "__main__":
    #check if settings file was specified
    if len(sys.argv) == 2:
        settings_filename = sys.argv[1]
    else:
        settings_filename = 'settings.ini'
    if not os.path.isfile(settings_filename):
        print('Could not load ' + settings_filename + ', using default settings')
        param_webifi_connect_name = 'connect name'
        param_webifi_password = 'password'
        param_webifi_enable_logging = False
        param_webifi_network_names = []
        param_webifi_network_names.append('network 1')
    else:
        config = ConfigParser.ConfigParser()
        config.read(settings_filename)
        connection_list = config.options('WebifiConnectionDetails')
        param_webifi_connect_name = config.get('WebifiConnectionDetails', 'connectname')
        param_webifi_password = config.get('WebifiConnectionDetails', 'connectpassword')
        param_webifi_enable_logging = True
        if config.get('WebifiConnectionDetails', 'enableLogging') == '0':
            param_webifi_enable_logging = False
        param_webifi_network_names = ''
        network_names_option = 'network'
        for item in connection_list:  # search for network names
            if item[:len(network_names_option)] == network_names_option:
                if len(param_webifi_network_names) > 0:
                    param_webifi_network_names += '\r\n'
                param_webifi_network_names += config.get('WebifiConnectionDetails', item)
    gui_controls = GuiControls(param_webifi_connect_name, param_webifi_password, param_webifi_enable_logging, param_webifi_network_names)