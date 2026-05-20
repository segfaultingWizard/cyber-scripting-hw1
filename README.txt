Launch server first, client attempts connecting periodically.
Interface is like a bash shell with a few built-ins.

Retrieved files go to ~/GrabbedFiles or equivalent.

Custom command syntax:
grab <remote filepath>
send <local filepath> <remote filepath>
screencap
yara <local yara rules filepath>

Example commands:
grab C:\Users\John\Desktop\passwords.txt
send /home/user/Desktop/malware.exe C:\Users\John\Desktop\photo.jpg.exe
screencap
yara /home/user/yara.txt
