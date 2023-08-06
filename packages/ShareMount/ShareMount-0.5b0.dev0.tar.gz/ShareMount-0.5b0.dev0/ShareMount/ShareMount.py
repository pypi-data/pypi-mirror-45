import traceback
import os
import platform
import re
import sys
import datetime
import subprocess
import tempfile

class Mount():
	"""
	Mount share on Linx and MacOS

	"""

	def __init__(self, mount_local='', username='', password='', mount_remote='', domain=''):
		"""
		Mount share on Liunx and MacOS


		**MacOS only requires the remote mount point in most instances, however credentials can be supplied**


		Usage:

			local = ''

			remote = '//remote/share/path'

			username = ''

			password = ''

			domain = ''

			**Initialse Class**

			share = Mount(mount_local, username, password, mount_remote, domain)

			**Mount Share**

			share._mount()

			**Unmount Share**

			share._un_mount()

		"""		
		self.operating_system = sys.platform
		self.mount_local = mount_local
		self.username = username
		self.password = password
		self.mount_remote = mount_remote
		self.domain = domain


	def _check_mount(self):
		"""
		Check if mount already exists
		"""		
		found = False
		command_check = "mount"
		process_check = subprocess.Popen(command_check, shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
		output_check = process_check.communicate()[0]
		line = output_check.splitlines()
		if self.mount_remote.endswith('/'):
			self.mount_remote = self.mount_remote[:-1]
		for i in line:
			pattern = '{}.*'.format(self.mount_remote.replace('//', '\/')).encode()
			matches = re.search(pattern,i)
			if matches:
				mat = re.match(b'.*\son\s(.*?)\s.*',i)
				if mat:
					self.mount_local = mat.groups()[0]
					found = True				
				return found

		return found


	def _un_mount(self):
		"""
		Unmount share
		"""				


		found = False
		command_check = "mount"
		process_check = subprocess.Popen(command_check, shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
		output_check = process_check.communicate()[0]
		line = output_check.splitlines()
		if self.mount_remote.endswith('/'):
			self.mount_remote = self.mount_remote[:-1]
		for i in line:
			pattern = '{}.*'.format(self.mount_remote).encode()
			matches = re.search(pattern,i)
			if matches:
				mat = re.match(b'.*\son\s(.*?)\s.*',i)
				if mat:
					self.mount_local = mat.groups()[0]
					found = True

		if found:
			try:
				command = 'umount -f {}' .format(self.mount_local.decode())
				proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
				stdout_value = proc.communicate()[0]
				found = self._check_mount()
				if not found:
					pass
				else:
					return 

			except Exception:
				print('An unhandled exception has occured')
				print(traceback.print_exc())


	def _mount(self):
		"""
		Attempt to map network share
		"""				

		if '//' in self.mount_remote:
			self.mount_remote = self.mount_remote.replace('//', '')

		found = self._check_mount()

		if not found:

			try:

				if self.operating_system == 'darwin':

					self.mount_remote = self.mount_remote.replace(' ', '%20')

					if not self.username:
						self.username = 'guest'					
						if not self.domain:
							if not self.password:
								command = ("osascript -e 'mount volume \"smb://guest:guest@{r}\"'".format(r=self.mount_remote))
					else:
						command = ("osascript -e 'mount volume \"smb://{d};{u}:{p}@{r}\"'".format(r=self.mount_remote, u=self.username, p=self.password, d=self.domain, m= self.mount_local))				

				if self.operating_system == 'linux':

					if not self.username:
						self.username = 'root'

					now = datetime.datetime.now().strftime("%B-%d-%Y")

					if not self.mount_local:
						self.mount_local = tempfile.gettempdir() + '/' + now + '_tmpmount'

					if not os.path.exists(self.mount_local):
						try:
							os.makedirs( self.mount_local)
							os.chmod( self.mount_local, 0o777)

						except Exception:
							print('An unhandled exception has occured')
							print(traceback.print_exc())

					self.mount_local = self.mount_local.replace(' ', '\ ')
					self.mount_remote = self.mount_remote.replace(' ', '\ ')		

					command = "sudo mount -t cifs //{r} {m} -o username={u},password='{p}',domain={d},vers=2.0" .format(r=self.mount_remote, u=self.username, p=self.password, d=self.domain, m=self.mount_local)

				proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
				stdout_value = proc.communicate()[0]	
				if 'Permission denied\n' in stdout_value.decode():
					print('Permission Denied!: specify valid credentials')
					sys.exit()
				found = self._check_mount()

			except Exception:
				print('An unhandled exception has occured')
				print(traceback.print_exc())

		if found:
			return self.mount_local
		else:
			print(stdout_value)
			return (stdout_value)

