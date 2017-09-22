#!/bin/sh
# Description: sanity test for acl package
# Author: Milos Malik <mmalik@redhat.com>

##### Variable Declaration #####
VERSION=1.0

# FAIL unless test explicitly passes
RESULT=FAIL

# Each pass increases SCORE by 1
SCORE=0
TOTAL=8

# Set language so we know what results to test for
set_lang=0
old_lang=$LANG
new_lang=en_US.UTF-8

# Which package and which utility do we test?
PACKAGE=acl

##### Function Declaration #####

log () {
	printf "\n:: $1 ::\n"
}

check_exit_code () {
	echo -e "\t* exit code: $1"
	if [ $1 $2 $3 ] ; then
		let "SCORE += 1"
	fi
}

##### Begin Test #####

log "[`date +%H:%M:%S`] Begin Test - $TEST-$VERSION"

# Warn if not running as root that test might fail
e_user=$(whoami)
if [[ x"${e_user}" != x"root" ]]; then
        log "Warning, not running as root! This test might fail."
fi

# Temporarily set LANG to value we can trust results from
if [[ x"${LANG}" != x"${new_lang}" ]]; then
        log "Warning, LANG not set to ${new_lang}!"
        log "Temporarily setting LANG to ${new_lang}, was ${old_lang}"

        set_lang=1
        export LANG=${new_lang}
        log "Done, LANG=${new_lang}."
fi

log "getfacl -h"
getfacl -h >& /dev/null
check_exit_code $? -eq 0

log "getfacl --help"
getfacl --help >& /dev/null
check_exit_code $? -eq 0

log "getfacl -v"
getfacl -v >& /dev/null
check_exit_code $? -eq 0

log "getfacl --version"
getfacl --version >& /dev/null
check_exit_code $? -eq 0

log "setfacl -h"
setfacl -h >& /dev/null
check_exit_code $? -eq 0

log "setfacl --help"
setfacl --help >& /dev/null
check_exit_code $? -eq 0

log "setfacl -v"
setfacl -v >& /dev/null
check_exit_code $? -eq 0

log "setfacl --version"
setfacl --version >& /dev/null
check_exit_code $? -eq 0

# Reset LANG to original value
if [[ ${set_lang} == 1 ]]; then
        log "Resetting LANG to ${old_lang}."
        export LANG=${old_lang}
        log "Done, LANG=${old_lang}."
fi

log "[`date +%H:%M:%S`] End Test - $TEST-$VERSION"

##### Report results #####

log "SCORE: ${SCORE}/${TOTAL}"

if [ ${SCORE} -eq ${TOTAL} ] ; then
# everything was OK
        log "RESULT: PASS"
        printf "\n\n"
    exit 0
else
# something failed
        log "RESULT: FAIL"
        printf "\n\n"
    exit 1
fi

##### End Test #####
