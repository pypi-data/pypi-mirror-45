from .swarm_api import *

if __name__ == "__main__":
    swarm_api = SwarmApi()

    ################################################
    # applications api
    ################################################
    # swarm_api.create_application('./test/compose.yaml', 'swarmtest4', 'swarm test 4')
    # swarm_api.query_applications('test7')
    # swarm_api.query_applications()
    # swarm_api.stop_application('RedPacket')
    # swarm_api.start_application('swarmtest')
    # swarm_api.kill_application('RedPacket')
    # swarm_api.delete_application('RedPacket')
    # swarm_api.redeploy_application('RedPacket')
    # swarm_api.update_application('RedPacket')

    ################################################
    # services api
    ################################################
    # swarm_api.query_services('api')
    # swarm_api.query_service('RedPacket', 'api')
    # swarm_api.start_service('RedPacket', 'api')
    # swarm_api.stop_service('RedPacket', 'api')
    # swarm_api.kill_service('RedPacket', 'api')
