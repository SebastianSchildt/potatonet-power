import urwid
from yesno import ConfirmButton

class ElectricityPodlet(object):
	def __init__(self, name, nr):
		self.name=name
		self.nr=nr
		self.PWRstate='off'
		self.ETHstate='unknown'
		self.buildGui()

	def buildGui(self):
		txt=urwid.Text(('nodehead', self.name), align='center')
		#headline=urwid.Filler(txt,"middle")
		headline=urwid.Padding(txt,align="center")
		headline=urwid.AttrMap(headline,'nodehead')


		eth=urwid.Text('Eth Link: '+str(self.ETHstate),align='left')
		if self.PWRstate=='on':
			#self.btn=urwid.Button("Switch PWR Off")
			self.btn=ConfirmButton("Switch PWR Off", self.PWRPress)
			self.pwr=urwid.Text( ('nodeON' ,'Power: '+str(self.PWRstate)), align='left')

		else:
			#self.btn=urwid.Button("Switch PWR On")
			self.btn=ConfirmButton("Switch PWR On", self.PWRPress)
			self.pwr=urwid.Text( ('nodeOFF' ,'Power: '+str(self.PWRstate)), align='left')


		#urwid.connect_signal(self.btn, 'click', self.PWRPress, self.name)
		#self.btnHolder=urwid.AttrMap(self.btn, 'btn', focus_map='reversed')
		self.btnHolder=self.btn
		#p=urwid.Pile([ urwid.BoxAdapter(headline,1), ('pack',self.pwr), ('pack',eth), ('pack',self.btnHolder) ])
		p=urwid.Pile([ headline, ('pack',self.pwr), ('pack',eth), ('pack',self.btnHolder) ])
		
		self.ui=urwid.LineBox(p)
		

	def PWRPress(self):
		if self.PWRstate == 'off':
			self.PWRstate='on'
			self.btn.set_label("Switch PWR Off")
			self.pwr.set_text( ('nodeON','Power: '+str(self.PWRstate)))

		else:
			self.PWRstate='off'
			self.btn.set_label("Switch PWR On")
			self.pwr.set_text( ('nodeOFF','Power: '+str(self.PWRstate)))







