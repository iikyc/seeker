#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <limits.h>


void iocCollection(char path[50]) {

	char cmdbuf[256];
	char hashDirectories[4][30] = {"$HOME/Desktop", "$HOME/Downloads", "/etc/init.d", "/etc/profile.d"};

	for (int i = 0; i < 4; i++) {
		snprintf(cmdbuf, sizeof(cmdbuf), "find %s -maxdepth 1 -type f -exec sha256sum '{}' >> %s/files/hashes.txt \\;", hashDirectories[i], path);
		system(cmdbuf);
		snprintf(cmdbuf, sizeof(cmdbuf), "find %s -type f -executable -exec sh -c \"echo FILE:{} >> %s/files/ioc.txt && strings {} | grep -E \'rm|arp|users|netstat|uname|groups|tcpdump|LD_PRELOAD\\s\' >> %s/files/ioc.txt\" \\;", hashDirectories[i], path, path);
		system(cmdbuf);
	}
	// Installed packages
	snprintf(cmdbuf, sizeof(cmdbuf), "echo Installed: $(apt list --installed | wc -l) >> %s/system/packages.txt", path);
	system(cmdbuf);
	// Upgradable packages
	snprintf(cmdbuf, sizeof(cmdbuf), "echo Upgradable: $(apt list --upgradable | wc -l) >> %s/system/packages.txt", path);
	system(cmdbuf);

}

void networkCollection(char path[50]) {

	char cmdbuf[256];
	// Network interfaces
	snprintf(cmdbuf, sizeof(cmdbuf), "ifconfig > %s/system/interfaces.txt", path);
	system(cmdbuf);
	// Routing table
	snprintf(cmdbuf, sizeof(cmdbuf), "netstat -rn > %s/system/route_table.txt", path);
	system(cmdbuf);
	iocCollection(path);
}

void browserCollection(char path[50]) {

	char cmdbuf[256];
	// Firefox history
	snprintf(cmdbuf, sizeof(cmdbuf), "find $HOME/.mozilla/firefox -name places.sqlite -exec cp '{}' %s/browsers/firefox.sqlite \\;", path);
	system(cmdbuf);
	// Google Chrome history
	snprintf(cmdbuf, sizeof(cmdbuf), "cp $HOME/.config/google-chrome/Default/History %s/browsers/chrome.sqlite", path);
	system(cmdbuf);
	networkCollection(path);

}

void fileCollection(char path[50]) {

	char cmdbuf[256];
	// Trash
	snprintf(cmdbuf, sizeof(cmdbuf), "ls $HOME/.local/share/Trash/files > %s/files/trash.txt", path);
	system(cmdbuf);
	browserCollection(path);
}

void logCollection(char path[50]) {
	
	char cmdbuf[256];
	// auth.log
	snprintf(cmdbuf, sizeof(cmdbuf), "cat /var/log/auth.log > %s/logs/auth_log.txt", path);
	system(cmdbuf);
	// dpkg.log
	snprintf(cmdbuf, sizeof(cmdbuf), "cat /var/log/dpkg.log > %s/logs/dpkg_log.txt", path);
	system(cmdbuf);
	// syslog
	snprintf(cmdbuf, sizeof(cmdbuf), "cat /var/log/syslog > %s/logs/syslog.txt", path);
	system(cmdbuf);
	// Last Logins
	snprintf(cmdbuf, sizeof(cmdbuf), "last > %s/logs/last.txt", path);
	system(cmdbuf);
	// Vim files
	snprintf(cmdbuf, sizeof(cmdbuf), "cat $HOME/.viminfo > %s/logs/vim_log.txt", path);
	system(cmdbuf);
	fileCollection(path);
}

void systemCollection(char path[50]) {

	char hostname[HOST_NAME_MAX + 1];
	gethostname(hostname, HOST_NAME_MAX + 1);
	char cmdbuf[256];
	// Current user
	snprintf(cmdbuf, sizeof(cmdbuf), "whoami > %s/system/system_information.txt", path);
	system(cmdbuf);
	// Hostname
	snprintf(cmdbuf, sizeof(cmdbuf), "cat /etc/hostname >> %s/system/system_information.txt", path);
	system(cmdbuf);
	// Timezone
	snprintf(cmdbuf, sizeof(cmdbuf), "cat /etc/timezone >> %s/system/system_information.txt", path);
	system(cmdbuf);
	// Users
	snprintf(cmdbuf, sizeof(cmdbuf), "cat /etc/passwd > %s/system/users.txt", path);
	system(cmdbuf);
	// Command history
	snprintf(cmdbuf, sizeof(cmdbuf), "strings $HOME/.bash_history | grep -E 'sudo|git|ssh|rm|rmdir|wget' > %s/system/bash_history.txt", path);
	system(cmdbuf);
	// Operating system version
	snprintf(cmdbuf, sizeof(cmdbuf), "cat /etc/os-release > %s/system/operating_system.txt", path);
	system(cmdbuf);
	// Storage
	snprintf(cmdbuf, sizeof(cmdbuf), "df -h > %s/system/disks.txt", path);
	system(cmdbuf);
	// Call the next function
	logCollection(path);
}

void init() {
	// Hostname to create the parent directory
	char hostname[HOST_NAME_MAX + 1];
	gethostname(hostname, HOST_NAME_MAX + 1);

	// Read the custodian name
	char custodian_name[30];
	printf("[->] Investigator name: ");
	scanf("%s", &custodian_name);
	printf("[*] Custodian name set to: %s\n", custodian_name);

	// Read the data storage path
	char target_path[50];
	printf("\n[->] Target path (Enter . to store data in current directory): ");
	scanf("%s", &target_path);
	printf("[*] Files will be stored at: %s/%s\n", target_path, hostname);

	// Create the data directory in the target path
	char cmdbuf[256];
	snprintf(cmdbuf, sizeof(cmdbuf), "mkdir %s/%s", target_path, hostname);
	system(cmdbuf);

	// Custody info
	snprintf(cmdbuf, sizeof(cmdbuf), "echo 'Investigator: %s' > %s/%s/log.txt", custodian_name, target_path, hostname);
	system(cmdbuf);
	snprintf(cmdbuf, sizeof(cmdbuf), "echo 'Extraction started at: ' $(date) >> %s/%s/log.txt", target_path, hostname);
	system(cmdbuf); 

	// Build path to pass to other functions
	char created_path[256];
	snprintf(created_path, sizeof(created_path), "%s/%s", target_path, hostname);

	// Create the sub-directories to store data
	char subdirectories[4][10] = {"system", "logs", "files", "browsers"};

	for (int i = 0; i < 4; i++) {
		snprintf(cmdbuf, sizeof(cmdbuf), "mkdir %s/%s", created_path, subdirectories[i]);
		system(cmdbuf);
	}

	// Call the next function
	systemCollection(created_path);
}

void startup() {
	init();
}

int main() {
	startup();
	return 0;
}
