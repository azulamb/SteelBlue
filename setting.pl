#!/usr/bin/perl

package STEELBLUESETTING;

# Setting file.

########################################
# Common Setting                       #
########################################

# Document root.
our $DOCROOT = '.';

# Use charset.
our @CHARSET = ( 'euc-jp', 'shiftjis', 'iso-2022-jp', 'utf8' );

# Permit command. ( 'chmod', 'mkdir', 'rm', 'mv' )
our @CMD = ( 'chmod', 'mkdir', 'cp', 'rm', 'mv' );

########################################
# index.cgi Setting                    #
########################################

# Page title
our $TITLE = 'STEEL BLUE';

# Script path.
our $SCRIPT = './index.cgi';

# Base URL.
our $BASEURL = '';

# View item in page( 0 = max ).
our $PAGENUM = 50;

# Use text view file extension.
our @EXTTXT = qw ( c cgi cpp css h hdml hpp htm html js pl pm py sh text txt );

# Use image view file extension.
our @EXTIMG = qw ( gif jpeg jpg ping png );

# Downloader.
our $DOWNLOADER = './downloader.cgi';

########################################
# uploader.cgi Setting                 #
########################################

# Default directory permission.
our $DIRPARMISIION  = 0705;

# Read buffer size.
our $BUFFERSIZE = 1024;

# Max upload size.
our $MAXSIZE = 0;

# JSON ContentType
our $JSONCONTENTTYPE = 'Content-Type: application/json; charset=utf-8';

########################################
# downloader.cgi Setting               #
########################################

# Force download.
our $DOWNLOAD = 1;


