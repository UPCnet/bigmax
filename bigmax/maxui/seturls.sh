#!/bin/bash
sed -i "s/\(url('\/\)/url('https:\/\/$1\//g" maxui.css
sed -i "s/\(src=\"\/\)/src=\"https:\/\/$1\//g" maxui.js
