import urwid
import time
import epod
import dialog
from yesno import ConfirmButton

palette = [
    ('banner', 'black', 'light gray'),
    ('streak', 'black', 'dark red'),
    ('bg', 'white', 'dark blue'),
    ('btn', 'black', 'light cyan', 'bold'),
    ('nodehead', 'black', 'yellow'),
    ('nodeON', 'dark green', 'dark blue'),
    ('nodeOFF', 'dark red', 'dark blue'),
    ('popbg', 'white', 'dark red'),
    ('reversed', 'standout', '')]


def exit_on_q(key):
    global armed
    if key in ('q', 'Q') and not armed:
    	footer.set_text( ('banner', " Really exit (y/n)? ") )
    	armed=True
    elif key in ('n', 'N') and armed:
    	footer.set_text( ('banner', " Press q to exit ") )
    	armed=False
    elif key in ('y', 'Y') and armed:
        raise urwid.ExitMainLoop()
    elif key == 'f1':
        btn_init.open_pop_up()
    elif key == 'f2':
        btn_state.open_pop_up()
    elif key == 'f3':
        btn_3d.open_pop_up()
    elif key == 'f12':
        btn_quit.open_pop_up()
        
    else:
    	footer.set_text( ('banner',"Unknown input :"+str(repr(key))))
    
def item_chosen(button, choice):
    footer.set_text( ('banner',"You chose: "+str(choice)))
    
def re_init():
    print("YO")
    pass

def update_state():
    pass

def enable_3d():
    #sa.Alert("Msg","Jo")
    d=dialog.do_yesno("Realy", 10,22)
    exitcode, exitstring = d.main()
    #print("Code is "+str(exitcode)+" string is "+str(exitstring))
    #loop.screen=urwid.raw_display.Screen()
    loop.widget=p
    loop.draw_screen()

def quit():
    raise urwid.ExitMainLoop()


armed = False

title = urwid.Text(('banner', " PotatoControl "), align='center')
map1 = urwid.AttrMap(title, 'streak')

fill = urwid.Filler(map1, 'top')
map2 = urwid.AttrMap(fill, 'bg')

footer = urwid.Text(('banner', " Press q to exit "), align='left')
map3 = urwid.AttrMap(footer, 'bg')


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







p=urwid.Pile([('pack',map1), map4, ('pack',buttonrow), ('pack',map3)])

#p=urwid.Pile([map2, nodes, ('pack',map3)])

#loop = urwid.MainLoop(map2, palette, unhandled_input=exit_on_q)
loop = urwid.MainLoop(p, palette, unhandled_input=exit_on_q,pop_ups=True)
loop.run()