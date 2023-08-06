Requires python 3.5 or greater

Every directory can have a .template.html. there is a small template preprocessor
reference files: like this %%{path-relative-to-current-file}%%

Put content into template like this: %%{%%}%% if you don't specify where the content should go,
the content is placed below the template content

.template.html files are applied to all files on the same level or below in the directory structure

how to set title of page? maybe in the templates we can overwrite it

## Building
`build.py` compiles the file in the source directory into a distribution directory.

you can use it like this:

```
python3 build.py
```

this will compile all files

or you can specify particular files that you want to compile:

```
python3 build.py index.html src/javascript_tutorial/index.html
```

all filepaths are relative to the source directory

the default source directory is `./src` and the default distribution directory is `./dist`

you can change these via command line:

```
python3 build.py index.html --dist /var/www/html/mysite --src /home/user/website_files
```

you can also give build.py a mix of directories and files. if you give it directories,
it will compile all files who are siblings or children (it is recursive).

## Watching
You can use `watch.py` to scan the filesystem on a certain interval for changes, and compile
the files that have changed (and only those files)

this can be more efficient than having to compile the whole site

the interface is similar to `build.py`

```
python3 watch.py
```

this will watch all files in the source directory, if files are added/deleted/modified, those files
will be recompiled

```
python3 watch.py src/javascript_tutorial
```

this will watch all files in the src/javascript_tutorial folder

you can specify the source and distribution directories too with the `--src` and `--dist` flags

you can also specify the interval that the scan is run with the `--interval` flag


## TODO
- make some way of specifying title from child pages
