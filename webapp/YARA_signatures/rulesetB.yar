rule privesc {
	strings:
		$sudo_perm_check = "sudo -l"
		$crontab_check = "crontab -l"
		$linpeas = "linpeas.sh"
		$find = "find . -exec /bin/sh \; -quit"
	condition:
		$sudo_perm_check or $crontab_check or $linpeas or $find
}
