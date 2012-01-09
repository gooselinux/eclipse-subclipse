#!/bin/sh
VERSION=1.6.5
svn export --username guest --password "" http://subclipse.tigris.org/svn/subclipse/tags/subclipse/$VERSION/subclipse subclipse-$VERSION
rm -rf ./subclipse-$VERSION/org.tigris.subversion.clientadapter.javahl.win32
tar -czf subclipse-$VERSION.tgz subclipse-$VERSION
