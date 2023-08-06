# # class for different generating a single service
# class Service():
#     """
#     Service manages the creation of a service.
#     """

#     # subclass build
#     class Build():
#         """
#         service.build
#         """
#         # initializer
#         def __init__(self):
#             self.build = {}

#         # add context
#         def context(self, input):
#             if(isinstance(input, str)):
#                 self.build['context'] = input
#                 return True
#             else:
#                 raise Exception('INVALID INPUT: "{}" is not a string'.format(input))

#         # add dockerfile
#         def dockerfile(self, input):
#             if(isinstance(input, str)):
#                 self.build['dockerfile'] = input
#                 return True
#             else:
#                 raise Exception('INVALID INPUT: "{}" is not a string'.format(input))

#         # add args
#         def args(self, input):
#             if(isinstance(input, list)):
#                 self.build['args'] = input
#                 return True
#             else:
#                 raise Exception('INVALID INPUT: "{}" is not a list'.format(input))

#         # add cache_from
#         def cache_from(self, input):
#             if(isinstance(input, list)):
#                 self.build['cache_from'] = input
#                 return True
#             else:
#                 raise Exception('INVALID INPUT: "{}" is not a list'.format(input))

#         # add labels
#         def labels(self, input):
#             if(isinstance(input, list) or isinstance(input, dict)):
#                 self.build['labels'] = input
#                 return True
#             else:
#                 raise Exception('INVALID INPUT: "{}" is not a list or dict'.format(input))

#         # add wshm_size
#         def shm_size(self, input):
#             if(isinstance(input, int) or isinstance(input, str)):
#                 self.build['shm_size'] = input
#                 return True
#             else:
#                 raise Exception('INVALID INPUT: "{}" is not an integer'.format(input))

#         # add target
#         def target(self, input):
#             if(isinstance(input, str)):
#                 self.build['target'] = input
#                 return True
#             else:
#                 raise Exception('INVALID INPUT: "{}" is not a string'.format(input))

#         #return self as dictionary
#         def get_dict(self):
#             return(dict(self.build))

#     class Deploy():
#         """
#         service.deploy
#         """
#         class RestartPolicy():
#             """
#             service.deploy.restart_policy
#             """
#             #initializer
#             def __init__(self):
#                 self.restart_policy = {}

#             #add restart policy condition
#             def condition(self, input):
#                 """
#                 Add restart policy condition, if unset will default to
#                 @type input: string
#                 @param input: One of 'none', 'on-failure' or 'any'
#                 """
#                 if(isinstance(input, str)):
#                     if(input in ['none', 'on-failure', 'any']):
#                         self.restart_policy['condition'] = input
#                     else:
#                         raise Exception("INVALID INPUT: '{}' is not One of 'none', 'on-failure' or 'any'".format(input))
#                 else:
#                     raise Exception('INVALID INPUT: "{}" is not a string'.format(input))

#             #add restart policy delay
#             def delay(self, input):
#                 """
#                 add delay to restart policy
#                 @type:  string
#                 @param: How long to wait between restart attempts
#                 """
#                 if(isinstance(input, str)):
#                     self.restart_policy['delay'] = input
#                 else:
#                     raise Exception('INVALID INPUT: "{}" is not a string'.format(input))

#             #add restart policy delay
#             def max_attempts(self, input):
#                 """
#                 add max attempts to restart policy
#                 @type:  integer
#                 @param: How many times to attempt to restart a container before giving up
#                 """
#                 if(isinstance(input, str)):
#                     self.restart_policy['max_attempts'] = input
#                 else:
#                     raise Exception('INVALID INPUT: "{}" is not an integer'.format(input))

#             #add restart policy delay
#             def window(self, input):
#                 """
#                 add window to restart policy
#                 @type:  integer
#                 @param: How long to wait before deciding if a restart has succeeded
#                 """
#                 if(isinstance(input, str)):
#                     self.restart_policy['window'] = input
#                 else:
#                     raise Exception('INVALID INPUT: "{}" is not a string'.format(input))
            
#             #return self dictionary
#             def get_dict(self):
#                 """
#                 Return service.deploy dictionary
#                 """
#                 return(dict(self.restart_policy))

#         #initializer
#         def __init__(self):
#             self.deploy = {}
#             self.restart_policy = self.RestartPolicy()
#             self.deploy['restart_policy'] = self.restart_policy

#         #add context
#         def endpoint_mode(self, input):
#             if(isinstance(input, str)):
#                 self.deploy['endpoint_mode'] = input
#                 return True
#             else:
#                 raise Exception('INVALID INPUT: "{}" is not a string'.format(input))

