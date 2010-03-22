all:
	make -C media

messages:
	find . -name "locale" -mindepth 2 -maxdepth 2 | sed 's/^/cd /g' | sed 's@locale@ \&\& django-admin  makemessages -l th \&\& cd ../@g' | sh
	find . -name "locale" -mindepth 2 -maxdepth 2  | sed 's/^/cd /g' | sed 's@locale@ \&\& django-admin  makemessages -l en \&\& cd ../@g' | sh

compilemessages:
	find . -name "locale" -mindepth 2 -maxdepth 2  | sed 's/^/cd /g' | sed 's@locale@ \&\& django-admin compilemessages \&\& cd ../@g' | sh

                                                                                                                                         
