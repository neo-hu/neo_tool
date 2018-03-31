
# python常用又记不住的方法

## 快速生成大文件

    from tempfile import mkstemp
    from neo_tool.n_file import fallocate
    f = fallocate.Fallocate()
    fd, tmp_file = mkstemp()
    size = 1024
    f(fd, 0, 0, size)
    
## 高效的零拷贝
  
    from neo_tool.n_file import splice
    s = splice.Splice()
    r, w = os.pipe()
    with open("/tmp/_splice.txt", "rb") as f:
        bytes_in_pipe, _1, _2 = s(f, None, w, None, 51, 0)
        with open("/tmp/_splice_w.txt", "wb") as wf:
            print(s(r, None, wf, None, 1024, 0))
            
    s = splice.Tee()

## md5 socket
    from neo_tool.net.md5_socket import get_md5_socket
    s = get_md5_socket()
    os.write(s, "11111111211111111111")
    hex_checksum = ''.join("%02x" % ord(c) for c in os.read(s, 16))
    print(hex_checksum)
