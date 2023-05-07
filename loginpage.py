import PySimpleGUI as sg
import client as cl
import time

global_name = ""
status = ""

def create_login_window():
    sg.theme('DarkAmber') 

    layout = [  [sg.Text('Enter your username : '), sg.InputText()],
                [sg.Text('Enter your password : '), sg.InputText(key='-pwd-', password_char='*')],
                [sg.Button('Ok'), sg.Button('Cancel')], ]

    window = sg.Window('Zap Chat Login', layout,size=(700, 120),element_justification='c')

    return window


def get_login_details(window):
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break
        elif event == "Ok" and values == None:
          show_failure_window()
        else:
            return values

def show_unavailable_window():
    sg.theme('DarkAmber')
    layout_column = [[sg.Text('Any messages sent will deliver when he signs in again',justification='center')],
              [sg.Button('Ok')],[sg.Button('Cancel')]]

    layout = [[sg.Column(layout_column, element_justification='center')]]
    

    window = sg.Window(global_name+' is unavailable :( !', layout)

    while True:
        event, _ = window.read()
        if event == sg.WIN_CLOSED :
            return False
        elif event == "Ok":
            window.close()
            create_chat_window()
            return False
        elif event == "Cancel":
            window.close()
            show_success_window()
            return False


def show_success_window():
    sg.theme('DarkAmber')  
    layout_column = [[sg.Text('Who would you like to chat with?',justification='center'),sg.InputText()],
              [sg.Button('Continue')],[sg.Button('Logout')]]
    layout = [[sg.Column(layout_column, element_justification='center')]]
    window = sg.Window('Welcome to Zap Chat!', layout,size=(700, 120),element_justification='c')
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == 'Continue' and values != None:
            name = values[0]
            global global_name
            global_name = name
            cl.send_name_to_server(name)
            time.sleep(30)
            cl.receive_peer_info()
            time.sleep(10)
            if cl.global_status == "Offline":
                print(global_name + " is unavailable")
                window.close()
                show_unavailable_window()
                create_chat_window()
                return False
            else:
                window.close()
                create_chat_window()
                return False   
        elif event == 'Logout':
          window.close()
          start()
          return False

def show_failure_window():
    sg.theme('DarkAmber')
    layout_column = [
        [sg.Text('Incorrect Username or Password',justification='center')],
        [sg.Button('Retry')]
        ]

    layout = [[sg.Column(layout_column, element_justification='center')]]
    window = sg.Window('Login Error', layout)
    while True:
        event, _ = window.read()
        if event == sg.WIN_CLOSED :
            return False
        elif event == "Retry":
            window.close()
            return True

def create_chat_window():
    global global_name
    print("global name: ", global_name)
    layout = [[sg.Text('Now chatting with: '+global_name, size=(40, 1))],
          [sg.Output(size=(110, 20), font=('Helvetica 10'))],
          [sg.Multiline(size=(70, 5), enter_submits=False, key='-QUERY-', do_not_clear=False),
           sg.Button('SEND', button_color=(sg.YELLOWS[0], sg.BLUES[0]), bind_return_key=True),
           sg.Button('EXIT', button_color=(sg.YELLOWS[0], sg.GREENS[0]))]]

    window = sg.Window('Chat window', layout, font=('Helvetica', ' 13'), default_button_element_size=(8,2), use_default_focus=False, finalize=True)
    
    while True: 
        event, value = window.read()
        if event in (sg.WIN_CLOSED, 'EXIT'): 
            window.close()
            show_success_window()
            break
        if event == 'SEND':
            query = value['-QUERY-'].rstrip()
            print("You"+ ": "+query, flush=True)

    window.close()
    
def start():
    cl.connect_to_server()
    window = create_login_window()
    username, password = get_login_details(window).values()
    window.close()
    while True:
        if username == "sarah" and password == "123":
            cl.send_name_to_server(username)
            show_success_window()
            break
        if username == "jim" and password == "123":
            cl.send_name_to_server(username)
            show_success_window()
            break
        else:
            if show_failure_window():
                window = create_login_window()
                username, password = get_login_details(window).values()
                window.close()

if __name__ == "__main__":
    start()
