CicadaArchive
=============
This repo contains all relevant files to the Cicada 3301 puzzle,
as well as the tools for organising, searching, submitting, and
visualising those files.

Concept
-------
The concept behind this project is to keep an exhaustive list of
files relating to the Cicada 3301 puzzle, capable of storing:

- Original file archives - Files posted by 3301 themselves
- Research - Background knowledge on the elements of the puzzle
- Analysis - Measurements and observations made on the puzzles themselves
- Ideas/Theories - For inspiring solution attempts
- Solutions/Documentation - For documenting the successful solutions of past puzzle parts
- Resources - Tools and learning materials helpful to solvers

All while keeping them searchable, maintainable, and decentralized.
Tools are supplied to automatically (for the most part) tag and index
new files into a flexible searchable and filterable format that is
stored right here in the repo in a json file. This allows manageable
forking and merging of repos. Files are stored de-centrally across
contributors machines, so even if the github repo gets taken down,
the files remain accessible.

How it works
------------
The project features a hierarchical list of tags designed to fit
all possible related files into useful tag trees that can be filtered and
searched for easy access to files that are relevant to you. `archive.py` is a
CLI controller for the tagging mechanisms. You can use it to tag files from the
command line, automatically populating the `tagdb.json` file. This file can then
be committed and merged with other repos, combining archives together
collaboratively.

Hierarchical tags are used to create tag trees that allow custom tagging
conventions to be applied to different fractals of the tag tree. It's actually
really simple I promise! The tag tree is stored in `tags.json` as a JSON Object.
A tag tree ends with a `null` value. Tagging works recursively, so you can think
of the tag tree one level at a time. Each key of the tag tree is the name used
to describe its value object's keys. For example:

```
tool:
    hammer: null
    screwdriver: null
    saw: null
```

The tagger is prompted for all tag trees in the root of the object. If the
value of the selected tag is not `null`, and is instead an object containing
more tags, the tagger is recursively asked for a tag from that object.

This method of hierarchical tagging allows us to have multiple category systems
that apply selectively to other categories. For example:

```
location:
    garage:
        box number:
            1
            2
            3
    workshop
    shed
    storage

size:
    small
    medium
    large

material:
    wood
    metal
    plastic

tool:
    hammer:
        type:
            automatic
            manual

    screwdriver:
        head type:
            phillips
            flat
            torx

        form factor:
            manual
            bit

    saw:
        form factor:
            band saw
            circular saw
            automatic hacksaw
            hand saw

        part type:
            blade
            body
            accessory
```

With the above tag tree for sorting tools, a user could easily select all tools
for wood in the workshop, all saw blades, or specifically only the metal cutting
ones. They could select all small saw's suitable for cutting wood, and from the
tag tree would be able to see where that saw is stored.
