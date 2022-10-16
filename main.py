from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
import os
from kivy.properties import NumericProperty
from time import sleep
from kivy.uix.screenmanager import ScreenManager,Screen
import shutil
Builder.load_string('''
<Root>:
	BoxLayout:
		orientation:'vertical'
		BoxLayout:
			canvas.before:
				Color:
					rgba:0,0,0,1
				Rectangle:
					size:self.size
					pos:self.pos
			size_hint_y:0.08
			size_hint_x:1
			BoxLayout:
				Label:
					text:"MADE WITH KIVY BY AJ"
					pos:self.pos
					size:self.size
			BoxLayout:
				size_hint:0.2,1
				pos_hint:{'right':1}
				Button:
					text:'SETTINGS'
					on_press:root.changescreen()
		BoxLayout:
			orientation:'vertical'
			canvas.before:
				Color:
					rgba:1,1,1,0.3
				Rectangle:
					size:self.size
					pos:self.pos
			BoxLayout:
				size_hint:1,0.15
				pos_hint_y:{'top':1}
				Label:
					size:self.size
					text:
					id:label1
			BoxLayout:
				orientation:'vertical'
				padding:"100dp"
				Button:
					id:button1
					font_size:24
					font_type:'Italic'
					text:' Delete Empty Files and Folder'
					on_release:root.deleteRepeater()
					on_press:root.changetext1a()
				Button:
					id:button2
					font_size:24
					text:'Delete Thumbnails'
		#			on_press:root.changetext2()
					on_release:root.Clearthumbnails()	

<Settings>:
	BoxLayout:
		orientation:'vertical'
		size:self.size
		BoxLayout:
			size_hint_y:0.2
			BoxLayout:
				Label:
					size_hint_x:0.4
					font_size:20
					id:scan
					text:'ScanTimes :' + str(root.scantimesupdate)
				BoxLayout:
					Button:
						text:'<'
						id:decrease
						on_press:root.decrease()
						disabled:False
					Button:
						text:'>'
						on_press:root.increase()
		BoxLayout:
			orientation:'vertical'
			BoxLayout:
				size_hint_y:0.2
				orientation:'vertical'
				Label:
					size:self.size
					pos:self.pos
					color:1,0,0,1
					text:"SCANTIMES INCREASES ACCURACY OF DELETION"
			BoxLayout:
				size_hint_y:0.2
				Button:
					size:self.size
					pos:self.pos
					text:'Back'
					on_press:root.back()
					border: 10,10,10,10
			BoxLayout:
 
 '''
)
'''
Bujlder.load_file(''/storage/sdcard0/App project with kivy/storagemanager.kv")
'''

n=0
freespace=0
newfreespace=0
scantimes=30

class Root(Screen):
	def delete(self):
		try:
			listofsubfolders=[x[0] for x in os.walk('/storage/sdcard0')]
		except FileNotFoundError:
			listofsubfolders=[x[0] for x in os.walk('/storage/emulated/0')]
		except:
			listofsubfolders=[x[0] for x in os.walk('/storage/emulated/legacy')]
		for subfolder in listofsubfolders:
			try:
				os.rmdir(subfolder)
			except:
				sffs=os.listdir(subfolder)
				if len(sffs) !=0:
					sffss=[os.path.join(subfolder,i) for i in sffs]
#					print(sffs)
					for subfolderfile in sffss:
						if os.stat(subfolderfile).st_size==0:
							os.remove(subfolderfile)
	def deleteRepeater(self):
		global n
		global scantimes
		while n<scantimes:
			self.delete()
			self.changetext1a()
			n+=1
			if n==(scantimes-1):
				self.changetext1b()
				self.freespaceupdate()
				n=0
				break
				
	#		Event().wait(3)
	#		asyncio.run(changetext1back())
			
	def changetext1a(self):
		self.ids.button1.text='Please Wait'
	def changetext1b(self):
		self.ids.button1.text='Delete Empty Files and Folder'
	
	
	def changetext2(self):
		self.ids.button2.text='Please Wait....'
		
	
		
		
	def changescreen(self): 
		sm.current ='screen2'

	def freespaceupdate(self):
		global freespace
		global newfreespace
		sleep(2)
		try:
			newfreespace=shutil.disk_usage('/storage/emulated/legacy').free
		except FileNotFoundError:
			newfreespace=shutil.disk_usage('/storage/sdcard0').free
		except:
			newfreespace=shutil.disk_usage('/storage/emulated/0').free
		freespacechange=-(freespace-newfreespace)
#		print(freespacechange)
		if freespacechange>0:
			self.ids.label1.text=str(round((freespacechange/(1024.161881**2)),3))+ "MB Freed"
#			global freespace
			freespace=newfreespace
		if freespacechange<=0:
			self.ids.label1.text='Storage at Optimal Level'

	
	
	def Clearthumbnails(self):
		try:
			listofsubfolders=[x[0] for x in os.walk('/storage/sdcard0')]
		except FileNotFoundError:
			listofsubfolders=[x[0] for x in os.walk('/storage/emulated/0')]
		except:
			listofsubfolders=[x[0] for x in os.walk('/storage/emulated/legacy')]
		for subfolder in listofsubfolders:
			try:
				if 'thumbnail' in subfolder:
					shutil.rmtree(subfolder)
					self.freespaceupdate()
			except:
				self.freespaceupdate()
				continue
				
		
class Settings(Screen):
	scantimesupdate=30
	def decrease(self):
		global scantimes
		if scantimes==3:
			self.alert()
			self.scantimesupdate=3
			
		else:
			self.scantimesupdate-=1
			self.ids.scan.text='ScanTimes:' + str(self.scantimesupdate)
			scantimes=self.scantimesupdate
		print(scantimes)
		
	def alert(self):
		self.ids.scan.text="Can't go any Lower "
		
		
	
	def increase(self):
		self.scantimesupdate+=1
		self.ids.scan.text='ScanTimes:'+str(self.scantimesupdate)
		global scantimes
		scantimes=self.scantimesupdate

	def back(self):
		global sm
		global scantimes
		scantimes=self.scantimesupdate
		sm.current='screen1'
		
	pass
	
	
	
sm=ScreenManager()
class StorageManagerApp(App):
	def build(self):
		global sm
		sm=ScreenManager()
		sm.add_widget(Root(name='screen1'))
		sm.add_widget(Settings(name='screen2'))
		sm.current='screen1'
		return sm
		
	def on_pause(self):
		return True
		
	def on_resume(self):
		return True
	
	
if __name__=='__main__':
	try:
		freespace=shutil.disk_usage('/storage/emulated/legacy').free
	except FileNotFoundError:
		freespace=shutil.disk_usage('/storage/sdcard0').free
	except:
		freespace=shutil.disk_usage('/storage/emulated/0').free
	StorageManagerApp().run()