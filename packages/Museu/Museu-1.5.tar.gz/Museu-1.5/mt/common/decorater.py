#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-04-10 15:16:29
# @Author  : Blackstone
# @to      :




class decorater(object):

	_subscriber_pool={}
	_singlton_storage={}

	@staticmethod
	def lock(func):

		import threading
		func._lock=threading.Lock()
		def wrap(*args,**kw):
			with func._lock:
				return func(*args,**kw)
		return wrap


	@classmethod
	def publisher(cls,name):
		
		def wrap(classname):

			subscribers=cls._subscriber_pool.get(name)
			#print(subscribers)
			classname.update=lambda self,a=None:[x.notify(msg=a)   for x in cls._subscriber_pool.get(name)]
			return classname
		return wrap
			

	@classmethod
	def subscriber(cls,name):
		def wrap(classname):
			instance=classname()
			if cls._subscriber_pool.get(name) is None:
				cls._subscriber_pool[name]=[instance]
			else:
				cls._subscriber_pool[name].append(instance)

			# classname.notify=lambda a:print(1) or print(2)
			return classname
		return wrap



	@classmethod
	def singleton(cls,classname):
		def wrap(*args,**kw):
			
			_instance=decorater._singlton_storage.get(classname,None)
			
			if _instance is None:
				_instance=classname(*args,**kw)
				decorater._singlton_storage[classname]=_instance

			#print("********************************\n",_instance)

			return _instance

		return wrap

	
	@classmethod
	def safe_singleton(cls,classname):
		@decorater.lock
		def wrap(*args,**kw):
			
			_instance=decorater._singlton_storage.get(classname,None)
			
			if _instance is None:
				_instance=classname(*args,**kw)
				decorater._singlton_storage[classname]=_instance

			#print("********************************\n",_instance)

			return _instance

		return wrap



	def cached(func):

		def init():
			pass

		def get_sign(*str_):
			out=""
			for _ in str_:
				out+=str(_)

			import uuid,warnings
			if len(out)>1000000000:
				warnings.warn("签串太长,not check.")
				out=uuid.uuid3(uuid.NAMESPACE_URL, out)

			return out


		
		def wrap(*args,**kw):
			# print("*"*100)
			# print("func=>",func)
			# print("args=>",args)
			# print("kw=>",kw)

			sign=get_sign(args,kw)

			log("函数签名=>%s"%sign)

			if not hasattr(func,"_cache"):
				func._cache={}

				

			if func._cache.get(sign) is None:
				func._cache[sign]=func(*args,**kw)


			return func._cache.get(sign)


		return wrap


	@classmethod
	def test_time(cls,func):
		def wrap(*args,**kw):

			print(cls)
			import time
			v1=time.time()

			re=func(*args,**kw)
			v2=time.time()

			log("Function %s spend %s sec. "%(func,v2-v1))
			return re

		return wrap







	

def log(msg):
	import datetime,sys

	time=(str(datetime.datetime.now())[:19])
	print("[Debug]-%s-  %s "%(time,msg))











