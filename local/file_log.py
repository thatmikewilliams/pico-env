import machine
import utime
import os
import io
import sys

#from local.logger import Logger

#__log = Logger("FileLog")
class FileLog:
    def __init__(self, filename, max_file_size):
#        __log.debug(f"__init__(filename={filename}, max_file_size={max_file_size}")
        self.filename = filename
        self.max_file_size = max_file_size

    # writes whatever is passed to it to the file
    def write_line(self, data):
#        __log.debug("write_line")
        self.write(data + "\r\n")

    # writes whatever is passed to it to the file
    def write(self, data):
#        __log.debug("write_line")
        # open in append - creates if not existing, will append if it exists
        f = open(self.filename, "a")
        f.write(data)
        f.close()
        self.__apply_max_file_size()

    def write_exception(self, e):
#        __log.debug(f"write_exception {e}")
        buf = io.StringIO()
        sys.print_exception(e, buf)
        self.write_line(buf.getvalue())

    def __apply_max_file_size(self):
#        __log.debug("__apply_max_file_size")
        current_size = self.__get_file_size()
        if current_size > self.max_file_size:
#            __log.debug(f"file size {current_size} exceeds max {self.max_file_size}")
            print(f"file size {current_size} exceeds max {self.max_file_size}")
            self.__rotate_files()
            
    # returns the size of the file, or 0 if the file does not exist
    def __get_file_size(self):
        # f is a file-like object.
        try:
            # Open read - this throws an error if file does not exist - in that case the size is 0
            f = open(self.filename, "r")
            f.seek(0, 2)
            size = f.tell()
            f.close()
            return size
        except:
            # if we wanted to know we could print some diagnostics here:
            #print("Exception - File does not exist?")
            return 0

    def __rotate_files(self):
        os.rename(self.filename, self.filename + ".1")
        
    #This removes one line from the file by copying the whole file except the first line to a new file 
    # and then renaming it
    def __remove_oldest_lines(self, bytes_to_remove):
#        __log.debug("__remove_oldest_line")
        tmpName = self.filename + '.bak'

        # open both files
        with open(self.filename, 'r') as readFrom, open(tmpName, 'w') as writeTo:
            # read the first line and throw it away. This moves the file handle on by 1 line.
            readFrom.readline() 
            # now Read the rest of the lines from original file one by one and write them to the dummy file
            for char in readFrom:
                writeTo.write(char)
        # now close all the handles and swap the file names around.
        readFrom.close()
        writeTo.close()
        os.remove(self.filename)
        os.rename(tmpName, self.filename)
