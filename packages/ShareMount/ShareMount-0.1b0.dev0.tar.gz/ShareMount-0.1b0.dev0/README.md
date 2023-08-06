**ShareMount**
-----
**Mount Shares on Linux and MacOS**
 
>Author: Darryl Lane  |  Twitter: @darryllane101

>https://github.com/darryllane/ShareMount


**Pip Install Instructions**

Note: To test if pip is already installed execute.

`pip -V`

(1) Mac and Kali users can simply use the following command to download and install `pip`.

`curl https://bootstrap.pypa.io/get-pip.py -o - | python`

**ShareMount Install Instructions**

(1) Once `pip` has successfully downloaded and installed, we can install 'ShareMount':

`sudo pip install ShareMount`

**Example:**

			**Initialse Class**	
			
			remote = '//remote/share/path'
			
			share = Mount(mount_remote)
			
			**Mount Share**
			
			share._mount()
			
			**Unmount Share**
			
			share._un_mount()


Change/Feature Requests
====
* Windows Mount

Changelog
====
* Version __0.1b.0dev__ (__03/05/2019__):
  * init