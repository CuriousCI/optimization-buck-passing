- TODO: send the results
- TODO: just an API request
- TODO: which is the openbox API?

```python
# for _ in range(10):
#     config_dict = remote_advisor.get_suggestion()
#     config = Configuration(remote_advisor.config_space, config_dict)
#     print(config)
#     trial_info = {}
#     observation = {"": 1}
#     # il worker fa trials
#
#     # trial_info['cost'] = (datetime.datetime.now() - start_time).seconds
#     trial_info["worker_id"] = 0
#     trial_info["trial_info"] = "None"
#
#     remote_advisor.update_observation(
#         config_dict,
#         observation["objectives"],
#         observation["constraints"],
#         trial_info=trial_info,
#         trial_state=SUCCESS,  # TODO: if a job terminates before the time, then it must be set as failed
#     )

# task riguarda un job

# while |active_workers| < 10 (iperparametro)
# 1. send a worker
# 2. worker does the stuff
```


```python
# 1. orchestrator fa da server e riceve messaggi dal job (seee, me rimetto a fare l'API?)
# 2. orchestrator manda job, e i job si divertono con OpenBox (reverse engineering dell'API)
```



```python
# Config = tuple[int]

# Blackbox = Callable[[Config], int]

# this needs the ip of openbox, from where it asks for a suggestion from the API, this can be done
# def run_blackbox(task_id: TaskId, blackbox: Blackbox) -> None:
#     # this can be "framworked"
#
#     # TODO: read the fucking parameters / task from somwhere, doesn't matter where
#     # - just a REST API request
#     config = (1,)
#     observation = blackbox(config)


# @dataclass(frozen=True)
# class TaskConfig:
#
#     pass
#
#
# class RemoteWorkerAdvisor:
#     def __init__(self) -> None:
#         pass
#
#     pass


# self.base_url = 'http://%s:%d/bo_advice/' % (server_ip, port)
#
# # Register task
# res = requests.post(self.base_url + 'task_register/',
#                     data={'email': self.email, 'password': self.password, 'task_name': task_name,
#                             'config_space_json': config_space_json,
#                             'num_constraints': num_constraints, 'num_objectives': num_objectives,
#                             'max_runs': self.max_runs,
#                             'options': json.dumps(options), 'max_runtime_per_trial': max_runtime_per_trial,
#                             'active_worker_num': active_worker_num, 'parallel_type': parallel_type})
# res = json.loads(res.text)
#
# if res['code'] == 1:
#     self.task_id = res['task_id']
# else:
#     raise Exception('Server error %s' % res['msg'])


# def get_suggestion(self):
#     res = requests.post(self.base_url + 'get_suggestion/',
#                         data={'task_id': self.task_id})
#     res = json.loads(res.text)
#
#     if res['code'] == 1:
#         config_dict = json.loads(res['res'])
#         return config_dict
#     else:
#         raise exception('server error %s' % res['msg'])


# def update_observation(self, config_dict, objectives, constraints=[], trial_info={}, trial_state=SUCCESS):
#     res = requests.post(self.base_url + 'update_observation/',
#                         data={'task_id': self.task_id, 'config': json.dumps(config_dict),
#                               'objectives': json.dumps(objectives), 'constraints': json.dumps(constraints),
#                               'trial_state': trial_state, 'trial_info': json.dumps(trial_info)})
#     res = json.loads(res.text)
#     if res['code'] == 0:
#         raise Exception('Server error %s' % res['msg'])

# def get_result(self):
#     res = requests.post(self.base_url + 'get_result/', data={'task_id': self.task_id})
#     res_dict = res.json()
#     result = json.loads(res_dict.get('result'))
#     history = json.loads(res_dict.get('history'))
#     return result, history


# app_name = 'bo_advice'
# urlpatterns = [
#     # ex: /bo_advice/task_register/
#     path('task_register/', views.task_register, name='task_register'),
#     # ex: /bo_advice/get_suggestion/
#     path('get_suggestion/', views.get_suggestion, name='get_suggestion'),
#     # ex: /bo_advice/update_observation/
#     path('update_observation/', views.update_observation, name='update_observation'),
#     # ex: /bo_advice/get_result/
#     path('get_result/', views.get_result, name='get_result'),
# ]

# TODO: abastract, with a method "do job" ? No!
# TODO: make it concrete, and pass as argument the function, which takes a "config"

# TODO: use OpenBox stuff if you can, or just apricopt!


# def blackbox(config: Config) -> None:
#     pass


# class Worker:
#     pass
```
