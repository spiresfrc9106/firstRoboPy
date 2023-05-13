from http.server import SimpleHTTPRequestHandler
import socketserver
import socket
import threading
import functools

import wpilib

_dashboardWidgetList = []

indexTmpltTxt = ""
with open("webserver/www/index.html_tmplt", "r") as infile:
    indexTmpltTxt = infile.read()
    
htmlTmpltTxt = ""
with open("webserver/www/dashboard/dashboard.html_tmplt", "r") as infile:
    htmlTmpltTxt = infile.read()
    
jsTmpltTxt = ""
with open("webserver/www/dashboard/dashboard.js_tmplt", "r") as infile:
    jsTmpltTxt = infile.read()

class TemplatingRequestHandler(SimpleHTTPRequestHandler):

    # from https://gist.github.com/HaiyangXu/ec88cbdce3cdbac7b8d5
    extensions_map = {
        '': 'application/octet-stream',
        '.manifest': 'text/cache-manifest',
        '.html': 'text/html',
        '.png': 'image/png',
        '.jpg': 'image/jpg',
        '.svg':	'image/svg+xml',
        '.css':	'text/css',
        '.js':'application/x-javascript',
        '.wasm': 'application/wasm',
        '.json': 'application/json',
        '.xml': 'application/xml',
    }
    
    def do_GET(self):

        if self.path == "/index.html" or self.path == "/":
            
            if(wpilib.RobotBase.isSimulation()):
                deployText = "Simulation \n"
            else:
                deployText = str(wpilib.deployinfo.getDeployData()) + "\n"
                deployText += f"RIO FPGA Sw: v{wpilib.RobotController.getFPGAVersion()} r{wpilib.RobotController.getFPGARevision()} \n"
                deployText += f"RIO Serial Number:{wpilib.RobotController.getSerialNumber()} \n"
                deployText += f"{wpilib.RobotController.getComments()} \n"


            filledOut = indexTmpltTxt.replace("${BUILD_INFO}", deployText)
                     
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()                

            self.wfile.write(filledOut.encode())

            return SimpleHTTPRequestHandler

        elif self.path == "/dashboard/dashboard.html":

            filledOut = ""

            htmlText = ""
            for widget in _dashboardWidgetList:
                htmlText += widget.getHTML()
                htmlText += "\n"
                
            filledOut = htmlTmpltTxt.replace("${WIDGETS_HTML}", htmlText)
                     
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()                

            self.wfile.write(filledOut.encode())

            return SimpleHTTPRequestHandler
        
        elif self.path == "/dashboard/dashboard.js":

            jsInstantiate = ""
            jsUpdate = ""
            jsCallback = ""
            jsSetData = ""
            jsSetNoData = ""
            subscribeLine = "nt4Client.subscribePeriodic(["

            for w in _dashboardWidgetList:
                jsInstantiate += w.getJSDeclaration()
                jsInstantiate += "\n"

                jsUpdate += w.getJSUpdate()
                jsUpdate += "\n"

                jsSetData += w.getJSSetData()
                jsSetData += "\n"

                jsSetNoData += w.getJSSetNoData()
                jsSetNoData += "\n"

                jsCallback += w.getJSCallback()
                jsCallback += "\n"

                subscribeLine +=  w.getTopicSubscriptionStrings()

            # Remove the trailing comma and close out the line
            subscribeLine = subscribeLine[:-1]
            subscribeLine += "], 0.05);" # 50ms sample rate
            subscribeLine += "\n"

            filledOut = jsTmpltTxt
            filledOut = filledOut.replace("${WIDGETS_INSTANTIATE}", jsInstantiate)
            filledOut = filledOut.replace("${WIDGETS_NT4_SUBSCRIBE}", subscribeLine)
            filledOut = filledOut.replace("${WIDGETS_UPDATE}", jsUpdate)
            filledOut = filledOut.replace("${WIDGETS_SET_VALUE}", jsSetData)
            filledOut = filledOut.replace("${WIDGETS_SET_NO_DATA}", jsSetNoData)
            filledOut = filledOut.replace("${WIDGETS_CALLBACK}", jsCallback)

            self.send_response(200)
            self.send_header("Content-Type", "application/x-javascript")
            self.end_headers()

            self.wfile.write(filledOut.encode())

            return SimpleHTTPRequestHandler
        
        else:
            return SimpleHTTPRequestHandler.do_GET(self)
        


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class Webserver():
    
    def __init__(self):
        
        handler = functools.partial(TemplatingRequestHandler, 
                                     directory="webserver/www/")

        hostname=socket.gethostname()   
        ipAddr=socket.gethostbyname(hostname)   
        port = 5805

        self.server = ThreadedTCPServer(("", port), handler)

        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        self.serverThread = threading.Thread(target=self.server.serve_forever)
        # Exit the server thread when the main thread terminates
        self.serverThread.daemon = True
        self.serverThread.start()
        print(f"Server started on {hostname} at {ipAddr}:{port} " + 
              "in thread { self.serverThread.name}")
        
    def __del__(self):
        print("Server shutting down")
        self.shutdown()
            
    def shutdown(self):
        self.server.shutdown()
        self.serverThread.join()
        
    def addDashboardWidget(self, widget):
        _dashboardWidgetList.append(widget)