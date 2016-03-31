import random,re,string
firstnames = ['Coleman',	'Garry','Chandler',	'Marco'	,'Colon','Sammy','Willis','Thomas','Ballard','Stanley','Newton','Robbin','Shyla','Rodolfo','Marielle','Lorriane','Walker','Lucila','Cecelia','Modesto','Linh','Delorse','Lisha','Jeneva','Neda','Sherise','Christin','Tanja','Lachelle','An','Werner']
lastnames = ['Marielle','Lorriane','Walker','Lucila','Cecelia','Modesto','Linh','Delorse','Lisha','Jeneva','Neda','Sherise','Coleman',	'Garry','Chandler',	'Marco'	,'Colon','Sammy','Willis','Thomas','Ballard','Stanley','Newton','Watts','Shyla','Rodolfo','Marielle','Lorriane','Walker','Lucila']
companies = ['TRW','HELLA','SAS','BROSE','VW','FOXCONN','SONY','LG','MIBA','HONEYWELL','QWE','LKA','LKT','KRIVA','SKLAD','BMW','RENAULT','LEVA','DEA','PROG']
position = ['programator','skladnik','detekcia','manazer','elektroprojektant','konstrukter','mechanik','elektrikar','sofer']
password= 'test'
names=['skrutkovanie','zvaracia stanica','prieduchy pre b915','pasovy dopravnik','carousel','montaz pedalovky','leak tester','tester','pripravok bmw','pripravok porsche']
messages= ['ewrwetewtwet','ewtewtew','tewsdgdsfg','ewtewt','ewtewtewwetwe','ewtewtwetwet','tjtyjytjytjtyj','tewtewtewgweragerherh','ryeryerhe','tew','tweeiogjorih','wtfgerwoigjroeia']
domains = ['sk','org','com','net','cz']

def randomword(length):
   return ''.join(random.choice(string.lowercase) for i in range(length)) 

def companyid():
	return random.randint(0,len(companies)-1)
def firstname():
	return firstnames[random.randint(0,len(firstnames)-1)]

def lastname():
	return lastnames[random.randint(0,len(lastnames)-1)]

def getposition():
	return position[random.randint(0,len(position)-1)]

def password():
	return password

def mail(name):
	names= re.split(' ',name)
	return str(names[0]+'.'+names[1]+str(random.randint(0,10))+'@mts.'+domains[random.randint(0,len(domains)-1)] )
def username():
	return firstname()+' '+lastname()

def name():
	return names[random.randint(0,len(names)-1)]	
def message():
	return messages[random.randint(0,len(messages)-1)]	
def comment():
	return message()
def phone():
	return str(random.randint(1,9))+str(random.randint(1,9))+str(random.randint(1,9))+str(random.randint(1,9))+str(random.randint(1,9))+str(random.randint(1,9))+str(random.randint(1,9))+str(random.randint(1,9))


def name():
	return firstname()+' '+lastname()