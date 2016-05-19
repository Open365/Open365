/*
 * This file is an example of the information that can be set for each
 * docker host. The 'host' value is required, while the rest are optional.
 * If no 'wsHost' value is specified and the flag ENABLE_DISTRIBUTED_WS
 * is true, we will use the docker host IP as the default IP.
 */

var hostsInfo = {
    /*'EU': [{
        host: 'tcp://1.1.1.1:444',
        tlsVerify: 0,
        machineName: 'docker-machine',
        wsHost: '9.9.9.9'
    }, {
        host: 'tcp://2.2.2.2:444',
        tlsVerify: 0,
        wsHost: '9.9.9.9'
    }],
    'US': [{
        host: 'tcp://3.3.3.3:444',
        wsHost: '5.5.5.5'
    }, {
        host: 'tcp://4.4.4.4:444',
        tlsVerify: 0,
        machineName: 'docker-machine',
        wsHost: '8.8.8.8'
    }],
    'ES': [{
        host: 'tcp://5.5.5.5:444'
    }],*/
    'defaultValues': [{
        host: 'unix:///var/run/docker.sock'
    }]
};

module.exports = hostsInfo;