#         #add labels
#         def labels(self, input):
#             if(isinstance(input, list) or isinstance(input, dict)):
#                 self.deploy['labels'] = input
#                 return True
#             else:
#                 raise Exception('INVALID INPUT: "{}" is not a list or dict'.format(input))
        
#         #add placement, constraints
#         def placement_constraints(self, input):
#             if(isinstance(input, list)):
#                 self.deploy['placement'] = {}
#                 self.deploy['placement']['constraints'] = input
#             else:
#                 raise Exception('INVALID INPUT: "{}" is not a list'.format(input))

#         #add placement preference
#         def placement_preference(self, input):
#             if(isinstance(input, list)):
#                 self.deploy['placement'] = {}
#                 self.deploy['placement']['preference'] = input
#             else:
#                 raise Exception('INVALID INPUT: "{}" is not a list'.format(input))

#         #add replicas
#         def replicas(self, input):
#             if(isinstance(input, int)):
#                 self.deploy['replicas'] = input
#             else:
#                 raise Exception('INVALID INPUT: "{}" is not an integer'.format(input))

#         #add resources limit cpu
#         def resources_limits_cpu(self, input):
#             if(isinstance(input, str)):
#                 self.deploy['resources']['limits']['cpus'] = input
#             else:
#                 raise Exception('INVALID INPUT: "{}" is not a string'.format(input))

#         #add resources limit memory
#         def resources_limits_memory(self, input):
#             if(isinstance(input, str)):
#                 self.deploy['resources']['limits']['memory'] = input
#             else:
#                 raise Exception('INVALID INPUT: "{}" is not a string'.format(input))

#         #add resources reservations cpu
#         def resources_reservations_cpu(self, input):
#             if(isinstance(input, str)):
#                 self.deploy['resources']['limits']['cpus'] = input
#             else:
#                 raise Exception('INVALID INPUT: "{}" is not a string'.format(input))

#         #add resources reservations memory
#         def resources_reservations_memory(self, input):
#             if(isinstance(input, str)):
#                 self.deploy['resources']['limits']['memory'] = input
#             else:
#                 raise Exception('INVALID INPUT: "{}" is not a string'.format(input))

#         #def restart policy rollback_config TODO: implement this in another class
#         def rollback_config(self, input):
#             raise NotImplementedError

#         #def restart policy update_config TODO: implement this in another class
#         def update_config(self, input):
#             raise NotImplementedError

#         #return self dictionary
#         def get_dict(self):
#             if(bool(self.deploy)):
#                 self.deploy['restart_policy'] = self.restart_policy.get_dict()
#                 if('condition' not in self.deploy['restart_policy']):
#                     del self.deploy['restart_policy']
#                 return(dict(self.deploy))
#             else:
#                 raise Exception('ERROR: service.deploy is empty')

#     #initializer
#     def __init__(self, name):
#         self.name = name
#         self.service = {name:{}}
#         self.build = self.Build()
#         self.deploy = self.Deploy()
#         self.service[self.name]['build'] = self.build
#         self.service[self.name]['deploy'] = self.deploy

#     # add cap
#     def cap_add(self, input):
#         if(isinstance(input, list)):
#             self.service[self.name]['cap_add'] = input
#             return True
#         else:
#             raise Exception('INVALID INPUT: "{}" is not a list'.format(input))

#     # cap drop
#     def cap_drop(self, input):
#         if(isinstance(input, list)):
#             self.service[self.name]['cap_drop'] = input
#             return True
#         else:
#             raise Exception('INVALID INPUT: "{}" is not a list'.format(input))
    
#     # add cgroup_parent
#     def cgroup_parent(self, input):
#         if(isinstance(input, str)):
#             self.service[self.name]['cgroup_parent'] = input
#             return True
#         else:
#             raise Exception('{} -- is not a string'.format(input))
    
#     # add command
#     def command(self, input):
#         if((isinstance(input, str)) or (isinstance(input, list))):
#             self.service[self.name]['command'] = input
#         else:
#             raise Exception('INVALID INPUT: "{}" is not a string or list'.format(input))

#     # add a dictionary with wanted configs
#     def configs_add(self, input):
#         if(isinstance(input, dict)):
#             self.service[self.name]['configs'] = input
#             return True
#         else:
#             raise Exception('INVALID INPUT: "{}" is not a dictionary'.format(input))

#     # removes configs dictionary
#     def configs_remove(self):
#         if('configs' not in self.service[self.name]):
#             raise Exception('service.configs does not exist. Nothing to remove.')
#         else:
#             del self.service[self.name]['configs']

