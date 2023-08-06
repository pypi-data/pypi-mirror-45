import yaml
import os

# MODIFIES THE YAML DUMP FUNCTION, BETTER INDENTATION
class MyDumper(yaml.Dumper):

    def increase_indent(self, flow=False, indentless=False):
        return super(MyDumper, self).increase_indent(flow, False)

# class for creating a single service
class Service():
    """
    Service manages the creation of a service.
    """

    #subclass healthcheck
    class HealthCheck():
        """
        service.HealthCheck
        """
        #initializer
        def __init__(self):
            self.healthcheck = {}

        #disable heathcheck
        def disable(self):
            """
            To disable any default healthcheck set by the image
            """
            self.healthcheck = {'disable':'true'}

        #add healthcheck test
        def test(self, input):
            """
            add test key and value to service.healthcheck
            @type   string, list
            @param  Configure a check that’s run to determine whether \
                    or not containers for this service are “healthy”.
            """
            if((isinstance(input, list)) or (isinstance(input, str))):
                self.healthcheck['test'] = input
            else:
                raise Exception('INVALID INPUT: "{}" is not a string or list'.format(input))

        #add interval
        def interval(self, input):
            """
            add interval key and value to service.healthcheck
            @type   string
            @param  The healthcheck will first run interval seconds \
                    after the container is started, and then again interval \
                    seconds after each previous check completes.
            """
            if(isinstance(input, str)):
                self.healthcheck['interval'] = input
            else:
                raise Exception('INVALID INPUT: "{}" is not a string'.format(input))

        #add timeout
        def timeout(self, input):
            """
            add timeout key and value to service.healthcheck
            @type   string
            @param  Lenght of time the healthcheck command will be run before it is considered failed.
            """
            if(isinstance(input, str)):
                self.healthcheck['timeout'] = input
            else:
                raise Exception('INVALID INPUT: "{}" is not a string'.format(input))

        #add retries
        def retries(self, input):
            """
            add retries key and value to service.healthcheck
            @type   int
            @param  Number of failures before the container is \
                    considered unhealthy
            """
            if(isinstance(input, int)):
                self.healthcheck['retries'] = input
            else:
                raise Exception('INVALID INPUT: "{}" is not an integer'.format(input))

        #add start_period
        def start_period(self, input):
            """
            add start_period key and value to service.healthcheck
            @type   string
            @param  start_period provides initialization time for \
                    containers that need time to boot.
            """
            if(isinstance(input, str)):
                self.healthcheck['start_period'] = input
            else:
                raise Exception('INVALID INPUT: "{}" is not a string'.format(input))

        #return self as dictionary
        def get_dict(self):
            return(dict(self.healthcheck))

    # subclass build
    class Build():
        """
        service.build
        """
        # initializer
        def __init__(self):
            self.build = {}

        # add context
        def context(self, input):
            """
            add context key and value to service.build
            @type   string
            @param  Either a path to a directory containing \
                a Dockerfile, or a url to a git repository.
            """
            if(isinstance(input, str)):
                self.build['context'] = input
                return True
            else:
                raise Exception('INVALID INPUT: "{}" is not a string'.format(input))

        # add dockerfile
        def dockerfile(self, input):
            """
            add dockerfile key and value to service.build
            @type   string
            @param  Alternate Dockerfile.
            """
            if(isinstance(input, str)):
                self.build['dockerfile'] = input
                return True
            else:
                raise Exception('INVALID INPUT: "{}" is not a string'.format(input))

        # add args
        def args(self, input):
            """
            add args key and value to service.build
            @type   list
            @param  Add build arguments, which are environment \
                    variables accessible only during the build process.
            """
            if(isinstance(input, list)):
                self.build['args'] = input
                return True
            else:
                raise Exception('INVALID INPUT: "{}" is not a list'.format(input))

        # add cache_from
        def cache_from(self, input):
            """
            add cache_from key and value to service.build
            @type   list
            @param  A list of images that the engine uses for \
                    cache resolution.
            """
            if(isinstance(input, list)):
                self.build['cache_from'] = input
                return True
            else:
                raise Exception('INVALID INPUT: "{}" is not a list'.format(input))

        # add labels
        def labels(self, input):
            """
            add labels key and value to service.build
            @type   list, dict
            @param  Add metadata to the resulting image using Docker labels.
            """
            if(isinstance(input, list) or isinstance(input, dict)):
                self.build['labels'] = input
                return True
            else:
                raise Exception('INVALID INPUT: "{}" is not a list or dict'.format(input))

        # add wshm_size
        def shm_size(self, input):
            """
            add smh_size key and value to service.build
            @type   int, string
            @param  Set the size of the /dev/shm partition \
                    for this build’s containers.
            """
            if(isinstance(input, int) or isinstance(input, str)):
                self.build['shm_size'] = input
                return True
            else:
                raise Exception('INVALID INPUT: "{}" is not an integer'.format(input))

        # add target
        def target(self, input):
            """
            add target key and value to service.build
            @type   string
            @param  Build the specified stage.
            """
            if(isinstance(input, str)):
                self.build['target'] = input
                return True
            else:
                raise Exception('INVALID INPUT: "{}" is not a string'.format(input))

        #return self as dictionary
        def get_dict(self):
            return(dict(self.build))

    # subclass deploy
    class Deploy():
        """
        service.deploy
        """
        class RestartPolicy():
            """
            service.deploy.restart_policy
            """
            #initializer
            def __init__(self):
                self.restart_policy = {}

            #add restart policy condition
            def condition(self, input):
                """
                Add restart policy condition, if unset will default to
                @type input: string
                @param input: One of 'none', 'on-failure' or 'any'
                """
                if(isinstance(input, str)):
                    if(input in ['none', 'on-failure', 'any']):
                        self.restart_policy['condition'] = input
                    else:
                        raise Exception("INVALID INPUT: '{}' is not One of 'none', 'on-failure' or 'any'".format(input))
                else:
                    raise Exception('INVALID INPUT: "{}" is not a string'.format(input))

            #add restart policy delay
            def delay(self, input):
                """
                add delay to restart policy
                @type:  string
                @param: How long to wait between restart attempts
                """
                if(isinstance(input, str)):
                    self.restart_policy['delay'] = input
                else:
                    raise Exception('INVALID INPUT: "{}" is not a string'.format(input))

            #add restart policy delay
            def max_attempts(self, input):
                """
                add max attempts to restart policy
                @type:  integer
                @param: How many times to attempt to restart a container before giving up
                """
                if(isinstance(input, str)):
                    self.restart_policy['max_attempts'] = input
                else:
                    raise Exception('INVALID INPUT: "{}" is not an integer'.format(input))

            #add restart policy delay
            def window(self, input):
                """
                add window to restart policy
                @type:  integer
                @param: How long to wait before deciding if a restart has succeeded
                """
                if(isinstance(input, str)):
                    self.restart_policy['window'] = input
                else:
                    raise Exception('INVALID INPUT: "{}" is not a string'.format(input))

            #return self dictionary
            def get_dict(self):
                """
                Return service.deploy dictionary
                """
                return(dict(self.restart_policy))

        #initializer
        def __init__(self):
            self.deploy = {}
            self.restart_policy = self.RestartPolicy()
            self.deploy['restart_policy'] = self.restart_policy

        #add context
        def endpoint_mode(self, input):
            """
            add endpoint_mode key and value to service.deploy
            @type   string
            @param  Specify a service discovery method for \
                    external clients connecting to a swarm.
            """
            if(input in ['vip', 'dnsrr']):
                if(isinstance(input, str)):
                    self.deploy['endpoint_mode'] = input
                    return True
                else:
                    raise Exception('INVALID INPUT: "{}" is not a string'.format(input))
            else:
                raise Exception('INVALID INPUT: "{}" is not One of "vip" or "dnsrr"'.format(input))

        #add labels
        def labels(self, input):
            """
            add labels key and value to service.deploy
            @type   list, dict
            @param  Specify labels for the service. \
                    These labels are only set on the service, \
                    and not on any containers for the service.
            """
            if(isinstance(input, list) or isinstance(input, dict)):
                self.deploy['labels'] = input
                return True
            else:
                raise Exception('INVALID INPUT: "{}" is not a list or dict'.format(input))

        #add placement, constraints
        def placement_constraints(self, input):
            """
            add placement.constraints key and value to service.deploy
            @type   list
            @param  Specify placement constraints.
            """
            if(isinstance(input, list)):
                self.deploy['placement'] = {}
                self.deploy['placement']['constraints'] = input
            else:
                raise Exception('INVALID INPUT: "{}" is not a list'.format(input))

        #add placement preference
        def placement_preference(self, input):
            """
            add placement.preferences key and value to service.deploy
            @type   list
            @param  Specify placement preferences.
            """
            if(isinstance(input, list)):
                self.deploy['placement'] = {}
                self.deploy['placement']['preference'] = input
            else:
                raise Exception('INVALID INPUT: "{}" is not a list'.format(input))

        #add replicas
        def replicas(self, input):
            """
            add replicas key and value to service.deploy
            @type   int
            @param  If the service is replicated (default), specify the number \
                    of containers that should be running at any given time.
            """
            if(isinstance(input, int)):
                self.deploy['replicas'] = input
            else:
                raise Exception('INVALID INPUT: "{}" is not an integer'.format(input))

        #add deploy.global
        def mode(self, input):
            """
            add mode key and value to service.deploy
            @type   string or int (if replicated, specify number of replicas)
            @param  Either global (exactly one container per swarm node) \
                    or replicated (a specified number of containers).
            """
            if((isinstance(input, str)) and (input == 'global')):
                self.deploy['mode'] = input
            elif(isinstance(input, int)):
                self.deploy['mode'] = 'replicated'
                self.replicas(input)

        #add resources limit cpu
        def resources_limits_cpu(self, input):
            """
            add limits.memory key and value to service.deploy
            @type   string
            @param  Configures resource constraints.
            """
            if(isinstance(input, str)):
                self.deploy['resources']['limits']['cpus'] = input
            else:
                raise Exception('INVALID INPUT: "{}" is not a string'.format(input))

        #add resources limit memory
        def resources_limits_memory(self, input):
            """
            add limits.memory key and value to service.deploy
            @type   string
            @param  Configures resource constraints.
            """
            if(isinstance(input, str)):
                self.deploy['resources']['limits']['memory'] = input
            else:
                raise Exception('INVALID INPUT: "{}" is not a string'.format(input))

        #add resources reservations cpu
        def resources_reservations_cpu(self, input):
            """
            add reservations.cpu key and value to service.deploy
            @type   string
            @param  Configures resource constraints.
            """
            if(isinstance(input, str)):
                self.deploy['resources']['reservations']['cpus'] = input
            else:
                raise Exception('INVALID INPUT: "{}" is not a string'.format(input))

        #add resources reservations memory
        def resources_reservations_memory(self, input):
            """
            add reservations.memory key and value to service.deploy
            @type   string
            @param  Configures resource constraints.
            """
            if(isinstance(input, str)):
                self.deploy['resources']['reservations']['memory'] = input
            else:
                raise Exception('INVALID INPUT: "{}" is not a string'.format(input))

        #def restart policy rollback_config TODO: implement
        def rollback_config(self, input):
            raise NotImplementedError

        #def restart policy update_config TODO: implement
        def update_config(self, input):
            raise NotImplementedError

        #return self dictionary
        def get_dict(self):
            """
            get deploy dictionary
            """
            #check if deploy.restart_policy was defined
            self.deploy['restart_policy'] = self.restart_policy.get_dict()
            if(not bool(self.deploy['restart_policy'])):
                del self.deploy['restart_policy']
            return(dict(self.deploy))

    #initializer
    def __init__(self, name):
        self.name = name
        self.service = {}
        self.build = self.Build()
        self.deploy = self.Deploy()
        self.healthcheck = self.HealthCheck()
        self.service['build'] = self.build
        self.service['deploy'] = self.deploy
        self.service['healthcheck'] = self.healthcheck

    # add cap
    def cap_add(self, input):
        """
        add cap_add key and value to service
        @type   list
        @param  Add container capabilities.
        """
        if(isinstance(input, list)):
            self.service['cap_add'] = input
            return True
        else:
            raise Exception('INVALID INPUT: "{}" is not a list'.format(input))

    # cap drop
    def cap_drop(self, input):
        """
        add cap_drop key and value to service
        @type   list
        @param  Drop container capabilities.
        """
        if(isinstance(input, list)):
            self.service['cap_drop'] = input
            return True
        else:
            raise Exception('INVALID INPUT: "{}" is not a list'.format(input))

    # add cgroup_parent
    def cgroup_parent(self, input):
        """
        add cgroup_parent key and value to service
        @type   string
        @param  Specify an optional parent cgroup for the container.
        """
        if(isinstance(input, str)):
            self.service['cgroup_parent'] = input
            return True
        else:
            raise Exception('{} -- is not a string'.format(input))

    # add command
    def command(self, input):
        """
        command for the container to run
        @type   str, list
        @param  Override the default command.
        """
        if((isinstance(input, str)) or (isinstance(input, list))):
            self.service['command'] = input
        else:
            raise Exception('INVALID INPUT: "{}" is not a string or list'.format(input))

    #TODO: add long syntax of this option
    # add a dictionary with wanted configs
    def configs(self, input):
        """
        reference configs this service will use, only short syntax is available.
        @type   list
        @param  Grant access to configs.
        """
        if(isinstance(input, list)):
            self.service['configs'] = input
            return True
        else:
            raise Exception('INVALID INPUT: "{}" is not a list'.format(input))

    # add container_name
    def container_name(self, input):
        """
        Add container_name key and value to this service
        @type   string
        @param  Specify a custom container name, rather than a generated default name.
        """
        if(isinstance(input, str)):
            self.service['container_name'] = input
        else:
            raise Exception('INVALID INPUT: "{}" is not a string'.format(input))

    # add credential_spec using file
    def credential_spec_file(self, input):
        """
        Add credential_spec file key and value to this service
        @type   string
        @param  Configure the credential spec for managed service account.
        """
        if(isinstance(input, str)):
            self.service['credential_spec'] = {"file":input}
            if('registry' in self.service['credential_spec']):
                del self.service['credential_spec']['registry']
        else:
            raise Exception('INVALID INPUT: "{}" is not a string'.format(input))

    # add credential_spec using registry
    def credential_spec_registry(self, input):
        """
        Add credential_spec registry key and value to this service
        @type   string
        @param  Configure the credential spec for managed service account.
        """
        if(isinstance(input, str)):
            self.service['credential_spec'] = {"registry":input}
            if('file' in self.service['credential_spec']):
                del self.service['credential_spec']['file']
        else:
            raise Exception('INVALID INPUT: "{}" is not a string'.format(input))

    # add service dependenies
    def depends_on(self, input):
        """
        add depends_on key to service
        @type   list
        @param  Express dependencies of this services to another
        """
        if(isinstance(input, list)):
            self.service['depends_on'] = input
        else:
            raise Exception("INVALID INPUT: '{}' is not a list".format(input))

    # add devices
    def devices(self, input):
        """
        add devices section to service
        @type   list
        @param  List of device mappings.
        """
        if(isinstance(input, list)):
            self.service['devices'] = input
        else:
            raise Exception("INVALID INPUT: '{}' is not a list".format(input))

    def dns(self, input):
        """
        add dns section to service
        @type   str, list
        @param  Custom DNS servers. Can be a single value or a list.
        """
        if((isinstance(input, str)) or (isinstance(input, list))):
            self.service['dns'] = input
        else:
            raise Exception("INVALID INPUT: '{}' is not a list or string".format(input))

    # add dns_search
    def dns_search(self, input):
        """
        add dns_search to service
        @type   str, list
        @param  Custom DNS search domains. Can be a single value or a list.
        """
        if((isinstance(input, str)) or (isinstance(input, list))):
            self.service['dns_search'] = input
        else:
            raise Exception("INVALID INPUT: '{}' is not a list or string".format(input))

    # add entrypoint
    def entrypoint(self, input):
        """
        add entrypoint to service
        @type   str, list
        @param  Override the default entrypoint.
        """
        if((isinstance(input, str)) or (isinstance(input, list))):
            self.service['entrypoint'] = input
        else:
            raise Exception("INVALID INPUT: '{}' is not a list or string".format(input))

    # add env_file
    def env_file(self, input):
        """
        add env_file to service
        @type   str, list
        @param  Add environment variables from a file.
        """
        if((isinstance(input, str)) or (isinstance(input, list))):
            self.service['env_file'] = input
        else:
            raise Exception("INVALID INPUT: '{}' is not a list or string".format(input))

    # add environment
    def environment(self, input):
        """
        add environment to service
        @type   dict, list
        @param  Add environment variables. Any boolean values need to be enclosed in quotes.
        """
        if((isinstance(input, dict)) or (isinstance(input, list))):
            self.service['environment'] = input
        else:
            raise Exception("INVALID INPUT: '{}' is not a dictionary or string".format(input))

    # add expose
    def expose(self, input):
        """
        add expose to service
        @type   list
        @param  Expose ports without publishing them to the host machine \
                - they’ll only be accessible to linked services.
        """
        if(isinstance(input, list)):
            self.service['expose'] = input
        else:
            raise Exception("INVALID INPUT: '{}' is not a list.".format(input))

    # add ports
    def ports(self, input):
        """
        add ports to service
        @type   list
        @param  Expose ports. specify both ports (HOST:CONTAINER)
        """
        if(isinstance(input, list)):
            self.service['ports'] = input
        else:
            raise Exception("INVALID INPUT: '{}' is not a list.".format(input))

    # add external_links
    def external_links(self, input):
        """
        add external_links to service
        @type   list
        @param  Link to containers started outside this docker-compose.yml \
                or even outside of Compose, especially for containers that \
                provide shared or common services.
        """
        if(isinstance(input, list)):
            self.service['external_links'] = input
        else:
            raise Exception("INVALID INPUT: '{}' is not a list.".format(input))

    # add extra_hosts
    def extra_hosts(self, input):
        """
        add extra_hosts to service
        @type   list
        @param  Add hostname mappings.
        """
        if(isinstance(input, list)):
            self.service['extra_hosts'] = input
        else:
            raise Exception("INVALID INPUT: '{}' is not a list.".format(input))

    # add image
    def image(self, input):
        """
        add image to service
        @type   string
        @param  Specify the image to start the container from.
        """
        if(isinstance(input, str)):
            self.service['image'] = input
        else:
            raise Exception("INVALID INPUT: '{}' is not a string.".format(input))

    # enable init
    def init(self):
        """
        set service.init to True
        """
        self.service['init'] = 'true'

    # add isolation
    def isolation(self, input):
        """
        add isolation to service
        @type   string
        @param  Specify a container’s isolation technology.
        """
        if(isinstance(input, str)):
            self.service['isolation'] = input
        else:
            raise Exception("INVALID INPUT: '{}' is not a string.".format(input))

    # add labels
    def labels(self, input):
        """
        add labels to service
        @type   list, dict
        @param  Add metadata to containers using Docker labels.
        """
        if((isinstance(input, dict)) or (isinstance(input, list))):
            self.service['labels'] = input
        else:
            raise Exception("INVALID INPUT: '{}' is not a list or dict.".format(input))

    # add logging
    def logging(self, input):
        """
        add logging to service, \
        full description of logging is needed through input
        @type   dict
        @param  Logging configuration for the service.
        """
        if(isinstance(input, dict)):
            self.service['logging'] = input
        else:
            raise Exception("INVALID INPUT: '{}' is not a dict.".format(input))

    # add network_mode
    def network_mode(self, input):
        """
        add network_mode to service
        @type   string
        @param  Network mode.
        """
        if(isinstance(input, str)):
            self.service['network_mode'] = input
        else:
            raise Exception("INVALID INPUT: '{}' is not a string.".format(input))

    # add networks
    def networks(self, input):
        """
        add networks to service, use a dict for more options i.ei ALIASSES
        @type   list, dict
        @param  Networks to join, referencing entries under the \
                top-level networks key.
        """
        if((isinstance(input, list) or (isinstance(input, dict)))):
            self.service['networks'] = input
        else:
            raise Exception("INVALID INPUT: '{}' is not a list or dictionary.".format(input))

    # add restart
    def restart(self, input='"no"'):
        """
        add restart to service
        @type   str
        @param  What circumstances to restart the container on
        """
        if(isinstance(input, str)):
            if(input in ['"no"','always', 'always', 'unless-stopped']):
                self.service['restart'] = input
            else:
                raise Exception("INVALID INPUT: '{}' is not One of 'no','always', 'always', 'unless-stopped'.".format(input))
        else:
            raise Exception("INVALID INPUT: '{}' is not a string.".format(input))

    # add volumes
    def volumes(self, input):
        """
        add volumes entry to service
        @type   list
        @param  Mount host paths or named volumes, \
                specified as sub-options to a service.
        """
        if(isinstance(input, list)):
            self.service['volumes'] = input
        else:
            raise Exception("INVALID INPUT: '{}' is not a list or dictionary.".format(input))

    # get name
    def get_name(self):
        """
        Get service name
        """
        return(self.name)

    #spit out service dictionary
    def spit(self):
        """
        Output the description (dictionary) of this service
        """
        #make sure service.build was defined correctly
        self.service['build'] = self.build.get_dict()
        if(bool(self.service['build'])):
            if('context' not in self.service['build']):
                del self.service['build']
                raise Exception('ERROR: service.build was defined without a context')
        else:
            del self.service['build']

        #make sure service.deploy was defined correctly
        self.service['deploy'] = self.deploy.get_dict()
        if(not bool(self.service['deploy'])):
            del self.service['deploy']

        #make sure service.heathcheck was defined correctly
        self.service['healthcheck'] = self.healthcheck.get_dict()
        if(bool(self.service['healthcheck'])):
            if('test' not in self.service['healthcheck']):
                del self.service['healthcheck']
                raise Exception('ERROR: service.healthcheck was defined without a test')
        else:
            del self.service['healthcheck']

        return(dict(self.service))

# class for managing all services
class Compose():
    """
    Services manages every service within a compose.
    """
    def __init__(self):
        self.compose = {'version': "3.7", 'services':{}}
        self.path = os.getcwd()

    # add service to compose
    def add_service(self, input):
        """
        Add a service into compose
        @type   service
        @param  service object
        """
        self.compose['services'][input.name] = input.spit()

    # add configs to compose
    def create_config(self,input):
        """
        add a dictionary with wanted config options to compose
        @type   dict
        @param  a dictionary defining the config attributes
        """
        if(isinstance(input, dict)):
            self.compose['configs'] = input
        else:
            raise Exception("INVALID INPUT: '{}' is not a dictionary.".format(input))

    # make compose file
    def make_compose(self, path=None):
        """
        create compose file in this directory
        @type string
        @param path to compose output location
        """
        if(path==None):
            path=self.path
        with open(path+'/docker-compose.yaml', 'w') as this_file:
            yaml.dump(self.compose, this_file, Dumper=MyDumper, default_flow_style=False)
