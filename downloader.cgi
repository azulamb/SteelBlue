#!/usr/bin/perl

use strict;
use warnings;

use utf8;
use Encode;
use Encode::Guess qw/euc-jp shiftjis iso-2022-jp utf8/;

########################################
# Setting                              #
########################################

require './setting.pl';

#our $DOCROOT = '.';
#our $DOWNLOAD = 1;

# MIME Type table.
our %MIMETYPE =
(
  '123'     => { 'type' => 'bin', 'mime' => 'application/vnd.lotus-1-2-3' },
  '3g2'     => { 'type' => 'bin', 'mime' => 'video/3gpp2' },
  '3gp'     => { 'type' => 'bin', 'mime' => 'video/3gpp' },

  'ai'      => { 'type' => 'bin', 'mime' => 'application/postscript' },
  'aif'     => { 'type' => 'bin', 'mime' => 'audio/x-aiff' },
  'aifc'    => { 'type' => 'bin', 'mime' => 'audio/x-aiff' },
  'aiff'    => { 'type' => 'bin', 'mime' => 'audio/x-aiff' },
  'album'   => { 'type' => 'bin', 'mime' => 'application/album' },
  'amc'     => { 'type' => 'bin', 'mime' => 'application/x-mpeg' },
  'api'     => { 'type' => 'bin', 'mime' => 'application/x-httpd-isapi' },
  'asc'     => { 'type' => 'txt', 'mime' => 'text/plain' },
  'asd'     => { 'type' => 'bin', 'mime' => 'application/astound' },
  'asf'     => { 'type' => 'bin', 'mime' => 'video/x-ms-asf' },
  'asis'    => { 'type' => 'bin', 'mime' => 'httpd/send-as-is' },
  'asn'     => { 'type' => 'bin', 'mime' => 'application/astound' },
  'asp'     => { 'type' => 'bin', 'mime' => 'application/x-asap' },
  'asx'     => { 'type' => 'bin', 'mime' => 'video/x-ms-asf' },
  'au'      => { 'type' => 'bin', 'mime' => 'audio/basic' },
  'avi'     => { 'type' => 'bin', 'mime' => 'video/x-msvideo' },

  'bcpio'   => { 'type' => 'bin', 'mime' => 'application/x-bcpio' },
  'bin'     => { 'type' => 'bin', 'mime' => 'application/octet-stream' },
  'bmp'     => { 'type' => 'bin', 'mime' => 'image/bmp' },

  'cco'     => { 'type' => 'bin', 'mime' => 'application/x-cocoa' },
  'cct'     => { 'type' => 'bin', 'mime' => 'application/x-cct' },
  'cdf'     => { 'type' => 'bin', 'mime' => 'application/x-netcdf' },
  'cgi'     => { 'type' => 'txt', 'mime' => 'application/x-httpd-cgi' },
  'class'   => { 'type' => 'bin', 'mime' => 'application/octet-stream' },
  'clp'     => { 'type' => 'bin', 'mime' => 'application/x-msclip' },
  'cocoa'   => { 'type' => 'bin', 'mime' => 'application/x-cocoa' },
  'com'     => { 'type' => 'bin', 'mime' => 'application/octet-stream' },
  'cpio'    => { 'type' => 'bin', 'mime' => 'application/x-cpio' },
  'cpt'     => { 'type' => 'bin', 'mime' => 'application/mac-compactpro' },
  'crd'     => { 'type' => 'bin', 'mime' => 'application/x-mscardfile' },
  'csh'     => { 'type' => 'txt', 'mime' => 'application/x-csh' },
  'csm'     => { 'type' => 'bin', 'mime' => 'chemical/x-csml' },
  'csml'    => { 'type' => 'bin', 'mime' => 'chemical/x-csml' },
  'css'     => { 'type' => 'txt', 'mime' => 'text/css' },
  'd96'     => { 'type' => 'bin', 'mime' => 'x-world/x-d96' },

  'dcr'     => { 'type' => 'bin', 'mime' => 'application/x-director' },
  'dir'     => { 'type' => 'bin', 'mime' => 'application/x-director' },
  'dl'      => { 'type' => 'bin', 'mime' => 'application/x-WebSync-plugin' },
  'dms'     => { 'type' => 'bin', 'mime' => 'application/octet-stream' },
  'doc'     => { 'type' => 'bin', 'mime' => 'application/msword' },
  'dot'     => { 'type' => 'bin', 'mime' => 'application/x-dot' },
  'dvi'     => { 'type' => 'bin', 'mime' => 'application/x-dvi' },
  'dwf'     => { 'type' => 'bin', 'mime' => 'drawing/x-dwf' },
  'dwg'     => { 'type' => 'bin', 'mime' => 'image/vnd' },
  'dxr'     => { 'type' => 'bin', 'mime' => 'application/x-director' },

  'ebk'     => { 'type' => 'bin', 'mime' => 'application/x-expandedbook' },
  'emb'     => { 'type' => 'bin', 'mime' => 'chemical/x-embl-dl-nucleotide' },
  'embl'    => { 'type' => 'bin', 'mime' => 'chemical/x-embl-dl-nucleotide' },
  'eps'     => { 'type' => 'bin', 'mime' => 'application/postscript' },
  'es'      => { 'type' => 'bin', 'mime' => 'audio/echospeech' },
  'esl'     => { 'type' => 'bin', 'mime' => 'audio/echospeech' },
  'etc'     => { 'type' => 'bin', 'mime' => 'application/x-earthtime' },
  'etx'     => { 'type' => 'txt', 'mime' => 'text/x-setext' },
  'evy'     => { 'type' => 'bin', 'mime' => 'application/x-envoy' },
  'exe'     => { 'type' => 'bin', 'mime' => 'application/octet-stream' },
  'ez'      => { 'type' => 'bin', 'mime' => 'application/andrew-inset' },

  'fdf'     => { 'type' => 'bin', 'mime' => 'application/vnd' },
  'fgd'     => { 'type' => 'bin', 'mime' => 'application/x-director' },
  'fif'     => { 'type' => 'bin', 'mime' => 'image/fif' },
  'fm'      => { 'type' => 'bin', 'mime' => 'application/x-maker' },
  'fvi'     => { 'type' => 'bin', 'mime' => 'video/isivideo' },

  'gau'     => { 'type' => 'bin', 'mime' => 'chemical/x-gaussian-input' },
  'gif'     => { 'type' => 'bin', 'mime' => 'image/gif' },
  'gtar'    => { 'type' => 'bin', 'mime' => 'application/x-gtar' },
  'gz'      => { 'type' => 'bin', 'mime' => 'application/octet-stream' },

  'hdf'     => { 'type' => 'bin', 'mime' => 'application/x-hdf' },
  'hdml'    => { 'type' => 'txt', 'mime' => 'text/x-hdml;charset=Shift_JIS' },
  'hlp'     => { 'type' => 'bin', 'mime' => 'application/winhlp' },
  'hqx'     => { 'type' => 'bin', 'mime' => 'application/mac-binhex40' },
  'htm'     => { 'type' => 'txt', 'mime' => 'text/html' },
  'html'    => { 'type' => 'txt', 'mime' => 'text/html' },

  'ice'     => { 'type' => 'bin', 'mime' => 'x-conference/x-cooltalk' },
  'ico'     => { 'type' => 'bin', 'mime' => 'image/vnd.microsoft.icon' },
  'ief'     => { 'type' => 'bin', 'mime' => 'image/ief' },
  'ifm'     => { 'type' => 'bin', 'mime' => 'image/gif' },
  'ifs'     => { 'type' => 'bin', 'mime' => 'image/ifs' },
  'iges'    => { 'type' => 'bin', 'mime' => 'model/iges' },
  'igs'     => { 'type' => 'bin', 'mime' => 'model/iges' },
  'ins'     => { 'type' => 'bin', 'mime' => 'application/x-NET-Install' },
  'ips'     => { 'type' => 'bin', 'mime' => 'application/x-ipscript' },
  'ipx'     => { 'type' => 'bin', 'mime' => 'application/x-ipix' },
  'ivr'     => { 'type' => 'bin', 'mime' => 'i-world/i-vrml' },

  'jbw'     => { 'type' => 'bin', 'mime' => 'application/x-js-taro' },
  'jfw'     => { 'type' => 'bin', 'mime' => 'application/x-js-taro' },
  'jnlp'    => { 'type' => 'bin', 'mime' => 'application/x-java-jnlp-file' },
  'jpe'     => { 'type' => 'bin', 'mime' => 'image/jpeg' },
  'jpeg'    => { 'type' => 'bin', 'mime' => 'image/jpeg' },
  'jpg'     => { 'type' => 'bin', 'mime' => 'image/jpeg' },
  'js'      => { 'type' => 'bin', 'mime' => 'application/x-javascript' },
  'jtd'     => { 'type' => 'bin', 'mime' => 'application/x-js-taro' },

  'kar'     => { 'type' => 'bin', 'mime' => 'audio/midi' },
  'kjx'     => { 'type' => 'bin', 'mime' => 'application/x-kjx' },

  'latex'   => { 'type' => 'bin', 'mime' => 'application/x-latex' },
  'lcc'     => { 'type' => 'bin', 'mime' => 'application/fastman' },
  'lcl'     => { 'type' => 'bin', 'mime' => 'application/x-digitalloca' },
  'lcr'     => { 'type' => 'bin', 'mime' => 'application/x-digitalloca' },
  'lha'     => { 'type' => 'bin', 'mime' => 'application/octet-stream' },
  'lzh'     => { 'type' => 'bin', 'mime' => 'application/octet-stream' },

  'm13'     => { 'type' => 'bin', 'mime' => 'application/x-msmediaview' },
  'm14'     => { 'type' => 'bin', 'mime' => 'application/x-msmediaview' },
  'm3u'     => { 'type' => 'bin', 'mime' => 'audio/x-mpegurl' },
  'man'     => { 'type' => 'bin', 'mime' => 'application/x-troff-man' },
  'map'     => { 'type' => 'bin', 'mime' => 'application/x-httpd-imap' },
  'mbd'     => { 'type' => 'bin', 'mime' => 'application/mbedlet' },
  'mcf'     => { 'type' => 'txt', 'mime' => 'text/mcf' },
  'mcp'     => { 'type' => 'bin', 'mime' => 'application/netmc' },
  'mct'     => { 'type' => 'bin', 'mime' => 'application/x-mascot' },
  'md'      => { 'type' => 'txt', 'mime' => 'text/x-markdown' },
  'mdb'     => { 'type' => 'bin', 'mime' => 'application/x-msaccess' },
  'mdc'     => { 'type' => 'bin', 'mime' => 'application/x-mediadesc' },
  'mdx'     => { 'type' => 'bin', 'mime' => 'application/x-mediadesc' },
  'me'      => { 'type' => 'bin', 'mime' => 'application/x-troff-me' },
  'mesh'    => { 'type' => 'bin', 'mime' => 'model/mesh' },
  'mid'     => { 'type' => 'bin', 'mime' => 'audio/midi' },
  'midi'    => { 'type' => 'bin', 'mime' => 'audio/midi' },
  'mif'     => { 'type' => 'bin', 'mime' => 'application/vnd.mif' },
  'mio'     => { 'type' => 'bin', 'mime' => 'audio/x-mio' },
  'mmf'     => { 'type' => 'bin', 'mime' => 'application/x-smaf' },
  'mng'     => { 'type' => 'bin', 'mime' => 'video/x-mng' },
  'mny'     => { 'type' => 'bin', 'mime' => 'application/x-msmoney' },
  'mocha'   => { 'type' => 'bin', 'mime' => 'application/x-mocha' },
  'mof'     => { 'type' => 'bin', 'mime' => 'application/x-yumekara' },
  'mol'     => { 'type' => 'bin', 'mime' => 'chemical/x-mdl-molfile' },
  'mop'     => { 'type' => 'bin', 'mime' => 'chemical/x-mopac-input' },
  'mov'     => { 'type' => 'bin', 'mime' => 'video/quicktime' },
  'movie'   => { 'type' => 'bin', 'mime' => 'video/x-sgi-movie' },
  'mp2'     => { 'type' => 'bin', 'mime' => 'audio/mpeg' },
  'mp3'     => { 'type' => 'bin', 'mime' => 'audio/mpeg' },
  'mp4'     => { 'type' => 'bin', 'mime' => 'video/mp4' },
  'mpe'     => { 'type' => 'bin', 'mime' => 'video/mpeg' },
  'mpeg'    => { 'type' => 'bin', 'mime' => 'video/mpeg' },
  'mpg'     => { 'type' => 'bin', 'mime' => 'video/mpeg' },
  'mpg4'    => { 'type' => 'bin', 'mime' => 'video/mp4' },
  'mpga'    => { 'type' => 'bin', 'mime' => 'audio/mpeg' },
  'mpp'     => { 'type' => 'bin', 'mime' => 'application/vnd.ms-project' },
  'mrl'     => { 'type' => 'txt', 'mime' => 'text/x-mrml' },
  'ms'      => { 'type' => 'bin', 'mime' => 'application/x-troff-ms' },
  'msh'     => { 'type' => 'bin', 'mime' => 'model/mesh' },
  'mus'     => { 'type' => 'bin', 'mime' => 'x-world/x-d96' },

  'nc'      => { 'type' => 'bin', 'mime' => 'application/x-netcdf' },
  'nm'      => { 'type' => 'bin', 'mime' => 'application/x-nvat' },
  'nva'     => { 'type' => 'bin', 'mime' => 'application/x-neva1' },
  'nvat'    => { 'type' => 'bin', 'mime' => 'application/x-nvat' },

  'oda'     => { 'type' => 'bin', 'mime' => 'application/oda' },
  'oke'     => { 'type' => 'bin', 'mime' => 'audio/karaoke' },
  'olh'     => { 'type' => 'bin', 'mime' => 'application/x-onlivehead' },
  'olr'     => { 'type' => 'bin', 'mime' => 'application/x-onlivereg' },
  'olv'     => { 'type' => 'bin', 'mime' => 'x-world/x-vrml1.0' },

  'pac'     => { 'type' => 'bin', 'mime' => 'audio/x-pac' },
  'pae'     => { 'type' => 'bin', 'mime' => 'audio/x-epac' },
  'pbm'     => { 'type' => 'bin', 'mime' => 'image/x-portable-bitmap' },
  'pcv'     => { 'type' => 'bin', 'mime' => 'application/x-pcnavi' },
  'pdb'     => { 'type' => 'bin', 'mime' => 'chemical/x-pdb' },
  'pdf'     => { 'type' => 'bin', 'mime' => 'application/pdf' },
  'pfr'     => { 'type' => 'bin', 'mime' => 'application/font-tdpfr' },
  'pgm'     => { 'type' => 'bin', 'mime' => 'image/x-portable-graymap' },
  'pgn'     => { 'type' => 'bin', 'mime' => 'application/x-chess-pgn' },
  'pl'      => { 'type' => 'txt', 'mime' => 'application/x-perl' },
  'pm'      => { 'type' => 'txt', 'mime' => 'application/x-perl' },
  'pmd'     => { 'type' => 'bin', 'mime' => 'application/x-pmd' },
  'png'     => { 'type' => 'bin', 'mime' => 'image/png' },
  'pnm'     => { 'type' => 'bin', 'mime' => 'image/x-portable-anymap' },
  'pot'     => { 'type' => 'bin', 'mime' => 'application/vnd.ms-powerpoint' },
  'ppm'     => { 'type' => 'bin', 'mime' => 'image/x-portable-pixmap' },
  'pps'     => { 'type' => 'bin', 'mime' => 'application/vnd.ms-powerpoint' },
  'ppt'     => { 'type' => 'bin', 'mime' => 'application/vnd.ms-powerpoint' },
  'prc'     => { 'type' => 'bin', 'mime' => 'application/x-palmpilot' },
  'ps'      => { 'type' => 'bin', 'mime' => 'application/postscript' },
  'pub'     => { 'type' => 'bin', 'mime' => 'application/x-mspublisher' },

  'qcp'     => { 'type' => 'bin', 'mime' => 'audio/vnd.qcelp' },
  'qt'      => { 'type' => 'bin', 'mime' => 'video/quicktime' },
  'py'      => { 'type' => 'txt', 'mime' => 'application/x-python' },

  'ra'      => { 'type' => 'bin', 'mime' => 'audio/x-realaudio' },
  'rb'      => { 'type' => 'txt', 'mime' => 'application/x-ruby' },
  'ram'     => { 'type' => 'bin', 'mime' => 'audio/x-pn-realaudio' },
  'rdf'     => { 'type' => 'bin', 'mime' => 'application/xml' },
  'ras'     => { 'type' => 'bin', 'mime' => 'image/x-cmu-raster' },
  'rgb'     => { 'type' => 'bin', 'mime' => 'image/x-rgb' },
  'rm'      => { 'type' => 'bin', 'mime' => 'audio/x-pn-realaudio' },
  'roff'    => { 'type' => 'bin', 'mime' => 'application/x-troff' },
  'rp'      => { 'type' => 'bin', 'mime' => 'image/vnd.rn-realpix' },
  'rpm'     => { 'type' => 'bin', 'mime' => 'audio/x-pn-realaudio-plugin' },
  'rt'      => { 'type' => 'txt', 'mime' => 'text/vnd.rn-realtext' },
  'rtf'     => { 'type' => 'txt', 'mime' => 'text/rtf' },
  'rtx'     => { 'type' => 'txt', 'mime' => 'text/richtext' },
  'rv'      => { 'type' => 'bin', 'mime' => 'video/vnd.rn-realvideo' },
  'rxnfile' => { 'type' => 'bin', 'mime' => 'chemical/x-mdl-rxnfile' },

  'scd'     => { 'type' => 'bin', 'mime' => 'application/x-msschedule' },
  'sds'     => { 'type' => 'bin', 'mime' => 'application/x-onlive' },
  'sea'     => { 'type' => 'bin', 'mime' => 'application/octet-stream' },
  'sgm'     => { 'type' => 'txt', 'mime' => 'text/sgml' },
  'sgml'    => { 'type' => 'txt', 'mime' => 'text/sgml' },
  'sh'      => { 'type' => 'txt', 'mime' => 'application/x-sh' },
  'shar'    => { 'type' => 'bin', 'mime' => 'application/x-shar' },
  'silo'    => { 'type' => 'bin', 'mime' => 'model/mesh' },
  'sit'     => { 'type' => 'bin', 'mime' => 'application/x-stuffit' },
  'skd'     => { 'type' => 'bin', 'mime' => 'application/x-koan' },
  'skm'     => { 'type' => 'bin', 'mime' => 'application/x-koan' },
  'skp'     => { 'type' => 'bin', 'mime' => 'application/x-koan' },
  'skt'     => { 'type' => 'bin', 'mime' => 'application/x-koan' },
  'slc'     => { 'type' => 'bin', 'mime' => 'application/x-salsa' },
  'smi'     => { 'type' => 'bin', 'mime' => 'application/smil' },
  'smil'    => { 'type' => 'bin', 'mime' => 'application/smil' },
  'smp'     => { 'type' => 'bin', 'mime' => 'application/studiom' },
  'snd'     => { 'type' => 'bin', 'mime' => 'audio/basic' },
  'spl'     => { 'type' => 'bin', 'mime' => 'application/x-futuresplash' },
  'sprite'  => { 'type' => 'bin', 'mime' => 'application/x-sprite' },
  'spt'     => { 'type' => 'bin', 'mime' => 'application/x-spt' },
  'src'     => { 'type' => 'bin', 'mime' => 'application/x-wais-source' },
  'sv4cpio' => { 'type' => 'bin', 'mime' => 'application/x-sv4cpio' },
  'sv4crc'  => { 'type' => 'bin', 'mime' => 'application/x-sv4crc' },
  'svf'     => { 'type' => 'bin', 'mime' => 'image/vnd' },
  'svi'     => { 'type' => 'bin', 'mime' => 'application/softvision' },
  'svr'     => { 'type' => 'bin', 'mime' => 'x-world/x-svr' },
  'swf'     => { 'type' => 'bin', 'mime' => 'application/x-shockwave-flash' },

  't'       => { 'type' => 'bin', 'mime' => 'application/x-troff' },
  'talk'    => { 'type' => 'txt', 'mime' => 'text/x-speech' },
  'tar'     => { 'type' => 'bin', 'mime' => 'application/x-tar' },
  'tbp'     => { 'type' => 'bin', 'mime' => 'application/x-timbuktu' },
  'tbt'     => { 'type' => 'bin', 'mime' => 'application/timbuktu' },
  'tcl'     => { 'type' => 'bin', 'mime' => 'application/x-tcl' },
  'tex'     => { 'type' => 'txt', 'mime' => 'application/x-tex' },
  'texinfo' => { 'type' => 'bin', 'mime' => 'application/x-texinfo' },
  'tgf'     => { 'type' => 'bin', 'mime' => 'chemical/x-mdl-tgf' },
  'tif'     => { 'type' => 'bin', 'mime' => 'image/tiff' },
  'tiff'    => { 'type' => 'bin', 'mime' => 'image/tiff' },
  'tki'     => { 'type' => 'bin', 'mime' => 'application/x-tkined' },
  'tkined'  => { 'type' => 'bin', 'mime' => 'application/x-tkined' },
  'tlk'     => { 'type' => 'bin', 'mime' => 'application/x-tlk' },
  'tr'      => { 'type' => 'bin', 'mime' => 'application/x-troff' },
  'trm'     => { 'type' => 'bin', 'mime' => 'application/x-msterminal' },
  'tsp'     => { 'type' => 'bin', 'mime' => 'application/dsptype' },
  'tsv'     => { 'type' => 'txt', 'mime' => 'text/tab-separated-values' },
  'ttz'     => { 'type' => 'bin', 'mime' => 'application/t-time' },
  'txt'     => { 'type' => 'txt', 'mime' => 'text/plain' },

  'ustar'   => { 'type' => 'bin', 'mime' => 'application/x-ustar' },

  'vcd'     => { 'type' => 'bin', 'mime' => 'application/x-cdlink' },
  'vdo'     => { 'type' => 'bin', 'mime' => 'video/vdo' },
  'vex'     => { 'type' => 'bin', 'mime' => 'application/x-yumekara' },
  'vgm'     => { 'type' => 'bin', 'mime' => 'video/x-videogram' },
  'vgp'     => { 'type' => 'bin', 'mime' => 'video/x-videogram-plugin' },
  'vgx'     => { 'type' => 'bin', 'mime' => 'video/x-videogram' },
  'vif'     => { 'type' => 'bin', 'mime' => 'video/x-vif' },
  'viv'     => { 'type' => 'bin', 'mime' => 'video/vnd.vivo' },
  'vivo'    => { 'type' => 'bin', 'mime' => 'video/vnd.vivo' },
  'vqe'     => { 'type' => 'bin', 'mime' => 'audio/x-twinvq-plugin' },
  'vqf'     => { 'type' => 'bin', 'mime' => 'audio/x-twinvq' },
  'vql'     => { 'type' => 'bin', 'mime' => 'audio/x-twinvq' },
  'vrml'    => { 'type' => 'bin', 'mime' => 'model/vrml' },
  'vrt'     => { 'type' => 'bin', 'mime' => 'x-world/x-vrt' },

  'wav'     => { 'type' => 'bin', 'mime' => 'audio/x-wav' },
  'wax'     => { 'type' => 'bin', 'mime' => 'audio/x-ms-wax' },
  'wbmp'    => { 'type' => 'bin', 'mime' => 'image/vnd.wap.wbmp' },
  'wbxml'   => { 'type' => 'bin', 'mime' => 'application/vnd.wap.wbxml' },
  'wfp'     => { 'type' => 'bin', 'mime' => 'application/wfphelpap' },
  'wi'      => { 'type' => 'bin', 'mime' => 'image/wavelet' },
  'wk1'     => { 'type' => 'bin', 'mime' => 'application/vnd.lotus-1-2-3' },
  'wk3'     => { 'type' => 'bin', 'mime' => 'application/vnd.lotus-1-2-3' },
  'wk4'     => { 'type' => 'bin', 'mime' => 'application/vnd.lotus-1-2-3' },
  'wm'      => { 'type' => 'bin', 'mime' => 'video/x-ms-wm' },
  'wma'     => { 'type' => 'bin', 'mime' => 'audio/x-ms-wma' },
  'wmd'     => { 'type' => 'bin', 'mime' => 'video/x-ms-wmd' },
  'wmf'     => { 'type' => 'bin', 'mime' => 'application/x-msmetafile' },
  'wml'     => { 'type' => 'txt', 'mime' => 'text/vnd.wap.wml;charset=Shift_JIS' },
  'wmlc'    => { 'type' => 'bin', 'mime' => 'application/vnd.wap.wmlc' },
  'wmls'    => { 'type' => 'txt', 'mime' => 'text/vnd.wap.wmlscript' },
  'wmlsc'   => { 'type' => 'bin', 'mime' => 'application/vnd.wap.wmlscriptc' },
  'wmv'     => { 'type' => 'bin', 'mime' => 'video/x-ms-wmv' },
  'wmx'     => { 'type' => 'bin', 'mime' => 'video/x-ms-wmx' },
  'wmz'     => { 'type' => 'bin', 'mime' => 'video/x-ms-wmz' },
  'wri'     => { 'type' => 'bin', 'mime' => 'application/x-mswrite' },
  'wrl'     => { 'type' => 'bin', 'mime' => 'model/vrml' },
  'ws2'     => { 'type' => 'bin', 'mime' => 'application/x-WebSync2-Plugin' },
  'wse'     => { 'type' => 'bin', 'mime' => 'application/x-WebSync-plugin' },
  'wss'     => { 'type' => 'bin', 'mime' => 'application/x-WebSync-plugin' },
  'wv'      => { 'type' => 'bin', 'mime' => 'video/wavelet' },
  'wvh'     => { 'type' => 'bin', 'mime' => 'video/x-webview-h' },
  'wvp'     => { 'type' => 'bin', 'mime' => 'video/x-webview-p' },
  'wvx'     => { 'type' => 'bin', 'mime' => 'video/x-ms-wvx' },

  'xbd'     => { 'type' => 'bin', 'mime' => 'application/vnd.fujixerox.docuworks.binder' },
  'xbm'     => { 'type' => 'bin', 'mime' => 'image/x-xbitmap' },
  'xdm'     => { 'type' => 'bin', 'mime' => 'application/x-xdma' },
  'xdw'     => { 'type' => 'bin', 'mime' => 'application/vnd.fujixerox.docuworks' },
  'xhm'     => { 'type' => 'bin', 'mime' => 'application/xhtml+xml' },
  'xht'     => { 'type' => 'bin', 'mime' => 'application/xhtml+xml' },
  'xhtm'    => { 'type' => 'bin', 'mime' => 'application/xhtml+xml' },
  'xhtml'   => { 'type' => 'bin', 'mime' => 'application/xhtml+xml' },
  'xla'     => { 'type' => 'bin', 'mime' => 'application/vnd.ms-excel' },
  'xlc'     => { 'type' => 'bin', 'mime' => 'application/vnd.ms-excel' },
  'xll'     => { 'type' => 'bin', 'mime' => 'application/x-excel' },
  'xlm'     => { 'type' => 'bin', 'mime' => 'application/vnd.ms-excel' },
  'xls'     => { 'type' => 'bin', 'mime' => 'application/vnd.ms-excel' },
  'xlt'     => { 'type' => 'bin', 'mime' => 'application/vnd.ms-excel' },
  'xlw'     => { 'type' => 'bin', 'mime' => 'application/vnd.ms-excel' },
  'xml'     => { 'type' => 'txt', 'mime' => 'text/xml' },
  'xpm'     => { 'type' => 'bin', 'mime' => 'image/x-xpixmap' },
  'xsl'     => { 'type' => 'txt', 'mime' => 'text/xml' },
  'xwd'     => { 'type' => 'bin', 'mime' => 'image/x-xwindowdump' },
  'xyz'     => { 'type' => 'bin', 'mime' => 'chemical/x-xyz' },

  'z'       => { 'type' => 'bin', 'mime' => 'application/octet-stream' },
  'zac'     => { 'type' => 'bin', 'mime' => 'application/x-zaurus-zac' },
  'zip'     => { 'type' => 'bin', 'mime' => 'application/zip' },

  '.'       => { 'type' => 'bin', 'mime' => 'application/octet-stream' }, # Unknown
);

