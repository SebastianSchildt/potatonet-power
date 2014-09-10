import urwid
import time
import epod


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
    else:
    	footer.set_text( ('banner',"Unknown input :"+str(repr(key))))
    
def item_chosen(button, choice):
    footer.set_text( ('banner',"You chose: "+str(choice)))
    


armed = False

palette = [
    ('banner', 'black', 'light gray'),
    ('streak', 'black', 'dark red'),
    ('bg', 'black', 'dark blue'),
    ('btn', 'yellow', 'dark blue'),
    ('nodehead', 'black', 'yellow'),
    ('nodeON', 'dark green', 'dark blue'),
    ('nodeOFF', 'dark red', 'dark blue'),
    ('reversed', 'standout', '')]

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
map4 = urwid.AttrMap(fill2, 'btn')



p=urwid.Pile([('pack',map1), map4, ('pack',map3)])

#p=urwid.Pile([map2, nodes, ('pack',map3)])

#loop = urwid.MainLoop(map2, palette, unhandled_input=exit_on_q)
loop = urwid.MainLoop(p, palette, unhandled_input=exit_on_q)
loop.run()