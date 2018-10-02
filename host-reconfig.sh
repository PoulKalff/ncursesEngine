#!/bin/sh
#
# This file is normally distributed by cfengine.
#
# Host reconfiguration after cloning or change of network.
#
# Linux version
#

FILES=/pack/sysadmin/files
BINDIR=`dirname $0`
NETVAULT=/usr/netvault

ECHO="/bin/echo -e"
SED="/bin/sed"
AWK="/usr/bin/awk"
GREP="/bin/grep"
EGREP="/bin/egrep"
LDAPSEARCH="/usr/bin/ldapsearch"
IP="/sbin/ip"
HEAD="/usr/bin/head"


if [ "`whoami`" != "root" ]; then
  echo "Abort, running this script requires root privileges"
  exit 1
fi

$ECHO  "\nHost-reconfig.sh can be run any number of times. Configurations are categorized"
$ECHO "and it is easy choose the part that needs reconfiguration."
$ECHO "\nIf the server has just been cloned it is importent to generate new SSH"
$ECHO "and Cfengine key-pairs."

# -------------------------------------------
# Change hostname/IP/network
# -------------------------------------------

$ECHO "\nChange hostname/IP/network configuration (y/N)? \c"
read ans
if [ "$ans" = "y" ]; then
    IFACE=`$IP -f inet -o link | $GREP -v LOOPBACK | $SED 's/^.*: \(.*\): .*$/\1/' | $HEAD -1`

    $ECHO "\nCurrent running IPv4 and/or IPv6 configuration for '$IFACE':"
    $ECHO "----------------------"
    ip -f inet addr show $IFACE
    ip -f inet6 addr show $IFACE

    $ECHO "\n\tNodename: \c"
    cat /etc/hostname

    IFACEFILE="/etc/network/interfaces"
    IPv4=`$IP -f inet  addr  show dev $IFACE | grep "inet .* scope global $IFACE" | head -n1 | awk '{ print $2 }'`
    GWv4=`$IP -f inet  route show dev $IFACE | grep "default via .* metric .*"   | head -n1 | awk '{ print $3 }' | cut -d '/' -f1`
    IPv6=`$IP -f inet6 addr  show dev $IFACE | grep "inet6 .* scope global" | head -n1 | awk '{ print $2 }'`
    GWv6=`$IP -f inet6 route show dev $IFACE | grep "default via .* metric .*"   | head -n1 | awk '{ print $3 }' | cut -d '/' -f1`

    # Determine if this hos is dual-stacked ofr v4/v6 single stacked
    if [ "`echo $IPv4 | wc -c`" -gt 3 ] ; then
        IPv4Present=1
    else
        IPv4Present=0
    fi
    if [ "`echo $IPv6 | wc -c`" -gt 3 ] ; then
        IPv6Present=1
    else
        IPv6Present=0
    fi

    if [ $IPv4Present -eq 0 ] && [ $IPv6Present -eq 1 ] ; then
        ipconf=1
    elif [ $IPv4Present -eq 1 ] && [ $IPv6Present -eq 1 ] ; then
        ipconf=2
    elif [ $IPv4Present -eq 1 ] && [ $IPv6Present -eq 0 ] ; then
        ipconf=3
    elif [ $IPv4Present -eq 0 ] && [ $IPv6Present -eq 0 ] ; then
        ipconf=99
        echo $ECHO "Warning: No current IPv4 or IPv6 configuration found"
    fi
    if [ $ipconf -eq 2 ] || [ $ipconf -eq 3 ] ; then
	    $ECHO "\tIPv4 address:  $IPv4"
	    $ECHO "\tIPv4 gateway:  $GWv4"
    fi
    if [ $ipconf -eq 1 ] || [ $ipconf -eq 2 ]; then
	    $ECHO "\tIPv6 address:  $IPv6"
	    $ECHO "\tIPv6 gateway:  $GWv6"
    fi

    $ECHO "------------------------------------------------"
    $ECHO "\nEnter new values (type Enter to keep old values)"
    $ECHO "------------------------------------------------"
    $ECHO "Which protocol types will this host be using (scope global addresses)?"
    $ECHO "(1) IPv6 only"
    $ECHO "(2) IPv4+IPv6 (Dual stacking)"
    $ECHO "(3) IPv4 only"
    $ECHO "\nEnter wanted configuration (current configuration is $ipconf ): \c"
    read ans
    if [ "x$ans" != "x" ] ; then
        ipconf=$ans
    fi
      

    if [ -z "$ipconf" ] || [ $ipconf -lt 1 ] || [ $ipconf -gt 3 ] ; then
        $ECHO "Invalid answer. Exiting!"
        exit 1
    fi
    # -- New nodename --
    $ECHO " Nodename (`cat /etc/hostname 2>/dev/null`): \c"
    read ans
    if [ ! -z "$ans" ]; then
	$ECHO $ans > /etc/hostname
    fi

    # -- New interface configuration --
    IPCONF=""
    IPCONF="${IPCONF}# The loopback network interface\n"
    IPCONF="${IPCONF}auto lo\n"
    IPCONF="${IPCONF}iface lo inet loopback\n\n"
    IPCONF="${IPCONF}# The primary network interface\n"
    IPCONF="${IPCONF}auto $IFACE\n"
    if [ $ipconf -ge 2 ] && [ $ipconf -le 3 ] ; then
        $ECHO " IPv4 address in CIDR notation ($IPv4):\c"
        read ans
	if [ ! -z "$ans" ]; then
	    IPv4=$ans
	fi
        # Determine IPv4 netmask
        case `echo $IPv4 | cut -d'/' -f2` in
            30)
                IPv4Netmask="255.255.255.252"
                ;;
            29)
                IPv4Netmask="255.255.255.248"
                ;;
            28)
                IPv4Netmask="255.255.255.240"
                ;;
            27)
                IPv4Netmask="255.255.255.224"
                ;;
            26)
                IPv4Netmask="255.255.255.192"
                ;;
            25)
                IPv4Netmask="255.255.255.128"
                ;;
            24)
                IPv4Netmask="255.255.255.0"
                ;;
            23)
                IPv4Netmask="255.255.254.0"
                ;;
            22)
                IPv4Netmask="255.255.252.0"
                ;;
            21)
                IPv4Netmask="255.255.248.0"
                ;;
            20)
                IPv4Netmask="255.255.240.0"
                ;;
            *)
                $ECHO "The entered subnetmask is not within the range 20-30 or the address entered was not a valid IPv4 address in CIDR notation"
                $ECHO "Exiting!"
                exit 1
                ;;
        esac

        $ECHO " Default IPv4 gateway ($GWv4):\c"
        read ans
	if [ ! -z "$ans" ]; then
	    GWv4=$ans
	fi
        IPCONF="${IPCONF}iface $IFACE inet static\n"
        IPCONF="${IPCONF}    address `echo $IPv4 | cut -d '/' -f1`\n"
        IPCONF="${IPCONF}    netmask ${IPv4Netmask}\n"
        IPCONF="${IPCONF}    gateway ${GWv4}\n\n"
    fi
    if [ $ipconf -ge 1 ] && [ $ipconf -le 2 ] ; then
        $ECHO " IPv6 address including netmask ($IPv6):\c"
        read ans
	if [ ! -z "$ans" ]; then
	    IPv6=$ans
	fi

        $ECHO " Default IPv6 gateway ($GWv6):\c"
        read ans
	if [ ! -z "$ans" ]; then
	    GWv6=$ans
	fi
        IPCONF="${IPCONF}iface $IFACE inet6 static\n"
        IPCONF="${IPCONF}    address `echo $IPv6 | cut -d '/' -f1`\n"
        IPCONF="${IPCONF}    netmask `echo $IPv6 | cut -d '/' -f2`\n"
        IPCONF="${IPCONF}    gateway ${GWv6}\n\n"
    fi

    # Backup old file and write new
    mv $IFACEFILE $IFACEFILE.old
    $ECHO $IPCONF > $IFACEFILE
