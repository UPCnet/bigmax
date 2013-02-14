#!/bin/bash
#
# Sets the correct url for css resources, i and html images based on a url parameter
# i.e. http://rocalcom.upc.edu (WITHOUT Trailing slash)
# This has to be executed in a local branch in production with its correct url
#
sed -i "s/\(url('\/\)/url('https:\/\/$1\//g" maxui.css
sed -i "s/\(src=\"\/\)/src=\"https:\/\/$1\//g" maxui.js
