#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <sys/time.h>
#include <sys/select.h>

#define BUF_SIZE 100
#define MAX_CLNT 256

void error_handling(char *buf);

int main(int argc, char *argv[])
{
	int clnt_cnt=0;
	int clnt_socks[MAX_CLNT];
	int serv_sock, clnt_sock;
	struct sockaddr_in serv_adr, clnt_adr;
	struct timeval timeout;
	fd_set fds, cpy_fds;

	socklen_t adr_sz;
	int fd_max, str_len, fd_num, i;
	char buf[BUF_SIZE];
	if(argc != 2) {
		printf("Usage : %s <port>\n", argv[0]);
		exit(1);
	}

	serv_sock=socket(PF_INET, SOCK_STREAM, 0);
	memset(&serv_adr, 0, sizeof(serv_adr));
	serv_adr.sin_family = AF_INET;
	serv_adr.sin_addr.s_addr = htonl(INADDR_ANY);
	serv_adr.sin_port = htons(atoi(argv[1]));
	
	if(bind(serv_sock, (struct sockaddr*) &serv_adr, sizeof(serv_adr)) == -1)
		error_handling("bind() error");
	if(listen(serv_sock, 5) == -1)
		error_handling("listen() error");

	FD_ZERO(&fds);
	FD_SET(serv_sock, &fds);
	fd_max = serv_sock;

	while(1)
	{
		cpy_fds = fds;
		timeout.tv_sec = 5;
		timeout.tv_usec = 5000;

		if((fd_num = select(fd_max + 1, &cpy_fds, 0, 0, &timeout)) == -1){
			break;
		}
		
		if(fd_num == 0) {
			continue;
		}
		
		for(i = 0; i < fd_max + 1; i++)
		{
			if(FD_ISSET(i, &cpy_fds))
			{
				if(i == serv_sock) // connection request!
				{
					
					adr_sz = sizeof(clnt_adr);
					clnt_sock = accept(serv_sock, (struct sockaddr*)&clnt_adr, &adr_sz);
					clnt_socks[clnt_cnt++]=clnt_sock;
					FD_SET(clnt_sock, &fds);
					if(fd_max < clnt_sock)
						fd_max = clnt_sock;
					printf("connected client: %d \n", clnt_sock);
				}
				else // read message!
				{
					str_len = read(i, buf, BUF_SIZE);
					if(str_len == 0) // close request!
					{
						for(int j=0; j<clnt_cnt; j++)   // remove disconnected client
						{
							if (i == clnt_socks[j])
							{
								while (j < clnt_cnt - 1)
								{
									clnt_socks[j] = clnt_socks[j + 1];
									j++;
								}
							break;
							}
						}
						clnt_cnt--;
						FD_CLR(i, &fds);
						close(i);
						printf("closed client: %d \n", i);
					}
					else // echo!
					{
						for(int j=0;j<clnt_cnt;j++){
							write(clnt_socks[j], buf, str_len);
						}
					}
				}
			}
		}
	}
	close(serv_sock);
	return 0;
}

void error_handling(char *buf)
{
	fputs(buf, stderr);
	fputc('\n', stderr);
	exit(1);
}
