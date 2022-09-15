## File: cachesimulator.py
## Author(s): Andrew Lackey
## Date: 12/08/2021
## Section: Student section number 
## E-mail(s): andrewlackey@tamu.edu 
## Description: This program is a cache simulator, only item failed to implement is the LRU.


import sys #command line argument
import math #for some math stuff like log
import random #used for my random replacement 
import re #used sometimes to remove 0x from hex values

##ram initializations, the ram is initioalized from user input of range for ram and ram is then loaded from input.txt through a command line argument
print("*** Welcome to the cache simulator ***")
print("initializing the RAM:")
## get user data for init-ram from 0x00 to 0x00-0xFF including
init_ram = input() #input hex values
##splits init-ram at spaces so we can address position 1 and 2 to get the range of ram
start_end = init_ram.split(" ") #get hex start and end of ram and split at space
##convert hex to decimal + 1 to get the start index
start = int(start_end[1],16) + 1 #get decimal start value for hex in init-ram
##convert hex to decimal + 1 to get the end index
end = int(start_end[2],16) + 1 #get decimal end value for hex in init-ram
from_file = [] #to store content from file
from_file = ["00" for i in range(256)] #initialize the RAM to "00" and a size of 256
f = open(sys.argv[1],"r") #open filename read from command line
counter = 0 #make sure we dont go over the end value
for line in f: #go line by line down the file 
    if counter == end: #makes sure we dont add too much to RAM
        break
    from_file[counter] = line.strip() #add contents of each line to a new cell in from_file while removing \n
    counter += 1 #increment the counter
f.close() #close file read
# print(from_file) #tester for correctness
# print(len(from_file)) #tester for correctness
print("RAM successfully initialized!")

## user inputed data and calculations for indexing later on 
#this block is user input and some calculations for future use
print("configure the cache:")
cache_size = input("cache size: ") #C number of bytes
data_block_size = input("data block size: ") #B bytes per block
associativity = input("associativity: ") #E 1, 2, or 4 lines per set
number_cache_sets = int(cache_size)/(int(data_block_size) * int(associativity)) #S number of sets
address_width = 8 #m number of main memory address bits
unique_address = 2^8 #M maximum number of unique memory address
data_block = math.log(int(data_block_size),2) #b number of block offset bits
set_index_bit = math.log(number_cache_sets,2) #s number of set index bits
tag_bits = address_width - (set_index_bit + data_block) #t number of tag bits
replcement_policy = input("replacement policy: ") 
write_hit_policy = input("write hit policy: ")
write_miss_policy = input("write miss policy: ")
print("cache successfully configured!")
# print(tag_bits)
# print(set_index_bit)
# print(data_block)

## create a cache hit variable and a cache miss variable and created the 2d array with blank poitions for the cache
cache_hits = 0
cache_misses = 0
cache = [["" for i in range((int(data_block_size)+3))] for j in range((int(number_cache_sets)*int(associativity)))] #2d array for my cache
#print(cache) #format tester
## fills valid bit of all positions to 0 and dirty bit of all positions to 0
for i in range(int(number_cache_sets)*int(associativity)):
    cache[i][0] = "0" #make all valid bits 0 in initialization
    cache[i][1] = "0" #make all dirty bits zero in initialization
quit = False

