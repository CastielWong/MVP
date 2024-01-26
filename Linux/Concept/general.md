
- [Directory](#directory)
- [Authentication](#authentication)
  - [SSH](#ssh)
- [Permission](#permission)
- [Reference](#reference)


Linux Kernel + Apps = Distro (Distribution, Flavor)

The shell prompt of a normal user typically ends with a dollar sign ($), while the super user ends with a pound sign (#).

Exit status:
- 0: successful
- 1 - 255: failed

| I/O Name | Abbreviation | File Descriptor |
| --- | --- | --- |
| Standard Input | stdin | 0 |
| Standard Output | stdout | 1 |
| Standard Error | stderr | 2 |

Redirection:
- `&`: used with redirection to signal that a file descriptors being used
- `2>&1`: combine stderr and standard output
- `2>{file}`: redirect standard error to a file
- `/dev/null`: redirect output to nowhere (null device)


## Directory
Common:

- /: "Root", the top of the file system hierarchy
- /bin: binaries and other executable programs
- /etc: system configuration files
- /home: home directories
- /opt: optional or third party software
- /tmp: temporary space, typically cleared on reboot
- /usr: user related programs
    - /bin
    - /sbin: system administration binaries
    - /lib
    - /local: locally installed software that is not part of the base OS
- /var: variable data, most notably log files
    - log: log files

Other:
- /boot: files needed to booth the OS
- /cdrom: mount point for CD-ROMs
- /cgroup: control groups hierarchy
- /dev: device files, typically controlled by the OS and the system administrators
- /export: shared file systems
- /lib: system libraries
- /lib64: system libraries, 64 bit
- /lost+found: used by the file system to store recovered files after a file system check has been performed
- /media: used to mount removable media like CD-ROMs
- /srv: contains data which is served by the system
    - /www: web server files
    - /ftp: FTP files
- /sys: used to display and sometimes configure the devices known to the Linux kernel

Applications that are not part of the base OS can be installed in:
- /usr/local
- /opt


## Authentication
As a root user, it has the privileges and it's responsible to manage users under due diligence.

```sh
# change a user's password
passwd {user}

# add a user to the sudo group to enable it to run with `sudo`
adduser {user} sudo
```

### SSH
Sample configuration for SSH in "~/.ssh/config":
```sh
Host {host alias}
    HostName {ip}/{alias}
    Port {port}
    AddKeysToAgent yes
    UseKeychain yes
    IdentityFile {path to private id file}
    User {user name}
```



## Permission
There are four categories of use: User (Owner), Group, Other, All (Public)

There are three special modes: setuid, setgid, sticky

The permission for file and directory

| Permission | File | Directory |
| --- | --- | --- |
| Read (r) | allows a file to be read | allows file names in the directory to be read |
| Write (w) | allows a file to be modified | allows entries to be modified within the directory |
| Execute (x) | allows the execution of a file | allows access to contents and metadata for entries |

The Permission Table is shown below:

| Number | Permission Type | Symbol |
| --- | --- | --- |
| 0 | no permission | --- |
| 1 | execute | --x |
| 2 | write | -w- |
| 3 | execute + write | -wx |
| 4 | read | r-- |
| 5 | read + execute | r-x |
| 6 | read + write | rw- |
| 7 | read + write + execute | rwx |

Examples:
```sh
# grant owner with execute permission
chmod u+x {file}
# revoke public write permission
chmod o-w {file}
# revoke group and public read and write permission
chmod go-rw {file}
# grant all users with read permission only
chmod a=r {file}

# change the owner and group of a file
chown {owner}:{group} {file}
```


## Reference
- Linux Tutorial: https://ryanstutorials.net/linuxtutorial/
- The Linux command line for beginners: https://tutorials.ubuntu.com/tutorial/command-line-for-beginners
- 17 useful rsync Command Examples in Linux: https://www.linuxtechi.com/rsync-command-examples-linux/
- SUID and SGID Permissions in Linux: https://www.tecmint.com/how-to-find-files-with-suid-and-sgid-permissions-in-linux/
- 35 Practical Examples of Linux Find Command: https://www.tecmint.com/35-practical-examples-of-linux-find-command/
- Input Output Redirection in Linux/Unix Examples: https://www.guru99.com/linux-redirection.html
- cURL Command Tutorial with Examples: https://www.booleanworld.com/curl-command-tutorial-examples/
- Pushd and Popd Commands in Linux: https://linuxize.com/post/popd-and-pushd-commands-in-linux/
- What does “--” (double-dash) mean: https://unix.stackexchange.com/questions/11376/what-does-double-dash-mean/11382#11382
- How to find your IP address in Linux: https://opensource.com/article/18/5/how-find-ip-address-linux
- What is the difference between test, [ and [[:https://mywiki.wooledge.org/BashFAQ/031
- Linux 常用命令全拼: https://mp.weixin.qq.com/s/QXqTW6AJf3rV8Ua2U3uYTg