fi

# -------------------------------------------
# Change nameserver config
# -------------------------------------------

$ECHO "\nChange nameserver configuration (y/N)? \c"
read ans
if [ "$ans" = "y" ]; then
	$ECHO "\nCurrent configuration:"
	$ECHO "----------------------"

	if [ -f /etc/resolv.conf ] ;then
		domain=`$EGREP '^domain' /etc/resolv.conf |$AWK '{print $2}'`
		$ECHO " DNS domain: $domain"
		nameservers=`$EGREP '^nameserver' /etc/resolv.conf |$AWK '{print $2}'`
		nscomb=""
		for ns in $nameservers; do
			nscomb="$nscomb $ns"
		done
		$ECHO " Nameservers:$nscomb"
		search=`$EGREP '^search' /etc/resolv.conf |$AWK '{print $2,$3,$4,$5,$6,$7}'`
		$ECHO " Search domains: $search"
	else
		$ECHO " No /etc/resolv.conf configured"
	fi

	# -- New DNS domain --
	$ECHO " DNS domain ($domain): \c"
	read ans
	if [ ! -z "$ans" ]; then
		domain=$ans
	fi

	# -- New Nameservers --
	$ECHO " Nameservers ($nscomb ): \c"
	read ans
	if [ ! -z "$ans" ]; then
		nameservers=$ans
	fi

	# -- New search domain list --
	$ECHO " Search domain list ($search): \c"
	read ans
	if [ ! -z "$ans" ]; then
		search=$ans
	fi

	$ECHO "\nUpdating /etc/resolv.conf file"
	cp /etc/resolv.conf /etc/resolv.conf.bak
	$ECHO "domain $domain" > /etc/resolv.conf
	for ns in $nameservers; do
		$ECHO "nameserver $ns" >> /etc/resolv.conf
	done
	$ECHO "search\c" >> /etc/resolv.conf
	for i in $search; do
		$ECHO " $i\c" >> /etc/resolv.conf
	done
	$ECHO >> /etc/resolv.conf
        # Fix that /etc/resolv.conf gets overwritten at boot on Ubuntu
        resolv_tail_file=/etc/resolvconf/resolv.conf.d/tail
        if [ -e $resolv_tail_file ]; then
                $ECHO "Found $resolv_tail_file. Copying /etc/resolv.con to $resolv_ail_file"
                cp /etc/resolv.conf $resolv_tail_file      
        fi
