#!/usr/bin/python
# -*- coding: utf-8 -*-
import cgi,cgitb
import connection
from random import randint
import email_config
print "Cache-Control:no-store, no-cache, must-revalidate"
from jinja2 import Template, Environment, FileSystemLoader
cgitb.enable()
templateLoader = FileSystemLoader( searchpath="/" )
templateEnv = Environment( loader=templateLoader )
form = cgi.FieldStorage() 
email = form.getvalue('email')
password  = form.getvalue('password')
name=form.getvalue('name')
contact=form.getvalue('contact')
type=form.getvalue('type')
institute=form.getvalue('institute')
code = randint(100000000,9999999999)
to = email
var=""

subject = "Account Confirmation @ NeoScript.in"
message = '\n You account is created successfully. Just follow this link to activate your account.\nhttp://www.neoscript.in/confirm_account.py?var='+str(code)+'&email='+str(email)

sql = "SELECT email_id,code FROM confirmation WHERE email_id = '{0}'".format(email)
connection.cursor.execute(sql)
data = connection.cursor.fetchall()
if connection.cursor.rowcount>0:
	message = "\nFollow this link to activate your account. \nhttp://www.neoscript.in/confirm_account.py?var="+str(data[0][1])+"&email="+str(data[0][0])+".\nUse your previously registered password to login. if you have forgot your password then just recover it using forgot password opton after activating your account."
	to = str(data[0][0])
	var = {"var":"You are already registered in neoscript.in, we are sending a new link to your mail. please check your mail and confirm your account."}
else:
	if type=='student':
		register_no=form.getvalue('r_no')
		query="insert into student(name,email_id, contact, institute, rno) values(%s,%s,%s,%s,%s)"
		query1="insert into confirmation values(%s,%s,%s,%s,%s)"
		connection.cursor.execute(query,(name,email,contact,institute,register_no))
		connection.cursor.execute(query1,(email,password,type,name,str(code)))
	else:
		query="insert into teacher values(%s,%s,%s,%s,%s)"
		query1="insert into confirmation values(%s,%s,%s,%s,%s)"
		connection.cursor.execute(query,(name,email,"Null",contact,institute))
		connection.cursor.execute(query1,(email,password,type,name,str(code)))
	connection.db.commit()
status = email_config.sendemail(to,subject,message)
print "Content-Type: text/html\n\n"
TEMPLATE_FILE = "/var/www/html/redirect_account_pending.html" 
template = templateEnv.get_template( TEMPLATE_FILE )
print template.render(var)
#print "Location: index1.py"
	
