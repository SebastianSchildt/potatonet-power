import urwid

class YesNo(urwid.WidgetWrap):
    """A dialog that appears with nothing but a close button """
    signals = ['yes', 'no']
    def __init__(self):

        ybutton = urwid.Button(('btn',"YES"))
        nbutton = urwid.Button(('btn',"NO"))
        col=urwid.Columns([ybutton,nbutton])

        urwid.connect_signal(nbutton, 'click',
            lambda button:self._emit("no"))

        urwid.connect_signal(ybutton, 'click',
            lambda button:self._emit("yes"))


        pile = urwid.Pile([urwid.Text(
            "Relly?\n"), col])
        fill = urwid.Filler(pile)
        self.__super.__init__(urwid.AttrWrap(fill, 'popbg'))



class ConfirmButton(urwid.PopUpLauncher):

    def __init__(self, label, callback):
        self.realbtn=urwid.Button(label)
        self.callback=callback
        urwid.connect_signal(self.realbtn, 'click',
            lambda button: self.open_pop_up())
        
        btn=urwid.AttrMap(self.realbtn, 'btn', focus_map='reversed')
        btn=urwid.Padding(btn, left=2, right=2)
        
        self.yes=False

        self.__super.__init__(btn)
        

    def create_pop_up(self):
        pop_up = YesNo()
        urwid.connect_signal(pop_up, 'no',
            lambda button: self.close_pop_up())
        urwid.connect_signal(pop_up, 'yes', self.perform_action)

        return pop_up

    def perform_action(self,data):
        self.callback()
        self.close_pop_up()

    def set_label(self, newlabel):
        self.realbtn.set_label(newlabel)


    def get_pop_up_parameters(self):
        return {'left':2, 'top':-3, 'overlay_width':16, 'overlay_height':3}