fi

# -------------------------------------------
# Change NTP config
# -------------------------------------------

$ECHO "\nChange NTP configuration (y/N)? \c"
read ans
if [ "$ans" = "y" ]; then
	$ECHO "\nCurrent configuration:"
	$ECHO "----------------------"
	if [ -f /etc/ntp.conf ]; then
		cat /etc/ntp.conf
	else
		$ECHO "None."
	fi

	$ECHO "\nEnter NTP servers seperated by space: \c"
	read ans
	if [ -n "$ans" ]; then
		$ECHO "# NTP servers" >/etc/ntp.conf
		for ntpsrv in $ans; do
			$ECHO "server $ntpsrv minpoll 4 maxpoll 7 burst" >> /etc/ntp.conf
		done
		$ECHO "Updated NTP configuration."
    /etc/init.d/ntp restart 
		$ECHO "Restarted NTP service"
	else
		$ECHO "Nothing changed."
	fi
fi


# -------------------------------------------
# Generate new SSH keys
# -------------------------------------------

$ECHO "\nGenerate new SSH keys (y/N)? \c"
read ans
if [ "$ans" = "y" ]; then
	echo
	rm /etc/ssh/ssh_host_*_key
	rm /etc/ssh/ssh_host_*_key.pub
  dpkg-reconfigure openssh-server
fi


# ---------------------------------------------
# Configure Nullmailer
# ---------------------------------------------

