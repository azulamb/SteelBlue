#!/usr/bin/perl

use strict;
use warnings;

use FileViewer;

########################################
# Setting                              #
########################################

require './setting.pl';

#our $DOCROOT = '.';
#our $TITLE = 'SteelBlue';
#our $SCRIPT = './index.cgi';
#our $BASEURL = '';
#our $PAGENUM = 50;
#our @EXTTXT = qw ( c cgi cpp css h hdml hpp htm html js pl pm py sh text txt );
#our @EXTIMG = qw ( gif jpeg jpg ping png );
#our $DOWNLOADER = './downloader.cgi';

########################################
# Program                              #
########################################

# GET data.
our %GET  = &Get( 'path', 'page' );

print "Content-type:text/html\n\n";

print &Main();

########################################
# HTML out                             #
########################################

sub Main()
{
  my $path = $GET{ 'path' };
  my $page = $GET{ 'page' };

  # Path check.
  if ( $path =~ /(\.\.)/ || $path =~ /^(\/)/){ $path = ''; }

  # Page check.
  if ( $page eq '' || $page =~ /[^ 0-9]/ ){ $page = 0; }

  # HTML out.

  my $html = '';

  $html .= &HtmlHead();

  $html .= &HtmlToolbar( $path );

  $html .= &HtmlUploader( $path );

  $html .= '<div class="maincontent">';
  if ( -f $STEELBLUESETTING::DOCROOT . '/' . $path )
  {
    # File view
    $html .= &HtmlFileView( $path );
  } else
  {
    # Directory view.
    $html .= &HtmlDirectory( $path, $page );
  }
  $html .= '</div>';

  $html .= &HtmlFoot();

  return $html;
}

sub HtmlHead()
{
  return sprintf( '<!DOCTYPE html>
<html lang="ja">
 <head>
 <meta charset="utf-8">
  <title>%s</title>
  <meta name="author" content="Hiroki" />
  <link rel="icon" href="data:image/vnd.microsoft.icon;base64,AAABAAEAEBAAAAEAIABoBAAAFgAAACgAAAAQAAAAIAAAAAEAIAAAAAAAQAQAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAACxhUMXsYlODQAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAALSDRCm0gke8tIJG/7SCRu+0gkbhs4JGpbOCR2yzhEIbAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAC1gUeQs4JG6bWBR10AAAAAAAAAAAAAAACzgE0Ks4NI
QLWARTC2gEkOAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAs4JGrLWDRnEAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAa2g0ZCtIJHjrSCRta0hEY6AAAAAAAAAAAAAAAAAAAAALWCR1q2g0ZCAAAAAAAAAACz
gEQetIJGZrSCRrC0gkbztIJG/7SCRv+0gkb/tIFHSwAAAAEAAAAAAAAAAAAAAAAAAAAJtYNGcQAA
AACygkU/tIJG/7SCRv+0gkb/tIJG/7SCRv+0gkb/tIJH67SCR3C3g0gnAAAAAAAAAAAAAAAAAAAA
ALOARiizgE0Ks4FGirSCRv+0gkb/tIJG/7SCRv+0gkb/tIJG/7SCRsS0gUaYtYFHXaqAQAwAAAAA
AAAAAAAAAAAAAAAAs4BGKLSCRtS0gkb/tIJG/7SCRv+0gkb/tIJG/7SCRv+0g0actIJFv7SCRZOq
gEAMsYBFGgAAAAAAAAAAAAAAALWEQh+0gkb/tIJG/7SCRv+0gkb/tYJG4rSDRpq1gkVgtYJFYLSC
Ru20gUbJAAAAALSCRz0AAAADAAAAAAAAAACzgkdotIJG/7SCRv+0gkbks4FGTbOCRXa0gkW/tIJG
+rSCRv+0gkb/tIJG4wAAAACvgEAQs4JHbAAAAAAAAAAAtYNGqLSCRv+0gkb/tINGoLSCRqe0g0ac
tIJFrbSCRv+0gkb/tIJG/7WCRsAAAAAAAAAAB7SCRqsAAAAAAAAAALSBRVW0gkb9tYJGubSCRjMA
AAAEAAAAAK6GQxO0gkXgtYNFnrOERDwAAAAAAAAAALSCRVyzgkalAAAAAAAAAAAAAAABsIRGHQAA
AAAAAAAAAAAAAAAAAAAAAAAAu4hED7GARyS1gkY3tIRGOrSCRYG0gkbas4JHLwAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAbOCRy+0gEYsAAAABgAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAA//8AAM//AAAA/wAAHD8AAD8PAAAwDwAAoAcAAIADAADAAQAAwAUAAMAEAADABgAAwwwAAO+A
AAD/8wAA//8AAA==" />
  <link rel="stylesheet" href="./style.css">
  <script src="./upload.js"></script>
  <script>
    document.addEventListener( "DOMContentLoaded", function (){ Init(); }, false);
  </script>
 </head>
<body>
  <header><a href="%s" class="icon"><div class="icon"></div></a><h1><a href="%s">%s</a></h1></header>
',
  $STEELBLUESETTING::TITLE,
  $STEELBLUESETTING::SCRIPT,
  $STEELBLUESETTING::SCRIPT, $STEELBLUESETTING::TITLE );
}

