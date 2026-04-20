import os
import io
import sys
import json
import hashlib
import argparse

print(
    """
     ,+++77777++=:,                    +=                      ,,++=7++=,,
    7~?7   +7I77 :,I777  I          77 7+77 7:        ,?777777??~,=+=~I7?,=77 I
=7I7I~7  ,77: ++:~+777777 7     +77=7 =7I7     ,I777= 77,:~7 +?7, ~7   ~ 777?
77+7I 777~,,=7~  ,::7=7: 7 77   77: 7 7 +77,7 I777~+777I=   =:,77,77  77 7,777,
  = 7  ?7 , 7~,~  + 77 ?: :?777 +~77 77? I7777I7I7 777+77   =:, ?7   +7 777?
      77 ~I == ~77=77777~: I,+77?  7  7:?7? ?7 7 7 77 ~I   7I,,?7 I77~
       I 7=77~+77+?=:I+~77?     , I 7? 77 7   777~ +7 I+?7  +7~?777,77I
         =77 77= +7 7777         ,7 7?7:,??7     +7    7   77??+ 7777,
             =I, I 7+:77?         +7I7?7777 :             :7 7
                7I7I?77 ~         +7:77,     ~         +7,::7   7
               ,7~77?7? ?:         7+:77           77 :7777=
                ?77 +I7+,7         7~  7,+7  ,?       ?7?~?777:
                   I777=7777 ~     77 :  77 =7+,    I77  777
                     +      ~?     , + 7    ,, ~I,  = ? ,
                                    77:I+
                                    ,7
                                     :777
                                        :

                              [ Archive Manager ]
"""
)
print(
    """\
Thank you for helping to keep this archive up to date. Before you can create a
pull request, you need to update the tags of the files you've added.
"""
)


