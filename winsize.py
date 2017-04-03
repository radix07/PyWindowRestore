import win32con
import win32gui
import win32process
import pickle

STRUCT_PID = 0
STRUCT_LABEL = 1
STRUCT_HANDLE = 2
STRUCT_COORDS = 3

def isRealWindow(hWnd):
    '''Return True iff given window is a real Windows application window.'''
    if not win32gui.IsWindowVisible(hWnd):
        return False
    if win32gui.GetParent(hWnd) != 0:
        return False
    hasNoOwner = win32gui.GetWindow(hWnd, win32con.GW_OWNER) == 0
    lExStyle = win32gui.GetWindowLong(hWnd, win32con.GWL_EXSTYLE)
    if (((lExStyle & win32con.WS_EX_TOOLWINDOW) == 0 and hasNoOwner)
      or ((lExStyle & win32con.WS_EX_APPWINDOW != 0) and not hasNoOwner)):
        if win32gui.GetWindowText(hWnd):
            return True
    return False

def getWindowSizes():
    '''
    Return a list of tuples (handler, (width, height)) for each real window.
    '''
    def callback(hWnd, windows):
        if not isRealWindow(hWnd):
            return
        rect = win32gui.GetWindowRect(hWnd)
        name = win32gui.GetWindowText(hWnd)
        _, pid = win32process.GetWindowThreadProcessId(hWnd)
        windows.append((pid,name,hWnd, rect))
        #windows.append((pid,name,hWnd, (rect[2] - rect[0], rect[3] - rect[1])))
    windows = []
    win32gui.EnumWindows(callback, windows)
    return windows

def setWindowSize(winSt):
    def callback(hWnd, windows):
        if not isRealWindow(hWnd):
            return
        _, pid = win32process.GetWindowThreadProcessId(hWnd)
        if(pid == winSt[STRUCT_PID]):
            win_rect = winSt[STRUCT_COORDS]
            try:
                win32gui.MoveWindow(hWnd, win_rect[0], win_rect[1], win_rect[2]-win_rect[0],win_rect[3]-win_rect[1], True)
            except:
                print "Can't Move:",winSt[STRUCT_LABEL]
                pass
    windows = []
    win32gui.EnumWindows(callback, windows)
    return windows

save = 0
load = 1
if save:
    file1 = open("layout.pkl",'wb')
    pickle.dump(getWindowSizes(),file1)
    file1.close()
    for win in getWindowSizes():
        print win

if load:
    file1 = open('layout.pkl','rb')
    struct = pickle.load(file1)
    file1.close()
    for i in struct:
        setWindowSize(i)



