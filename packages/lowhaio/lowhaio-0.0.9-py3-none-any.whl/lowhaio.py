import asyncio
import ipaddress
import urllib.parse
import ssl
import socket

from aiodnsresolver import (
    TYPES,
    Resolver,
)


def streamed(data):
    async def _streamed():
        yield data
    return _streamed()


async def buffered(data):
    return b''.join([chunk async for chunk in data])


def Pool(resolver=Resolver, ssl_context=ssl.create_default_context, recv_bufsize=65536):

    loop = \
        asyncio.get_running_loop() if hasattr(asyncio, 'get_running_loop') else \
        asyncio.get_event_loop()
    ssl_context = ssl_context()
    resolve, _ = resolver()

    async def request(method, url, params=(), headers=(), body=streamed(b'')):
        parsed_url = urllib.parse.urlsplit(url)
        host, _, port_specified = parsed_url.netloc.partition(':')

        async def get_ip_address():
            try:
                return str(ipaddress.ip_address(host))
            except ValueError:
                return str((await resolve(host, TYPES.A))[0])
        ip_address = await get_ip_address()

        scheme = parsed_url.scheme
        port = \
            port_specified if port_specified != '' else \
            443 if scheme == 'https' else \
            80

        sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM,
                             proto=socket.IPPROTO_TCP)
        sock.setblocking(False)

        try:
            await loop.sock_connect(sock, (ip_address, port))
            if scheme == 'https':
                sock = ssl_context.wrap_socket(sock,
                                               server_hostname=host,
                                               do_handshake_on_connect=False)
                await complete_handshake(sock)

            outgoing_qs = urllib.parse.urlencode(params, doseq=True).encode()
            outgoing_path = urllib.parse.quote(parsed_url.path).encode()
            outgoing_path_qs = outgoing_path + \
                ((b'?' + outgoing_qs) if outgoing_qs != b'' else b'')
            outgoing_header = \
                method + b' ' + outgoing_path_qs + b' HTTP/1.1\r\n' + \
                b'host:' + host.encode('idna') + b'\r\n' + \
                b''.join(
                    key + b':' + value + b'\r\n'
                    for (key, value) in headers
                ) + \
                b'\r\n'
            await sendall(sock, outgoing_header)

            async for chunk in body:
                if chunk:
                    await sendall(sock, chunk)

            unprocessed = b''
            while True:
                incoming = await recv(sock)
                if not incoming:
                    raise Exception()
                unprocessed += incoming
                header_end = unprocessed.index(b'\r\n\r\n')
                if header_end != -1:
                    break
            header_bytes, unprocessed = unprocessed[:header_end], unprocessed[header_end + 4:]
            lines = header_bytes.split(b'\r\n')
            code = lines[0][9:12]
            response_headers = tuple(
                (key.strip().lower(), value.strip())
                for line in lines[1:]
                for (key, _, value) in (line.partition(b':'),)
            )
            response_headers_dict = dict(response_headers)
            content_length = int(response_headers_dict[b'content-length'])

        except BaseException:
            sock.close()
            raise

        async def response_body():
            total_received = 0
            total_remaining = content_length

            try:
                if unprocessed and total_remaining:
                    yield unprocessed
                    total_remaining -= len(unprocessed)

                while total_remaining:
                    chunk = await recv(sock)
                    total_received += len(chunk)
                    total_remaining -= len(chunk)
                    if total_remaining < 0:
                        raise Exception()
                    if not chunk:
                        break
                    yield chunk
            finally:
                sock.close()

        return code, response_headers, response_body()

    async def sendall(sock, data):
        try:
            latest_num_bytes = sock.send(data)
        except (BlockingIOError, ssl.SSLWantWriteError):
            latest_num_bytes = 0
        else:
            if latest_num_bytes == 0:
                raise IOError()

        if latest_num_bytes == len(data):
            return

        total_num_bytes = latest_num_bytes

        def writer():
            nonlocal total_num_bytes
            try:
                latest_num_bytes = sock.send(data_memoryview[total_num_bytes:])
            except (BlockingIOError, ssl.SSLWantWriteError):
                pass
            except BaseException as exception:
                if not result.cancelled():
                    result.set_exception(exception)
            else:
                total_num_bytes += latest_num_bytes
                if latest_num_bytes == 0 and not result.cancelled():
                    result.set_exception(IOError())
                elif total_num_bytes == len(data) and not result.cancelled():
                    result.set_result(None)

        result = asyncio.Future()
        fileno = sock.fileno()
        loop.add_writer(fileno, writer)
        data_memoryview = memoryview(data)

        try:
            return await result
        finally:
            loop.remove_writer(fileno)

    async def recv(sock):
        try:
            return sock.recv(recv_bufsize)
        except (BlockingIOError, ssl.SSLWantReadError):
            pass

        def reader():
            try:
                chunk = sock.recv(recv_bufsize)
            except (BlockingIOError, ssl.SSLWantReadError):
                pass
            except BaseException as exception:
                if not result.cancelled():
                    result.set_exception(exception)
            else:
                if not result.cancelled():
                    result.set_result(chunk)

        result = asyncio.Future()
        fileno = sock.fileno()
        loop.add_reader(fileno, reader)

        try:
            return await result
        finally:
            loop.remove_reader(fileno)

    async def complete_handshake(ssl_sock):
        try:
            return ssl_sock.do_handshake()
        except (ssl.SSLWantReadError, ssl.SSLWantWriteError):
            pass

        def handshake():
            try:
                ssl_sock.do_handshake()
            except (ssl.SSLWantReadError, ssl.SSLWantWriteError):
                pass
            except BaseException as exception:
                if not done.done():
                    done.set_exception(exception)
            else:
                if not done.done():
                    done.set_result(None)

        done = asyncio.Future()
        fileno = ssl_sock.fileno()
        loop.add_reader(fileno, handshake)
        loop.add_writer(fileno, handshake)

        try:
            return await done
        finally:
            loop.remove_reader(fileno)
            loop.remove_writer(fileno)

    async def close():
        pass

    return request, close
