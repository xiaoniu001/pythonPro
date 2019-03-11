import asyncio
import time


async def add(x, y):
	print("add 函数:", x + y)
	
	await sleep()
	return x + y


async def sleep():
	for i in range(100000000):
		continue


async def reduce(x, y):
	print("reduce 函数:", x + y)
	
	await sleep()
	return x + y


async def compute(x):
	print("compute 函数:", x)
	for i in range(x):
		continue
	await sleep()
	return x


def hello(task):
	print(task.result())
	print("hello 您已完成add函数")


if __name__ == '__main__':
	# 单个任务
	# cor = add(5, 15)
	# print(cor)  # 这是一个协程对象
	# task = asyncio.ensure_future(cor)  # 将携程对象转化成task对象 方式一
	# loop = asyncio.get_event_loop()  # 注册一个循环事件
	#
	# # task = loop.create_task(cor)  # 将携程对象转化成task对象 方式二
	# print(task)  # 一个任务对象
	# task.add_done_callback(hello)  # 任务完成后回调 方式一
	# loop.run_until_complete(task)
	# print(task.result())  # 任务完成后回调 方式二
	
	# 多任务
	start = time.time()
	task_add = asyncio.ensure_future(add(5, 10))
	task_reduce = asyncio.ensure_future(reduce(789, 45))
	task_compute = asyncio.ensure_future(compute(100))
	tasks = [task_add, task_compute, task_reduce]
	
	loop = asyncio.get_event_loop()
	loop.run_until_complete(asyncio.wait(tasks))
	end = time.time()
	print('Cost time:', end - start)
	print(task_add.result(), task_reduce.result(), task_compute.result())
