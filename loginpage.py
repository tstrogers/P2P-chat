import PySimpleGUI as sg

# Create the Window
def create_login_window():
    sg.theme('DarkAmber')   # Add a touch of color
    # All the stuff inside your window.
    layout = [  [sg.Text('Enter your username : '), sg.InputText()],
                [sg.Text('Enter your password : '), sg.InputText()],
                [sg.Button('Ok'), sg.Button('Cancel')] ]

    window = sg.Window('Zap Chat Login', layout)

    return window


def get_login_details(window):
# Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break
        elif event == "Ok" and values == None:
          show_failure_window()
        else:
            return values

def show_success_window():
    sg.theme('DarkAmber')   # Add a touch of color
    # All the stuff inside your window.
    #layout = [[sg.Text("Who would you like to chat with?", justification = 'left'),sg.InputText()],
    #          [sg.Button('Continue')],[sg.Button('Logout')]]
    #layout = [
    layout_column = [[sg.Text('Who would you like to chat with?',justification='center'),sg.InputText()],
              [sg.Button('Continue')],[sg.Button('Logout')]]

    layout = [[sg.Column(layout_column, element_justification='center')]]
    

    window = sg.Window('Welcome to Zap Chat!', layout)
    while True:
        event, values = window.read()
        print("values: ", values)
        if event == sg.WIN_CLOSED: # if user closes window or clicks cancel
            break
        elif event == 'Logout':
          window.close()
          start()
          return False
    window.close()


def show_failure_window():
    sg.theme('DarkAmber')   # Add a touch of color
    # All the stuff inside your window.
    #layout = [[sg.Text("Incorrect Username or Password")],[sg.Button('Retry')]]
    layout_column = [
        [sg.Text('Incorrect Username or Password',justification='center')],
        [sg.Button('Retry')]
        ]

    layout = [[sg.Column(layout_column, element_justification='center')]]
    window = sg.Window('Login Error', layout)
    while True:
        event, _ = window.read()
        if event == sg.WIN_CLOSED : # if user closes window or clicks cancel
            return False
        elif event == "Retry":
            window.close()
            return True


def start():
    window = create_login_window()
    username, password = get_login_details(window).values()
    window.close()
    while True:
        if username == "test" and password == "123":
            show_success_window()
            break
        else:
            if show_failure_window():
                window = create_login_window()
                username, password = get_login_details(window).values()
                window.close()

if __name__ == "__main__":
    start()


# def main():
#   pass

# if __name__ == "__main__":

#      main()