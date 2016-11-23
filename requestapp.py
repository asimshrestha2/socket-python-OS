class Requestapp:
    resstate = {
        200 : "HTTP/1.1 200 OK",
        400 : "HTTP/1.1 400 Bad Request",
        404 : "HTTP/1.1 404 Not Found"
    }

    def __init__(self, path, body, status=200):
        self.status = status
        self.header = {}
        self.body = body
        self.response = """\
%s

%s"""
        if path != "":
            self.__findContentType(path)
        else:
            print "No Path Given."

    def __findContentType(self, path):
        pathsplit = path.split('.')
        fileType = pathsplit[len(pathsplit)-1]
        if(fileType == "png" or fileType == "jpg"):
            self.__contentType("image/" + fileType)
        elif(fileType == "html" or fileType == "css"):
            self.__contentType("text/" + fileType)
        elif(fileType == "js"):
            self.__contentType("text/javascript")
        else:
            self.__contentType("text/plain")

    def __contentType(self, type):
        self.header["Content-Type"] = type
        print self.header

    def getResponse(self):
        status = Requestapp.resstate[self.status]

        hres = status + "\r\n"

        for k, v in self.header.items():
            hres = hres + k + ": " + v + "\r\n"

        self.response = self.response % (hres, self.body)
        print self.response
        return self.response