########################################
# Program                              #
########################################

&Main();

sub Main()
{
  my $query = exists( $ENV{ 'QUERY_STRING' } ) ? $ENV{ 'QUERY_STRING' } : '';

  my %GET = &DecodeGet( $query );

  if ( $GET{ 'p' } =~ /(\.\.)/ || $GET{ 'p' } =~ /^(\/)/){ $GET{ 'p' } = ''; }
  my $path = $STEELBLUESETTING::DOCROOT . '/' . $GET{ 'p' };

  my $name = $GET{ 'n' };
  if ( $name eq '' )
  {
    my ( @el ) = split( /\//, $path );
    $name = pop( @el );
    if ( $name eq '' ){ $name = 'notitle'; }
  }

  my $ext = '.';
  if ( -f $path && $name =~ /\.([^ \.]+)$/ )
  {
    $ext = $1;
  }
  $ext =~ tr/A-Z/a-z/;

  unless ( exists( $MIMETYPE{ $ext } ) ){ $ext = '.'; }

  return &OutputFile( $path, $name, $ext, $GET{ 'enc' }, $GET{ 'dec' } );
}

sub OutputFile()
{
  my ( $file, $name, $ext, $enc, $dec ) = ( @_ );

  my $size = 0;
  if ( open( FILE, $file ) )
  {
    my @state = stat( $file );
    $size = $state[ 7 ];
  }

  # HTTP Header.
  printf( 'Content-Length: %d%s', $size, "\n" );
  printf( 'Content-Type: %s%s', $MIMETYPE{ $ext }->{ 'mime' }, "\n" );
  if ( $size > 0 && $STEELBLUESETTING::DOWNLOAD )
  {
    printf( 'Content-Disposition: attachment; filename="%s"%s', $name, "\n" );
  }
  print "\n";

  if ( $size > 0 )
  {
    if ( $MIMETYPE{ $ext }->{ 'type' } eq 'txt' && $enc ne '' )
    {
      if ( $dec eq '' )
      {
        while ( <FILE> )
        {
          print &Encode::encode( $enc, $_ );
        }
      } else
      {
        while ( <FILE> )
        {
          &Encode::from_to( $_, $dec, $enc );
          print $_;
        }
      }
      close( FILE );
    } else
    {
      binmode( STDOUT );
      binmode( FILE );
      while ( <FILE> ){ print $_; }
      close( FILE );
    }
  }

}

sub DecodeGet()
{
  my ( $query ) = ( @_, '' );
  my %ret;
  $ret{ 'p' } = '';
  $ret{ 'n' } = '';
  $ret{ 'enc' } = '';
  $ret{ 'dec' } = '';

  my @args = split( /&/, $query );
  foreach ( @args )
  {
    my ( $name, $val ) = split( /=/, $_, 2 );
    $val =~ tr/+/ /;
    $val =~ s/%([0-9a-fA-F][0-9a-fA-F])/pack('C', hex($1))/eg;
    $ret{ $name } = $val;
  }

  return %ret;
}
