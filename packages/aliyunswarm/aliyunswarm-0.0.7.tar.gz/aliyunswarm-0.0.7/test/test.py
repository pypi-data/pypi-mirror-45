from aliyunswarm import *

if __name__ == "__main__":
    swarm_api = SwarmApi()

    ################################################
    # applications api
    ################################################
    swarm_api.create_application('./test/compose/compose.yaml', 'swarmtest', 'swarm test')
    swarm_api.query_applications('swarmtest')
    swarm_api.query_applications()
    swarm_api.stop_application('swarmtest')
    swarm_api.start_application('swarmtest')
    swarm_api.kill_application('swarmtest')
    # swarm_api.delete_application('swarmtest')
    # swarm_api.redeploy_application('swarmtest')
    # swarm_api.update_application('swarmtest')

    ################################################
    # services api
    ################################################
    # swarm_api.query_services('api')
    # swarm_api.query_service('swarmtest', 'api')
    # swarm_api.start_service('swarmtest', 'api')
    # swarm_api.stop_service('swarmtest', 'api')
    # swarm_api.kill_service('swarmtest', 'api')