sub HtmlToolbar()
{
  my ( $path ) = ( @_ );
  my $html = '';

  $html .= '  <div class="toolbar">' . "\n";
  $html .= '    <table><tr>' . "\n";
  $html .= sprintf( '      <td class="back"><a href="%s?path=%s"><div id="backbutton"></div></a></td>', $STEELBLUESETTING::SCRIPT, &URLEncode( &UpDirectory( $path ) ) ) . "\n";
  $html .= sprintf( '      <td class="address">%s%s</td>', $STEELBLUESETTING::BASEURL, $path ) . "\n";
  $html .= '    </tr></table>' . "\n";
  $html .= '  </div>' . "\n";

  return $html;
}

sub HtmlFoot()
{
  return sprintf( '
  <footer><a href="https://github.com/HirokiMiyaoka/SteelBlue">SteelBlue</a> made by Hiroki @ (azulitenet/Hiroki_Miyaoka)</footer>
</body>
</html>' );
}

sub HtmlUploader()
{
  my ( $path ) = ( @_ );
  my $html = '';

  $html .= sprintf( '  <div class="uploader" id="dragupload">' ) . "\n";
  $html .= sprintf( '  <p>Select file or drag & drop files in this area.</p>' ) . "\n";
  $html .= sprintf( '    <form action="./uploader.cgi" method="post" enctype="multipart/form-data">' ) . "\n";
  $html .= sprintf( '      <table><tr><td>' ) . "\n";
  $html .= sprintf( '      <input type="file" name="upfile" class="upfile" />' ) . "\n";
  $html .= sprintf( '      </td><td>' ) . "\n";
  $html .= sprintf( '      <input type="hidden" name="path" value="%s" id="path" />', &URLEncode( $path ) ) . "\n";
  $html .= sprintf( '      <input type="hidden" name="ref" value="%s" />', &URLEncode( $STEELBLUESETTING::SCRIPT . '?path=' . &URLEncode( $path ) ) ) . "\n";
  $html .= sprintf( '      <input type="submit" name="send" value="Uplaod" class="submit" />' ) . "\n";
  $html .= sprintf( '      </td></tr></table>' ) . "\n";
  $html .= sprintf( '    </form>' ) . "\n";
  $html .= sprintf( '  </div>' ) . "\n";

  return $html;
}

sub HtmlDirectory()
{
  my ( $path, $page ) = ( @_ );
  my ( $dnum, $fnum, @list ) = &LoadDirectory( $path, '', $page * $STEELBLUESETTING::PAGENUM, ($page + 1) * $STEELBLUESETTING::PAGENUM - 1 );
  my $num = $dnum + $fnum;
  my $pagehtml = &HtmlPage( $page, $num );
  unless ( $path eq '' || $path =~ /(\/)$/ ){ $path .= '/'; }

  my $html = '';

  $html .= '  <div class="filelist">' . "\n";
  $html .= $pagehtml;
  $html .= '    <table>' . "\n";

  $html .= '      <thead>' . "\n";
  $html .= sprintf( '        <tr><td class="checkbox" id="checkbox"><input type="checkbox"></td><td class="filename" id="filename">Name</td><td class="time" id="time">Update</td><td class="permission" id="permission">Permission</td><td class="dl" id="dl">DL</td></tr>%s', "\n" );
  $html .= '      </thead>' . "\n";

  $html .= '      <tfoot>' . "\n";
  $html .= sprintf( '        <tr><td colspan="5">Directory:%d, File:%d, Total:%d</td></tr>%s', $dnum, $fnum, $num, "\n" );
  $html .= '      </tfoot>' . "\n";

  $html .= '      <tbody>' . "\n";
  foreach ( @list )
  {
    my @state = stat( $STEELBLUESETTING::DOCROOT . '/' . $path . $_ );
    if ( $_ =~ /(\/)$/ )
    {
      # Directory.
      $html .= sprintf( '        <tr><td class="checkbox"><input type="checkbox"></td><td class="filename"><a href="%s?%s">%s</a></td><td class="time">-</td><td class="permission">%s</td><td class="dl">-</td></tr>%s',
                        $STEELBLUESETTING::SCRIPT, 'path=' . ( $_ eq '../' ? &UpDirectory( $path ) : &URLEncode( $path . $_ )), $_,
                        &Permission( $state[ 2 ] ),
                        "\n" );
    } else
    {
      # File.
      my $renewtime = &FormatTime( $state[ 9 ] );

      $html .= sprintf( '        <tr><td class="checkbox"><input type="checkbox"></td><td class="filename"><a href="%s?%s">%s</a></td><td class="time">%s</td><td class="permission">%s</td><td class="dl"><a href="%s?%s">DL</a></td></tr>%s',
                        $STEELBLUESETTING::SCRIPT, 'path=' . &URLEncode( $path . $_), $_,
                        $renewtime,
                        &Permission( $state[ 2 ] ),
                        $STEELBLUESETTING::DOWNLOADER, 'p=' . &URLEncode( $path . $_),
                        "\n" );
    }
  }
  $html .= '      </tbody>' . "\n";

  $html .= '    </table>' . "\n";
  $html .= $pagehtml;
  $html .= '  </div>' . "\n";

  return $html;
}

sub HtmlPage()
{
  my ( $now, $item ) = ( @_ );
  my $html = '';
  my $urlbase = sprintf( '%s?path=%s', $STEELBLUESETTING::SCRIPT, &URLEncode( $GET{ 'path' } ) );

  $html .= '    <div class="page">';

  if ( $now > 0 )
  {
    $html .= sprintf( '<a href="%s&page=%d">&lt;&lt;</a> ', $urlbase, $now - 1 );
  } else
  {
    $html .= '&lt;&lt; ';
  }

  my $i;
  for ( $i = 0 ; $i < $now ; ++$i )
  {
    $html .= sprintf( '<a href="%s&page=%d"></a> ', $urlbase, $i );
  }
  $html .= sprintf( '<b>%d</b>', $now );
  for ( ; $i * $STEELBLUESETTING::PAGENUM < $item ; ++$i )
  {
    $html .= sprintf( ' <a href="%s&page=%d"></a>', $urlbase, $i );
  }

  if ( $STEELBLUESETTING::PAGENUM * ($now + 1) < $item )
  {
    $html .= sprintf( ' <a href="%s&page=%d">&gt;&gt;</a>', $urlbase, $now + 1 );
  } else
  {
    $html .= ' &gt;&gt;';
  }

  $html .= '</div>';

  return $html . "\n";
}

sub HtmlFileView()
{
  my ( $path ) = ( @_ );

  my $html = '';

  my $fv = FileViewer->new( $STEELBLUESETTING::DOCROOT . '/' . $path );

  $fv->AddExtTxt( @STEELBLUESETTING::EXTTXT );
  $fv->AddExtImg( @STEELBLUESETTING::EXTIMG );

  $html .= '<div class="fileview" id="textfile">';
  $html .= '<h2>' . $path . '</h2>';

  my @state = stat( $STEELBLUESETTING::DOCROOT . '/' . $path );
  $html .= '<table class="fileinfo">' . "\n" . '<tr>' . "\n";
  $html .= sprintf( '<td class="dl"><a href="%s?%s"><div id="dlbutton"></div></a></td>', $STEELBLUESETTING::DOWNLOADER, '&p=' . &URLEncode( $path ) ) . "\n";
  $html .= sprintf( '<td>%dB</td>', $fv->GetFileSize() ) . "\n";
  $html .= sprintf( '<td>%s:%s</td>', &Getpwuid( $state[ 4 ] ), &Getgrgid( $state[ 5 ] ) ) . "\n";
  $html .= sprintf( '<td class="permission">%s</td>', &Permission( $state[ 2 ] ) ) . "\n";
  $html .= sprintf( '<td class="time">%s</td>', &FormatTime( $state[ 9 ] ) ) . "\n";
  $html .= '</tr>' . "\n" . '</table>' . "\n";

  $html .= '<div class="view">' . $fv->View() . '</div>';

  if ( $fv->IsText() )
  {
    $html .= sprintf( '<div class="line">Line : %d</div>', $fv->GetLine() );
  } else
  {
    $html .= sprintf( '<div class="line">Size : %d</div>', $fv->GetFileSize() );
  }

  $html .= '</div>';

  return $html;
}

########################################
# Subroutine                           #
########################################

sub Permission()
{
  my ( $permission ) = ( @_ );
  my ( $admin, $group, $user ) = split( //, substr((sprintf "%03o", $permission), -3) );
  return &Permission_( $admin ) . &Permission_( $group ) . &Permission_( $user );
}

sub Permission_()
{
  my ( $per ) = ( @_ );
  my $ret = '';
  if ( $per & 1 ){ $ret = "x"; } else { $ret = '-'; }
  if ( $per & 2 ){ $ret = $ret . "w"; } else { $ret = $ret . '-'; }
  if ( $per & 4 ){ $ret = $ret . "r"; } else { $ret = $ret . '-'; }
  return $ret;
}

sub LoadDirectory()
{
  my ( $dir_, $sort, $start, $end ) = ( @_, 0, 0 );

  $dir_ =~ s/(\/)$//;

  my $dir = $STEELBLUESETTING::DOCROOT;

  if ( $dir_ ne '' && $dir_ ne '.' )
  {
    $dir .= '/' . $dir_;
  } else
  {
    $dir_ = '';
  }

  unless ( $dir =~ /(\/)$/ ){ $dir .= '/'; }

  my @list;
  my @dirs;
  my @files;

  if ( opendir( DIR, $dir ) )
  {
    my @tmp = readdir( DIR );
    closedir( DIR );

    foreach ( @tmp )
    {
      if ( $_ ne '.' && $_ ne '..' )
      {
        if ( -d $dir . $_ )
        {
          push( @dirs, $_ . '/' );
        } else
        {
          push( @files, $_ );
        }
      }
    }
  }

  push( @list, sort{ $a cmp $b }( @dirs ) );
  if ( $dir_ ne '' ){ unshift( @list, '../' ); }
  my $dirsnum = scalar( @list );
  push( @list, sort{ $a cmp $b }( @files ) );
  my $filesnum = scalar( @files );

  if ( scalar( @list ) <= $start ){ return (); }

  if ( $end <= $start ){ $end = scalar( @list ) - 1; }

  if ( scalar( @list ) <= $end ){ $end = scalar( @list ) - 1; }

  return ( $dirsnum, $filesnum, @list[ $start .. $end ] );
}

sub FormatTime()
{
  my ( $time ) = ( @_ );
  my ($sec, $min, $hour, $day, $month, $year) = localtime( $time );
  return sprintf( '%d/%02d/%02d %02d:%02d:%02d', $year + 1900, $month + 1, $day, $hour, $min, $sec );
}

sub UpDirectory()
{
  my ( $dir ) = ( @_ );
  $dir =~ s/(\/)$//;
  my @tmp = split( /\//, $dir );
  pop( @tmp );
  return join( '/', @tmp );
}

sub Getpwuid()
{
  my ( $id ) = ( @_ );
  my $os = $^O;
  if ( $os =~ /MSWin/ || $os eq 'dos' ){ return '-'; }
  return getpwuid( $id );
}

sub Getgrgid()
{
  my ( $id ) = ( @_ );
  my $os = $^O;
  if ( $os =~ /MSWin/ || $os eq 'dos' ){ return '-'; }
  return getgrgid( $id );
}

########################################
# Decode & Encode                      #
########################################

sub URLEncode
{
  my( @encode ) = ( @_ );
  foreach ( @encode )
  {
    $_ =~ s/([^\w\=\& ])/'%'.unpack("H2", $1)/eg;
    $_ =~ tr/ /+/;
  }
  if ( scalar( @encode ) == 1 )
  {
    return $encode[0];
  } else
  {
    return @encode;
  }
}

sub Get
{
  my ( @names ) = ( @_ );

  my $query = exists ( $ENV{ 'QUERY_STRING' } ) ? $ENV{ 'QUERY_STRING' } : '';

  my %ret = &DecodeCommon( $query  );

  foreach ( @names )
  {
    unless ( exists ( $ret{ $_ } ) )
    {
      $ret{ $_ } = '';
    }
  }

  return %ret;
}

sub DecodeCommon( \$ )
{
  my @args = split( /&/, $_[0] );
  my %ret;
  foreach ( @args )
  {
    my ( $name, $val ) = split( /=/, $_, 2 );
    $val =~ tr/+/ /;
    $val =~ s/%([0-9a-fA-F][0-9a-fA-F])/pack('C', hex($1))/eg;
    unless ( exists ( $ret{ $name } ) )
    {
      $ret{ $name } = $val;
    } else
    {
      unless ( ref ( $ret{ $name } ) eq 'ARARY' )
      {
        my $tmp = $ret{ $name };
        delete ( $ret{ $name } );
        $ret{ $name }[ 0 ] = $tmp;
      }
      push ( @{ $ret{$name} }, $val );
    }
  }

  return %ret;
}