#     # add container_name
#     def container_name(self, input):
#         if(isinstance(input, str)):
#             self.service[self.name]['container_name'] = input
#         else:
#             raise Exception('INVALID INPUT: "{}" is not a string'.format(input))

#     # add credential_spec using file
#     def credential_spec_file(self, input):
#         if(isinstance(input, str)):
#             self.service[self.name]['credential_spec'] = {"file":input}
#             if('registry' in self.service[self.name]['credential_spec']):
#                 del self.service[self.name]['credential_spec']['registry']
#         else:
#             raise Exception('INVALID INPUT: "{}" is not a string'.format(input))
    
#     # add credential_spec using registry
#     def credential_spec_registry(self, input):
#         if(isinstance(input, str)):
#             self.service[self.name]['credential_spec'] = {"registry":input}
#             if('file' in self.service[self.name]['credential_spec']):
#                 del self.service[self.name]['credential_spec']['file']
#         else:
#             raise Exception('INVALID INPUT: "{}" is not a string'.format(input))

#     # add service dependenies
#     def depends_on(self, input):
#         if(isinstance(input, list)):
#             self.service[self.name]['depends_on'] = input
#         else:
#             raise Exception("INVALID INPUT: '{}' is not a list".format(input))
    
#     # add devices
#     def devices(self, input):
#         """
#         add devices section to service
#         @type   list
#         @param  List of device mappings.
#         """
#         if(isinstance(input, list)):
#             self.service[self.name]['devices'] = input
#         else:
#             raise Exception("INVALID INPUT: '{}' is not a list".format(input))

#     # add dns 
#     def dns(self, input):
#         """
#         add dns section to service
#         @type   str, list
#         @param  Custom DNS servers. Can be a single value or a list.
#         """
#         if((isinstance(input, str)) or (isinstance(input, list))):
#             self.service[self.name]['dns'] = input
#         else:
#             raise Exception("INVALID INPUT: '{}' is not a list or string".format(input))

#     # add dns_search
#     def dns_search(self, input):
#         """
#         add dns_search to service
#         @type   str, list
#         @param  Custom DNS search domains. Can be a single value or a list.
#         """
#         if((isinstance(input, str)) or (isinstance(input, list))):
#             self.service[self.name]['dns_search'] = input
#         else:
#             raise Exception("INVALID INPUT: '{}' is not a list or string".format(input))
    
#     # add entrypoint
#     def entrypoint(self, input):
#         """
#         add entrypoint to service
#         @type   str, list
#         @param  Override the default entrypoint.
#         """
#         if((isinstance(input, str)) or (isinstance(input, list))):
#             self.service[self.name]['entrypoint'] = input
#         else:
#             raise Exception("INVALID INPUT: '{}' is not a list or string".format(input))

#     # add env_file
#     def env_file(self, input):
#         """
#         add env_file to service
#         @type   str, list
#         @param  Add environment variables from a file.
#         """
#         if((isinstance(input, str)) or (isinstance(input, list))):
#             self.service[self.name]['env_file'] = input
#         else:
#             raise Exception("INVALID INPUT: '{}' is not a list or string".format(input))

#     # add environment
#     def environment(self, input):
#         """
#         add environment to service
#         @type   dict, list
#         @param  Add environment variables. Any boolean values need to be enclosed in quotes.
#         """
#         if((isinstance(input, dict)) or (isinstance(input, list))):
#             self.service[self.name]['environment'] = input
#         else:
#             raise Exception("INVALID INPUT: '{}' is not a dictionary or string".format(input))

#     # add expose
#     def expose(self, input):
#         """
#         add expose to service
#         @type   list
#         @param  Expose ports without publishing them to the host machine \
#                 - they’ll only be accessible to linked services.
#         """
#         if(isinstance(input, list)):
#             self.service[self.name]['expose'] = input
#         else:
#             raise Exception("INVALID INPUT: '{}' is not a list.".format(input))

#     # add ports
#     def ports(self, input):
#         """
#         add ports to service
#         @type   list
#         @param  Expose ports. specify both ports (HOST:CONTAINER)
#         """
#         if(isinstance(input, list)):
#             self.service[self.name]['ports'] = input
#         else:
#             raise Exception("INVALID INPUT: '{}' is not a list.".format(input))

