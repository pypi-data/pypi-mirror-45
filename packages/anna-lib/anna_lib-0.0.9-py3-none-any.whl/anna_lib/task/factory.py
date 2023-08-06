import types
import inspect
import string
from importlib import import_module


def get_site_package(site: str) -> str:
	if site == 'test':
		return 'anna_unittasks'
	return 'anna_tasks.' + site


def parse_site_config(config: object) -> tuple:
	return getattr(config, 'url'), getattr(config, 'sequence')


def get_tasks(site: str) -> tuple:
	if isinstance(site, (list, tuple)) and len(site) == 1:
		return get_tasks(site[0])
	elif not isinstance(site, str):
		raise TypeError
	package = get_site_package(site)
	url, sequence = parse_site_config(import_module(package + '.config'))
	tasks = []
	for task in sequence:
		tasks.append(get_task(site, task))
	return url, tasks


def get_task(site: str, task: str) -> tuple:
	task = get_site_package(site) + '.' + task
	module = import_module(task)
	return task, inspect.getsource(module)


def load_task(driver: object, task: tuple) -> tuple:
	module = types.ModuleType(task[0])
	exec(task[1], module.__dict__)
	task_class = string.capwords(task[0].split('.')[-1].replace('_', ' ')).replace(' ', '')
	task = module.__dict__[task_class](driver)
	return module.__dict__['__name__'], task


def create(driver: object, site: str, task: str) -> object:
	task = get_task(site, task)
	return load_task(driver, task)