if [ -f /etc/nullmailer/remotes ]; then
	$ECHO "\nConfigure Nullmailer (y/N)? \c"	
	read ans
	if [ "$ans" = "y" ]; then
		me=`cat /etc/mailname`
		remotes=`$AWK '{print $1}' /etc/nullmailer/remotes`
		if $GREP '\-\-port=' /etc/nullmailer/remotes >/dev/null 2>&1; then
			remotesport=`$SED 's/^.*\-\-port\=\([0-9]*\)\( .*\)*$/\1/' /etc/nullmailer/remotes`
		else
			remotesport='25'
		fi
		$ECHO "\n Nullmailer 'me' ($me): \c"
		read ans
		if [ -n "$ans" ]; then
			echo "$ans" > /etc/mailname
		fi
		$ECHO "\n Outgoing SMTP server ($remotes): \c"
		read ans
		if [ -n "$ans" ]; then
			remotes="$ans"
		fi
		$ECHO "\n Outgoing SMTP server port ($remotesport): \c"
		read ans
		if [ -n "$ans" ]; then
			remotesport="$ans"
		fi
		$ECHO "$remotes smtp --port=$remotesport" > /etc/nullmailer/remotes
		$ECHO "\n Restarting nullmailer."
		/etc/init.d/nullmailer restart
		$ECHO
	fi	
fi


# ---------------------------------------------
# Configure NetVault client name and passsword
# ---------------------------------------------

if [ -f ${NETVAULT}/config/configure.cfg ]; then
	$ECHO "\nConfigure NetVault (y/N)? \c"	
	read ans
	if [ "$ans" = "y" ]; then
		$ECHO "\nStopping NetVault."
		${NETVAULT}/etc/startup.sh stop
		
		nv_name=`${NETVAULT}/util/nvgetstanza config configure.cfg null Machine clients`
		$ECHO "\nEnter hostname (${nv_name}): \c"
		read ans
		if [ -n "$ans" ]; then
			${NETVAULT}/util/nvsetstanza config configure.cfg null Machine clients "$ans" FALSE
			${NETVAULT}/util/nvsetstanza config configure.cfg null Machine Name "$ans" FALSE
		fi

		$ECHO "\nSet new NetVault client password (y/N)? \c"	
		read ans
		if [ "$ans" = "y" ]; then
			$ECHO "\nEnter new NetVault client password: \c"
			stty -echo
			read password
			stty echo
			${NETVAULT}/bin/nvpassword "${password}"
			echo
		fi

		$ECHO "\nSet firewall ports  (y/N)? \c"	
		read ans
		if [ "$ans" = "y" ]; then
			$ECHO "\nEnter forewall port range [20031-20099]: \c"
			read ans
			if [ -z "$ans" ]; then
				ans="20031-20099"
			fi
			${NETVAULT}/util/nvsetstanza config firewall.cfg Devices "Ports" Value "$ans" FALSE
			${NETVAULT}/util/nvsetstanza config firewall.cfg Devices "Out Ports" Value "$ans" FALSE
			${NETVAULT}/util/nvsetstanza config firewall.cfg MsgChannel "Ports" Value "$ans" FALSE
			${NETVAULT}/util/nvsetstanza config firewall.cfg MsgChannel "Out Ports" Value "$ans" FALSE
			${NETVAULT}/util/nvsetstanza config firewall.cfg NDMP "Ports" Value "$ans" FALSE
			${NETVAULT}/util/nvsetstanza config firewall.cfg NDMP "Out Ports" Value "$ans" FALSE
			${NETVAULT}/util/nvsetstanza config firewall.cfg Network "Out Ports" Value "$ans" FALSE
		fi

		$ECHO "\nStarting NetVault\n"
		${NETVAULT}/etc/startup.sh start
	fi
fi


# ---------------------------------------------
# Configure Cfengine
# ---------------------------------------------

