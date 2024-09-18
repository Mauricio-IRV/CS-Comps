Note: I sometimes switched from second to third person throughout this assignment, so I'd like to apologize about that from a readers perspective before hand.

## Bandit Level 0 -> 1

    > Password: bandit0

1. Log into the remote server using SSH

   > ssh -p 2220 bandit0@bandit.labs.overthewire.org

2. List the files in the directory

   > ls

3. View contents of README either via concat or vim

   > cat README

4. Logout of the remote server
   > exit

## Bandit Level 1 -> 2

    > Password: ZjLjTmM6FvvyRnrb2rfNWOZOTa6ip5If

1. Use the password found in the README from level one to log into bandit1

   > ssh -p 2220 bandit1@bandit.labs.overthewire.org

2. List the files in the current directory

   > ls

3. This will display a file named with a dash i.e. "-" which will contain the password to the next user. The problem is that dashed files are usually flags for options so to print the file content you can either use the ">" operator, or prefix the dash with a "./" to denote that it's a path to a file that we're looking at.

   > cat ./-

4. Logout of the remote server
   > exit

## Bandit Level 2 -> 3

    > Password: 263JGJPfgU6LtdEvgfWU1XP5yac29mFx

1. Use the password found in the "-" file from level two to log into bandit2

   > ssh -p 2220 bandit2@bandit.labs.overthewire.org

2. List the files in the current directory

   > ls

3. This will display a file with spaces in it. Bash uses white space as a delimeter, so to refer to the file you need to either use a backslash "\" to escape the spaces, or wrap the pathname in quotes to view its contents.

   > cat "spaces in this filename"

4. Logout of the remote server
   > exit

## Bandit Level 3 -> 4

    > Password: MNk8KNH3Usiio41PRUEoDFPqfxLPlSmx

1. Use the password found in the previous level to log into bandit3

   > ssh -p 2220 bandit3@bandit.labs.overthewire.org

2. List the files in the current directory

   > ls

3. You'll see that there's a directory named "inhere," let's explore that directory.

   > cd inhere

4. You'll enter the directory but soon realize it's empty via "ls..." or is it?! If you do ls -a you'll notice that there's a hidden file which contains the password

   > ls -a

5. You'll then be able to find the password in the file "...Hiding-From-You" so let's view its contents

   > cat ...Hiding-From-You

6. Logout of the remote server
   > exit

## Bandit Level 4 -> 5

    > Password: 2WmrDFRmJIq3IPxneAaMGhap0pFhF3NJ

1. Use the password found in the previous level to log into bandit4

   > ssh -p 2220 bandit4@bandit.labs.overthewire.org

2. List the files in the current directory

   > ls

3. You'll once again see that there's a directory named "inhere," let's go to it

   > cd inhere

4. Then after using "ls" once more, we'll find that there's a list of files, but are password can be in any one of them. Thankfully we know that our targeted file is the only human readable file, and so we can use the "file" command to filter out our options. To avoid doing "file" for each individual file, we can use the asterisk wildcard to list the file type for all of the files in the directory, noting that we need to specify that its a path via "./" because all the files start with a dash ("-").

   > file ./\*

5. After viewing the list we can quickly find that the only ASCII text file i.e human readable file, is "-file07" so let's print its contents.

   > cat ./-file07

6. Logout of the remote server
   > exit

## Bandit Level 5 -> 6

    > Password: 4oQYVPkxZOOEOO5pTW81FB8j8lxXGUQw

1. Use the password found in the "-" file from level two to log into bandit5

   > ssh -p 2220 bandit5@bandit.labs.overthewire.org

2. List the files in the current directory

   > ls

3. You'll once again see that there's a directory named "inhere," let's go to it

   > cd inhere

4. Finding the password for this directory has some criterion such as
   - File of size 1033 bytes
   - Non Executable
   - Human Readable, so ASCII text

The "find" command in bash has a lot of flags that can fulfill some of these options. For example, it has -executable which determines if a file is executable, and -size which filters for files of a said size with "c" being the suffix for bytes. Simply filtering for the file size was honestly enough, when I had first used "du" I had realized this, but I wanted to fulfuill all the criterion. Here's what I was able to come up with:

> find inhere -type f -size 1033c ! -executable

I did get stuck on filtering out the ASCII text once the first two criterion were met though, since I wasn't exactly sure on how to juxtapose the two commands together. I had initially just tried using the command followed by a pipe with grep, but this did not work and I tried a couple other things and got stumped. Eventually I decided to just google the walkthrough for this level and resulted with this.

> find inhere -type f -size 1033c ! -executable -exec file {} \; | grep ASCII

I don't fully understand why "find inhere -type f -size 1033c ! -executable" this path result doesn't count as a path, but once I do "file {}" it does which can then be piped into grep.

5. From here it's standard protocol. Read the file & get the password

   > cat inhere/maybehere07/.file2

6. Logout of the remote server

   > exit

   > Referenced: https://mayadevbe.me/posts/overthewire/bandit/level6/

## Bandit Level 6 -> 7

    > Password: HWasnPhtq9AVKe0dmk45nxy20cvUa6EG

