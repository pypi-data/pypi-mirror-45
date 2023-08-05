#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-04-11 09:02:01
# @Author  : Blackstone
# @to      :

from decroate import decorater
from config  import Debug

@decorater.publisher("publisher-1")
class A(object):
	pass
	@decorater.test_time
	def go(self):
		pass

@decorater.subscriber("publisher-1")
class B(object):

	def notify(self,msg=None):
		print("notify itself=>",msg)


@decorater.subscriber("publisher-1")
class C(object):

	def notify(self,msg=None):
		print("notify itself=>",msg)



@decorater.safe_singleton
class S(object):

	def __init__(self):
		#print(self)
		pass


@decorater.test_time
def aa():
	print("1")

@decorater.cached
def num(a):
	print("wiat.")
	return 100



class T:
	@decorater.cached
	def b(self,a,c=6):
		print("spend wait.")
		return 10+a


@decorater.test_time
def g(s):
	import uuid


	print(uuid.uuid3(uuid.NAMESPACE_URL,s))


def get_status():
	return Debug


if __name__=="__main__":
	from decroate import set_log_level
	set_log_level(True)
	A().go()
	g("fda")






