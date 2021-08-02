# HTML to Markdown (html2md)
HTML to Markdown conversion tool.

Tested with [fiquipedia.es](http://fiquipedia.es) 

## A bit of history
This is a fork of [gsites2md](https://github.com/joaquinOnSoft/gsites2md), a tool
to migrate Google Site pages to Markdown. The original project includes 
some features that only apply to fiquipedia.es, so I decided to fork this project
to provide a more generic tool (site independent).

## Running on the command line

```
Convert an HTML file or folder (and its content) in a Markdown file

Execution:
	python HTML2mdCLI.py -s <input_file_or_folder> -d <destination_path>
	
where:
	-h, --help: Print this help
	-s, --source <source_path>: (Mandatory) source file or folder
	-d, --dest <dest_path>: (Mandatory) destination file or folder
	-r, --replace : (Optional) Flag: Replace Google Drive links to local links (It WON'T download the content by default. You must use in conjunction with --download to force the download)
	-D, --download : (Optional) Flag: Download Google Drive content to local drive.This option will have effect only if is used in conjunction with --replace, otherwise will be ignored
	-u, --url: (Optional) Use the page title, header of level 1 or the last section of the URL as URL description (only when URL link a description are the same). NOTE: This option can be slow.
	-t, --timeout <seconds>: (Optional) Timeout, in seconds, to use in link validation connections. It admits milliseconds, e.g. "0.750" or seconds "2". By default is unlimited
```

## Setting up your development environment
These are some recommended readings in order to set up a local environment using PyCharm;
   * [Create a Project from GitHub](https://www.jetbrains.com/pycharm/guide/tips/create-project-from-github/)
   * [Setting Up a Virtual Environment In PyCharm](https://arcade.academy/venv_install/index.html)
   
## Unit testing
> In order to execute the unit test that downloads content from Google Drive, you must have access to the 
> Google Drive account where the content is stored. 

## Download a copy of a website

This application needs a local copy of a website to use as input. The source HTML will be 
converted to Markdown.

### Prerequisites on Linux (Ubuntu/Debian)

#### Install 'wget'
> $ apt-get install wget

### Prerequisites on Mac

#### Install Homebrew
> $ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

#### Install 'wget'
> $ brew install wget

### Using 'wget' to download a local copy of a website
> wget --content-disposition --recursive -p http://www.fiquipedia.es

### URL parameters in file names downloaded by wget
If the server is kind, it might be sticking a `Content-Disposition header on 
the download advising your client of the correct filename. Telling `wget` to 
listen to that header for the final filename is as simple as:

> wget --content-disposition

Otherwise, you need to execute this script to remove the URL parameters from
the file names added by `wget` 

```sh
# /bin/bash
for i in `find $1 -type f`
do
    output=`echo $i | cut -d? -f1`
    if [ $i != $output ]
    then
        mv $i $output
    else
        echo "Skiping $i"
    fi
done
```
