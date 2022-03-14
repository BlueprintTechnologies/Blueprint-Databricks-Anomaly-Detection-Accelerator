#!/usr/bin/env python
"""
Created on Wednesday, January 19, 2022 at 09:57:55 by 'Wesley Cobb <wesley@bpcs.com>'
Copyright (C) 2022, by Blueprint Technologies. All Rights Reserved.
 
Last edited: <2022-01-21 09:07:47 wcobb>
 
"""
import os, sys, time
import pandas as pd

class RemoteError(Exception):
    pass

class Remote:
    """
    Remote is a class that is intended to simplify various operations across 
    filesystems and remote machines.  It implements some of the most common
    filesystem tasks: listdir, exists, touch, remove, mkdir, rmdir with ssh
    and also provides a few utilities: isdir, isfile, and islink for exploring.

    Note that if one adds the sshkey for the LOCAL machine to the 'authorized_keys'
    file in ones ~/.ssh directory, then this class and all of its methods will
    also work seamlessly on the LOCAL machine as well.

    The class also has a method for a more flexible 'system' command to use
    in place of os.system(...) -- this version returns a list of strings as
    the output of the remote.system(...) invocation.
    
    Inputs:

       username:str -- name of account that Remote(...) should connect with
                       this defaults to the current username...

       hostname:str -- computer to which Remote(...) should connect... this defaults
                       to the current machine...

       portnum:int  -- port number that Remote(...) should use for the connection...
                       this defaults to the usual port 22 for ssh...

       verbose:bool -- should we be chatty?

       debug:bool   -- should be absurdly verbose about what we're doing?

       results_root:str -- directory to which temporary results are written on the LOCAL machine

    Methods:

       system(self, command:str, classic:bool) -- executes a system command just like os.system
                                                  by default but if classic = False, then returns 
                                                  a list of strings as a result rather than an 
                                                  integer status code

       listdir(self, search:str) -- returns a list of strings for the filenames in the remote
                                    search path. these are full paths to the files not just the
                                    names along

       exists(self, search:str) -- tests for the existence of a path on the remote host

       touch(self, search:str) -- updates or creates a remote path on the remote host

       remove(self, search:str)  -- removes a remote path

       mkdir(self, search:str, mode:int, parents:bool) -- creates a directory and possibly the
                                                          parent directories for it and possibly
                                                          permission modes

       rmdir(self, search:str, files_too:bool) -- removes (possibly recursively) directories and
                                                  their contents

       isdir(self, search:str) -- tests whether a remote path is a directory

       islink(self, search:str) -- tests whether a remote path is a symbolic link

       isfile(self, search:str) -- tests whether a remote path is a file

       get_tempfile(self, suffix:str) -- returns a temporary filename, possibly with
                                         a suffix specified by the user...

    @TODO: please improve this documentation

    """
    def __init__(self,
                 username:str    = None,
                 hostname:str    = None,
                 portnum:int     = None,
                 results_dir:str = None,
                 verbose:bool    = False,
                 debug:bool      = False,
                ):
        """
        """
        self.args = {}
        self.args['debug'] = debug
        self.args['verbose'] = verbose
        #
        # if no username has been defined then default to the current user...
        #
        if (username == None):
            try:
                self.args['username'] = os.environ["USER"]
            except:
                try:
                    self.args['username'] = os.environ["USERNAME"]
                except:
                    try:
                        self.args['username'] = os.getlogin()
                    except:
                        raise RemoteError(f"No username was supplied, and have been unable to establish LOCAL username")
        else:
            self.args['username'] = username
        #
        # if no hostname has been defined then default to the current hostname...
        #
        if (hostname == None):
            self.args['hostname'] = os.uname().nodename
        else:
            self.args['hostname'] = hostname
        #
        # if no portnum has been defined then default to the unix standard of 22...
        #
        if (portnum == None):
            self.args['portnum'] = 22
        else:
            self.args['portnum'] = portnum
        #
        # if no results_dir has been defined then attempt to find something that
        # makes sense, if all else fails fall back to writing to the current
        # local directory...
        #
        if (results_dir == None):
            if (sys.platform == "linux"):
                self.args['results_dir'] = "/dev/shm"
            elif (sys.platform == "darwin"):
                self.args['results_dir'] = "/tmp"
            else:
                #
                # giving up and writing to the local directory...
                # note that this would normally only happen on windows
                # and it is possible that several methods in this
                # package won't work there anyway...
                #
                self.args['results_dir'] = "."
        else:
            self.args['results_dir'] = results_dir

    def __str__(self):
        """
        A string representation of the class that is used when
        an instance of the class (e.g. 'remote') is printed:

        print(remote)

        @TODO: please improve this documentation
        """
        val = "<Remote "
        for key in self.args.keys():
            val += f"{key}='{self.args[key]}', "
        return val[:-2] + " />"

    def __repr__(self):
        """
        A string representation about the class that is used
        in interactive mode (i.e. in an ipython shell or 
        jupyter notebook)

        @TODO: please improve this documentation
        """
        val = "class 'Remote' with "
        for key in self.args.keys():
            val += f"{key}='{self.args[key]}', "
        return val[:-2]

    def __tempfile__(self) -> str:
        """
        Get a temporary filename based on the timestamp.

        @TODO: please improve this documentation
        """
        return f"{round(time.time(), 7)}.task"
            
    def system(self, command:str, classic:bool = True):
        """
        The same functionality as os.system() on the
        remote site.  If the argument 'classic' is set
        to False the behavior is altered and instead
        of returning a status code, a list of results
        is returned instead.
        
          Input:
               command:str  -- the command to be executed
               classic:bool -- True (default) returns a status code, False returns a list of strings with content
        
          Output:
               status:int (classic == True) or results:[str] (classic == False)

        @TODO: please improve this documentation
        """
        results_path = os.path.join(self.args['results_dir'], self.__tempfile__())
        cmd = (f"ssh -p {self.args['portnum']} {self.args['username']}@{self.args['hostname']} " + f"\'{command}\' 2>&1 >>{results_path}")
        status = os.system(cmd)
        if (classic):
            return status
        else:
            if (status != 0):
                raise RemoteError(f"command '{cmd}' failed with status = {status}")
            results = open(results_path, "r")
            contents = results.readlines()
            results.close()
            os.remove(results_path)
            return contents

    def listdir(self, search:str, meta:bool = False):
        """
        Perform the same functionality as os.listdir() on
        the remote site. The optional parameter 'meta' alters
        the behavior and instead of returning a list of files,
        the function returns a dataframe of metadata about the
        files.

        @TODO: please improve this documentation
        """
        results_path = os.path.join(self.args['results_dir'], self.__tempfile__())
        if (meta == False):
            command = f"ls -1 {search}"
            results = self.system(command = command, classic = False)
            files = []
            for item in results:
                if ((item != ".") and (item != "..")):
                    this_file = os.path.join(search, item.strip())
                    files.append(this_file)
            return files
        else:
            metadata = pd.DataFrame()
            command = f"ls -l {search}"
            results = self.system(command = command, classic = False)
            month_encoder = {"Jan":"01", "Feb":"02", "Mar":"03", "Apr":"04",
                             "May":"05", "Jun":"06", "Jul":"07", "Aug":"08",
                             "Sep":"09", "Oct":"10", "Nov":"11", "Dec":"12",}
            modes = []
            items = []
            owner = []
            group = []
            fsize = []
            mtime = []
            name  = [] # if name contains spaces then the entry could have many parts
            for entry in results:
                if ((entry[0:6] != "total ") and (entry[0:4] != "ls -l")):
                    this_entry = entry.split()
                    if (self.args['debug']):
                        print("entry: %s" % this_entry)
                    this_modes = this_entry[0]
                    this_items = int(this_entry[1])
                    this_owner = this_entry[2]
                    this_group = this_entry[3]
                    this_fsize = int(this_entry[4])
                    this_month = this_entry[5]
                    this_day   = this_entry[6]
                    if (":" in this_entry[7]):
                        #
                        # then the modified time is within the past 6-months and this year...
                        #
                        this_year = int(time.asctime().split()[-1])
                        this_time = this_entry[7]
                    else:
                        this_year = this_entry[7]
                        this_time = "00:00"
                    this_mtime = f"{this_year}-{month_encoder[this_month]}-{this_day}T{this_time}"
                    if (self.args['debug']):
                        print("mtime: %s" % this_mtime)
                    this_name = "".join([(one+" ") for one in this_entry[8:]]).strip()
                    if (self.args['debug']):
                        print("name: %s" % this_name)
                    modes.append(this_modes)
                    items.append(this_items)
                    owner.append(this_owner)
                    group.append(this_group)
                    fsize.append(this_fsize)
                    mtime.append(this_mtime)
                    name.append(this_name)
            metadata.insert(len(metadata.columns), 'modes', modes)
            metadata.insert(len(metadata.columns), 'items', items)
            metadata.insert(len(metadata.columns), 'owner', owner)
            metadata.insert(len(metadata.columns), 'group', group)
            metadata.insert(len(metadata.columns), 'fsize', fsize)
            metadata.insert(len(metadata.columns), 'mtime', mtime)
            metadata.insert(len(metadata.columns), 'name',  name)
            return metadata

    def exists(self, search:str) -> bool:
        """
        Perform the search analogous to os.path.exists(x) to 
        test for the existence of 'x' on the remote site.

        @TODO: please improve this documentation
        """
        command = (f"if [ -e '{search}' ]; then echo 'True' ; else echo 'False'; fi")
        results = self.system(command = command, classic = False)
        if (len(results) == 1):
            return bool(eval(results[0]))
        else:
            return False

    def touch(self, search:str) -> None:
        """
        Perform a 'touch' operation on the file specified by 'search'.
        That means create an empty file if none exists, otherwise update
        the 'last touched' timestamp.

        @TODO: please improve this documentation
        @FIXME: deal with absence of touch on windows
        """
        command = f"touch {search}"
        results = self.system(command = command, classic = False)
        return None

    def remove(self, search:str) -> None:
        """
        Removes a file

        @TODO: please improve this documentation
        @FIXME: make this work with windows in general
        """
        command = f"rm -f {search}"
        results = self.system(command = command, classic = False)
        return None

    def mkdir(self, search:str, mode:int = None, parents:bool = True) -> None:
        """
        Creates a directory with permission modes, possibly filling in
        the path to the directory as well.

        @TODO: please improve this documentation
        @FIXME: make this work with windows in general
        """
        if (parents):
            if (mode == None):
                command = f"mkdir -p {search}"
            else:
                command = f"mkdir -m {mode} -p {search}"
        else:
            if (mode == None):
                command = f"mkdir {search}"
            else:
                command = f"mkdir -m {mode} {search}"
        results = self.system(command = command, classic = False)
        return None

    def isdir(self, search:str) -> bool:
        """
        Tests whether a target is a directory

        @TODO: please improve this documentation
        @FIXME: make this work with windows in general
        """
        command = f"if [ -d '{search}' ]; then echo 'True' ; else echo 'False' ; fi"
        results = self.system(command = command, classic = False)
        if (len(results) == 1):
            return bool(eval(results[0]))
        else:
            return False

    def isfile(self, search:str) -> bool:
        """
        Tests whether a target is a file

        @TODO: please improve this documentation
        @FIXME: make this work with windows in general
        """
        command = f"if [ -f '{search}' ]; then echo 'True' ; else echo 'False' ; fi"
        results = self.system(command = command, classic = False)
        if (len(results) == 1):
            return bool(eval(results[0]))
        else:
            return False

    def islink(self, search:str) -> bool:
        """
        Tests whether a target is a symbolic link

        @TODO: please improve this documentation
        @FIXME: make this work with windows in general
        """
        command = f"if [ -L '{search}' ]; then echo 'True' ; else echo 'False' ; fi"
        results = self.system(command = command, classic = False)
        if (len(results) == 1):
            return bool(eval(results[0]))
        else:
            return False
        
    def rmdir(self, search:str, files_too:bool = False) -> None:
        """
        Removes a directory sub-tree, possibly recursively

        @TODO: please improve this documentation
        @FIXME: make this work with windows in general
        """
        # verify that 'search' is a directory...
        if (self.isdir(search)):
            if (files_too):
                command = f"rm -rf {search}"
            else:
                files = self.listdir(search)
                print(f"...in remote.rmdir you have NOT specified files_too = True\n" +
                      f"   and remote {search} contains {len(files)} files, namely:")
                print("")
                for id,item in enumerate(files):
                    print(f"\t{id}. '{item}'")
                print("")
                raise RemoteError(f"files_too = {files_too}, therefore may not delete files from remote directory")
        results = self.system(command = command, classic = False)
        return None
    
if (__name__ == "__main__"):
    """
    """
    print("")
    #
    #
    #
    this_computer = Remote()

    that_computer = Remote(username = "wcobb", hostname = "serenity")
    
    
    
