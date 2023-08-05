
===|simplified file management|===


=English:

Program simplified file management can make it easier for you to work with files.

info: 
print(sifima.name); 
print(sifima.version); 
print(sifima.author); 
print(sifima.info). 


sifima.create([name_file]) - creates an empty file


sifima.write([name_file], [text]) - writes a specific text to a file or creates a file with a specific text.


sifima.remove([name_file]) - deletes the file


sifima.read([name_file]) - reads the file.


that would output the file, it is necessary to make sifima.read into a variable


text = sifima.read([name_file])