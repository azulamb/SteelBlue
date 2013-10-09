package FileViewer;

########################################
# FileViewer module                    #
########################################

# TOTO:Markdown

sub new()
{
  my ( $package, $file ) = ( @_, '' );

  my $hash = {
    'file' => $file,
    'line' => -1,
    'txtext' => './ext_text.txt',
    'imgext' => './ext_img.txt',
    'type' => '',
  };

  return bless( $hash, $package );
}

sub AddExtTxt()
{
  my ( $self, @data ) = ( @_ );
  $self->AddExt_( 'exttxt', @data );
}

sub AddExtImg()
{
  my ( $self, @data ) = ( @_ );
  $self->AddExt_( 'extimg', @data );
}

sub AddExt_()
{
  my ( $self, $key, @data ) = ( @_ );
  foreach ( @data )
  {
    $self->{ $key }{ $_ } = '';
  }
}

sub View()
{
  my ( $self ) = ( @_ );

  my $html = '';

  if ( $self->IsText() )
  {
    # Text.
    $html .= $self->ViewText();

  } elsif ( $self->IsImage() )
  {
    # Image.
    $html .= $self->ViewImage();

  } else
  {
    # Binary.
  }

  return $html;
}

sub ViewText()
{
  my ( $self ) = ( @_ );

  my $html .= '<ol>' . "\n";
  if ( open( FILE, $self->{ 'file' } ) )
  {
    my @line = <FILE>;
    close( FILE );

    my $line;
    foreach( @line )
    {
      $html .= sprintf( '  <li><pre>%s</pre></li>', &FileViewer::Sanitize( $_ ) ) . "\n";
      ++$line;
    }
    $self->{ 'line' } = $line;

  } else
  {
    $html = sprintf( 'Cannot open [ %s ].', $self->{ 'file' } );
  }
  $html .= '</ol>' . "\n";

  return $html;
}

sub Sanitize()
{
  my ( $txt ) = ( @_ );

  $txt =~ s/\&/\&amp;/;
  $txt =~ s/\</\&lt;/g;
  $txt =~ s/\>/\&gt;/g;
  $txt =~ s/\r\n|\n|\r/\<br \/\>/g;

  return $txt;
}

sub ViewImage()
{
  my ( $self ) = ( @_ );

  my $html = sprintf( '<img src="%s" />', $self->{ 'file' } );

  return $html;
}

sub IsText()
{
  my ( $self ) = ( @_ );
  if ( $self->{ 'type' } ne '' ){ return ($self->{ 'type' } eq 'txt'); }
  if ( exists( $self->{ 'exttxt' } ) )
  {
    if ( exists( $self->{ 'exttxt' }{ $self->GetExtension() } ) )
    {
      $self->{ 'type' } = 'txt';
      return 1;
    }
  } elsif ( $self->_IsFileExtCheck( 'exttxt', $self->{ 'file' }, $self->{ 'txtext' } ) )
  {
    $self->{ 'type' } = 'txt';
    return 1;
  }
  return 0;
}

sub IsImage()
{
  my ( $self ) = ( @_ );
  if ( $self->{ 'type' } ne '' ){ return $self->{ 'type' } eq 'img'; }
  if ( exists( $self->{ 'extimg' } ) )
  {
    if ( exists( $self->{ 'extimg' }{ $self->GetExtension() } ) )
    {
      $self->{ 'type' } = 'txt';
      return 1;
    }
  } elsif ( $self->_IsFileExtCheck( 'extimg', $self->{ 'file' }, $self->{ 'imgext' } ) )
  {
    $self->{ 'type' } = 'img';
    return 1;
  }
  return 0;
}

sub _IsFileExtCheck()
{
  my ( $self, $key, $filepath, $file ) = ( @_ );
  my $ret = 0;
  if ( -f $filepath && open( FILE, $file ) )
  {
    my @list = <FILE>;
    close( FILE );

    my $ext = $self->GetExtension( $filepath );

    foreach ( @list )
    {
      my $ext_ = $_;
      chomp( $ext_ );
      $self->AddExt_( $key, $ext );
      if ( $ext_ eq $ext ){ $ret = 1; }
    }
  }
  return $ret;
}

sub GetExtension()
{
  my ( $self, $filepath ) = ( @_, '' );
  if ( $filepath eq '' ) { $filepath = $self->{ 'file' }; }
  $filepath =~ /\.([^ \.]+)$/;
  my $ext = $1;
  $ext =~ tr/A-Z/a-z/;
  return $ext;
}

sub GetFileSize()
{
  my ( $self ) = ( @_ );
  my @state = stat( $self->{ 'file' } );
  return $state[ 7 ];
}

sub GetLine(){ return ($_[ 0 ])->{ 'line' }; }

1;