#     # add external_links
#     def external_links(self, input):
#         """
#         add external_links to service
#         @type   list
#         @param  Link to containers started outside this docker-compose.yml \
#                 or even outside of Compose, especially for containers that \
#                 provide shared or common services.
#         """
#         if(isinstance(input, list)):
#             self.service[self.name]['external_links'] = input
#         else:
#             raise Exception("INVALID INPUT: '{}' is not a list.".format(input))

#     # add extra_hosts
#     def extra_hosts(self, input):
#         """
#         add extra_hosts to service
#         @type   list
#         @param  Add hostname mappings. 
#         """
#         if(isinstance(input, list)):
#             self.service[self.name]['extra_hosts'] = input
#         else:
#             raise Exception("INVALID INPUT: '{}' is not a list.".format(input))

#     # add image
#     def image(self, input):
#         """
#         add image to service
#         @type   string
#         @param  Specify the image to start the container from.
#         """
#         if(isinstance(input, str)):
#             self.service[self.name]['image'] = input
#         else:
#             raise Exception("INVALID INPUT: '{}' is not a string.".format(input))

#     # enable init
#     def init(self):
#         """
#         set service.init to True
#         """
#         self.service[self.name]['init'] = 'true'

#     # add isolation
#     def isolation(self, input):
#         """
#         add isolation to service
#         @type   string
#         @param  Specify a container’s isolation technology.
#         """
#         if(isinstance(input, str)):
#             self.service[self.name]['isolation'] = input
#         else:
#             raise Exception("INVALID INPUT: '{}' is not a string.".format(input))

#     # add labels
#     def labels(self, input):
#         """
#         add labels to service
#         @type   list, dict
#         @param  Add metadata to containers using Docker labels.
#         """
#         if((isinstance(input, dict)) or (isinstance(input, list))):
#             self.service[self.name]['labels'] = input
#         else:
#             raise Exception("INVALID INPUT: '{}' is not a list or dict.".format(input))

#     # add logging
#     def logging(self, input):
#         """
#         add logging to service, \
#         full description of logging is needed through input
#         @type   dict
#         @param  Logging configuration for the service.
#         """
#         if(isinstance(input, dict)):
#             self.service[self.name]['logging'] = input
#         else:
#             raise Exception("INVALID INPUT: '{}' is not a dict.".format(input))

#     # add network_mode
#     def network_mode(self, input):
#         """
#         add network_mode to service
#         @type   string
#         @param  Network mode.
#         """
#         if(isinstance(input, str)):
#             self.service[self.name]['network_mode'] = input
#         else:
#             raise Exception("INVALID INPUT: '{}' is not a string.".format(input))

#     # add networks
#     def networks(self, input):
#         """
#         add networks to service, use a dict for more options i.ei ALIASSES
#         @type   list, dict
#         @param  Networks to join, referencing entries under the \
#                 top-level networks key.
#         """
#         if((isinstance(input, list) or (isinstance(input, dict)))):
#             self.service[self.name]['networks'] = input
#         else:
#             raise Exception("INVALID INPUT: '{}' is not a list or dictionary.".format(input))

#     # add restart
#     def restart(self, input='"no"'):
#         """
#         add restart to service
#         @type   str
#         @param  What circumstances to restart the container on
#         """
#         if(isinstance(input, str)):
#             if(input in ['"no"','always', 'always', 'unless-stopped']):
#                 self.service[self.name]['restart'] = input
#             else:
#                 raise Exception("INVALID INPUT: '{}' is not One of 'no','always', 'always', 'unless-stopped'.".format(input))
#         else:
#             raise Exception("INVALID INPUT: '{}' is not a string.".format(input))

#     # add volumes
#     def volumes(self, input):
#         """
#         add volumes entry to service
#         @type   list
#         @param  Mount host paths or named volumes, \
#                 specified as sub-options to a service.
#         """
#         if(isinstance(input, list)):
#             self.service[self.name]['volumes'] = input
#         else:
#             raise Exception("INVALID INPUT: '{}' is not a list or dictionary.".format(input))

#     # get name
#     def get_name(self):
#         """
#         Get service name
#         """
#         return(self.name)
    
#     #spit out compose dictionary
#     def spit(self):
#         if(bool(self.build.get_dict())):
#             self.service[self.name]['build'] = self.build.get_dict()
#             if('context' not in self.service[self.name]['build']):
#                 del self.service[self.name]['build']
#                 raise Exception('ERROR: service.build was defined without a context')
#         else:
#             del self.service[self.name]['build']
#         if(bool(self.deploy.get_dict())):
#             self.service[self.name]['deploy'] = self.deploy.get_dict()
#         else:
#             del self.service[self.name]['deploy']
#         return(dict(self.service))
