Main Commands:<br/>
(1) Main	function:	The	main	function	connects	and	disconnects	the	database,	prints	out	a	
menu	for	the	user	and	calls	each	function.	At	the	start	of	the	program,	the	user	will	be	
asked	to	enter	the	name	of	the	database	to	connect	to.	Once	connected	the	user	has	
the	option	to	sign	up	as	a	new	user	or	login.	After	logging,	the	main	menu	for	
interacting	with	the	database	will	be	provided	allowing	the	following	interactions.<br/>
(2) List	products: Lists	all	products	that	have	active	sales	associated	to	them.	For	each	
product	that	qualifies,	the	product	id,	description,	number	of	reviews,	average	rating	
and	number	of	sales	associated	are	listed	in	descending	order	of	the	number	of	active	
sales. From this	listing,	the	user	may	perform	the	following:<br/>
I. Write	a	product	review<br/>
II. List	all	reviews	of	the	product<br/>
III. List	all	active	sales of	the	product<br/>
(3) Search	for	sales:	The	user	may	enter	one	or	more	keywords	and	the	system	will	retrieve	
all	active	sales	with	said	keyword	in	either	the	sales	description	or	product	description.	<br/>
(4) 1-2	Follow-up:	From	the	listings	of	either	action	1	or	2,	the	user	may	select	a	sale	which	
will	provide	more	details	about	the	selected        sale.	The	following	actions	will	be	enabled:<br/>
I. Place	a bid	on	the	selected	sale<br/>
II. List	all	active	sales	of	the	seller<br/>
III. List	all	active	reviews	of	the	seller<br/>
(5) Post	a	sale:	The	user	enters	a	product	id	(optional),	sale	end	date	and	time,	sale	
description,	condition	and	a	reserved	price (optional) which	will	then	be	posted	as	a	
sale	in	the	current	database.<br/>
(6) Search	for	users:	The	user	enters	a	keyword	which	will	then	return	all	user	profiles	that	
have	the	keyword	in	either	name	or	email. Writing a	review	will	overwrite	a	previous	
review on	that	user. From	the	set	of	users,	the	following	actions	are	enabled:<br/>
I. Write	a	review<br/>
II. List	all	active	listings	of	the	user<br/>
III. List	all	reviews	of	the	user<br/>
