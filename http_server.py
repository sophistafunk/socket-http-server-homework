import logging
import mimetypes
import os
import socket
import sys
import traceback


FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)
logger = logging.getLogger(__name__)


def response_ok(body=b'This is a minimal response', mimetype=b'text/plain'):
    """Returns a basic HTTP response"""
    logging.info('Sending response to client')
    return b'\r\n'.join([
        b'HTTP/1.1 200 OK',
        b'Content-Type: ' + mimetype,
        b'',
        body,
    ])


def response_method_not_allowed():
    """Returns a 405 Method Not Allowed response"""
    logging.info('Invalid method call')
    return b'\r\n'.join([
        b'HTTP/1.1 405 Method Not Allowed',
        b'',
        b'You can not do that on this server!',
    ])


def response_not_found():
    """Returns a 404 Not Found response"""
    logging.info('Content not found')
    return b'\r\n'.join([
            b'HTTP/1.1 404 Not Found',
            b'',
            b'Content not found!',
        ])


def parse_request(request):
    """
    Given the content of an HTTP request, returns the path of that request.

    This server only handles GET requests, so this method shall raise a
    NotImplementedError if the method of the request is not GET.
    """

    method, path, version = request.split('\r\n')[0].split(' ')
    logging.info(f'parsing request: {method}, {path}, {version}')
    
    if method != 'GET':
        logging.info(f'method requested: {method}')
        raise NotImplementedError

    return path

def response_path(path):
    """
    This method should return appropriate content and a mime type.

    If the requested path is a directory, then the content should be a
    plain-text listing of the contents with mimetype `text/plain`.

    If the path is a file, it should return the contents of that file
    and its correct mimetype.

    If the path does not map to a real location, it should raise an
    exception that the server can catch to return a 404 response.

    Ex:
        response_path('/a_web_page.html') -> (b"<html><h1>North Carolina...",
                                            b"text/html")

        response_path('/images/sample_1.png')
                        -> (b"A12BCF...",  # contents of sample_1.png
                            b"image/png")

        response_path('/') -> (b"images/, a_web_page.html, make_type.py,...",
                             b"text/plain")

        response_path('/a_page_that_doesnt_exist.html') -> Raises a NameError

    """

    # TODO: Raise a NameError if the requested content is not present
    # under webroot.

    local_path = os.path.join(os.getcwd(),'webroot', path)
    logging.info(local_path)
    place_holder = local_path
    if path not in place_holder:
        raise NameError
    else:
        with open(place_holder, 'wb') as content:
            content.write()
            while content != '':
                content.write()
            mime_type = mimetypes.guess_type(path)[0]

    # TODO: Fill in the appropriate content and mime_type given the path.
    # See the assignment guidelines for help on "mapping mime-types", though
    # you might need to create a special case for handling make_time.py
    #
    # If the path is "make_time.py", then you may OPTIONALLY return the
    # result of executing `make_time.py`. But you need only return the
    # CONTENTS of `make_time.py`.
    
    #content = b"not implemented"
    #mime_type = b"not implemented"

    return content, mime_type


def server(log_buffer=sys.stderr):
    address = ('127.0.0.1', 10000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    logging.info(f'making a server on {address[0]}:{address[1]} {log_buffer}')
    sock.bind(address)
    sock.listen(1)

    try:
        while True:
            logging.info('waiting for a connection')
            conn, addr = sock.accept()  # blocking
            try:
                logging.info(f'connection - {addr[0]}:{addr[1]}')
                request = ''
                while True:
                    data = conn.recv(1024)
                    request += data.decode('utf8')
                    if '\r\n\r\n' in request:
                        break
                logging.info(f'Request received:\n{request}\n\n')

                try:
                    path = parse_request(request)

                    # TODO: Use response_path to retrieve the content and the mimetype,
                    # based on the request path.

                    content, mimetype = response_path(path)

                    # TODO:
                    # If response_path raised
                    # a NameError, then let response be a not_found response. Else,
                    # use the content and mimetype from response_path to build a 
                    # response_ok.
                    response = response_ok(
                        body=content,
                        mimetype=mimetype
                    )
                except NotImplementedError:
                    response = response_method_not_allowed()

                conn.sendall(response)
            except:
                traceback.print_exc()
            finally:
                conn.close() 

    except KeyboardInterrupt:
        sock.close()
        return
    except:
        traceback.print_exc()


if __name__ == '__main__':
    server()
    sys.exit(0)