class ArchiveManager(object):
    def __init__(self, debug=False):

        self.use_path_tags_exclusive = True
        self.get_tags_from_path = True

        self.bl_files = [
            "tagdb.json",
            "tags.json",
            "archive.py",
            "README.md",
            "static.html",
        ]
        self.bl_dirs = [".git"]

        hashes = []
        # load the tag database from file
        with open("tagdb.json") as tdb:
            self.tagdb = json.loads(tdb.read())

        # loads the tag list
        with open("tags.json") as tf:
            self.tags = json.loads(tf.read())

        if not debug:
            self.parser = argparse.ArgumentParser(
                description="Tags cicada files for archiving",
                usage="python3 %s <command> [<flags>] [<args>]\n\n" % sys.argv[0]
                + "Command list:\n"
                + "\tautotag - Wizard for tagging new files\n"
                + "\ttag - Modify the tags of a given file(s)\n"
                + "\thelp - Print this help info\n",
            )

            self.parser.add_argument("command", help="Subcommand to run")
            args = self.parser.parse_args(sys.argv[1:2])
            # if command exists
            if args.command[0] != "_" and hasattr(self, args.command):
                # run command
                getattr(self, args.command)()
            else:
                raise UnrecognizedCommand

    def help(self):
        self.parser.print_help()

    def _is_blacklisted(self, path: str):
        path = os.path.normpath(path).split(os.path.sep)
        # file is blacklisted
        if path[-1] in self.bl_files:
            return True
        # folder is blacklisted
        elif any([x in self.bl_dirs for x in path[:-1]]):
            return True
        # filename starts with a .
        elif path[-1][0] == ".":
            return True
        return False

    def _is_tagged(self, path: str):
        hash = self._hash_file(path)

        # merge the old tags with the new one (in case the file has moved or tags )
        if hash in self.tagdb["files"]:
            return True
        return False

    def autotag(self):
        parser = argparse.ArgumentParser(description="Wizard for tagging new files")
        parser.add_argument(
            "directories",
            action="store",
            nargs="*",
            help="Optional directory(s) to search in",
        )
        args = parser.parse_args(sys.argv[2:])
        paths = args.directories or ["."]
        hashes = []
        # iterate all the files, adding automatic tags where possible
        for path in paths:
            # merge the old tags with the new one (in case the file has moved or tags )
            for root, file in self._get_files(path=path):
                filepath = os.path.join(root, file)
                if self._is_tagged(filepath):
                    continue

                # store the current hashes for later (used to determine removed files)
                hashes.append(hash)

                file_tags = self._tag_file(os.path.join(root, file), hash)

    def tag(self):
        parser = argparse.ArgumentParser(
            description="Sets the tags of a file. Directories are set recurrsively"
        )
        parser.add_argument(
            "files", type=str, help="File(s) or folder(s) to tag", nargs="+"
        )
        args = parser.parse_args(sys.argv[2:])
        # get file hash
        # get tags
        for file in args.files:
            print(self._tag_file(file, self._hash_file(file)))
        # store tags

    def search(self):
        parser = argparse.ArgumentParser(
            description="Searches the database for files matching a query"
        )
        parser.add_argument(
            "queries", type=str, help="Queries that match the returned files", nargs="+"
        )
        args = parser.parse_args(sys.argv[2:])

        files = []
        for file in self.tagdb["files"]:
            # does the file match all our queries?
            match = True
            for query in args.queries:
                # if previous tags did not match, we can skip
                if not match:
                    break
                # parse query, optionally accepting the form parent:child
                if ":" in query:
                    pair = query.split(":")
                    parent = pair[0]
                    child = pair[1]
                else:
                    parent = False
                    child = query
                match = False
                for path in self.tagdb["files"][file]["tags"]:
                    for i, tag in enumerate(path):
                        if child == tag:
                            if not parent or path[i - 1] == parent:
                                match = True
                                break
                    if match:
                        break
                if match:
                    files.append(file)
        return files

    def untag(self):
        parser = argparse.ArgumentParser(
            description="Unsets the tags of a file. Directories are set recurrsively"
        )
        parser.add_argument(
            "files", type=str, help="File(s) or folder(s) to tag", nargs="+"
        )
        args = parser.parse_args(sys.argv[2:])
        for file in args.files:
            del self.tagdb["files"][self._hash_file(file)]
            self._commit_tags()
        print("The requested files have been untagged")

    def webserver(self):
        parser = argparse.ArgumentParser(
            description="Starts a flask webserver for GUI tagging and searching"
        )
        parser.add_argument(
            "--host",
            metavar="h",
            type=str,
            help="Host for the local webserver",
            default="localhost",
        )
        parser.add_argument(
            "--port",
            metavar="p",
            type=int,
            help="Port for the local webserver",
            default="8080",
        )
        args = parser.parse_args(sys.argv[2:])
        from flask import Flask

        app = Flask(__name__, static_url_path="", static_folder=".")

        @app.route("/")
        def index():
            return app.send_static_file("static.html")

        # gets a list of untagged files in the archive
        @app.route("/1/get_untagged")
        def get_untagged():
            untagged_files = []
            # for all the files in the archive
            for root, file in self._get_files():
                # check if the file is tagged
                filepath = os.path.join(root, file)
                if self._is_tagged(filepath):
                    continue
                untagged_files.append(
                    {
                        "path": os.path.normpath(filepath),
                        "tags": self._get_path_tags(filepath),
                    }
                )

            return json.dumps(untagged_files)

        # tags a file
        @app.route("/1/tag_file")
        def tag_file():
            pass

        @app.route("/1/search_files")
        def search_files():
            pass

        app.run(host=args.host, port=args.port, debug=True)

    def _get_files(self, path="."):
        for root, directories, files in os.walk(path):
            for file in files:
                if not self._is_blacklisted(os.path.join(root, file)):
                    yield root, file

    def _commit_tags(self):
        with open("tagdb.json", "w") as tagdb_file:
            tagdb_file.write(json.dumps(self.tagdb, indent=1))

    # automatically suggest tags
    def _get_path_tags(self, path):
        path_tag = []
        # auto add tag path for the directory it's in
        tag_level = self.tags.copy()

        def get_pairs(d, path=[]):
            if not d:
                return False
            for parent in d:
                if isinstance(d[parent], dict):
                    for child in d[parent]:
                        p = get_pairs(d[parent][child], path=path + [parent, child])
                        if p:
                            yield from p
                        yield (parent, child), path + [parent, child]

        for folder_name in os.path.normpath(path).split(os.sep):
            for pair, path in get_pairs(tag_level):
                if folder_name == pair[1]:
                    if path[:-2] in path_tag:
                        path_tag.remove(path[:-2])
                    path_tag.append(path)
                    break

        return path_tag

    # get the hashsum of the file at path
    def _hash_file(self, path):
        hasher = hashlib.sha256()
        with open(path, "rb") as f:
            buf = f.read(pow(2, 16))
            while len(buf) > 0:
                hasher.update(buf)
                buf = f.read(pow(2, 16))
        return hasher.hexdigest()

    def _tag_file(self, filepath, hash):
        # request tags
        tags = self._request_tags(pretags=self._get_path_tags(filepath))
        # commit changes to tagdb
        self.tagdb["files"][hash] = {
            "tags": tags,
            "path": filepath
            # tagger? maybe get their git username
            # tag date?
        }
        self._commit_tags()
        return tags

    # use the tag tree to ask the user for tags
    def _request_tags(self, path=[], pretags=[], st=False):
        tags = self.tags.copy()
        # apply the path
        for key in path:
            tags = tags[key]
        if tags == None:
            # we reached the end of the tree
            return None
        ret_tags = []
        for tag in tags.keys():
            get_user_input = True
            input_tags = []
            # look in the path for tags
            if self.get_tags_from_path:
                for parent, child in pretags:
                    if tag == parent:
                        input_tags.append((parent, child))
                        if self.use_path_tags_exclusive:
                            get_user_input = False
            all = False
            # ask for tags
            while get_user_input:
                error = False
                curpath = (
                    " > ".join(
                        [
                            "%s:%s" % (path[i], path[i + 1])
                            for i in range(0, len(path), 2)
                        ]
                    )
                    or "root"
                )
                print("\nCurrent path: " + curpath)
                print("Please select one or more %s" % tag)
                # print(tags[tag], tag)
                tag_chips = [
                    "[%s:%s]" % (i + 1, key) for i, key in enumerate(tags[tag])
                ]
                i = input(" ".join(["[A:all] [N:None]"] + tag_chips) + ": ")
                # parse user submitted tags
                for input_tag in i.split(" "):
                    if input_tag.lower() == "a":
                        input_tags = [(tag, value) for value in tags[tag].keys()]
                        all = True
                        # input_tags = ["%s:%s"%(tag, value) for value in tags[tag].keys()]
                    elif input_tag.lower() == "n":
                        break
                    elif input_tag.isnumeric() and int(input_tag) <= len(tags[tag]):
                        input_tags.append(
                            [tag, list(tags[tag].keys())[int(input_tag) - 1]]
                        )
                    elif input_tag in tags[tag]:
                        input_tags.append([tag, input_tag])
                    else:
                        print(
                            "Sorry, tag `%s` wasn't recognized. Try again." % input_tag
                        )
                        error = True
                        break
                if error:
                    continue
                break
            for tag1, tag2 in input_tags.copy():
                if all:
                    tmp_tags = path + [tag1, tag2]
                else:
                    tmp_tags = self._request_tags(
                        path + [tag1, tag2], pretags=pretags, st=True
                    )
                if tmp_tags:
                    if st:
                        ret_tags.append(tmp_tags)
                    else:
                        ret_tags += tmp_tags[0]
                else:
                    ret_tags.append(path + [tag1, tag2])
                # print("ret_tags: ", ret_tags)
        return ret_tags

        input("Press [ENTER] to exit...")


class GenericException(Exception):
    details = "An unexpected error has occured"

    def __init__(self):
        super().__init__(self.details)


class UnrecognizedCommand(GenericException):
    details = (
        "A command was specified that was not recognized. Please check "
        + "input and try again"
    )


if __name__ == "__main__":
    ArchiveManager()
