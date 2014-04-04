#!/usr/bin/perl

use strict;
use warnings;
no warnings qw(once);
use CGI;

########################################
# Setting                              #
########################################

require './setting.pl';

#our $DOCROOT = '.';
#our $DIRPARMISIION  = 0705;
#our $JSONCONTENTTYPE = 'Content-Type: application/json; charset=utf-8';

########################################
# Main program                         #
########################################

#print '[' . &NewPath( './test1/test3/', './../test2/../../../test4' ) . ']';

print &Main();

sub Main()
{
  my $query = new CGI;

# list
# ref
# permission, owner, group, user
# path
# mode

  my $ref = &Decode( $query->param( 'ref' ) );
  my @list = ( $query->param( 'list' ) );

  # Get mode.
  my $mode = &GetMode( $query->param( 'mode' ) );
  if ( $mode eq '' ){ return &Error( $ref, sprintf( 'No mode.' ) ); }

  # Path check.
  my $path = &Decode( $query->param( 'path' ) );
  if ( $path =~ /(\.\.)/ || $path =~ /^(\/)/ ){ return &Error( $ref, 'Path error.' ); }
  if ( $path eq '' )
  {
    $path = './';
  } elsif ( -f $path )
  {
    my ( @el ) = split( /\//, $path );
    unshift( @list, pop( @el ) );
    $path = join( '/', @el ) . '/';
  } elsif ( ! ($path =~ /(\/)$/) )
  {
    $path .= '/';
  }

  if ( $mode eq 'mkdir' )
  {
    # Make directory.

    # Prepare permission.
    my $permission = &GetPermissiion( $query->param( 'permission' ) || '', $query->param( 'owner' ), $query->param( 'group' ), $query->param( 'user' ) );

    #&RecMkdir( $path );

    return &OpMkdir( $ref, $path, $permission, $list[ 0 ] );
  } elsif ( $mode eq 'chmod' )
  {
    # Change mode.

    # Prepare permission.
    my $permission = &GetPermissiion( $query->param( 'permission' ) || '', $query->param( 'owner' ), $query->param( 'group' ), $query->param( 'user' ) );

    if ( scalar( @list ) <= 1 && $list[ 0 ] eq '' ) { $list[ 0 ] = '.'; }
    return &OpChmod( $ref, $path, $permission, @list );
  } elsif( $mode eq 'cp' )
  {
    # File copy.

    return &OpCp( $ref, $path, $list[ 0 ], $query->param( 'new' ) );
  } elsif ( $mode eq 'mv' )
  {
    # Move file.

    return &OpMv( $ref, $path, $query->param( 'new' ), @list );
  } elsif ( $mode eq 'rm' )
  {
    # Delete file.

    return &OpRm( $ref, $path, @list );
  }

  return &Error( $ref, sprintf( 'Cannnot parmit command( %s ).', $mode ) );
}

########################################
# Command                              #
########################################

sub OpChmod()
{
  my ( $ref, $path, $permission, @name ) = ( @_ );
  foreach ( @name )
  {
    my $name = &Decode( $_ );
    if ( $name =~ /\.\./ || $name eq '' ) { next; }
    my $file = $STEELBLUESETTING::DOCROOT . '/' . $path . $name;
    chmod( $permission, $file );
  }
  return &Success( $ref );
}

sub OpMkdir()
{
  my ( $ref, $path, $permission, $name ) = ( @_ );

  $name = &Decode( $name );

  #if ( $name =~ /[^ 0-9a-zA-Z\_\-\(\)\[\]\{\}]/ ){ next; }
  if ( $name =~ /\.\./ ){ return &Error( $ref, 'Failure mkdir.' ); }
  my $dir = $STEELBLUESETTING::DOCROOT . '/' . $path . $name;
  if ( $name ne '' && !( -d $dir ) &&
       mkdir( $dir, $permission ) )
  {
    return &Success( $ref );
  }
  return &Error( $ref, 'Failure mkdir.' );
}

sub OpCp()
{
  my ( $ref, $path, $old, $new ) = ( @_ );

  $old = $STEELBLUESETTING::DOCROOT . '/' . $path . $old;

  unless ( -f $old ) { return &Error( $ref, 'File not found.' ); }

  $new = &NewPath( $path, &Decode( $new ) );
  $new =~ s/(\/)$//g;
  $new = $STEELBLUESETTING::DOCROOT . '/' . $new;

  if ( open( RFILE, "$old" ) && open( WFILE, "> $new" ) )
  {
    binmode( RFILE );
    binmode( WFILE );
    while ( <RFILE> ) { print WFILE $_; }
    close( WFILE );
    close( RFILE );
    return &Success( $ref );
  }

  return &Error( $ref, 'Cannot copy.' );
}

sub OpRm()
{
  my ( $ref, $path, @del ) = ( @_ );

  if ( -f $path )
  {
    unlink( $path );
    return &Success( $ref );
  }

  foreach ( @del )
  {
    my $name = &Decode( $_ );
    #if ( $name =~ /[^ 0-9a-zA-Z\_\-\(\)\[\]\{\}]/ ){ next; }
    if ( $name =~ /\.\./ ){ next; }
    my $file = $STEELBLUESETTING::DOCROOT . '/' . $path . $name;

    if ( -f $file )
    {
      unlink( $file );
    }
  }

  return &Success( $ref );
}

sub OpMv()
{
  my ( $ref, $path, $newpath, @list ) = ( @_ );

  $newpath = &NewPath( $path, &Decode( $newpath ) );
  if ( $newpath eq '' )
  {
    $newpath = './';
  } elsif ( $newpath =~ /^(\.\.)/ )
  {
    return &Error( $ref, 'Failure newpath.' );
  }

  foreach ( @list )
  {
    my $name = &Decode( $_ );
    if ( $name =~ /\.\./ ){ next; }
    my $oldfile = $STEELBLUESETTING::DOCROOT . '/' . $path . $name;
    my $newfile = $STEELBLUESETTING::DOCROOT . '/' . $newpath . $name;
    if ( -f $oldfile )
    {
      rename( $oldfile, $newfile );
    }
  }
  return &Success( $ref );
}

########################################
# Program                              #
########################################

sub GetMode()
{
  my ( @mode ) = ( @_ );
  my $mode = '';

  foreach ( @mode )
  {
    if ( $_ ne '' ) { $mode = $_; last; }
  }

  my $check = 1;
  foreach ( @STEELBLUESETTING::CMD )
  {
    if ( $_ eq $mode ){ $check = 0; last; }
  }

  if ( $check ){ $mode = ''; }

  return $mode;
}

sub GetPermissiion()
{
  my ( $p, $o, $g ,$u ) = ( @_, '', '', '' );

  my $check = 0;
  foreach ( @STEELBLUESETTING::CMD )
  {
    if ( $_ eq 'chmod' ){ $check = 1; }
  }
  unless ( $check ){ return -1; }

  my $permission = &Permission( $p );
  if ( $permission < 0 )
  {
    $permission = &Permission( $o, $g, $u );
  } else
  {
    $permission = $STEELBLUESETTING::DIRPARMISIION;
  }

  return $permission;
}

sub RecMkdir()
{
  my ( $path ) = ( @_ );
  unless ( -d $STEELBLUESETTING::DOCROOT . '/' . $path )
  {
    my ( @el ) = split( /\//, $path );

    # Make directory.
    $path = shift( @el ) . '/';
    foreach ( @el )
    {
      unless ( -d $STEELBLUESETTING::DOCROOT . '/' . $path . $_ ){ mkdir( $STEELBLUESETTING::DOCROOT . '/' . $path . $_, $STEELBLUESETTING::DIRPARMISIION ); }
      $path .= $_ . '/';
    }
  }
}

sub Permission()
{
  my ( $owner, $group, $user ) = ( @_, -1, -1 );

  if ( $owner =~ /([rwx\-][rwx\-][rwx\-])([rwx\-][rwx\-][rwx\-])([rwx\-][rwx\-][rwx\-])/ )
  {
    return oct( sprintf( '0%d%d%d', &Permission_( $1 ), &Permission_( $2 ), &Permission_( $3 ) ) );
  }

  if ( 0<= $owner && $owner <= 7 &&
       0<= $group && $group <= 7 &&
       0<= $user  && $user <= 7 )
  {
    return oct( sprintf( '0%d%d%d', $owner, $group, $user ) );
  }

  if ( $owner =~ /([\d]{0,1}[0-7]{3})/ ){ return oct( sprintf( '%04d', $1 ) ); }

  return -1;
}

sub Permission_()
{
  my ( $o, $g, $u ) = split( //, $_[ 0 ] );
  return sprintf( '%d', &PermissionCharactor2Number( $o ) + &PermissionCharactor2Number( $g ) + &PermissionCharactor2Number( $u ) );
}

sub PermissionCharactor2Number()
{
  my ( $p ) = ( @_ );
  if ( $p eq 'r' ){ return 4; }
  if ( $p eq 'w' ){ return 2; }
  if ( $p eq 'x' ){ return 1; }
  return 0;
}

sub NewPath()
{
  my ( $now, $add ) = ( @_ );
  $now =~ s/^(\.\/)//;
  $add =~ s/^(\.\/)//;
  my $path = $now . '/' . $add . '/';
  $path =~ s/\/+/\//g;
  while ( $path =~ s/[^ \/]+\/\.\.\/// ){}

  return $path;
}

########################################
# IO                                   #
########################################

sub Location()
{
  return sprintf( 'Location:%s', $_[ 0 ] ) . "\n\n";
}

sub JsonOut()
{
  my ( $result, $msg ) = ( @_ );
  return sprintf( '%s{"result":"%s","msg":"%s"}', $STEELBLUESETTING::JSONCONTENTTYPE . "\n\n", $result, $msg );
}

sub Success()
{
  my ( $ref ) = ( @_ );
  if ( $ref ) { return &Location( $ref ); }
  return &JsonOut( 'success', '' );
}

sub Error()
{
  my ( $ref, $msg ) = ( @_ );
if(open(FILE,">error.txt")){print FILE "$msg";close(FILE);}
  if ( $ref ) { return &Location( $ref ); }
  return &JsonOut( 'failure', $msg );
}

sub Decode()
{
  my ( $val ) = ( @_, "" );
  $val =~ tr/+/ /;
  $val =~ s/%([0-9a-fA-F][0-9a-fA-F])/pack('C', hex($1))/eg;
  return $val;
}
