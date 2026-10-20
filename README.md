# Beauregard NetGen

**Beauregard NetGen** is a static site generator for PHP-based websites, I built it as a side project at work and thought someone else might get some use out of it. Out of the box, it's hard-wired to compile v9 of [sladewatkins.com](https://www.sladewatkins.com). You'll need to configure it accordingly, unless you wish to replicate v9's structure (which is laid out in the python file).

## Installation
Put ``build.py`` in the root directory of your site. To make a build of your site, point your Terminal window at the root directory, and run the following command (which may vary by OS and platform; macOS shown below):

```
python3 build.py
```

## Configuration
Everything in this repository has comments, you should be able to easily locate what you're looking for. In case you need a glossary, I've included one below:

- Encoding: ``utf-8`` is mandatory across your entire site to use this script, all other encoding is unsupported by this script.
- PHP Include: you'll need these in your PHP files to do anything with this script. My recommendation is to use the same code structure I use (find in Examples below) and adapt the ``build.py`` script code accordingly for your file structure.
- ``parts``: speaking of includes -- these resources are your reusable assets like headers, footers, and navigation. By default, the script will look in the folder structure of ``assets/website/parts`` as that's where they are stored on v9.

### Examples
PHP include script is as follows (using navbar as an example):

```
<?php 
   $path = $_SERVER['DOCUMENT_ROOT'];
   $path .= "/assets/website/parts/navbar.php";
   include_once($path);
?>
```