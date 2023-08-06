# sortmerge
Very large file sorting

# Problem
Please see here below the challenge we would like you to solve:
Very large file sorting

Hint: External sorting is a term for a class of sorting algorithms that can handle massive amounts
of data.

Problem: You have a *very* large text file, so it does not fit in memory, with text lines. Sort the file
into an output file where all the lines are sorted in alphabetic order, taking into account all words
per line. The lines themselves do not need to be sorted and are not to be modified. Lines are
considered to be average in length so edge cases such as a file with just two very large lines
should still work but it is OK if performance suffers in that case.

Boundary: Use any programming language you feel comfortable with. Please use standard
libraries only, no batch or stream processing frameworks. Be as efficient as possible while
avoiding using standard library sorting routines. Provide a rationale for your approach. Design
schemas are welcome.

Please note that the file.txt that we use to measure the performance of the result is generated
via: 
```
ruby -e 'a=STDIN.readlines;5000000.times do;b=[];16.times do; b << a[rand(a.size)].chomp
end; puts b.join(" "); end' < /usr/share/dict/words > file.txt
```
Please send us the result via .zip file

# Solution
To solve the problem, I split the main file in other different files, which will be sorted according to the first two letters of each line. Once this task is complete, the directory where all the organized files are listed and they are added to the new final file, always using block_size.

After that, I listed the directory with this splitted files and appended, using block_size, in order to the output file sorted.

Below I will show how the script works.

```
~$ ruby -e 'a=STDIN.readlines;5000000.times do;b=[];16.times do; b << a[rand(a.size)].chomp end; puts b.join(" "); end' < /usr/share/dict/words > file.txt
~$ ./sortmerge.py -h
Usage: sortmerge.py [action] [options]

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -b BLOCKSIZE, --blocksize=BLOCKSIZE
                        Block size.
  -f FILENAME, --filename=FILENAME
                        Filename to sort.
  -o OUTPUT, --output=OUTPUT
                        Output filename.
  -t TMPDIR, --tmpdir=TMPDIR
                        Temporary directory.
~$ ./sortmerge.py -f file.txt -t tmpdir -o out.txt
~$ ls -la file.txt out.txt 
-rw-r--r-- 1 nobody nobody 719933298 Nov  3 10:33 file.txt
-rw-r--r-- 1 nobody nobody 719933298 Nov  3 10:35 out.txt
~$
```

