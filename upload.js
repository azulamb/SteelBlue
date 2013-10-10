function DragOver( event )
{
  event.preventDefault();
}

function Drop( event )
{
  var files = event.dataTransfer.files;

  var darea = document.getElementById( 'dragupload' );
  darea.addEventListener( 'dragover', null, false );
  darea.addEventListener( "drop", null, false );

  var path = document.getElementById( 'path' ).value;

  document.getElementById( 'dragupload' ).innerHTML = '<div id="loader"></div>';

  UPLOADED = 0;
  UPLOADMAX = files.length;

  var i;
  for ( i = 0 ; i < UPLOADMAX ; ++i )
  {
    UploadFile( "./uploader.cgi", path, files[ i ] );
  }
  event.preventDefault();
}

function HttpCreate()
{
  var httpobj = null;

  if ( window.navigator.userAgent.toLowerCase().indexOf( "chrome" ) > -1)
  {
    XMLHttpRequest.prototype.sendAsBinary = function( datastr )
      {
        function byteValue( x ) { return x.charCodeAt( 0 ) & 0xff; }
        var ords = Array.prototype.map.call( datastr, byteValue );
        var ui8a = new Uint8Array( ords );
        try
        {
          this.send( ui8a );
        } catch( error )
        {
          this.send( ui8a.buffer );
        }
      }
  }

  try
  {
    httpobj = new XMLHttpRequest();
  } catch( e )
  {
    httpobj = null;
  }

  return httpobj;
}

function UploadFile( address, path, file )
{

  var reader = new FileReader();
  reader.onload = function( event )
  {
    httpobj = HttpCreate();
    if ( httpobj )
    {
      var data = "";

      httpobj.open( "post", address, false );

      // TODO:
      var boundary = "----SDDUploaderFormBoundaryGhexpz6PUOeIP3Sc";

      // Multipart header.
      MultipartHeader( httpobj, boundary );

      // File data.
      data += MultipartFile( reader, 'upfile', file, boundary );

      // Path data.
      data += MultipartData( 'path', path, boundary );

      // Multipart footer.
      data += MultipartFooter( boundary )

      // Send data.
      httpobj.sendAsBinary( data );

      // Result.
      var result = JSON.parse( httpobj.responseText );

      ++UPLOADED;

      // Update progress bar.
      var loader = document.getElementById( 'loader' );

      var failid = '';
      if ( result.result !=  'success' ){ failid = ' class="error"' }

      loader.innerHTML += '<div style="width:' + ( 100 / UPLOADMAX ) + '%;"' + failid + '></div>';

      if ( UPLOADMAX <= UPLOADED ){ window.location.reload(); }
    }

    return 0;
  }
  reader.readAsBinaryString( file );

  return null;
}

function MultipartHeader( httpobj, boundary )
{
  httpobj.setRequestHeader( "content-type", "multipart/form-data; boundary=" + boundary );
}

function MultipartFooter( boundary )
{
  return "--" + boundary + "--";
}

function MultipartData( name, data, boundary )
{
  var str = "--" + boundary + "\r\n";

  str += "Content-Disposition: form-data; name=\"" + name + "\"\r\n";
  str += "\r\n";
  str += data + "\r\n";

  return str;
}

function MultipartFile( reader, name, file, boundary )
{
  var str = "--" + boundary + "\r\n";

  str += "Content-Disposition: form-data; name=\"" + name + "\"; filename=\"" + encodeURIComponent( file.name ) + "\"\r\n";
  str += "Content-Type: "+ file.type + "\r\n";
  str += "\r\n";
  str += reader.result + "\r\n";

  return str;
}

function Init()
{
  var darea = document.getElementById( 'dragupload' );

  if( darea.addEventListener )
  {
    darea.addEventListener( 'dragover', DragOver, false );
    darea.addEventListener( "drop", Drop, false );
  } else if( darea.attachEvent )
  {
    darea.attachEvent( "ondragover", function(event){DragOver(event);} );
    darea.attachEvent( "ondrop", Drop );
  }
}
