import webbrowser
import os

def start():

    url="file:"+os.getcwd()+os.sep+'peer1.html'

    # Open URL in a new tab, if a browser window is already open.
    #webbrowser.open_new_tab(url + 'doc/')

    # Open URL in new window, raising the window if possible.
    #webbrowser.register(r'C:\Program Files (x86)\Mozilla Firefox\Firefox.exe',webbrowser)
    os.spawnl(os.P_NOWAIT, r'C:\Program Files (x86)\Mozilla Firefox\Firefox.exe',
              r'FireFox', '-new-tab', url)

    #webbrowser.get('C:\Program Files (x86)\Mozilla Firefox\Firefox.exe')
    #webbrowser.open_new(url)