1. Use the password found in the previous level to log into bandit6

   > ssh -p 2220 bandit6@bandit.labs.overthewire.org

2. List the files in the current directory

   > ls

3. From here we need to change to the home directory (which also happens to be our parent directory) because our password is hidden under another directory.

   > cd ../

4. From here we need to recursively search for our file using the find command

   > find / -type f -user bandit7 -group bandit6 -size 33c

5. The problem with this result is that our answer is cluttered up with a bunch of permission denied. I tried using grep to filter out this output but tbh that did not work, and it makes sense that it didn't work because the permission denied is an error rather than a directory. Additionally, I was considering viewing permissions to filter any non executable files and only use find on those, but funny enough I'm pretty sure this approach didn't work because if I'm not mistaken, you need permissions to view permissions. Eventually I used the walkthrough once more and learned how you can use stdin [0]/stdout [1]/stderr [2] redirection to redirect the errors. They used 2 > where 2 is the code for stderr's to redirect the errors to a separate file, in this case /dev/null, which is a "black-hole." We're then left with the following

   > find / -type f -user bandit7 -group bandit6 -size 33c 2>/dev/null

6. This gives us a directory which we then view the contents of using cat to find the password.

   > cat /var/lib/dpkg/info/bandit7.password

7. From here we logout of the remote server
   > exit

## Bandit Level 7 -> 8

    > Password: morbNTDkSW6jIlUc0ymOdMaLnOlFVAaj

1. Use the password found in the previous level to log into bandit7

   > ssh -p 2220 bandit7@bandit.labs.overthewire.org

2. List the files in the current directory

   > ls

3. Here you'll find a data.txt file which contains a bountiful amount of passwords, but we need the one next to millionth. We can use one of greps options (such as -F, --fixed-strings, or -E, --extended-regexp, or even -e, patterns) for pattern syntax matching to filter out the line with the password we want. As such:

   > grep -F 'millionth' data.txt

4. Logout of the remote server
   > exit

## Bandit Level 8 -> 9

    > Password: dfwvzFQi4mU0wfNbFOe9RoWskMLg7eEc

1. Use the password found in the previous level to log into bandit8

   > ssh -p 2220 bandit8@bandit.labs.overthewire.org

2. List the files in the current directory

   > ls

3. You'll once again see that there's a file named "data.txt". Printing it to the screen will show that there's countless lines, so we'll need to find a unique line. Initially if you attempt to simply use the uniq command without sorting you'll find that it doesn't work. This is because the file needs to be sorted (i.e. repeated lines must be adjacent) for repeated line detection, as stated in the man page

- Note: 'uniq' does not detect repeated lines unless they are adjacent. You may want to sort the input first, or use 'sort -u' without 'uniq' \*

So we'll need to sort the file, and then pipe the stdout into uniq. As such:

> sort data.txt | uniq -u

4. Logout of the remote server
   > exit

## Bandit Level 9 -> 10

    > Password: 4CKMh1JI91bUIZZPXDqGanal4xvAg0JM

1. Use the password found in the previous level to log into bandit9

   > ssh -p 2220 bandit9@bandit.labs.overthewire.org

2. List the files in the current directory

   > ls

3. View the contents of data.txt

   > cat data.txt

4. Here you'll notice that most of it is illegable. We can use the "strings" command to filter out the "printable character sequences that are at least 4 characters long." Additionally we want to filter out any lines that do not contain multiple equals signs, for which we can use grep.
   > strings data.txt | grep ==

- We're then left with a few options, but it's a very short list to so we can easily spot the password.

6. Logout of the remote server
   > exit

## Bandit Level 10 -> 11

    > Password: FGUW5ilLVJrxX9kMYMmlN4MgbpfMiqey

1. Use the password found in the previous level to log into bandit10

   > ssh -p 2220 bandit10@bandit.labs.overthewire.org

2. List the files in the current directory

   > ls

3. View the contents of data.txt

   > cat data.txt

4. Here, based on the instructions we can note that this content is most likely in Base64, so we want to decode it to get the password, as such:

   > base64 -d data.txt

5. Logout of the remote server
   > exit

## Bandit 11 -> 12

    > Password: dtR173fZKb0RRsDFSGsg2RWnpNVj3qRr

1. Use the password found in the previous level to log into bandit11

   > ssh -p 2220 bandit11@bandit.labs.overthewire.org

2. List the files in the current directory

   > ls

3. View the contents of data.txt

   > cat data.txt

4. Here, based on the instructions, we know that the file is simply using a substitution cipher that consists of 13 place rotation (the ROT13 algorithm). As such we can use "tr" which translates characters to to decipher the content into a human readable text.
   > tr 'A-Za-z' 'N-ZA-Mn-za-m' < data.txt

## Bandit 12 -> 13

    > Password: 7x16WNeHIi5YkIhWsfFIqoognUTyj9Q4

> TBC...

### EOF

- P.S. It should be worth noting that I referenced many of the articles, provided throughout the exercises, found in the Bandit Overwire site. As the list is quite exhaustive I did not include them as references here, but they can be found there directly.
