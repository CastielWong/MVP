
```sh
# enter a directory
cd {directory}
# change to the previous directory
cd -
# list environment variables
printenv
# list files with type ("/" for directory, "@" for link, "*" for executable)
ls -al -F -t --color

# create a file
touch {file}
# create a shortcut path/symbolic link to a file
ln -s {source_file} {sym_link}

# create directory
mkdir {directory}
# remove a directory and all files inside
rm -r {directory}
# move a file
mv {file} {new_path}/{file}
# copy a file
cp {file} {copied_file}

# get file's number of lines, words and characters
wc {file}
# count the amount of files
ls ~ | wc -l
# sort the unique content by the nth column in a file
sort {file} -u -k{n}
# show content, cat stands for "concatenate"
cat -n {file}
# add content
cat {file_1} > {file_2}
# append content
cat {file_1} >> {file_2}
# redirect stdout and stderr to specified places
ls {file} {file_not_existed} 1> {out} 2> {out.err}
# redirect both stdout and stderr into an output file
ls {file} {file_not_existed} > {out} 2>&1
# redirect error message to the null device
ls {file} {file_not_existed} > /dev/null
# search a word in a file
cat {file} | grep "{word_1}\|{word_2}"
# search lines in a file via pattern
cat {file} | grep -E "{pattern_1}|{pattern_2}"
cat {file} | grep -e "{pattern_1}" -e "{pattern_2}"

# check contents in tar
tar [-]tf {file}.tar
# compress then create tar, tgz means tar.gz
tar -zcvf {file}.tgz {file1} {file2}
# compress files inside a directory in bz2 format, note that "bzip2" must be installed
tar -cjvf {path}/{file}.tar.bz2 {directory}
# compress in customized name with the command interpolation
tar -cjvf {path}/`hostname`-`TZ=Australia/Sydney date "+%Y-%m-%d-%H:%M:%S"`.gz {file}
# decompress/unzip tar
tar -xvf {file}.[tar| tar.bz2]

# check the file type
file {file}
# display printable strings from binary file
strings {binary_file}

# read file STDIN anonymously
wc -l < {file}
# redirect STDERR
ls -l {inexistent_file} 2> {new_file}
# redirect both STDERR and STDOUT
wc -l {file} {inexistent_file} > {new_file} 2>&1

# display directory stack, -l for full path, -v for listing
dirs -lv
# move to the specified directory and push it to dirs stack
pushd {directory}
# rearrange dirs stack by placing the one with index n from top and change directory
pushd -{n}
# pop out current directory and move to next one in dirs stack
popd
# pop out the (n + 1)th one started from bottom in dirs stack
popd +{n}

# retrieve specified lines from a large file
sed -n '{start_line}, {end_line}p; {stop_line}q' {file}
awk 'NR>=<start_line> && NR<=<end_line>; NR==<stop_line> {exit}' <file>

# find file (case-insensitive) under certain folder
find {folder} -iname {file}
# find folder without permission 0777
find {folder} -type d ! -perm 0777
# find Read-Only files under user's directory
find {folder} -user {user} -perm /u=r -print
# find all empty files
find {folder} -type f -empty
# find then delete file with certain extension
find {folder} -type f -name '*.{extension}' -delete
# find last a to b (x < y) days modified files
find {folder} -mtime +{x} -mtime -{y}
# find changed files in last hour
find {folder} -cmin -60
# find files between x MB and y MB (x < y)
find {folder} -size +{x}M -size -{y}M

# search text in files under certain directory
grep -rnw {folder} -e {pattern}
# perform a command over multiple rows
{cmd1} list | egrep {pattern} | awk '{print $n}' | xargs -n1 {cmd2} {args}

# compare files difference
diff {file1} {file12}
sdiff {file1} {file12}
vimdiff {file1} {file12}
```
