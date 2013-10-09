function DragOver( event )
{
  event.preventDefault();
}

function Drop( event )
{
  var files = event.dataTransfer.files;

  var path = document.getElementById( 'path' ).value;

  document.getElementById( 'dragupload' ).innerHTML = '<div id="loader"></div>';//<div id="progress"></div>

  UPLOADED = 0;
  UPLOADMAX = files.length;
  //LOADERLENGTH = document.getElementById( 'loader' ).clientWidth;

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
    /*try
    {
      httpObject = new ActiveXObject( "Msxml2.XMLHTTP" );
    } catch( e )
    {
      try
      {
        httpObject = new ActiveXObject( "Microsoft.XMLHTTP" );
      } catch( e )
      {
        return null;
      }
    }*/
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

      // File data.

      var boundary = "----SDDUploaderFormBoundaryGhexpz6PUOeIP3Sc";

      httpobj.setRequestHeader( "content-type", "multipart/form-data; boundary=" + boundary );

      data += "--" + boundary + "\r\n";

      data += "Content-Disposition: form-data; name=\"upfile\"; filename=\"" + encodeURIComponent( file.name ) + "\"\r\n";

      data += "Content-Type: "+ file.type + "\r\n";
      data += "\r\n";


      data += reader.result + "\r\n";

      data += "--" + boundary + "\r\n";

      // Path data.

      data += "Content-Disposition: form-data; name=\"path\"\r\n";
      data += "\r\n";

      data += encodeURIComponent( path ) + "\r\n";

      data += "--" + boundary + "--";

      httpobj.sendAsBinary( data );

      // Result.
      var result = JSON.parse( httpobj.responseText );

      var loader = document.getElementById( 'loader' );

      ++UPLOADED;

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

function Init()
{
  var darea = document.getElementById( 'dragupload' );

  if( darea.addEventListener )
  {
    darea.addEventListener( 'dragover', DragOver, false );
    darea.addEventListener( "drop", Drop, false );
    darea.addEventListener( 'ondragover', DragOver, false );
    darea.addEventListener( "ondrop", Drop, false );
  } else if( darea.attachEvent )
  {
    darea.attachEvent( "ondragover", function(event){DragOver(event);} );
    darea.attachEvent( "ondrop", Drop );
  }
}