if [ -f /etc/default/cfengine2 ] ; then
	$ECHO "\nConfigure Cfengine (y/N)? \c"	
	read ans
	if [ "$ans" = "y" ]; then
	  state=`$GREP RUN_CFEXECD /etc/default/cfengine2 |$AWK -F"=" '{print $2}'`
	  if [ $state -eq 0 ]; then
	    $ECHO "\n Cfengine state: Disabled\n"
	    $ECHO " Enable (y/N):\c"
	    read ans
	    if [ "$ans" = "y" ]; then
	      perl -pi -e 's/RUN_CF(EXECD)=./RUN_CF$1=1/g' /etc/default/cfengine2 
	      $ECHO " Enabled CFEXECD"
      fi
    fi
	  $ECHO "\nRecreate Cfengine keypair (y/N)? \c"
	  read ans
	  if [ "$ans" = "y" ]; then
		  /bin/rm -f /var/cfengine/ppkeys/localhost.priv /var/cfengine/ppkeys/localhost.pub
		  /usr/sbin/cfkey
		  echo
	  fi
    if [ ! -f /var/cfengine/inputs/update.conf ]; then
      $ECHO "INFO: There is no update.conf i /var/cfengine/inputs, cfagent will not run as expected!"
    fi
    $ECHO "Start Cfengine cfexecd (y/N)? \c"
		read ans
		if [ "$ans" = "y" ]; then
		    /etc/init.d/cfengine2 start
		fi
	fi
fi


# ---------------------------------------------
# Configure nss-ldap
# ---------------------------------------------

$ECHO "\nConfigure nss-ldap [user management] (y/N)? \c"	
read ans
if [ "$ans" = "y" ]; then
	hostname=`/bin/hostname`
	dnshost=`/usr/bin/host $hostname | $EGREP 'has ?(IPv6)? address' | $AWK '{print $1}'`
	$ECHO "\nFQDN hostname ($dnshost)? \c"
	read host
	if [ -z "$host" ]; then
		host=$dnshost
	fi
	dn=`$LDAPSEARCH -x -h opends.netic.dk -b "ou=Access,dc=netic,dc=dk" -D "cn=server-authentication,ou=Managers,dc=netic,dc=dk" -w sydNegJov -LLL cn=$host dn | $SED '/^ / {; H; d; }; /^ /! {; x; s/\n //; };' | $EGREP '^dn: ' | $SED 's/^dn: \(.*\)$/\1/'`
	if [ -n "$dn" ]; then
		$ECHO "\nConfiguring ldapclient"
		if [ -f /etc/nss-ldapd.conf ]; then
		  mv /etc/nss-ldapd.conf /etc/nss-ldapd.conf.bak
	  fi
	  if [ -f /etc/nsswitch.conf ]; then
	    cp /etc/nsswitch.conf /etc/nsswitch.conf.bak
    fi
	  $ECHO $dn
		if [ -f /etc/nslcd.conf ]; then
			nssldap_conf="/etc/nslcd.conf"
		else
			nssldap_conf="/etc/nss-ldapd.conf"
		fi
		$ECHO "# Configuration for Netic User Management" > $nssldap_conf
		$ECHO "uid nslcd" >> $nssldap_conf
		$ECHO "gid nslcd" >> $nssldap_conf
		$ECHO "uri ldap://opends.netic.dk/" >> $nssldap_conf
		$ECHO "base dc=netic,dc=dk" >> $nssldap_conf
		$ECHO "binddn cn=server-authentication,ou=Managers,dc=netic,dc=dk" >> $nssldap_conf
		$ECHO "bindpw sydNegJov" >> $nssldap_conf
		$ECHO "filter passwd (&(objectClass=posixAccount)(isMemberOf=$dn))" >> $nssldap_conf
		chmod 600 $nssldap_conf
		/etc/init.d/nslcd restart
		$SED 's/^passwd:.*$/passwd:     files ldap/' </etc/nsswitch.conf.bak | $SED 's/^group:.*$/group:      files ldap/' >/etc/nsswitch.conf
	else
		$ECHO "\nHost $host does not exist in ldap Access tree. Please add the host to ldap and try again."
	fi
fi

# -------------------------------------------
# Finish
# -------------------------------------------

$ECHO "\nReboot the server to see if everything is working."