## driver for the cache allowing the user to select what they want to do until they select quit
while not quit: #while loop for the cache
    print("*** Cache simulator menu ***")
    print("type one command: ")
    print("1. cache-read ")
    print("2. cache-write ")
    print("3. cache-flush")
    print("4. cache-view ") #the menu
    print("5. memory-view ")
    print("6. cahce-dump ")
    print("7. memory-dump ")
    print("8. quit")
    print("****************************")
    s = input()
    selection = s.split(" ") #splits input at space and gets command and any hex value with it
    ## if user inputs quit exit the loop and close the program
    if selection[0] == "quit": #quit program
        quit = True

    ##< read in a value from the ram and if it is not in cache load in cache and return the data if it hits in cache return the data at that point
    elif selection[0] == "cache-read": #cache-read reads from_file and loads in cache
        ##< read in a value from the ram and if it is not in cache load in cache and return the data if it hits in cache return the data at that point
        address =  list(format(int(selection[1],16), "b"))
        while len(address) < 8:
            address.insert(0, '0')
        #print(address) #tester
        tag = ""
        index = ""
        offset = ""
        for i in range(0, int(tag_bits)): #gets tag bits
            tag += address[i]
        for i in range(int(tag_bits), int(set_index_bit)+int(tag_bits)): #gets index bits
            index += address[i]
        for i in range(int(set_index_bit)+int(tag_bits), int(data_block)+int(set_index_bit)+int(tag_bits)): #gets offset bits
            offset += address[i]
        offset = int(offset, 2)
        if index == "": #index has no data set to 0
            index = 0
            print("set:0")
        else: #index has data set it
            index = int(index, 2)
            print("set:" + str(index))
        if tag == "": #tag has no data set it to 00
            tag = "00"
        else: #tag has data set it
            tag = "%02X" % int(tag, 2) #turn tag to binary without 0x
        print("tag:"+tag)
        hit = False
        data_in_file_index = int(selection[1],16) - offset # position of the data in from_file
        for i in range(index*int(associativity), (index*int(associativity)+int(associativity))): #check for hit in cache
            if tag == cache[i][2]: #hit in cache
                cache_hits += 1
                hit = True
                print("hit:yes")
                print("eviction_line:-1")
                data = cache[i][3]
                break
        if hit == False: #didnt hit anything
            print("hit:no")
            cache_misses += 1
            temp = ["1", "0", tag] #temp array to load into cache
            for i in range(int(data_in_file_index), int(data_block_size) + int(data_in_file_index)):
                temp.append(from_file[i])
            filled = False
            for i in range(index*int(associativity), (index*int(associativity)+int(associativity))):
                if cache[i][0] == "0": #valid bit = 0 so nothing in line
                    for j in range(len(temp)):
                        cache[i][j] = temp[j]
                    print("eviction_line:"+ str(i - index*int(associativity)))
                    data = cache[i][3+offset]
                    filled = True
                    break
            if filled == False: #means the cache set it was trying to put data in was full
                if replcement_policy == "1": # random replacement
                    replacement_line = random.randint(0, (int(associativity)-1))
                    for i in range(len(temp)):
                        cache[replacement_line*int(associativity) + index][i] = temp[i]
                    print("eviction_line:"+ str(int(replacement_line)))
        print("ram_address:" + selection[1])
        print("data:" +"0x"+ data)

    ## writed to either ram or cache or both depending on what the write-hit and write miss policy is
    elif selection[0] == "cache-write": #cache-write writes a bit to an address
        address =  list(format(int(selection[1],16), "b")) #take address to write convert to binary
        while len(address) < 8: #add zeros to front until len is 8
            address.insert(0, '0')
        #print(address) #tester
        tag = ""
        index = ""
        offset = ""
        for i in range(0, int(tag_bits)): #gets tag bits
            tag += address[i]
        for i in range(int(tag_bits), int(set_index_bit)+int(tag_bits)): #gets index bits
            index += address[i]
        for i in range(int(set_index_bit)+int(tag_bits), int(data_block)+int(set_index_bit)+int(tag_bits)): #gets offset bits
            offset += address[i]
        offset = int(offset, 2)
        if index == "": #if index has no data set it to 0
            index = 0
            print("set:0")
        else:
            index = int(index, 2)
            print("set:" + str(index))
        if tag == "":
            tag = "00"
        else:
            tag = "%02X" % int(tag, 2) #turn tag to binary without 0x
        print("tag:"+tag)
        hit = False
        data_in_file_index = int(selection[1],16) - offset #data in from_file
        data_to_write = re.sub("0x","",selection[2]) #get data to replace
        for i in range(index*int(associativity), (index*int(associativity)+int(associativity))): #check for hit
            if tag == cache[i][2]: #hit a tag
                cache_hits += 1
                hit = True
                print("write_hit:yes")
                print("eviction_line:-1")
                data = selection[2]
                if write_hit_policy == "1": #write both in cache and ram the new bit
                    from_file[data_in_file_index+offset] = data_to_write
                    cache[i][1] = "1"
                    cache[i][offset+3] = data_to_write
                    break
                if write_hit_policy == "2": #only write in cache the new bit
                    cache[i][1] = "1"
                    cache[i][offset+3] = data_to_write
                    break
        if hit == False:
            print("write_hit:no")
            cache_misses += 1
            if write_miss_policy == "2": #only replace the data in the ram
                from_file[data_in_file_index+offset] = data_to_write
                filled = True
            if write_miss_policy == "1": #replace both the data in the ram and load it in the cache
                from_file[data_in_file_index+offset] = data_to_write
                temp = ["1", "1", tag] #create a temporary array to load data into cache
                for i in range(int(data_in_file_index), int(data_block_size) + int(data_in_file_index)):
                    temp.append(from_file[i])
                filled = False
                for i in range(index*int(associativity), (index*int(associativity)+int(associativity))):
                    if cache[i][0] == "0": #valid bit = 0 so nothing is in the line
                        for j in range(len(temp)):
                            cache[i][j] = temp[j]
                        print("eviction_line:"+ str(i - index*int(associativity)))
                        cache[i][offset+3] = data_to_write
                        data = cache[i][3+offset]
                        filled = True
                        break
            if filled == False: #means the cache set it was trying to put data in was full
                if replcement_policy == "1": #random replacement policy
                    replacement_line = random.randint(0, (int(associativity)-1)) #makes random number from 0-(associativity-1)
                    for i in range(len(temp)):
                        cache[replacement_line*int(associativity) + index][i] = temp[i]
                    print("eviction_line:"+ str(int(replacement_line)))
        print("ram_address:"+selection[1])
        print("data:"+selection[2])
        print("dirty_bit:1")
        #print(cache)

    ## flushes out the cash and sets valid and dirty bit of all lines to 0 and the tag and data bits of all lines to 00
    elif selection[0] == "cache-flush": #emptys cash by putting 0 or 00 in a position depending on formatting
        for i in range(int(data_block_size)+3): #need two for loops to traverse the 2d array
            for j in range(int(number_cache_sets)*int(associativity)):
                cache[j][i] = "00" #data and tag bit flush
        for i in range(int(number_cache_sets)*int(associativity)):
            cache[i][0] = "0" #valid bit flush
            cache[i][1] = "0" #dirty bit flush
        #print(cache) #tester

    ## displays the cache content and information to console
    elif selection[0] == "cache-view": #view the cache in console
        print("cache_size:"+cache_size)
        print("data_block_size:"+data_block_size)
        print("associativity:"+associativity)
        if replcement_policy == "1": #formmating the 1 to random replacement
            print("replacement_policy:random_replacement")
        else: #format the 2
            print("replacement_policy:least_recent_used")
        if write_hit_policy == "1": #format the 1 to write through
            print("write_hit_policy:write_through")
        else: #format the 2
            print("write_hit_policy:write_back")
        if write_miss_policy == "1": #format the 1 to write allocate
            print("write_miss_policy:write_allocate")
        else: #format the 2
            print("write_miss_policy:no_write_allocate")
        print("number_of_cache_hits:"+ str(cache_hits))
        print("number_of_cache_misses:"+ str(cache_misses))
        print("cache_content:")
        for i in range(int(number_cache_sets)*int(associativity)): #nested loop to travers 2d cache
            for j in range(int(data_block_size)+3):
                print(cache[i][j], end=" ") #printing the cache with some formatting
            print("\n", end="")

    ## displays the ram content and information to console
    elif selection[0] == "memory-view": #displays the ram from_file
        print("memory_size:"+ str(end))
        print("memory_content:")
        print("address:data")
        for i in range(0, 256, 8): #start at 0 go to 256 incrementing by 8
            print("0x%X" % i, end=":") #puts the 0x.. value followed by : for formmating
            print(from_file[i] + " " + from_file[i+1]
            + " " + from_file[i+2] + " " + from_file[i+3]
            + " " + from_file[i+4] + " " + from_file[i+5]
            + " " + from_file[i+6] + " " + from_file[i+7])

    ## loads the cache content into a file cache.txt
    elif selection[0] == "cache-dump": #dumps the content of cache into cache.txt
        f = open("cache.txt", "w") #open cache.txt to write
        counter = 0
        for i in range(int(number_cache_sets)*int(associativity)):
            for j in range(3, int(data_block_size)+3): #start at 3 because my 2d array in the first 3 positions are the valid, dirty and tag bits
                f.write(str(cache[i][j]) + " ")
                counter += 1
            if counter != int(cache_size): #prevents trailing newline at end of file
                f.write("\n")
        f.close()

    ## loads the ram content into a file ram,txt
    elif selection[0] == "memory-dump": #dumps the content of from_file which is my ram and puts it in ram.txt
        f = open("ram.txt", "w") #open ram.txt to write
        current_node = 0
        for value in from_file: #increment through the values stored in from_file
            f.write(value) #write value from_file
            current_node += 1
            if current_node != len(from_file): #prevents trailing new line at end of file
                f.write("\n")
        f.close()
    