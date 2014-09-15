import urwid
import time
import epod
import dialog
from yesno import ConfirmButton

palette = [
    ('banner', 'black', 'light gray'),
    ('streak', 'black', 'dark red'),
    ('bg', 'white', 'dark blue'),
    ('btn', 'black,bold', 'light cyan'),
    ('nodehead', 'black', 'yellow'),
    ('nodeON', 'dark green', 'dark blue'),
    ('nodeOFF', 'dark red', 'dark blue'),
    ('popbg', 'white', 'dark red'),
    ('reversed', 'standout', '')]


def global_keys(key):
    if key == 'f1':
        btn_init.open_pop_up()
    elif key == 'f2':
        btn_state.open_pop_up()
    elif key == 'f3':
        btn_3d.open_pop_up()
    elif key == 'f12' or key == 'q':
        btn_quit.open_pop_up()
        
    #else:
    #	footer.set_text( ('banner',"Unknown input :"+str(repr(key))))
    
def item_chosen(button, choice):
    footer.set_text( ('banner',"You chose: "+str(choice)))
    
def re_init():
    print("YO")
    pass

def update_state():
    pass

def enable_3d():
    pass

def quit():
    raise urwid.ExitMainLoop()



title = urwid.Text(('banner', " PotatoControl "), align='center')
map1 = urwid.AttrMap(title, 'streak')

fill = urwid.Filler(map1, 'top')
map2 = urwid.AttrMap(fill, 'bg')



####Make a button thingy
body=[]
for c in range(0,20):
    button=epod.ElectricityPodlet("Node "+str(c),c)
    body.append(button.ui)

    #body.append(urwid.AttrMap(button.ui, None, focus_map='reversed'))


#menu=urwid.GridFlow(urwid.SimpleFocusListWalker(body),25,1,1,'center')
menu=urwid.GridFlow(body,25,3,1,'center')

nodes = urwid.Padding(menu, left=2, right=2)
fill2 = urwid.Filler(nodes, 'top')
map4 = urwid.AttrMap(fill2, 'bg')

#Buttons
btn_init =ConfirmButton("F1: ReInit Relais", re_init)
btn_state=ConfirmButton("F2: Update State", update_state)
btn_3d   =ConfirmButton("F3: Enable 3D Acceleration", enable_3d)
btn_quit =ConfirmButton("F12/Q: Quit", quit)

buttonrow=urwid.Columns([ btn_init, btn_state, btn_3d, btn_quit])
buttonrow=urwid.AttrMap(buttonrow, 'bg')







p=urwid.Pile([('pack',map1), map4, ('pack',buttonrow)])

#p=urwid.Pile([map2, nodes, ('pack',map3)])

#loop = urwid.MainLoop(map2, palette, unhandled_input=exit_on_q)
loop = urwid.MainLoop(p, palette, unhandled_input=global_keys,pop_ups=True)
loop.run()