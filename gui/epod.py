import urwid

class ElectricityPodlet(object):
	def __init__(self, name, nr):
		self.name=name
		self.nr=nr
		self.PWRstate='off'
		self.ETHstate='unknown'
		self.buildGui()

	def buildGui(self):
		txt=urwid.Text(('nodehead', self.name), align='center')
		headline=urwid.Filler(txt,"middle")


		eth=urwid.Text('Eth Link: '+str(self.ETHstate),align='left')
		if self.PWRstate=='on':
			self.btn=urwid.Button("Switch PWR Off")
			self.pwr=urwid.Text( ('nodeON' ,'Power: '+str(self.PWRstate)), align='left')

		else:
			self.btn=urwid.Button("Switch PWR On")
			self.pwr=urwid.Text( ('nodeOFF' ,'Power: '+str(self.PWRstate)), align='left')


		urwid.connect_signal(self.btn, 'click', self.PWRPress, self.name)
		self.btnHolder=urwid.AttrMap(self.btn, None, focus_map='reversed')

		p=urwid.Pile([ urwid.BoxAdapter(headline,1), ('pack',self.pwr), ('pack',eth), ('pack',self.btnHolder) ])
		self.ui=urwid.LineBox(p)
		

	def PWRPress(self, button, data):
		if self.PWRstate == 'off':
			self.PWRstate='on'
			self.btn.set_label("Switch PWR Off")
			self.pwr.set_text( ('nodeON','Power: '+str(self.PWRstate)))

		else:
			self.PWRstate='off'
			self.btn.set_label("Switch PWR On")
			self.pwr.set_text( ('nodeOFF','Power: '+str(self.PWRstate)))







